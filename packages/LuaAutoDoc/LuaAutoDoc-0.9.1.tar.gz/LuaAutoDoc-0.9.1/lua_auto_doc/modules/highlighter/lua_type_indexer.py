""" This module provides functions used to index various lua types. """

import re
from typing import Union
# pylint: disable=unused-import, unused-variable
from multiprocessing.connection import Connection
# pylint: enable=unused-import, unused-variable
from lua_auto_doc.modules.highlighter.indexer_support_functions import unroll_list, get_split_variables, remove_overlaps

# Regex patterns
# Regex pattern meant for filtering out strings and comments to avoid false positives
# Since strings and documentation relies on a named capture group, other patterns this two patterns are inserted into
# will have their own capture group shifted up by two, one for each pattern added
g_string_non_capture_pattern: re.Pattern = re.compile(r'''\"(?:[^"\\\n]|\\.|\\\n)*\"|\'(?:[^'\\\n]|\\.|\\\n)*\'|\[(?P<raised>=*)\[[\w\W]*?\](?P=raised)\]''', re.MULTILINE)
""" A filter pattern that matches all valid Lua strings, Contains 1 capture group."""
g_comments_and_documentation_non_capture_pattern: re.Pattern = re.compile(r'''(?:-{2}\[(?P<raised2>=*)\[[\w\W]*?\](?P=raised2)\]|--(?!-).*)|---.*''',
                                                                          re.MULTILINE)
""" A filter pattern that matches all valid Lua comments and documentation, Contains 1 capture group."""
g_compiled_filter_pattern: re.Pattern = re.compile(f'{g_string_non_capture_pattern.pattern}|{g_comments_and_documentation_non_capture_pattern.pattern}', re.MULTILINE)
""" A filter pattern that matches all valid Lua strings, comments and documentation, Contains 2 capture groups."""

# g_string_pattern adapted from Casimir et Hippolyte answer here: https://stackoverflow.com/questions/171480/regex-grabbing-values-between-quotation-marks
g_string_pattern: re.Pattern = re.compile(r'''(\"(?:[^"\\\n]|\\.|\\\n)*\"|\'(?:[^'\\\n]|\\.|\\\n)*\'|\[(?P<raised>=*)\[[\w\W]*?\](?P=raised)\])''', re.MULTILINE)
""" A pattern that matches all valid Lua strings, Group 1 captures the entire string including the "string start" and
    "string end" symbols."""
g_number_pattern: re.Pattern = re.compile(r'''(?<=[\W0-9])(0x[a-fA-F\d]*|\d+\.?\d+|(?<!\.)\.\d+|\d+\.?)''', re.MULTILINE)
""" A pattern that matches all valid Lua numbers, Group 1 captures the entire number."""
g_comments_and_documentation_pattern: re.Pattern = re.compile(r'''(-{2}\[(?P<raised2>=*)\[[\w\W]*?\](?P=raised2)\]|--(?!-).*)|---[ \t]*(?:@(\w*)[: \t]*([a-zA-Z_][\w\.]*(?:(?:[<\(]|(?<=fun)[ \t]|(?<=table[ \t]))[<\w, \t>\(\):]*[>\)?])?[?]?)[: \t]*(?:([a-zA-Z_][\w|\.]*(?:[< \(][<\w, \t>\(\):]*[>\)?])?[?]?)(?:[ \t]*:[ \t]*([a-zA-Z_][\w\.]*))?)?[: \t]*.*|(.*))(?<=\S)''', re.MULTILINE)
""" A pattern that matches all valid Lua comments and documentation.
Group 1 captures the entire comment including "--"
Group 2 is a named capture group to be ignored
Group 3 captures the documentation tag
Group 4 captures the follow-up word if it starts with a letter or underscore
Group 5 capture the next follow-up word if it starts with a letter or underscore and Group 4 got a match
Group 6 captures the type hint of a function if Group 5 got a match
Group 7 captures all the text of the line if Group 3 got no match."""

# Patterns for identifying local/global variables and functions
g_keyword_end_pair_pattern: re.Pattern = re.compile(r'''((?<![a-zA-Z_])function(?=[\w\.\: \t]*\()|(?<![a-zA-Z_])(?:end|do|if|repeat)(?!\w)|(?<=(?<![a-zA-Z_])until)[\S \t]*$)''', re.MULTILINE)
""" A pattern that matches all Lua keywords that are paired with an end keyword, Group 1 captures the keyword."""
g_function_pattern: re.Pattern = re.compile(r'''(local[ \t]*(?=function))?(function)?[ \t]*((?:([a-zA-Z_][\w\.:]*)[:]|([a-zA-Z_][\w\.:]*)[\.])?([a-zA-Z_][\w]*))(?=[ \t]*\()''', re.MULTILINE)
""" A pattern that matches various types of functions/methods.
Group 1 captures the "local" keyword
Group 2 capture the "function" keyword if Group 1 got no match
Group 3 captures ":" or "." that are between a class and its method
Group 4 capture the class that precedes the ":" that is captured by Group 3
Group 5 captures the class that precedes the "." that is captured by Group 3
Group 6 captures the method name that follows the ":" or "." that is captured by Group 3
Group 7 captures "function" if Group 1 got a match."""
g_local_variables_pattern: re.Pattern = re.compile(r'''local[ \t]*([a-zA-Z_][\w ,]*?) *=(?![\w]*[\(\"\'\]\)])''', re.MULTILINE)
""" A pattern that matches local variable declarations, Group 1 captures all the variables between "local" and "=" and
    will need to be processed to separate possible multiple variables."""
