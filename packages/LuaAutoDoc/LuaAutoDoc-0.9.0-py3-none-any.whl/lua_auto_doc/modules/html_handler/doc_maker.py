""" This module provides support for making documentation from a dictionary of DocEntry objects. """

import re
import os
import sys
import shutil
import fnmatch
import multiprocessing
from typing import Callable
from concurrent.futures import ProcessPoolExecutor
from lua_auto_doc.modules.lua_parser import doc_classes
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.progress_bar import ProgressBar
from lua_auto_doc.modules.html_handler.tag_mapper import tag_mapper, resolve_fragment
from lua_auto_doc.modules.html_handler.fragment_reader import g_html_fragment_pattern
from lua_auto_doc.modules.highlighter.indexer import index_code, indexed_code_to_html
from lua_auto_doc.modules.highlighter.highlighter import folder_generate_highlighted_html
from lua_auto_doc.modules.tools.misc import g_warning_colour, g_error_colour, g_end_colour
from lua_auto_doc.modules.lua_parser.doc_classes import DocEntry, DocModule, g_link_hint_pattern
from lua_auto_doc.modules.html_handler.data_store_maker import create_datastore, g_tag_content_pattern


# Regex patterns
g_complete_html_pattern: re.Pattern = re.compile(r'''<!DOCTYPE html>[\s\S]*?<html[\s\S]*?<head>[\s\S]*?</head>[\s\S]*?<body[\s\S]*?</body>[\s\S]*?</html>''',
                                                 re.MULTILINE)
""" A pattern that matches a complete html document. Declaration, html body, head and body. No group captures."""
# Second pass specific patterns
g_html_header_pattern: re.Pattern = re.compile(r'''<h(?P<header>\d)[^>]*?id="([^"]*)"[^>]*?>(.*?)</h(?P=header)''',
                                               re.MULTILINE)
""" A pattern used to find HTML headers and their ids.
Group 2 captures the id of the header
Group 3 captures the text of the header. NOTE! It will also captures any html tags nested inside the header.
"""
g_clean_pre_pattern: re.Pattern = re.compile(r'''<pre\s[^>]*?class="code-field-clean"[^>]*?>\n*([\s\S]*?)</pre>''',
                                             re.MULTILINE)
""" A pattern used to find HTML content inside <pre class="code-field-clean"> tags.
Group 1 captures the content inside the <pre> tag."""
g_li_tag_pattern: re.Pattern = re.compile(r'''<li[^>]*?>|</li>''', re.MULTILINE)
""" A pattern used to find <li> tags. """
g_numbered_pre_pattern: re.Pattern = re.compile(r'''<pre\s[^>]*?class="code-field-numbered"[^>]*?>\n*([\s\S]*?)</pre>''',
                                                re.MULTILINE)
""" A pattern used to find HTML content inside <pre class="code-field-numbered"> tags.
Group 1 captures the content inside the <pre> tag."""


def clean_build_directory(build_directory) -> None:
    """ Deletes the DocBuild folder if it exists.
    """
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory, ignore_errors=False, onerror=None)


