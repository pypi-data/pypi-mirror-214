""" This module provides support functions for various parts of the highlighter modules."""

import re
from json import load
from importlib import resources
# pylint: disable=unused-import, unused-variable
from multiprocessing.connection import Connection
# pylint: enable=unused-import, unused-variable


# Regex patterns
# Type patterns
g_posix_line_end_pattern: re.Pattern = re.compile(r'''(.*\Z)''')
""" A pattern that matches the entirety of the last line of a text, Group 1 captures the entire line."""


def _get_lua_built_ins(lua_version=5.1) -> dict[str, list[str]]:
    """ Reads LuaBuiltInCache and returns the built-ins for the specified version of Lua.

    :param lua_version: The version of Lua to get the methods for.

    :return: A dict of Lua built-ins separated into categories.
    """
    data_path: str = resources.files('lua_auto_doc').joinpath('modules/highlighter/LuaBuiltInCache.json')
    with open(data_path, 'r', encoding='utf-8') as file:
        json_cache: dict[str, dict[str, list[str]]] = load(file)
        if lua_version <= 5.1:
            return json_cache['5.1']
        if lua_version == 5.2:
            return json_cache['5.2']
        if lua_version == 5.3:
            return json_cache['5.3']

        return json_cache['5.4']


def _init_keywords(lua_version=5.1):
    """ Creates a list of Lua keywords.

    :param lua_version: The version of Lua to get the keywords for.

    :return: A list of Lua keywords.
    """
    keyword_list: list[str] = [
        'and',
        'break',
        'do',
        'else',
        'elseif',
        'end',
        'false',
        'for',
        'function',
        'if',
        'in',
        'local',
        'nil',
        'not',
        'or',
        'repeat',
        'return',
        'then',
        'true',
        'until',
        'while',
    ]
    if lua_version <= 5.4:
        keyword_list.append('goto')
    elif lua_version <= 5.3:
        keyword_list.append('goto')
    elif lua_version <= 5.2:
        keyword_list.append('goto')
    # Sort keywords by length so that longer keywords are matched first
    keyword_list.sort(key=len, reverse=True)

    return keyword_list


def _init_tokens(lua_version=5.1):
    """ Creates a list of Lua tokens.

    :param lua_version: The version of Lua to get the tokens for.

    :return: A list of Lua tokens.
    """
    token_list: list[str] = [
        '+',
        '-',
        '*',
        '/',
        '%',
        '^',
        '#',
        '==',
        '~=',
        '<=',
        '>=',
        '<',
        '>',
        '=',
        '(',
        ')',
        '{',
        '}',
        '[',
        ']',
        ';',
        ':',
        ',',
        '.',
        '..',
        '...',
    ]
    if lua_version <= 5.4:
        token_list.append('::')
        token_list.append('&')
        token_list.append('|')
        token_list.append('<<')
        token_list.append('>>')
        token_list.append('//')
    elif lua_version <= 5.3:
        token_list.append('::')
        token_list.append('&')
        token_list.append('|')
        token_list.append('<<')
        token_list.append('>>')
        token_list.append('//')
    elif lua_version <= 5.2:
        token_list.append('::')
    # Sort tokens by length so that longer tokens are matched first
    token_list.sort(key=len, reverse=True)

    return token_list