g_declared_global_variables_pattern: re.Pattern = re.compile(r'''(?<!local )(?!local)(?<!for )(?!for)(?<![\w,])(?!#BANNEDWORDS)([a-zA-Z_][\w ,]*?) *=(?![\w]*[\(\"\'\]\)=])''', re.MULTILINE)
""" A pattern that matches all variables with proceeding assignment that does not have "local" or "for" before it.
    Needs to be filtered by other pattern to avoid a lot of false positives. #BANNEDWORDS needs to be replaced with the
    actual banned words.
Group 1 captures all the variables before "=" and will need to be processed to separate possible multiple variables."""
g_global_variables_pattern: re.Pattern = re.compile(r'''(?<![\w\"\'\\:\.])(?!#BANNEDWORDS)([a-zA-Z_][\w]*)(?![\(\"\']|[\w]*\()''', re.MULTILINE)
""" A pattern that matches all theoretically valid variable names. Will need to be filtered by other pattern to avoid a
    lot of false positives. #BANNEDWORDS needs to be replaced with the actual banned words.
Group 1 captures the variable name."""
g_parameters_variables_pattern: re.Pattern = re.compile(r'''(?:function[ \t]*[a-zA-Z_][\w:\.]*|function)[ \t]*\(([a-zA-Z_][\w ,]*)''', re.MULTILINE)
""" A pattern that matches all function parameters. Group 1 captures all the parameters between "(" and ")" and will
    need to be processed to separate possible multiple parameters."""
g_for_loop_parameters_pattern: re.Pattern = re.compile(r'''(?<!\w)for[ \t]*([a-z-A-Z_][\w, \t]*?)(?=[ \t]*=|[ \t]*in)''', re.MULTILINE)
""" A pattern that matches all for loop parameters. Group 1 captures all the parameters between "for" and "=" or "in"
    and will need to be processed to separate possible multiple parameters."""
g_table_content_pattern: re.Pattern = re.compile(r'''[a-zA-Z_]\w*[ \t]+=[ \t]+{([\w\W]*?)}''', re.MULTILINE)
""" A pattern that matches all the content inside a table. Group 1 captures all the content between "{" and "}"."""""
g_table_field_pattern: re.Pattern = re.compile(r'''([a-zA-Z_]\w*)[ \t]*=\s*[\w'"{]''', re.MULTILINE)
""" A pattern that matches all the fields inside a table. Relies on g_table_content_pattern to restrict the search to
    only table contents. Group 1 capture the field."""
g_field_pattern: re.Pattern = re.compile(r'''#[ \t]*[a-zA-Z_]\w*\.[a-zA-Z_]\w*|[a-zA-Z_]\w*\.[a-zA-Z_]\w*\(|[a-zA-Z_]\w*\.([a-zA-Z_]\w*)''', re.MULTILINE)
""" A pattern that matches all fields not inside a table. Group 1 captures the field."""
# Special keywords and tokens
g_self_keyword_pattern: re.Pattern = re.compile(r'''(?:\.\.|[\(\[\{=])[ \t]*(?<!\w)(self)(?!\w)|(?<!\w)(self)(?=[\.:]|[\ t]*=)''', re.MULTILINE)
""" A pattern that matches all "self" keywords. Group 1 captures the "self" keyword. Group 2 captures the "self" keyword
    not caught by Group 1."""


def _scope_finder(elements: list[tuple[str, int]], code: str, scope_offset=0) -> list[dict[str, tuple[int, int]]]:
    """ Finds the scope of a code block.

    :param elements: A list of tuples containing the data (element_name, element_start index).
    :param code: The code to search.
    :param scope_offset: The offset to add to the scope, each +1 will expand the scope by 1.

    :return: A list of dictionaries containing the scope of each element.
    """
    # Get all keyword-end pairs
    keyword_end_pairs: list[dict[str, tuple[int, int]]] = get_pattern_indexes(code, g_keyword_end_pair_pattern,
                                                                              pattern_filter=True)

    # Count the number of keyword-end until the end od scope, once end_count > start_count
    scopes: list[dict[str, tuple[int, int]]] = []
    start_keywords: list[str] = ['function', 'do', 'if', 'repeat']
    for element_name, start_index in elements:
        start_count: int = scope_offset
        end_count: int = 0
        for keyword_end_pair in keyword_end_pairs:
            if start_index <= keyword_end_pair['start']:
                if code[keyword_end_pair['start']:keyword_end_pair['end']] in start_keywords:
                    start_count += 1
                else:
                    end_count += 1
                if end_count > start_count:
                    scopes.append({
                        element_name: (start_index, keyword_end_pair['end']),
                        }
                    )
                    break

                if keyword_end_pair == keyword_end_pairs[-1]:  # The scope is to the end of the code
                    scopes.append({
                        element_name: (start_index, len(code)),
                        }
                    )
        # Special case for variables that is defined after the last "end" in the code
        if end_count == 0:
            scopes.append({
                element_name: (start_index, len(code)),
                }
            )

    return scopes


# pylint: disable=unused-variable
def get_pattern_indexes(code: str, pattern: re.Pattern, pattern_filter=False, offset=0) -> list[dict[str, int]]:
    """ Generic function that gets the start and end indexes of a pattern in a code text.

    :param code: The string to get the pattern indexes for.
    :param pattern: The pattern to get the indexes for. The pattern must catch the pattern as the filter will make the
    matches noisy.
    :param pattern_filter: Whether to filter out strings, comments and documentation. Uses g_compiled_filter_pattern.

    :return: A list of dictionaries containing the start and end indexes of each pattern.
    """
    start_index: int = 1
    end_index: int = 1
    if pattern_filter:
        pattern = re.compile(f'{g_compiled_filter_pattern.pattern}|{pattern.pattern}', re.MULTILINE)
        start_index = 3
        end_index = 3

    start_end_indexes: list[dict[str, int]] = []
    for match in pattern.finditer(code):
        if match.regs[start_index][0] > -1:
            start_end_indexes.append({
                'start': match.regs[start_index][0] + offset,
                'end': match.regs[end_index][1] + offset,
            })

    return start_end_indexes


