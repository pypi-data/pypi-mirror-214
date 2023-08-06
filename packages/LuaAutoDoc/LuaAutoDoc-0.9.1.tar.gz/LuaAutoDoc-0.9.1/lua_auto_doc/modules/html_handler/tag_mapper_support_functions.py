""" This module provides support functions for tag_mapper."""

import re
from lua_auto_doc.modules.lua_parser import doc_classes


# Regex patterns
g_type_decomposition_pattern: re.Pattern = re.compile( r'''(?:&lt;|&gt;)|([a-zA-Z_][\w \t]*:)|(?<![a-zA-Z_])(function|func?|vararg)(?!\w)|([a-zA-Z_][\w\.]*(?:\(\))?)|(?<=[\W0-9])(0x[a-fA-F\d]*|\d+\.?\d+|(?<!\.)\.\d+|\d+\.?)''',
    re.MULTILINE)
""" The regex pattern used to decompose a type into its parts
Group 1 either captures the class name or filters away parameter names, needs to be investigated with
    doc_classes.find_see()
Group 2 captures the function keyword
Group 3 captures either a class method/field or a normal type following a parameter, needs to have its prior capture
    investigated
Group 4 captures a number, including hex and floats
"""
# main_page_navbar_href_processor specific patterns
g_parent_directory_pattern: re.Pattern = re.compile(r'''^../''')
""" A pattern that matches the parent directory path at the start of a link. No group captures."""
g_web_link_protocol_pattern: re.Pattern = re.compile(r'''^\w+://''')
""" A pattern that matches the protocol at the start of a link. No group captures."""


# pylint: disable=unused-variable
def main_page_navbar_href_processor(fragment, link_match,  start) -> str:
    """ Function for handling the NavBarCustomContent tag on the main page.
    Changes path references from being for the subdirectory html/ to the root directory.

    :param fragment: The NavBarCustomContent fragment.
    :param link_match: The match object for the link.
    :param start: The start index to start the fragment slice from.

    :return: The slice of the fragment with the link replaced.
    """
    new_fragment: str = ''
    if g_parent_directory_pattern.match(link_match.group(2)):
        new_link: str = g_parent_directory_pattern.sub('', link_match.group(2))
        new_fragment = f'{fragment[start:link_match.regs[2][0]]}{new_link}'
        start: int = link_match.regs[2][1]
    # Check if the link contains a web protocol
    elif g_web_link_protocol_pattern.match(link_match.group(2)):
        pass
    # Else it's most likely a path reference
    else:
        # If it does not reference the parent directory, it must reference a html file
        new_link: str = f'html/{link_match.group(2).lstrip("/")}'
        new_fragment = f'{fragment[start:link_match.regs[2][0]]}{new_link}'
        start: int = link_match.regs[2][1]

    return new_fragment, start


def _decompose_type(type_string) -> tuple[list[tuple[str, str, str, str]], list[list[int, int]]]:
    """ Decomposes a type string into its parts and stores the indices of the parts in index_list and the parts
    in decomposed_type.

    :type type_string: The string to decompose.

    :return: A tuple containing the decomposed type and the indices of the parts.
    """
    decomposed_type: list[tuple[str, str, str, str]] = []
    index_list: list[list[int, int]] = []
    for match in g_type_decomposition_pattern.finditer(type_string):
        if match.regs[1][0] != -1:
            index_list.append([match.regs[1][0], match.regs[1][1]])
            decomposed_type.append((match.group(1), match.group(2), match.group(3), match.group(4)))
        elif match.regs[2][0] != -1:
            index_list.append([match.regs[2][0], match.regs[2][1]])
            decomposed_type.append((match.group(1), match.group(2), match.group(3), match.group(4)))
        elif match.regs[3][0] != -1:
            index_list.append([match.regs[3][0], match.regs[3][1]])
            decomposed_type.append((match.group(1), match.group(2), match.group(3), match.group(4)))
        elif match.regs[4][0] != -1:
            index_list.append([match.regs[4][0], match.regs[4][1]])
            decomposed_type.append((match.group(1), match.group(2), match.group(3), match.group(4)))

    return decomposed_type, index_list