# pylint: disable=unused-variable
def get_reserved_keywords_dict(lua_version: float) -> dict[str, list[str]]:
    """ Init the global variables.

    :param lua_version: The version of Lua to use.
    """
    # Init variables
    # Lua keywords and tokens
    lua_reserved_keywords: list[str] = _init_keywords(lua_version)
    lua_reserved_tokens: list[str] = _init_tokens(lua_version)
    lua_reserved_rainbow_tokens: list[str] = [
        '(',
        ')',
        '{',
        '}',
        '[',
        ']',
    ]
    lua_reserved_rainbow_keywords: list[str] = [
        'end',
        'if',
        'elseif',
        'else',
        'then',
        'for',
        'while',
        'do',
        'repeat',
        'until',
        'function',  # Function got separate colouring system, we still need to match it to properly escape its end
    ]
    # Lua built-ins
    cache_dict: dict[str, list[str]] = _get_lua_built_ins(lua_version)
    lua_reserved_basic_functions: list[str] = cache_dict['basic']
    lua_reserved_metamethods: list[str] = cache_dict['metamethods']
    lua_reserved_environment_variables: list[str] = cache_dict['environment_variables']

    # Sort the built-in lists by length to ensure regex matches the longest possible string
    lua_reserved_basic_functions.sort(key=len, reverse=True)
    lua_reserved_metamethods.sort(key=len, reverse=True)
    lua_reserved_environment_variables.sort(key=len, reverse=True)

    return {
        'keywords': lua_reserved_keywords,
        'tokens': lua_reserved_tokens,
        'rainbow_tokens': lua_reserved_rainbow_tokens,
        'rainbow_keywords': lua_reserved_rainbow_keywords,
        'basic_functions': lua_reserved_basic_functions,
        'metamethods': lua_reserved_metamethods,
        'environment_variables': lua_reserved_environment_variables,
    }


def get_code(filename: str, encoding='utf-8') -> str:
    """ Gets the code from a file.

    :param filename: The name of the file to get the code from.
    :param encoding: The encoding of the file.

    :return: The code from the file.
    """
    with open(filename, 'r', encoding=encoding) as file:
        code: str = file.read()

    # Enforce POSIX line endings
    if g_posix_line_end_pattern.findall(code)[0] != '':
        code += '\n'

    return code


def unroll_list(list_to_unroll: list[list[any]]) -> list[any]:
    """ Unrolls a list of lists by one level. This is useful for removing the outer list of a list of lists. Will force
    there to be only one element of each instance in the list.

    :param list_to_unroll: The list to unroll.

    :return: The unrolled list.
    """
    unrolled_list: list[any] = []
    for element in list_to_unroll:
        for sub_element in element:
            if sub_element not in unrolled_list:
                unrolled_list.append(sub_element)

    return unrolled_list


def get_split_variables(names: str, offset: int) -> list[tuple[str, int]]:
    """ Splits up a string of variables separated by commas and returns a list of tuples containing the variable name
    and its index.

    :param names: The string of variables.
    :param offset: The offset to add to the index of the variables.

    :return: A list of tuples containing the variable name and its index.
    """
    variable_list: list[tuple[str, int]] = []
    name_list: list[str] = [name.strip() for name in names.split(',')]
    for name in name_list:
        if name != '':
            index: int = names.find(name)
            variable_list.append((name, index + offset))

    return variable_list


def remove_overlaps(index_list_1: list[dict[str, int]], index_list_2: list[dict[str, int]], priority_1=False) -> None:
    """ Removes overlaps between two lists of indexes, prioritises keeping the size of the smallest list.
    If both lists are of equal length, elements will be removed from the second list.

    :param index_list_1: The first list of indexes.
    :param index_list_2: The second list of indexes.
    :param priority_1: If True, all overlaps will be removed from the second list.
    """
    priority_1 = priority_1 or len(index_list_1) <= len(index_list_2)
    index_1_removal_queue: list[dict[str, int]] = []
    for index_1 in index_list_1:
        # Break if index_1['start'] is greater than the last index_2['end'] as index_1 is strictly increasing or if
        # index_list_2 is empty
        if len(index_list_2) == 0 or index_1['start'] > index_list_2[-1]['end']:
            break
        index_2_removal_queue: list[dict[str, int]] = []
        for index_2 in index_list_2:
            # Remove entry from the longest list (the greatest scope and thus overwritten) if encountering a conflict
            if index_1['start'] == index_2['start'] and index_1['end'] == index_2['end']:
                if priority_1:
                    index_2_removal_queue.append(index_2)
                else:
                    index_1_removal_queue.append(index_1)
                    break
            # Break if index_2['start'] is greater than index_1['end'] as index_2 is strictly increasing
            elif index_1['end'] < index_2['start']:
                break
        # Remove indexes from the second list
        for index in index_2_removal_queue:
            index_list_2.remove(index)
    # Remove indexes from the first list
    for index in index_1_removal_queue:
        index_list_1.remove(index)
# pylint: enable=unused-variable