def get_string_indexes(code: str) -> list[dict[str, int]]:
    """ Gets the start and end indexes of each string in a code text.

    :param code: The string to get the string indexes for.

    :return: A list of dictionaries containing the start and end indexes of each string.
    """
    string_indexes: list[dict[str, int]] = []
    # All matches are shifted one up as we insert g_comments_and_documentation_non_capture_pattern to the start of the
    # pattern to avoid checking for overlapping matches
    for match in re.finditer(f'{g_comments_and_documentation_non_capture_pattern.pattern}|{g_string_pattern.pattern}',
                             code, re.MULTILINE):
        if match.regs[2][0] != -1:
            string_indexes.append({
                'start': match.regs[2][0],
                'end': match.regs[2][1],
                }
            )

    return string_indexes


def get_keyword_indexes(code: str, reserved_lua_keywords_dict) -> list[dict[str, int]]:
    """ Gets the start and end indexes of each keyword in a code text.

    :param code: The string to get the keyword indexes for.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each keyword.
    """
    keyword_list = reserved_lua_keywords_dict['keywords'].copy()
    # Remove keywords with their own colouring system
    keyword_list.remove('true')
    keyword_list.remove('false')
    keyword_list.remove('nil')
    re_keywords = [re.escape(keyword) for keyword in keyword_list]
    keyword_pattern: re.Pattern = re.compile(rf'''(?<![a-zA-Z_])({"|".join(re_keywords)})(?!\w)''', re.MULTILINE)

    return get_pattern_indexes(code, keyword_pattern, pattern_filter=True)


def get_token_indexes(code: str, reserved_lua_keywords_dict: dict[str, list[str]]) -> list[dict[str, int]]:
    """ Gets the start and end indexes of each token in a code text.

    :param code: The string to get the token indexes for.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each token.
    """
    token_list = reserved_lua_keywords_dict['tokens'].copy()
    # Remove tokens with their own colouring system
    token_list.remove('.')
    token_list.remove('..')
    token_list.remove('...')
    re_tokens = [re.escape(token) for token in token_list]
    token_pattern: re.Pattern = re.compile(f'({"|".join(re_tokens)})', re.MULTILINE)

    return get_pattern_indexes(code, token_pattern, pattern_filter=True)


def get_rainbow_token_indexes(code: str, reserved_lua_keywords_dict: dict[str, list[str]]) -> list[dict[str, int]]:
    """ Gets the start and end indexes of each rainbow token in a code text.

    :param code: The string to get the rainbow token indexes for.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each rainbow token.
    """
    # Escape all rainbow tokens so that they can be used in a regex pattern
    re_rainbow_tokens = [re.escape(token) for token in reserved_lua_keywords_dict['rainbow_tokens']]
    re_rainbow_keywords = [re.escape(keyword) for keyword in reserved_lua_keywords_dict['rainbow_keywords']]
    rainbow_token_pattern: re.Pattern = re.compile(
        rf'''({"|".join(re_rainbow_tokens)}|(?<![a-zA-Z_])(?:{"|".join(re_rainbow_keywords)})(?!\w))''',
        re.MULTILINE)

    return get_pattern_indexes(code, rainbow_token_pattern, pattern_filter=True)


def get_self_keyword_indexes(code: str) -> list[dict[str, int]]:
    """ Gets the start and end indexes of each self keyword in a code text.

    :param code: The string to get the self keyword indexes for.

    :return: A list of dictionaries containing the start and end indexes of each self keyword.
    """
    self_keyword_indexes: list[dict[str, int]] = []
    pattern: re.Pattern = re.compile(f'{g_compiled_filter_pattern.pattern}|{g_self_keyword_pattern.pattern}',
                                     re.MULTILINE)
    for match in pattern.finditer(code):
        if match.regs[3][0] != -1:
            self_keyword_indexes.append({
                'start': match.regs[3][0],
                'end': match.regs[3][1],
                }
            )
        elif match.regs[4][0] != -1:
            self_keyword_indexes.append({
                'start': match.regs[4][0],
                'end': match.regs[4][1],
                }
            )

    return self_keyword_indexes


def _update_type_colours_indexes(offset: int, text, type_list: list[dict[str, int]], keyword_list: list[dict[str, int]],
                                 optional_list: list[dict[str, int]]) -> None:
    """ Appends to the given lists the indexes for the various type of keywords found in type documentation that
    have a unique colour associated with it.

    :param offset: The offset to add to the indexes.
    :param text: The text to get the indexes for.
    :param type_list: The list to append the type indexes to.
    :param keyword_list: The list to append the keyword indexes to.
    :param optional_list: The list to append the optional indexes to.
    """
    # pylint: disable=pointless-string-statement
    optional_pattern: str = r'''(\?(?=\Z))'''
    """ A pattern that matches the optional symbol at the end of the text. Group 1 captures the optional symbol."""
    function_pattern: str = r'''(?<![a-zA-Z_])(function|func?)(?!\w)'''
    """ A pattern that matches the function keyword or a shorthand version of it. Group 1 captures the keyword."""
    filter_pattern: str = r'''[a-zA-Z_][\w \t]*:'''  # Does not need to be caught
    """ A filter pattern that matches a substring ending with a colon. No groups are captured."""
    type_pattern: str = r'''([a-zA-Z_][\w]*)'''
    """ A pattern that matches a Lua type. Group 1 captures the type."""
    number_pattern: str = g_number_pattern.pattern

    colour_type_pattern: re.Pattern = re.compile(f'{optional_pattern}|{function_pattern}|{filter_pattern}|'
                                                 f'{type_pattern}|{number_pattern}',
                                                 re.MULTILINE)
    """ A pattern that is a combination of the optional_pattern, function_pattern, filter_pattern, type_pattern, and
    number_pattern.
    Group 1 captures the optional symbol.
    Group 2 captures the function keyword or a shorthand version of it.
    Group 3 captures the Lua type."""
    # pylint: enable=pointless-string-statement

    for match in colour_type_pattern.finditer(text):
        if match.regs[1][0] > -1:
            optional_list.append({
                'start': match.regs[1][0] + offset,
                'end': match.regs[1][1] + offset,
                }
            )
        elif match.regs[2][0] > -1:
            keyword_list.append({
                'start': match.regs[2][0] + offset,
                'end': match.regs[2][1] + offset,
                }
            )
        elif match.regs[3][0] > -1:
            type_list.append({
                'start': match.regs[3][0] + offset,
                'end': match.regs[3][1] + offset,
                }
            )
        elif match.regs[4][0] > -1:
            type_list.append({
                'start': match.regs[4][0] + offset,
                'end': match.regs[4][1] + offset,
                }
            )