def _get_colour_type_results(decomposed_type: list[tuple[str, str, str, str]], index_list: list[list[int, int]],
                             data_object: dict[str, any], current_data: dict[str, any], lua_primitives: list[str]) \
        -> list[str]:
    """ Loops through the decomposed types and creates a html formatted string for highlighting the types.

    :param decomposed_type: The decomposed type list.
    :param index_list: The index list of decomposed_type.
    :param data_object: The data object to use for certain tags.
    :param current_data: Data regarding the current file being built.
    :param lua_primitives: A list of lua primitives.

    :return: A list of html formatted strings for highlighting the types.
    """
    param_class, function_key, type_class_method, number = 0, 1, 2, 3
    results: list[str] = []
    skip_flag: bool = False
    for i, sublist in enumerate(decomposed_type):
        # If the lookahead got previously triggered, skip this iteration
        if skip_flag:
            skip_flag = False
            # Update index list
            index_list[i - 1][1] = index_list[i][1]
            index_list[i] = None
            continue
        # Either a parameter or a class
        if sublist[param_class]:
            # Check for match of an instance method
            if decomposed_type[i + 1][type_class_method]:
                href, _, _ = doc_classes.find_see(f'---@see {sublist[param_class]}'
                                                  f'{decomposed_type[i + 1][type_class_method]}',
                                                  data_object['doc_entries'],
                                                  data_object['doc_modules'],
                                                  ignore_miss=True)
                if href:
                    results.append(f'<a href="{"../" * current_data["folder_depth"]}{href}">{sublist[param_class]}'
                                   f'{decomposed_type[i + 1][type_class_method]}</a>')
                    skip_flag = True
                    continue

            # Else it's a parameter
            results.append(f'<span class="lua-param">{sublist[param_class]}</span>')
            continue

        # Check if it's a function keyword
        if sublist[function_key]:
            results.append(f'<span class="lua-function">{sublist[1]}</span>')
            continue

        # Check if it's a normal type or a class
        if sublist[type_class_method]:
            # Check if it's a primitive
            if sublist[type_class_method] in lua_primitives:
                results.append(f'<span class="lua-type">{sublist[type_class_method]}</span>')
                continue
            # Check if it's a class
            href, _, _ = doc_classes.find_see(f'---@see {sublist[type_class_method]}',
                                              data_object['doc_entries'],
                                              data_object['doc_modules'],
                                              ignore_miss=True)
            if href:
                results.append(
                    f'<a href="{"../" * current_data["folder_depth"]}{href}">{sublist[type_class_method]}</a>')
                continue
            # Else it's an unknown type
            results.append(f'<span class="lua-unknown">{sublist[type_class_method]}</span>')
            continue

        # Check if it's a number
        if sublist[number]:
            results.append(f'<span class="lua-number">{sublist[number]}</span>')
            continue

    return results


def colour_type(type_string: str, data_object: dict[str, any], current_data: dict[str, any]) -> str:
    """ Returns a string with the appropriate html tags for the parts of the (possible composite) type.

    :param type_string: The type string to colour.
    :param data_object: The data object to use for certain tags.
    :param current_data: Data regarding the current file being built.

    :return: A string with html tags with the correct colour classes.
    """
    if not type_string:
        return ''

    # Check for Lua primitives
    lua_primitives: list[str] = ['nil', 'boolean', 'number', 'integer', 'float', 'string', 'table', 'function',
                                 'CFunction', 'userdata', 'any', ]
    if type_string in lua_primitives:
        return f'<span class="lua-type">{type_string}</span>'
    # Check if the type is a simple, documented object
    href, _, _ = doc_classes.find_see(f'---@see {type_string}', data_object['doc_entries'],
                                      data_object['doc_modules'], ignore_miss=True)
    if href:
        return f'<a href="{"../" * current_data["folder_depth"]}{href}">{type_string}</a>'

    # Check if the type is a composite type
    decomposed_type, index_list = _decompose_type(type_string)

    # Add an empty list at the end to allow for a simple lookahead in the for loop
    if decomposed_type:
        decomposed_type.append((None, None, None, None))

    results: list[str] = _get_colour_type_results(decomposed_type, index_list, data_object, current_data,
                                                  lua_primitives)

    # Remove None values from index list
    index_list = [x for x in index_list if x]

    # Rebuild the string
    html_string: str = type_string[:index_list[0][0]]
    for i in range(len(results) - 1):
        html_string += results[i]
        html_string += type_string[index_list[i][1]:index_list[i + 1][0]]
    html_string += results[-1]
    html_string += type_string[index_list[-1][1]:]

    return html_string
# pylint: enable=unused-variable
