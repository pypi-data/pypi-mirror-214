""" This module provides support for parsing Lua files into a dictionary of DocEntry objects. """
import re
import os
from typing import Union
from hashlib import sha1
from lua_auto_doc.modules.lua_parser import doc_classes
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.progress_bar import ProgressBar
from lua_auto_doc.modules.lua_parser.doc_classes import DocLine, DocEntry, DocModule
from lua_auto_doc.modules.tools.misc import g_warning_colour, g_end_colour, g_error_colour


# Regex patterns
g_filter_pattern: re.Pattern = re.compile(r'''(\"(?:[^"\\\n]|\\.|\\\n)*\"|\'(?:[^'\\\n]|\\.|\\\n)*\'|\[(?P<raised>=*)\[[\w\W]*?\](?P=raised)\])|(\-{2}\[(?P<raised2>=*)\[[\w\W]*?\](?P=raised2)\]|--(?!-).*)|---.*''', re.MULTILINE)
""" A filter pattern that matches strings, multi-line strings, comments and doc lines. Group 1 captures strings,
 Group 3 captures comments. This pattern is for filtering only."""
g_module_pattern: re.Pattern = re.compile(r'''^[ \t]*---[ \t]*@module[ \t]+(.*)''', re.MULTILINE)
""" A pattern that matches module declaration lines. Group 1 captures the module name."""
g_invalid_module_description_pattern: re.Pattern = re.compile(r'''---[ \t]*@[ \t]*(?!description|see|internal|deprecated)\w*''', re.MULTILINE)
""" A pattern that matches invalid module description lines."""
g_doc_start_pattern: re.Pattern = re.compile(r'''(^[ \t]*---)''', re.MULTILINE)
""" A pattern that matches the start of a doc line. Group 1 captures the start of the doc line up to/including "---"."""
g_local_start_pattern: re.Pattern = re.compile(r'''^[ \t]*local(?=[ \t])''', re.MULTILINE)
""" A pattern that matches lines that start with "local". No capture groups."""
g_function_start_pattern: re.Pattern = re.compile(r'''^[ \t]*function(?=[ \t])''', re.MULTILINE)
""" A pattern that matches lines that start with "function". No capture groups."""
g_class_function_declaration_pattern: re.Pattern = re.compile(r'''^[ \t]*(local(?=[ \t]))?[ \t]*((?<!\w)function(?=[ \t]))?[ \t]*[a-zA-Z_]''', re.MULTILINE)
""" A pattern that matches lines that start with "local function", "local" or "function". Group 1 captures "local"
Group 2 captures "function"."""
g_ignore_pattern: re.Pattern = re.compile(r'''^[ \t]*---[ \t]*@ignore(?!\w)''', re.MULTILINE)
""" A pattern that matches lines that start with "--- @ignore". No capture groups."""
g_ignore_file_pattern: re.Pattern = re.compile(r'''^[ \t]*---[ \t]*@ignoreFile(?!\S)''', re.MULTILINE)
""" A pattern that matches lines that start with "--- @ignoreFile". No capture groups."""


def _filter_strings_and_comments(code: str) -> str:
    """ Removes all strings and comments from the code.

    :param code: The code to filter.

    :return: The filtered code.
    """
    instances: list[str] = []
    for match in g_filter_pattern.finditer(code):
        if match.group(1):
            instances.append((match.regs[1][0], match.regs[1][1]))
        elif match.group(3):
            instances.append((match.regs[3][0], match.regs[3][1]))

    start_index: int = 0
    clean_code: str = ''
    for instance in instances:
        clean_code += code[start_index:instance[0]]
        start_index = instance[1]
    clean_code += code[start_index:]

    return clean_code


def _list_is_class(comment_entries: list[DocLine]) -> bool:
    """ Checks if there is a class DocLine in the list.

    :param comment_entries: The list of comment entries.

    :return: True if there is a class DocLine in the list.
    """
    for entry in comment_entries:
        if entry.comment_type == 'class':
            return True
    return False


def _invalid_doc_entry(line: str, comment_entries: list[DocLine]) -> bool:
    """ Checks if the line belongs to an object that should be documented or not.

    :param line: The line to check.
    :param comment_entries: List of comment entries preceding the line.

    :return: True if the line should not be documented, False otherwise.
    """
    if line == '' or '=' in line and not _list_is_class(comment_entries):
        return True
    if 'function' not in line and '=' not in line:
        return True
    return False


def _is_module(line: str) -> bool:
    """ Checks if the line is a module.

    :param line: The line to check.

    :return: True if the line is a module, False otherwise.
    """
    try:
        return g_module_pattern.findall(line)[0]
    except IndexError:
        return False