# pylint: disable=unused-variable
def init_build_directory() -> None:
    """ Creates the DocBuild folder and subfolders.
    """

    # Taken from ArockiaRaj solution on
    # https://stackoverflow.com/questions/52071642/python-copying-the-files-with-include-pattern
    def include_pattern(*patterns) -> Callable:
        """Factory function that can be used with copytree() ignore parameter.

        Arguments define a sequence of glob-style patterns
        that are used to specify what files to NOT ignore.
        Creates and returns a function that determines this for each directory
        in the file hierarchy rooted at the source directory when used with
        shutil.copytree().

        :param patterns: A sequence of glob-style patterns that are used to specify what files to NOT ignore.

        :return: A function that determines what files to ignore.
        """
        def _ignore_patterns(path, names) -> set[str]:
            """ A template function for use with shutil.copytree() ignore parameter.

            :param path: The path to the directory.
            :param names: The names of the files in the directory.

            :return: A set of file names to ignore.
            """
            keep = set(name for pattern in patterns for name in fnmatch.filter(names, pattern))
            ignore = set(name for name in names if name not in keep and not os.path.isdir(os.path.join(path, name)))
            return ignore

        return _ignore_patterns

    stylesheets_directory: str = os.path.join(conf.get_build_directory(), 'stylesheets')
    scripts_directory: str = os.path.join(conf.get_build_directory(), 'scripts')
    html_directory: str = os.path.join(conf.get_build_directory(), 'html')
    favicon_directory: str = os.path.join(conf.get_build_directory(), 'favicon')
    assets_directory: str = os.path.join(conf.get_build_directory(), 'assets')
    data_directory: str = os.path.join(conf.get_build_directory(), 'data')
    build_directory: str = conf.get_build_directory()

    clean_build_directory(build_directory)
    os.mkdir(build_directory)
    os.mkdir(stylesheets_directory)
    os.mkdir(scripts_directory)
    os.mkdir(html_directory)
    os.mkdir(favicon_directory)
    os.mkdir(assets_directory)
    os.mkdir(data_directory)

    # Copy over files
    if os.path.isdir(conf.get_stylesheet_directory()):
        shutil.copytree(src=conf.get_stylesheet_directory(), dst=stylesheets_directory,
                        ignore=include_pattern('*.css', '*.sass', '*.scss'), dirs_exist_ok=True)
    if os.path.isdir(conf.get_scripts_directory()):
        shutil.copytree(src=conf.get_scripts_directory(), dst=scripts_directory,
                        ignore=include_pattern('*.js', '*.ts'), dirs_exist_ok=True)
    if os.path.isdir(conf.get_assets_directory()):
        shutil.copytree(src=conf.get_assets_directory(), dst=assets_directory, dirs_exist_ok=True)
    if os.path.isdir(conf.get_favicon_directory()):
        shutil.copytree(src=conf.get_favicon_directory(), dst=favicon_directory, dirs_exist_ok=True)

    # Copy over default files, but avoid overwriting existing files
    stylesheet_pattern: re.Pattern = re.compile(r'''\.(?:css|scss|sass)$''', re.IGNORECASE)
    inbuilt_stylesheet_directory: str = conf.get_default_stylesheet_directory()
    for file in os.listdir(inbuilt_stylesheet_directory):
        if not os.path.isfile(os.path.join(stylesheets_directory, file)) \
                and stylesheet_pattern.search(file) is not None:
            shutil.copy2(os.path.join(inbuilt_stylesheet_directory, file), os.path.join(stylesheets_directory, file))

    script_pattern: re.Pattern = re.compile(r'''\.(?:js|ts)$''', re.IGNORECASE)
    inbuilt_scripts_directory: str = conf.get_default_scripts_directory()
    for file in os.listdir(inbuilt_scripts_directory):
        if not os.path.isfile(os.path.join(scripts_directory, file)) and script_pattern.search(file) is not None:
            shutil.copy2(os.path.join(inbuilt_scripts_directory, file), os.path.join(scripts_directory, file))

    inbuilt_assets_directory: str = conf.get_default_assets_directory()
    for file in os.listdir(inbuilt_assets_directory):
        if not os.path.isfile(os.path.join(assets_directory, file)):
            shutil.copy2(os.path.join(inbuilt_assets_directory, file), os.path.join(assets_directory, file))

    inbuilt_favicon_directory: str = conf.get_default_favicon_directory()
    for file in os.listdir(inbuilt_favicon_directory):
        if not os.path.isfile(os.path.join(favicon_directory, file)):
            shutil.copy2(os.path.join(inbuilt_favicon_directory, file), os.path.join(favicon_directory, file))
# pylint: enable=unused-variable


