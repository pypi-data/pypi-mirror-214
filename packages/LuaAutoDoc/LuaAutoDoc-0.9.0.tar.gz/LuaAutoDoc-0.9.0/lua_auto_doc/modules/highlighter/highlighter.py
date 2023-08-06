""" This module provides support for analysing lua code and formatting it into a highlighted html fragment. """

import os
import sys
import multiprocessing
from hashlib import sha1
from tkinter import filedialog
from concurrent.futures import ProcessPoolExecutor
# pylint: disable=unused-import, unused-variable
from multiprocessing.connection import Connection
# pylint: enable=unused-import, unused-variable
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.progress_bar import ProgressBar
from lua_auto_doc.modules.lua_parser.lua_documentation_parser import g_ignore_file_pattern
from lua_auto_doc.modules.tools.misc import g_warning_colour, g_error_colour, g_end_colour
from lua_auto_doc.modules.html_handler.fragment_reader import get_fragment_from_tag, get_html_fragment_path
from lua_auto_doc.modules.highlighter.indexer_support_functions import get_code
from lua_auto_doc.modules.highlighter.indexer import index_code, indexed_code_to_html, index_fallback


def highlight(filename: str, source_code: str, html_template: str, lua_version: float) -> tuple[str, str]:
    """ Parses a lua file and creates a html string of the code highlighted with css classes.

    :param filename: The name of the file to highlight.
    :param source_code: The source code to highlight.
    :param html_template: The html file to use as a template.
    :param lua_version: The version of Lua code.

    :return: The formatted code and the html template with its LuaAutoDoc tags resolved.
    """
    if conf.get_native_highlighter():
        indexed_code: dict[int, set[str]] = index_code(source_code, lua_version)
        html_code: str = indexed_code_to_html(source_code, indexed_code)
        # Remove the fallback fragment if the code was indexed successfully
        html_template = html_template.replace('#LuaAutoDoc-HighlightFallback', '')
    else:
        html_code, html_template = index_fallback(source_code, html_template)
        highlight_fallback_fragment: str = get_fragment_from_tag('HighlightFallback')
        html_template = html_template.replace('#LuaAutoDoc-HighlightFallback', highlight_fallback_fragment)
        print(f'{g_warning_colour}Created highlighted html code with fallback mode for {filename}{g_end_colour}')

    return html_code, html_template


def create_highlighted_code(filename: str, destination_folder: str, lua_version=5.1, encoding='utf-8',
                            pipe=None) -> tuple[str, str, str]:
    """ Creates a highlighted html strings and return a tuple with the filename and file content.

    :param filename: The name of the file to create the highlighted html code fragment from.
    :param destination_folder: The path of the destination folder.
    :param lua_version: The version of Lua code.
    :param encoding: The encoding of the file, the html will be written in the same encoding.
    :param pipe: The pipe to send a ProgressBar update to
    :type pipe: Connection

    :return: A tuple with the hashed filename, the file content and relative file path.
    """
    # Read the html template
    try:
        html_fragment_path: str = get_html_fragment_path('SourceCodeMirror.html')
        with open(html_fragment_path, 'r', encoding='utf-8') as file:
            html_template: str = file.read()
    except FileNotFoundError as e:
        print(f'\n{g_error_colour}ERROR(SCH-0): While trying to read html template for source code, exiting:\n'
              f'{e}{g_end_colour}')
        raise FileNotFoundError(e) from e

    # Get the source code and index it
    source_code: str = get_code(filename, encoding)

    # Return if the @ignoreFile tag is present
    if g_ignore_file_pattern.search(source_code):
        if pipe:
            pipe.send(1)
        return None, None, None

    try:
        html_code, html_template = highlight(filename, source_code, html_template, lua_version)

    # pylint: disable=broad-except
    except Exception as e:
        print(f'\n{g_error_colour}ERROR(SCH-1): While indexing code: {e}\nMoving to fallback indexing.{g_end_colour}')
        html_code, html_template = index_fallback(source_code, html_template)
        highlight_fallback_fragment: str = get_fragment_from_tag('HighlightFallback')
        html_template = html_template.replace('#LuaAutoDoc-HighlightFallback', highlight_fallback_fragment)
        print(f'{g_warning_colour}Created highlighted html code with fallback mode for {filename}{g_end_colour}')
    # pylint: enable=broad-except

    html_text = html_template.replace('#LuaAutoDoc-SourceCode', html_code)

    # Create a hash of the filename to prevent collisions
    filename = os.path.normpath(filename)
    # noinspection InsecureHash
    hash_code: str = sha1(os.path.relpath(filename, conf.get_root_directory()).encode('utf-8')).hexdigest()[:10]
    new_file = os.path.join(conf.get_build_directory(),
                            'html',
                            f'sourcecode-{os.path.split(filename)[-1]}_{hash_code}.html')
    # Write the html code to a file
    if os.path.isfile(os.path.join(destination_folder, new_file)):
        print(f'\n{g_error_colour}ERROR(SCH-2): trying to write to file, but file already exists in destination '
              f'folder. This should not happen and might suggest a file conflict. Exiting.{g_end_colour}')
        sys.exit(1)

    if pipe:
        pipe.send(1)

    return new_file, html_text, os.path.relpath(filename, conf.get_root_directory())