def _get_formatted_class_name(line: str) -> str:
    """ Formats a class name from a lua line defining a class.

    :param name: The line to format.

    :return: The formatted class name to be easily parsed but DocEntry.__init__().
    """
    line = g_local_start_pattern.sub('', line).strip()
    full_name = line.split(' ')[0]
    return full_name


def _get_formatted_function_name(line: str) -> str:
    """ Formats a function name from a lua line defining a function.

    :param name: The line to format.

    :return: The formatted function name to be easily parsed but DocEntry.__init__().
    """
    line = g_local_start_pattern.sub('', line)
    line = g_function_start_pattern.sub('', line)
    line = line.split('(')[0].strip()
    return line


def _loop_lines(text: str) -> str:
    """ Loops over the lines in the text.

    :param text: The text to loop over.

    :return: A line from the text.
    """

    return iter(text.splitlines())


def _get_doc_entry(line: str, comment_entries: list[DocLine], line_number: int, module: str, relative_path: str,
                   hashed_filename: str) -> Union[DocEntry, None]:
    """ Creates a doc based on previous lines and the current one, called when no more "---" are detected.

    :param line: The line after the last "---" was detected, stripped for leading and trailing whitespace.
    :param comment_entries: List of comment entries preceding the line.
    :param line_number: Current line number.
    :param module: The module the documented lua object is in.
    :param relative_path: The relative path from source directory the line is in.

    :return: A doc entry to be documented or false if it was a normal variable.
    """
    # Return None if entry is invalid or ignored
    if _invalid_doc_entry(line, comment_entries):
        return None
    for entry in comment_entries:
        if g_ignore_pattern.search(entry.get_line()):
            return None

    match: re.Match = g_class_function_declaration_pattern.search(line)
    is_local: bool = match.group(1) == 'local'
    is_function: bool = match.group(2) == 'function'
    is_class: bool = False
    for entry in comment_entries:
        if entry.get_comment_type() == 'class':
            is_class = True

    if is_function:
        entry_type: str = 'function'
        name: str = _get_formatted_function_name(line)
    elif is_class:
        entry_type: str = 'class'
        name: str = _get_formatted_class_name(line)
    else:
        return None

    return DocEntry(name=name, entry_type=entry_type, locality=is_local, comment_entries=comment_entries,
                    line_number=line_number, def_line=line, module=module, relative_path=relative_path,
                    hashed_filename=hashed_filename)


def _creat_doc_entry(filename: str, relative_path: str, line: str, line_number: int, module: str,
                     temp_comment_holder: list[DocLine], doc_dict: dict[str, DocEntry]):
    """ Creates a doc entry based on collected DocLines in temp_comment_holder and adds it to doc_dict.

    :param filename: The filename of the file the entry is in.
    :param relative_path: The relative path from source directory the file is in.
    :param line: The line after the last "---" was detected, stripped for leading and trailing whitespace.
    :param line_number: Current line number.
    :param module: The name of module the documented lua object is in.
    :param temp_comment_holder: List of DocLines preceding the line.
    :param doc_dict: The dictionary to add the doc entry to.
    """
    # Create a hash of the filename to prevent collisions
    # noinspection InsecureHash
    hash_code: str = sha1(os.path.relpath(filename, conf.get_root_directory()).encode('utf-8')).hexdigest()[:10]
    source_code_mirror: str = f'{os.path.split(filename)[-1]}_{hash_code}.html'

    # Create DocEntry
    doc_entry = _get_doc_entry(line, temp_comment_holder, line_number + 1, module, relative_path,
                               source_code_mirror)
    parent_id_key: str = '-'
    if doc_entry and doc_entry.get_parent_id():
        parent_id_key = f'{doc_entry.get_hashed_filename()}:{doc_entry.get_parent_id()}'
    # Skip if doc_entry is hidden
    if doc_entry and doc_entry.is_hidden(conf.get_show_hidden()):
        pass
    # Add documented lua object if a valid line was found
    elif doc_entry and doc_entry.get_type() == 'function' and parent_id_key in doc_dict:
        doc_dict[parent_id_key].add_method(doc_entry)
        doc_entry.set_method_parent(doc_dict[parent_id_key])
    elif doc_entry:
        doc_dict[doc_entry.get_id()] = doc_entry