def _custom_page_navbar_handler(page: str) -> str:
    """ Parses a html page customised by the user and adds headers to the "current page" section in the navbar.

    :param page: The html page to parse.
    """
    headers: list[tuple[str, str, str]] = g_html_header_pattern.findall(page)
    current_page_index: int = page.find('class="nav-bar-list-content">') + len('class="nav-bar-list-content">')
    if len(headers) and current_page_index > len('<div class="nav-bar-list-content">'):
        start_page: str = page[:current_page_index]
        for header in headers:
            tag_id: str = header[1]
            name: str = ''.join(g_tag_content_pattern.findall(header[2]))
            if not name:
                name = header[2]
            start_page += \
                f'''<a href="#{tag_id}"><span class="nav-bar-list-button" data-prefix="  "><wbr>{name}</span></a>'''
        page = start_page + page[current_page_index:]

    return page


def _second_pass(page: str, doc_entries: dict[str, DocEntry], doc_modules: list[DocModule],
                 current_data: dict[str, any]) -> str:
    """ Goes through the html a second time to resolves remaining processes like ---@see.

    :param page: The page to resolve.
    :param doc_entries: The DocEntries to use for the search.
    :param doc_modules: The DocModules to use for the search.
    :param current_data: The current data to use for the search.

    :return: The resolved page.
    """
    while see := g_link_hint_pattern.search(page):
        href, name, _ = doc_classes.find_see(see.group(0), doc_entries, doc_modules)
        if href is not None:
            replace_text: str = page[see.regs[0][0]:see.regs[5][0]]
            new_text: str = f'<a href="{"../" * current_data["folder_depth"]}{href}">{name}</a> '
            page = page.replace(replace_text, new_text, 1)
        else:
            print(f'{g_warning_colour}File: {current_data["current_file"]}{g_end_colour}')
            break

    # Add headers to the "current page" navbar for special pages
    invalid_pages: list[str] = ['function', 'class', 'source', 'module']
    if current_data['context'] not in invalid_pages:
        page = _custom_page_navbar_handler(page)

    # Replace code fields with formatted code
    for match in g_clean_pre_pattern.finditer(page):
        code_content: str = match.group(1)
        indexed_code: dict[int, set[str]] = index_code(code_content, float(conf.get_lua_version()))
        html_code: str = indexed_code_to_html(code_content, indexed_code, default_linenum=False)
        html_code = g_li_tag_pattern.sub('', html_code)
        page = page.replace(code_content, html_code, 1)

    for match in g_numbered_pre_pattern.finditer(page):
        code_content: str = match.group(1)
        indexed_code: dict[int, set[str]] = index_code(code_content, float(conf.get_lua_version()))
        html_code: str = indexed_code_to_html(code_content, indexed_code, default_linenum=False)
        html_code = f'<ol class="ol-linenum-class">{html_code}</ol>'
        page = page.replace(code_content, html_code, 1)

    return page