def get_comments_and_documentation_indexes(code: str) -> tuple[list[dict[str, int]], list[dict[str, int]],
                                                               list[dict[str, int]], list[dict[str, int]],
                                                               list[dict[str, int]], list[dict[str, int]],
                                                               list[dict[str, int]], list[dict[str, int]]]:
    """ Gets the start and end indexes of each comment and documentation (details) in a code text.

    :param code: The string to get the comment and documentation indexes for.

    :return: A tuple containing a list of dictionaries containing the start and end indexes of keyword/text.
    """
    # Define the meaning of keywords with extra catch groups
    doc_one_word_type_keywords: list[str] = ['type', 'return', 'see', 'vararg', ]
    doc_one_word_name_keywords: list[str] = ['name', 'module', ]
    doc_two_word_type_keywords: list[str] = ['param', 'field', 'member', 'property', 'raise', ]
    doc_two_word_name_keywords: list[str] = ['alias', 'class', 'superclass', ]

    doc_type_indexes: list[dict[str, int]] = []
    doc_keyword_indexes: list[dict[str, int]] = []
    doc_name_indexes: list[dict[str, int]] = []
    doc_param_name_indexes: list[dict[str, int]] = []
    doc_tag_indexes: list[dict[str, int]] = []
    doc_optional_indexes: list[dict[str, int]] = []
    documentation_text_indexes: list[dict[str, int]] = []
    comment_indexes: list[dict[str, int]] = []

    ####### NOTICE #######
    # All matches are shifted one up as we insert g_string_non_capture_pattern to the start of the pattern to avoid
    # checking for overlapping matches
    for match in re.finditer(f'{g_string_non_capture_pattern.pattern}|{g_comments_and_documentation_pattern.pattern}',
                             code, re.MULTILINE):
        # Capture a -- comment
        if match.regs[2][0] > -1:
            comment_indexes.append({
                'start': match.regs[2][0],
                'end': match.regs[2][1],
                }
            )
            continue

        # Capture the documentation text if no documentation tag is found
        if match.regs[8][0] > -1:
            documentation_text_indexes.append({
                'start': match.regs[0][0],  # Start at the beginning of the match
                'end': match.regs[8][1],
                }
            )
            continue

        # Else if the match.group(4) is empty, it's a string, and we can "continue"
        if match.regs[4][0] < 0:
            continue

        # Capture the tag
        doc_tag_indexes.append({
            'start': match.regs[4][0],
            'end': match.regs[4][1],
            }
        )
        # Capture the documentation text
        documentation_text_indexes.append({
            'start': match.regs[0][0],  # Start at the beginning of the match
            'end': match.regs[0][1],  # End at the end of the match
            }
        )

        # Capture the one word type keyword
        if match.group(4) in doc_one_word_type_keywords:
            if match.regs[5][0] > -1:
                _update_type_colours_indexes(match.regs[5][0], match.group(5), doc_type_indexes, doc_keyword_indexes,
                                             doc_optional_indexes)
        # Capture the one word name keyword
        elif match.group(4) in doc_one_word_name_keywords:
            if match.regs[5][0] > -1:
                doc_name_indexes.append({  # Capture the name
                    'start': match.regs[5][0],
                    'end': match.regs[5][1],
                    }
                )
        # Capture the two word keywords
        elif match.group(4) in doc_two_word_type_keywords or match.group(4) in doc_two_word_name_keywords:
            # Capture the name
            if match.regs[5][0] > -1:
                doc_name_indexes.append({
                    'start': match.regs[5][0],
                    'end': match.regs[5][1],
                }
                )
                # Capture the type keyword
                if match.regs[6][0] > -1:
                    _update_type_colours_indexes(match.regs[6][0], match.group(6), doc_type_indexes,
                                                 doc_keyword_indexes, doc_optional_indexes)
                    # Capture the function type hint
                    if match.regs[7][0] > -1:
                        doc_type_indexes.append({
                            'start': match.regs[7][0],
                            'end': match.regs[7][1],
                        }
                        )

    return comment_indexes, doc_type_indexes, doc_name_indexes, doc_param_name_indexes, doc_tag_indexes, \
        documentation_text_indexes, doc_keyword_indexes, doc_optional_indexes