def _parse_lua_file(filename: str, relative_path: str, encoding='utf-8') -> tuple[list[DocModule], dict[str, DocEntry]]:
    """Get the Lua docs for a given file.

    :param filename: The name of the file to parse.
    :param relative_path: The relative path from source directory the file is in.
    :param encoding: The encoding of the file.

    :return: A dictionary of the docs.
    """
    # Normalise the filename
    filename = os.path.normpath(filename)

    if not filename.endswith('.lua'):
        filename += '.lua'

    with open(filename, 'r', encoding=encoding) as file:
        # clean up the code
        clean_file: str = _filter_strings_and_comments(file.read())

    # Return if @ignoreFile
    if g_ignore_file_pattern.search(clean_file):
        return [], {}

    doc_modules: list[DocModule] = []
    doc_dict: dict[str, DocEntry] = {}
    temp_comment_holder: list[DocLine] = []
    active_module_docstring: bool = False
    doc_start: bool = False
    module: str = ''
    for line_number, line in enumerate(_loop_lines(clean_file)):
        docstring: bool = g_doc_start_pattern.search(line) is not None

        # Check if line is a module
        if _is_module(line):
            module = _is_module(line)
            active_module_docstring = True
            # Reset comment holder in case of bad syntax from user
            temp_comment_holder = [DocLine(line, line_number + 1, filename)]
            continue
        if active_module_docstring and docstring:  # Module description
            if g_invalid_module_description_pattern.search(line) is not None:
                print(f'\n{g_warning_colour}ERROR(LDP-1): Detected invalid docstring below module declaration on line'
                      f' {line_number} in {relative_path}. Ignoring docstring.{g_end_colour}')
                continue
            temp_comment_holder.append(DocLine(line, line_number + 1, filename))
            continue
        if active_module_docstring:  # End of module docstring
            if module in doc_modules:
                index: int = doc_modules.index(module)
                doc_modules[index].extend(DocModule(module, temp_comment_holder))
            else:
                doc_modules.append(DocModule(module, temp_comment_holder))
            active_module_docstring = False
            temp_comment_holder = []
            continue

        # Check if line is a docstring
        if docstring:
            doc_start = True
            temp_comment_holder.append(DocLine(line, line_number + 1, filename))
        else:
            # Create a DocEntry if end of a docstring
            if doc_start:
                _creat_doc_entry(filename, relative_path, line, line_number, module, temp_comment_holder, doc_dict)
                # Reset variables
                doc_start = False
                temp_comment_holder = []

    return doc_modules, doc_dict


def _extend_module_list(main_list: list[DocModule], extension: list[DocModule]) -> list[DocModule]:
    """ Extends a list of DocModules with another list of DocModules, checking for duplicates.

    :param main_list: The list of DocModules to extend.
    :param extension: The list of DocModules to extend with.

    :return: The extended list of DocModules.
    """
    for module in extension:
        duplicate: bool = False
        for existing_module in main_list:
            if module.name == existing_module:
                existing_module.extend(module)
                duplicate = True
                break
        if not duplicate:
            main_list.append(module)

    return main_list


# pylint: disable=unused-variable
def parse_lua_folder(folder_name: str, encoding='utf-8') -> tuple[list[DocModule], dict[str, DocEntry]]:
    """Get the Lua docs for a given folder.

    :param folder_name: The name of the folder to search and parse.
    :param encoding: The encoding of the files to read.

    :return: A dictionary of the docs.
    """
    doc_dict: dict[str, DocEntry] = {}
    doc_modules: list[DocModule] = []
    if not os.path.isdir(folder_name):
        print(f'\n{g_error_colour}ERROR(LDP-4): {folder_name} is not a directory, with cwd: {os.getcwd()}.\n'
              f'Terminating program.{g_end_colour}')
        raise NotADirectoryError(f'{folder_name} is not a directory.')

    # Get total number of lua files
    total_lua_files: int = 0
    for _, _, filenames in os.walk(folder_name):
        for filename in filenames:
            if filename.endswith('.lua'):
                total_lua_files += 1

    # Set up ProgressBar
    progress_bar: ProgressBar = ProgressBar(total=total_lua_files, description='Scanning docstrings:')
    progress_bar.start()
    # Parse all lua files
    for root, _, filenames in os.walk(folder_name):
        for filename in filenames:
            if filename.endswith('.lua'):
                relative_path = os.path.join(os.path.relpath(root, folder_name), filename)
                modules, doc_objects = _parse_lua_file(f'{root}/{filename}', relative_path, encoding=encoding)
                doc_modules = _extend_module_list(doc_modules, modules)
                doc_dict.update(doc_objects)
                progress_bar.update(1)

    doc_classes.link_class_child_parents(doc_dict)
    doc_classes.link_method_child_parents(doc_dict)
    doc_classes.update_inherited_methods(doc_dict)
    doc_classes.init_see_lists(doc_dict, doc_modules)

    # Sort modules
    doc_modules.sort(key=lambda x: x.get_name().lower())

    return doc_modules, doc_dict
# pylint: enable=unused-variable