def _create_data_object(modules: list[DocModule], doc_entries: dict[str, DocEntry]) -> dict[str, any]:
    """ Creates a generic data object that tag_mapper() can use to get context for the HTML fragments.

    :param modules: The list of modules to create the data object from.
    :param doc_entries: The dictionary of DocEntry objects to create the data object from.

    :return: The data object.
    """
    def _add_to_module(entry: DocEntry) -> None:
        """ Adds the given DocEntry to the module it belongs to.

        :param entry: The DocEntry to add to the module.
        """
        for doc_module in modules:
            if doc_module.get_name() == entry.get_module():
                if entry.get_type() == 'class':
                    doc_module.add_class(entry)
                elif entry.get_type() == 'function':
                    doc_module.add_function(entry)
                else:
                    print(f'{g_warning_colour}WARNING: Unknown doc_entry type {entry.get_type()} encountered, please '
                          f'report this bug. Object will not be included in the documentation.{g_end_colour}')

    def _connect_entries_to_modules() -> None:
        for doc_entry in doc_entries.values():
            if doc_entry.get_module() != '':
                _add_to_module(doc_entry)
            elif doc_entry.get_type() == 'class':
                data_object['classes'].append(doc_entry)
            elif doc_entry.get_type() == 'function':
                data_object['functions'].append(doc_entry)
            else:
                print(f'{g_warning_colour}WARNING: Unknown doc_entry type {doc_entry.get_type()} encountered, please '
                      f'report this bug. Object will not be included in the documentation.{g_end_colour}')

    # Create the data object
    data_object: dict[str, any] = {
        'module_dict': {key.get_name(): key for key in modules},
        'classes': [],
        'functions': [],
        'stylesheets': [],
        'scripts': [],
        'doc_entries': doc_entries,
        'doc_modules': modules,
    }

    # Connect class and functions to their modules
    _connect_entries_to_modules()

    # Sort entries in the modules
    for module in modules:
        module.sort_entries()

    # Add default stylesheets and scripts to the data object
    valid_stylesheets: list[str] = ['.css', '.scss', '.sass', ]
    valid_scripts: list[str] = ['.js', '.ts', ]
    data_object['stylesheets'] = [
        'LuaAutoDoc.css',
        'GenericPages.css',
        'CodeObjects.css',
        'SourceCode.css',
        'SourceCodeFolderMap.css',
        'SearchPage.css',
    ]
    data_object['scripts'] = [
        'LuaAutoDoc.js',
        'ThemeChanger.js',
        'ElementSizeObserver.js',
        'NavBarListHandler.js',
        'SearchHandler.js',
        'SourceCodeFolderMap.js',
    ]
    if os.path.isdir(conf.get_stylesheet_directory()):
        for root, _, files in os.walk(conf.get_stylesheet_directory()):
            for file in files:
                if file not in data_object['stylesheets'] and os.path.splitext(file)[1] in valid_stylesheets:
                    data_object['stylesheets'].append(os.path.relpath(os.path.join(root, file),
                                                                      conf.get_stylesheet_directory()).replace('\\',
                                                                                                               '/'))
    if os.path.isdir(conf.get_scripts_directory()):
        for root, _, files in os.walk(conf.get_scripts_directory()):
            for file in files:
                if os.path.splitext(file)[1] in valid_scripts and file not in data_object['scripts']:
                    data_object['scripts'].append(os.path.relpath(os.path.join(root, file),
                                                                  conf.get_scripts_directory()).replace('\\',
                                                                                                        '/'))

    return data_object


def _generate_html(start_tag: str, tag_type: str, data_object: dict[str, any], current_data: dict[str, any],
                   destination_folder: str, file_name: str, pipe=None) -> tuple[str, str]:
    """ Generates the html code for given object.

    :param start_tag: The tag to start generating the html code from.
    :param tag_type: The type of the tag. tag_mapper/fragment
    :param data_object: The data object to use for the object
    :param current_data: Data regarding the current file being built.
    :param destination_folder: The folder to file is aimed at
    :param file_name: The name of the file to generate
    :param pipe: The pipe to send a message to when the file is done generating if multiprocessing is used.
    :type pipe: Connection

    :return: The file path and the html code.
    """
    if tag_type == 'tag_mapper':
        html_file: str = tag_mapper(start_tag, data_object, current_data)
        html_file = _second_pass(html_file, data_object['doc_entries'], data_object['doc_modules'], current_data)
    elif tag_type == 'fragment':
        html_file: str = resolve_fragment(start_tag, data_object, current_data)
    else:
        raise ValueError(f'{g_error_colour}Unknown tag type {tag_type} encountered, please report this bug.'
                         f'{g_end_colour}')

    if pipe:
        pipe.send(1)
    return os.path.join(destination_folder, file_name), html_file