def get_built_in_indexes(code: str, lua_version: float, reserved_lua_keywords_dict: dict[str, list[str]]) \
        -> tuple[list[dict[str, int]], list[dict[str, int]], list[dict[str, int]]]:
    """ Gets the start and end indexes of each cache in a code text.

    :param code: The string to get the cache indexes for.
    :param lua_version: The version of Lua to get the built-ins for.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each cache.
    """
    re_basic_functions = [re.escape(function) for function in reserved_lua_keywords_dict['basic_functions']]
    re_metamethods = [re.escape(metamethod) for metamethod in reserved_lua_keywords_dict['metamethods']]
    re_environment_variables = [re.escape(variable) for variable in reserved_lua_keywords_dict['environment_variables']]
    basic_functions_pattern: re.Pattern = re.compile(rf'(?:(?<=[\n \t])|^)({"|".join(re_basic_functions)})(?=[^\w])',
                                                     re.MULTILINE)
    metamethods_pattern: re.Pattern = re.compile(rf'(?:(?<=[\n \t])|^)({"|".join(re_metamethods)})(?=[^\w])',
                                                 re.MULTILINE)
    environment_variables_pattern: re.Pattern = re.compile(
        rf'(?:(?<=[\n \t])|^)({"|".join(re_environment_variables)})(?=[^\w])', re.MULTILINE)

    basic_functions_indexes = get_pattern_indexes(code, basic_functions_pattern, pattern_filter=True)
    metamethods_indexes: list[dict[str, int]] = []
    if lua_version > 5.2:
        metamethods_indexes = get_pattern_indexes(code, metamethods_pattern, pattern_filter=True)
    environment_variables_indexes = get_pattern_indexes(code, environment_variables_pattern, pattern_filter=True)

    return basic_functions_indexes, metamethods_indexes, environment_variables_indexes


def resolve_indexes(first_index_list: list[dict[str, int]],
                    second_index: list[dict[str, int]],
                    first_list_priority=False) -> tuple[list[dict[str, int]], list[dict[str, int]]]:
    """ Resolves any overlaps between two lists of indexes. Priority is given to the whatever index has the lowest start
    index, unless first_list_priority is set to True.

    :param first_index_list: The first list of indexes.
    :param second_index: The second list of indexes.
    :param first_list_priority: Whether to give priority to the first list of indexes.

    :return: A tuple containing the resolved lists of indexes.
    """
    temp_list_1: list[dict[str, int]] = first_index_list.copy()
    temp_list_2: list[dict[str, int]] = second_index.copy()
    for element_1 in first_index_list:
        # Break out of loop if element_1 has higher start index than the last element in temp_list_2 or if temp_list_2
        # is empty
        if len(temp_list_2) == 0 or element_1['start'] > temp_list_2[-1]['end']:
            break
        removal_queue_1: list[dict[str, int]] = []
        removal_queue_2: list[dict[str, int]] = []
        for element_2 in temp_list_2:
            # Break if element_1 has lower end index than element_2's start index
            if element_1['end'] < element_2['start']:
                break
            # Continue if element_2 has higher end index than element_1's start index
            if element_2['end'] < element_1['start']:
                continue

            if element_1['start'] <= element_2['start'] < element_1['end']:
                removal_queue_2.append(element_2)

            elif first_list_priority and element_2['start'] <= element_1['start'] < element_2['end']:
                removal_queue_2.append(element_2)

            elif element_2['start'] <= element_1['start'] <= element_2['end']:
                removal_queue_1.append(element_1)
                break

        # Remove entries collected
        for element in removal_queue_1:
            temp_list_1.remove(element)
        for element in removal_queue_2:
            temp_list_2.remove(element)

    return temp_list_1, temp_list_2


def resolve_var_function_indexes(weak_list: list[tuple[str, int]], strong_list: list[dict[str, int]]) \
        -> list[tuple[str, int]]:
    """ Resolves any conflicts where a var or function is inside a string or comment.

    :param weak_list: The list that will lose entries for any overlaps
    :param strong_list: The list that will keep all entries

    :return: The resolved list.
    """
    if len(weak_list) == 0 or len(strong_list) == 0:
        return weak_list

    temp_list: list[tuple[str, int]] = weak_list.copy()
    for weak_entry in weak_list:
        # Break out of loop if weak_entry has higher start index than the last element in strong_list or if strong_list
        if weak_entry[1] > strong_list[-1]['end']:
            break
        removal_queue: set[tuple[str, int]] = set()
        for strong_entry in strong_list:
            # Break if weak_entry has lower start index than strong_entry's start index
            if strong_entry['start'] > weak_entry[1]:
                break
            # Continue if strong_entry has lower end index than weak_entry's start index
            if strong_entry['end'] < weak_entry[1]:
                continue

            # Add entry to removal queue
            removal_queue.add(weak_entry)

        # Remove entries collected
        for element in removal_queue:
            temp_list.remove(element)

    return temp_list


def get_local_function_indexes(code: str, local_function_declaration_indexes: list[tuple[str, int]]) \
        -> list[dict[str, int]]:
    """ Gets the indexes of all functions in the code.

    :param code: The code to search.
    :param local_function_declaration_indexes: The indexes of the local function declarations.

    :return: A list of dictionaries containing the start and end indexes of each function.
    """
    # Get scopes of local functions
    local_function_scopes: list[dict[str, tuple[int, int]]] = _scope_finder(local_function_declaration_indexes, code,
                                                                            scope_offset=1)

    # Get indexes of local functions
    local_function_indexes: list[dict[str, int]] = []
    for function_index, function_scope in zip(local_function_declaration_indexes, local_function_scopes):
        index_offset: int = function_index[1]
        for match in re.finditer(rf'''(?<!\w){function_index[0]}(?!\w)''',
                                 code[function_scope[function_index[0]][0]:function_scope[function_index[0]][1]]):
            local_function_indexes.append({
                'start': match.start() + index_offset,
                'end': match.end() + index_offset,
                }
            )

    return local_function_indexes