# pylint: disable=unused-variable
def file_generate_highlighted_html(file_path='', destination_folder='', lua_version=5.1, encoding='utf-8') \
        -> tuple[str, str, str]:
    """ Takes in a file path and destination path and generates highlighted html code for it.

    :param file_path: The path of the file to generate highlighted html code for, should be the absolute path.
    :param destination_folder: The path of the destination folder.
    :param lua_version: The version of Lua to use.
    :param encoding: The encoding of the file.

    :return: A tuple with the hashed filename, the file content and relative file path.
    """
    if file_path == '':
        file_path = filedialog.askopenfilename(filetypes=[['Lua', '*.lua'], ['Any', '*']],
                                               title='Select file to highlight')
        if file_path == '':
            return None
    if destination_folder == '':
        destination_folder = filedialog.askdirectory(mustexist=True, title='Select destination folder')
        if destination_folder == '':
            return None

    return create_highlighted_code(file_path, destination_folder, lua_version, encoding)
# pylint: enable=unused-variable


# pylint: disable=unused-variable
def folder_generate_highlighted_html(folder_path='', destination_folder='', lua_version=5.1, encoding='utf-8') \
        -> list[tuple[str, str, str]]:
    """ Multiprocessing function that takes in a folder path and generates highlighted html code for every file in the
    folder and all subfolders.

    :param folder_path: The path of the folder to generate highlighted html code for.
    :param destination_folder: The path of the destination folder.
    :param lua_version: The version of Lua to use.
    :param encoding: The encoding of the files.

    :return: A list of tuples with the hashed filename, the file content and relative file path.
    """
    # Convert lua version to float
    lua_version = float(lua_version)

    # Get the folder path and destination folder
    if folder_path == '':
        folder_path = filedialog.askdirectory(mustexist=True, title='Select folder to generate HTML code for')
        if folder_path == '':
            return None
    if destination_folder == '':
        destination_folder = filedialog.askdirectory(mustexist=True, title='Select destination folder')
        if destination_folder == '':
            return None

    # Get all files in the folder
    files: list[str] = []
    for root, _, file_names in os.walk(folder_path):
        for file_name in file_names:
            if file_name.endswith('.lua'):
                files.append(os.path.join(root, file_name))

    # Set up ProgressBar
    conn_1, conn_2 = multiprocessing.Pipe()
    progress_bar = ProgressBar(total=len(files), description='Parsing Lua code:', pipe_rec_connection=conn_1,
                               pipe_send_connection=conn_2)
    progress_bar.start()
    # Generate the highlighted html code
    html_files: list[tuple[str, str, str]] = []

    if conf.get_multicore() > 1:
        files_len: int = len(files)
        with ProcessPoolExecutor(max_workers=conf.get_multicore()) as executor:
            html_files = executor.map(create_highlighted_code,
                                      files,
                                      [destination_folder] * files_len,
                                      [lua_version] * files_len,
                                      [encoding] * files_len,
                                      [conn_2] * files_len)
        html_files = list(html_files)
    else:
        progress_bar.close_listener()
        for file in files:
            html_files.append(create_highlighted_code(file, destination_folder, lua_version, encoding))
            progress_bar.update(1)

    # Remove any empty entries
    html_files = [entry for entry in html_files if entry[0] is not None]

    return html_files
# pylint: enable=unused-variable