def _get_build_file_info(data_object: dict[str, any], source_code_files: list[tuple[str, str, str]],
                         modules: list[DocModule]) -> list[dict[str, any]]:
    """ Creates a list of dicts containing file info for files to be created.

    :param data_object: The data object to use for the creation of the files.
    :param source_code_files: The list of html highlighted source code to create files of.
    :param modules: The list of modules to build the HTML files from.

    :return: A list of dicts containing file info for files to be created.
    """
    file_info: list[dict[str, any]] = []
    # Set up the main page
    file_info.append(
        {'current_data':
            {
                'context': 'file',
                'current_file': conf.get_main_page(),
                'folder_depth': 0,
                'page_name': 'Main Page',
            },
            'tag_type': 'tag_mapper',
            'start_tag': 'IndexHTML',
            'data_object': data_object,
            'destination_folder': conf.get_build_directory(),
            'file_name': conf.get_main_page()
        }
    )

    html_location: str = os.path.join(conf.get_build_directory(), 'html')
    # Set up Search Page
    file_info.append(
        {'current_data':
            {
                'context': 'search_page',
                'current_file': 'search_page.html',
                'folder_depth': 1,
                'page_name': 'Search',
            },
            'tag_type': 'tag_mapper',
            'start_tag': 'SearchPage',
            'data_object': data_object,
            'destination_folder': html_location,
            'file_name': 'search_page.html'
        }
    )
    # Set up the module pages
    for module in modules:
        file_info.append(
            {'current_data':
                {
                    'context': 'module',
                    'current_file': module.get_name(),
                    'folder_depth': 1,
                    'page_name': module.get_name(),
                    'entries': module.get_entries(),
                    'entry': module,
                },
                'tag_type': 'tag_mapper',
                'start_tag': 'ModulePage',
                'data_object': data_object,
                'destination_folder': html_location,
                'file_name': module.get_file_name(),
            }
        )
    # Set up the class pages
    if len(data_object['classes']) > 0:
        file_info.append(
            {'current_data':
                {
                    'context': 'class',
                    'current_file': 'Classes.html',
                    'folder_depth': 1,
                    'page_name': 'Classes',
                    'entries': data_object['classes'],
                },
                'tag_type': 'tag_mapper',
                'start_tag': 'ClassPage',
                'data_object': data_object,
                'destination_folder': html_location,
                'file_name': 'Classes.html',
            }
        )

    # Set up the function pages
    if len(data_object['functions']) > 0:
        file_info.append(
            {'current_data':
                {
                    'context': 'function',
                    'current_file': 'Functions.html',
                    'folder_depth': 1,
                    'page_name': 'functions',
                    'entries': data_object['functions'],
                },
                'tag_type': 'tag_mapper',
                'start_tag': 'FunctionPage',
                'data_object': data_object,
                'destination_folder': html_location,
                'file_name': 'Functions.html',
            }
        )

    # Set up source code mirror pages
    if not conf.get_hide_source_code():
        for filename, file_content, filepath in source_code_files:
            file_info.append(
                {'current_data':
                    {
                        'context': 'source',
                        'current_file': filename,
                        'folder_depth': 1,
                        'page_name': 'sourcecode',
                        'filepath': filepath,
                    },
                    'tag_type': 'fragment',
                    'start_tag': file_content,
                    'data_object': data_object,
                    'destination_folder': html_location,
                    'file_name': filename,
                }
            )
        # Add SourceCodeFolderMap
        file_info.append(
            {
                'current_data':
                    {
                        'context': 'folder_map',
                        'current_file': 'sourcecode.html',
                        'folder_depth': 1,
                        'page_name': 'Project Folder Map',
                    },
                'tag_type': 'tag_mapper',
                'start_tag': 'SourceCodeFolderMap',
                'data_object': data_object,
                'destination_folder': html_location,
                'file_name': 'sourcecodefoldermap.html',
            }
        )

    # Set up the custom pages added by the user
    for root, _, file in os.walk(conf.get_html_fragment_directory()):
        for filename in file:
            if filename.endswith('.html'):
                with open(os.path.join(root, filename), 'r', encoding=conf.get_encoding()) as f:
                    text: str = f.read()
                if g_complete_html_pattern.search(text) is not None and g_html_fragment_pattern.search(text) is None:
                    page_name: str = filename.replace('_', ' ').replace('-', ' ').replace('.html', '').capitalize()
                    file_info.append(
                        {'current_data':
                            {
                                'context': 'custom',
                                'current_file': filename,
                                'folder_depth': 1,
                                'page_name': page_name,
                                'filepath': os.path.join(root, filename),
                            },
                            'tag_type': 'fragment',
                            'start_tag': text,
                            'data_object': data_object,
                            'destination_folder': html_location,
                            'file_name': filename,
                        }
                    )

    return file_info