def get_global_function_indexes(code: str, global_function_declaration_indexes: list[tuple[str, int]],
                                banned_globals: list[str],
                                function_indexes: list[dict[str, Union[bool, dict[str, Union[str, int]]]]],
                                reserved_lua_keywords_dict: dict[str, list[str]]) \
        -> list[dict[str, int]]:
    """ Gets the indexes of all global functions in the code.

    :param code: The code to search.
    :param global_function_declaration_indexes: The indexes of the global function declarations.
    :param banned_globals: A list of all banned global names.
    :param function_indexes: A list of dicts containing detailed information about each function.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each global function.
    """
    # Run through and find all global functions based on declarations
    global_function_indexes: list[dict[str, int]] = []
    for function_index in global_function_declaration_indexes:
        index_offset: int = function_index[1]
        for match in re.finditer(rf'''(?<!\w){function_index[0]}(?!\w)''', code[index_offset:]):
            global_function_indexes.append({
                'start': match.start() + index_offset,
                'end': match.end() + index_offset,
                }
            )
    # Extend blacklist with Lua built-ins
    banned_globals.extend(reserved_lua_keywords_dict['basic_functions'])
    banned_globals.extend(reserved_lua_keywords_dict['metamethods'])
    banned_globals.extend(reserved_lua_keywords_dict['environment_variables'])

    # Make another run and add all global functions that are not declared and not in the extended blacklist
    for function_entry in function_indexes:
        if function_entry['global'] and not function_entry['declaration'] \
                and function_entry['name']['name'] not in banned_globals:
            global_function_indexes.append({
                'start': function_entry['name']['start'],
                'end': function_entry['name']['end'],
                }
            )

    return global_function_indexes


def get_function_indexes(code: str, overwrite_indexes: list[dict[str, int]],
                         reserved_lua_keywords_dict: dict[str, list[str]]) \
        -> tuple[list[dict[str, int]], list[dict[str, int]], list[dict[str, int]], list[dict[str, int]]]:
    """ Gets the indexes of all functions in the code.
    The return object will have the structure:

    object = {
        'local': [
            'function_name': [
                {
                'start': start_index,
                'end': end_index,
                },
            ],
        ],
        ...
        'global': [
            'function_name': [
                {
                'start': start_index,
                'end': end_index,
                }
            ],
        ],
    }

    :param code: The code to search.
    :param overwrite_indexes: The indexes of the comments, documentation, strings, etc... that have priority.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of dictionaries containing the start and end indexes of each local function.
    """
    function_indexes: list[dict[str, Union[bool, dict[str, Union[str, int]]]]] = []
    built_in_list: list[str] = []
    built_in_list.extend(reserved_lua_keywords_dict['basic_functions'])
    built_in_list.extend(reserved_lua_keywords_dict['metamethods'])
    built_in_list.extend(reserved_lua_keywords_dict['environment_variables'])
    for match in g_function_pattern.finditer(code):
        function_indexes.append({
            'locality': match.regs[1][0] > -1,
            'global': match.regs[1][0] == -1 and match.regs[4][0] == -1 and match.regs[5][0] == -1,
            'declaration': match.regs[2][0] > -1,
            'built-int': match.group(3) in built_in_list and match.regs[2][0] < 0,
            'instance_method': match.regs[4][0] > -1,
            'static_method': match.regs[5][0] > -1,
            'name': {
                'start': match.regs[6][0],
                'end': match.regs[6][1],
                'name': match.group(6),
            },
        }
        )
    # Init lists for tracking local and global functions, instance and static methods
    local_function_declaration_indexes: list[tuple[str, int]] = []
    instance_method_indexes: list[dict[str, int]] = []
    static_method_indexes: list[dict[str, int]] = []
    global_function_declaration_indexes: list[tuple[str, int]] = []
    # Blacklist Lua keywords from global function names
    banned_globals: list[str] = ['']
    banned_globals.extend(reserved_lua_keywords_dict['keywords'])
    banned_globals.extend(reserved_lua_keywords_dict['tokens'])
    # Populate the lists
    function_indexes_dummy: list[dict[str, Union[bool, dict[str, Union[str, int]]]]] = function_indexes.copy()
    for function_entry in function_indexes_dummy:
        if function_entry['locality']:
            local_function_declaration_indexes.append((function_entry['name']['name'], function_entry['name']['start']))
            function_indexes.remove(function_entry)
        elif function_entry['global'] and function_entry['declaration'] \
                and function_entry['name']['name'] not in banned_globals:
            global_function_declaration_indexes.append((function_entry['name']['name'],
                                                        function_entry['name']['start']))
            function_indexes.remove(function_entry)
        elif function_entry['instance_method'] and not function_entry['built-int']:
            instance_method_indexes.append({
                'start': function_entry['name']['start'],
                'end': function_entry['name']['end'],
                }
            )
            function_indexes.remove(function_entry)
        elif function_entry['static_method'] and not function_entry['built-int']:
            static_method_indexes.append({
                'start': function_entry['name']['start'],
                'end': function_entry['name']['end'],
                }
            )
            function_indexes.remove(function_entry)

    # Remove functions that are part of a string or comment
    local_function_declaration_indexes = resolve_var_function_indexes(weak_list=local_function_declaration_indexes,
                                                                      strong_list=overwrite_indexes)
    _, instance_method_indexes = resolve_indexes(overwrite_indexes, instance_method_indexes, first_list_priority=True)
    _, static_method_indexes = resolve_indexes(overwrite_indexes, static_method_indexes, first_list_priority=True)
    global_function_declaration_indexes = resolve_var_function_indexes(weak_list=global_function_declaration_indexes,
                                                                       strong_list=overwrite_indexes)

    # Get the function indexes
    local_function_indexes:  list[dict[str, int]] = get_local_function_indexes(code,
                                                                               local_function_declaration_indexes)
    global_function_indexes: list[dict[str, int]] = get_global_function_indexes(code,
                                                                                global_function_declaration_indexes,
                                                                                banned_globals, function_indexes,
                                                                                reserved_lua_keywords_dict)

    # Sort the lists
    local_function_indexes.sort(key=lambda x: x['start'])
    global_function_indexes.sort(key=lambda x: x['start'])

    # Resolve overlaps with overwrite indexes
    _, local_function_indexes = resolve_indexes(overwrite_indexes, local_function_indexes, first_list_priority=True)
    _, global_function_indexes = resolve_indexes(overwrite_indexes, global_function_indexes, first_list_priority=True)

    return local_function_indexes, global_function_indexes, instance_method_indexes, static_method_indexes


def get_field_indexes(code: str) -> list[dict[str, int]]:
    """ Returns a list of dictionaries containing the start and end indexes of all fields in the code.

    :param code: The code to search for fields.
    :param overwrite_indexes: The indexes of the comments, documentation, strings, etc... that have priority.

    :return: A list of dictionaries containing the start and end indexes of all fields in the code.
    """
    field_indexes: list[dict[str, int]] = []
    # Get all tables which may have fields in them
    table_indexes: list[dict[str, int]] = get_pattern_indexes(code, g_table_content_pattern, pattern_filter=True)
    # Get all fields in the tables
    for table_index in table_indexes:
        field_indexes.extend(get_pattern_indexes(code[table_index['start']:table_index['end']], g_table_field_pattern,
                                                 pattern_filter=True, offset=table_index['start']))

    # Get all fields that are not in a table
    field_indexes.extend(get_pattern_indexes(code, g_field_pattern, pattern_filter=True))

    # Sort the list
    field_indexes.sort(key=lambda x: x['start'])
    return field_indexes
# pylint: enable=unused-variable

def _get_variable_declaration_indexes(code: str, pattern: re.Pattern, overwrite_indexes: list[dict[str, int]]) \
        -> list[tuple[str, int]]:
    """ Gets the indexes of variable declarations in the code.

    :param code: The code to search.
    :param pattern: The pattern to search for.
    :param comment_indexes: The indexes of the comments, documentation and strings.

    :return: A list of tuples containing the variable name and its start index.
    """
    variable_declaration_indexes: list[tuple[str, int]] = []
    for match in pattern.finditer(code):
        name = code[match.regs[1][0]:match.regs[1][1]]
        if ',' in name:
            variables: list[tuple[str, int]] = get_split_variables(name, match.regs[1][0])
            variable_declaration_indexes.extend(variables)
        else:
            variable_declaration_indexes.append((name, match.regs[1][0]))

    # Remove variables that are part of a string or comment
    variable_declaration_indexes = resolve_var_function_indexes(weak_list=variable_declaration_indexes,
                                                                strong_list=overwrite_indexes)

    return variable_declaration_indexes

# pylint: disable=unused-variable
def get_variable_indexes(code: str, declaration_indexes: list[tuple[str, int]],
                         scope_indexes: list[dict[str, tuple[int, int]]]) -> list[list[dict[str, int]]]:
    """ Gets the indexes of variables within their scope in the code.

    :param code: The code to search.
    :param declaration_indexes: The indexes of the variable declarations in the code.
    :param scope_indexes: The indexes of the scopes to the variables.

    :return: A list of dictionaries containing the variable name and its indexes.
    """
    variable_indexes: list[list[dict[str, int]]] = []
    for variable_index, variable_scope in zip(declaration_indexes, scope_indexes):
        index_offset: int = variable_index[1]
        variable_dict_list: list[dict[str, int]] = []
        for match in re.finditer(rf'''(?<!\w){variable_index[0]}(?!\w|[ \t]*\()''',
                                 code[variable_scope[variable_index[0]][0]:variable_scope[variable_index[0]][1]]):
            variable_dict_list.append({
                'start': match.regs[0][0] + index_offset,
                'end': match.regs[0][1] + index_offset,
                }
            )
        variable_indexes.append(variable_dict_list.copy())

    return variable_indexes


def get_local_variable_indexes(code: str, overwrite_indexes: list[dict[str, int]]) -> list[list[dict[str, int]]]:
    """ Gets the indexes of local variables in the code.

    :param code: The code to search.
    :param overwrite_indexes: The indexes of the comments, documentation and strings that takes priority.

    :return: A list of lists of dictionaries containing the local variable name and its indexes.
    """
    local_variable_declaration_indexes: list[tuple[str, int]] \
        = _get_variable_declaration_indexes(code, g_local_variables_pattern, overwrite_indexes)

    # Get scopes of local variables
    local_variable_scopes: list[dict[str, tuple[int, int]]] = _scope_finder(local_variable_declaration_indexes, code)
    # Get indexes of local variables
    local_variable_indexes: list[list[dict[str, int]]] \
        = get_variable_indexes(code, local_variable_declaration_indexes, local_variable_scopes)

    return local_variable_indexes


def get_parameter_variable_indexes(code: str, overwrite_indexes: list[dict[str, int]]) -> list[list[dict[str, int]]]:
    """ Gets the indexes of parameter variables in the code.

    :param code: The code to search.
    :param overwrite_indexes: The indexes of the comments, documentation and strings that takes priority.

    :return: A list of lists of dictionaries containing the parameter variable name and its indexes.
    """
    parameter_declaration_indexes: list[tuple[str, int]] \
        = _get_variable_declaration_indexes(code, g_parameters_variables_pattern, overwrite_indexes)
    parameter_declaration_indexes.extend(_get_variable_declaration_indexes(code, g_for_loop_parameters_pattern,
                                                                           overwrite_indexes))
    parameter_declaration_indexes.sort(key=lambda x: x[1])
    # Get scopes of parameter variables
    parameter_variable_scopes: list[dict[str, tuple[int, int]]] = _scope_finder(parameter_declaration_indexes, code)
    # Get indexes of parameter variables
    parameter_variable_indexes: list[list[dict[str, int]]] \
        = get_variable_indexes(code, parameter_declaration_indexes, parameter_variable_scopes)

    return parameter_variable_indexes