# pylint: disable=unused-variable
def build_html(modules: list[DocModule], doc_entries: dict[str, DocEntry]) -> None:
    """ Starting with the main page, builds the HTML files for the documentation.

    :param modules: The list of modules to build the HTML files from.
    :param doc_entries: The dictionary of DocEntry objects to build the HTML files from.
    """
    # Create source code mirror pages
    source_code_files: list[tuple[str, str, str]]
    source_code_files = folder_generate_highlighted_html(folder_path=conf.get_root_directory(),
                                                         destination_folder=os.path.join(conf.get_build_directory(),
                                                                                         'html'),
                                                         lua_version=conf.get_lua_version(),
                                                         encoding=conf.get_encoding())

    # Create the data objects used for tag_mapper() and set list for feeding to _generate_html()
    data_object: dict[str, any] = _create_data_object(modules, doc_entries)
    file_info: list[dict[str, any]] = _get_build_file_info(data_object, source_code_files, modules)

    # Set up ProgressBar
    # Always add 2, main page and search page
    # Add 1 if script set to document source code (SourceCodeFolderMap
    file_generation_count: int = len(file_info)
    conn_1, conn_2 = multiprocessing.Pipe()
    progress_bar: ProgressBar = ProgressBar(total=file_generation_count, description='Generating HTML files:',
                                            pipe_rec_connection=conn_1, pipe_send_connection=conn_2)
    progress_bar.start()

    # Generate HTML files
    html_files: list[tuple[str, str]] = []
    if conf.get_multicore() > 1:
        with ProcessPoolExecutor(max_workers=conf.get_multicore()) as executor:
            html_files = executor.map(
                _generate_html,
                [entry['start_tag'] for entry in file_info],
                [entry['tag_type'] for entry in file_info],
                [entry['data_object'] for entry in file_info],
                [entry['current_data'] for entry in file_info],
                [entry['destination_folder'] for entry in file_info],
                [entry['file_name'] for entry in file_info],
                [conn_2] * len(file_info)
            )
        html_files = list(html_files)
    else:
        progress_bar.close_listener()
        for file in file_info:
            html_files.append(
                _generate_html(
                    start_tag=file['start_tag'],
                    tag_type=file['tag_type'],
                    data_object=file['data_object'],
                    current_data=file['current_data'],
                    destination_folder=file['destination_folder'],
                    file_name=file['file_name']
                )
            )
            progress_bar.update(1)

    # Create DataStore.json file
    create_datastore(html_files)

    # Set up ProgressBar
    progress_bar = ProgressBar(total=len(html_files), description='Writing HTML files to system:')
    progress_bar.start()

    # Create html files
    for file_name, html in html_files:
        if not os.path.isfile(file_name):
            with open(file_name, 'w', encoding=conf.get_encoding()) as html_file:
                html_file.write(html)
            progress_bar.update(1)
        else:
            print(
                f'\n{g_error_colour}ERROR(DM-3): File {file_name} already exists in destination folder. This should not'
                f' happen and might suggest a file conflict. Exiting.{g_end_colour}')
            sys.exit(1)
# pylint: enable=unused-variable