def get_global_variable_indexes(code: str, overwrite_indexes: list[dict[str, int]],
                                reserved_lua_keywords_dict: dict[str, list[str]]) \
        -> tuple[list[list[dict[str, int]]], list[dict[str, int]]]:
    """ Gets the indexes of global variables and declarations in the code.

    :param code: The code to search.
    :param overwrite_indexes: The indexes of the comments, documentation and strings that takes priority.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A list of lists of dictionaries containing the local variable name and its indexes.
    """
    # Declared global Variables
    # Get global variables
    banned_words: list[str] = reserved_lua_keywords_dict['keywords'].copy()
    banned_words.append('self')
    global_variables_pattern: re.Pattern = re.compile(g_declared_global_variables_pattern.pattern.replace(
        '#BANNEDWORDS', '|'.join(banned_words)), re.MULTILINE)
    global_variable_declaration_indexes: list[tuple[str, int]] \
        = _get_variable_declaration_indexes(code, global_variables_pattern, overwrite_indexes)

    # Get scopes of global variables
    global_variable_scopes: list[dict[str, tuple[int, int]]] = _scope_finder(global_variable_declaration_indexes, code)
    # Get indexes of global variables
    global_declared_variable_indexes: list[list[dict[str, int]]] \
        = get_variable_indexes(code, global_variable_declaration_indexes, global_variable_scopes)

    # Global Variables

    # Add built-ins to banned variables
    banned_words.extend(reserved_lua_keywords_dict['basic_functions'])
    banned_words.extend(reserved_lua_keywords_dict['metamethods'])
    banned_words.extend(reserved_lua_keywords_dict['environment_variables'])
    # Get global variables
    global_variables_pattern: re.Pattern \
        = re.compile(g_global_variables_pattern.pattern.replace('#BANNEDWORDS', '|'.join(banned_words)), re.MULTILINE)
    global_variable_indexes: list[dict[str, int]] = []
    for match in re.finditer(global_variables_pattern, code):
        global_variable_indexes.append({
            'start': match.regs[0][0],
            'end': match.regs[0][1],
            }
        )

    return global_declared_variable_indexes, global_variable_indexes


def get_all_variable_indexes(code: str, overwrite_indexes: list[dict[str, int]],
                             reserved_lua_keywords_dict: dict[str, list[str]]) \
        -> tuple[list[dict[str, int]], list[dict[str, int]], list[dict[str, int]]]:
    """ Gets the indexes of variables in the code.

    :param code: The code to search.
    :param overwrite_indexes: The indexes of the comments, documentation and strings that takes priority.
    :param reserved_lua_keywords_dict: A dictionary containing reserved Lua keywords.

    :return: A tuple containing the indexes of the local variables, parameter variables, declared global variables and
    global variables.
    """
    # Create list of banned variable names
    banned_variables: list[str] = []
    banned_variables.extend(reserved_lua_keywords_dict['keywords'])

    # Get local variables
    local_variable_indexes: list[list[dict[str, int]]] = get_local_variable_indexes(code, overwrite_indexes)
    # Get parameter variable
    parameter_variable_indexes: list[list[dict[str, int]]] = get_parameter_variable_indexes(code, overwrite_indexes)
    # Get global variables
    global_declared_variable_indexes, global_variable_indexes = get_global_variable_indexes(code, overwrite_indexes,
                                                                                            reserved_lua_keywords_dict)

    # Clean up variable indexes
    # Priority: local > parameter > declared global > global
    for local_var_list in local_variable_indexes:
        for param_var_list in parameter_variable_indexes:
            # Prune out needless calls
            if len(local_var_list) and len(param_var_list) and local_var_list[0]['start'] < param_var_list[-1]['end']:
                # Edits the lists directly so no return values
                remove_overlaps(local_var_list, param_var_list)

    # Unroll list of lists into a single list
    local_variable_indexes: list[dict[str, int]] = unroll_list(local_variable_indexes)
    local_variable_indexes.sort(key=lambda x: x['start'])
    parameter_variable_indexes: list[dict[str, int]] = unroll_list(parameter_variable_indexes)
    parameter_variable_indexes.sort(key=lambda x: x['start'])

    # Clean up global variables
    global_declared_variable_indexes: list[dict[str, int]] = unroll_list(global_declared_variable_indexes)
    _, global_variable_indexes = resolve_indexes(global_declared_variable_indexes, global_variable_indexes)
    global_variable_indexes.extend(global_declared_variable_indexes)
    global_variable_indexes.sort(key=lambda x: x['start'])
    _, global_variable_indexes = resolve_indexes(local_variable_indexes,
                                                 global_variable_indexes,
                                                 first_list_priority=True)
    _, global_variable_indexes = resolve_indexes(parameter_variable_indexes,
                                                 global_variable_indexes,
                                                 first_list_priority=True)

    # Resolve overlaps with overwrite_indexes
    _, local_variable_indexes = resolve_indexes(overwrite_indexes, local_variable_indexes, first_list_priority=True)
    _, parameter_variable_indexes = resolve_indexes(overwrite_indexes, parameter_variable_indexes,
                                                    first_list_priority=True)
    _, global_variable_indexes = resolve_indexes(overwrite_indexes, global_variable_indexes,
                                                 first_list_priority=True)

    return local_variable_indexes, parameter_variable_indexes, global_variable_indexes


def split_multiline_indexes(indexes_to_split: list[dict[str, int]],
                            newline_indexes: list[dict[str, int]]) -> list[dict[str, int]]:
    """ Splits multiline indexes into multiple indexes.

    :param indexes_to_split: The indexes to split.
    :param newline_indexes: The indexes of the newlines in the code.

    :return: A list of indexes.
    """
    split_indexes: list[dict[str, int]] = []
    for index in indexes_to_split:
        start_index = index['start']
        end_index = index['end']
        for newline_index in newline_indexes:
            if start_index <= newline_index['end'] < end_index:
                split_indexes.append({
                    'start': start_index,
                    'end': newline_index['end'],
                    }
                )
                start_index = newline_index['end'] + 1
        split_indexes.append({
            'start': start_index,
            'end': end_index,
            }
        )

    return split_indexes
# pylint: enable=unused-variable
