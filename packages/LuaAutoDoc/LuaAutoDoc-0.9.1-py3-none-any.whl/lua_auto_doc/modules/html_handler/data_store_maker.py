""" This module is used to crate the DataStore.json file that is used when searching the documentation."""

import os
import re
from json import dump
import multiprocessing
# pylint: disable=unused-import, unused-variable
from multiprocessing.connection import Connection
# pylint: enable=unused-import, unused-variable
from concurrent.futures import ProcessPoolExecutor
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.progress_bar import ProgressBar

# Regex patterns
g_code_object_pattern: re.Pattern = re.compile(r'''(<div class="code-object"[\s\S]*?(?=<div class="code-object"|<div id="footer">))''')
""" The pattern used to find the code objects in the html file. Group 0 is the entire code object."""
g_code_object_id_pattern: re.Pattern = re.compile(r'''<div class="code-object" id="(.*)"''')
""" The pattern used to find the id of the code object. Group 1 is the id."""
g_code_object_title_pattern: re.Pattern = re.compile(r'''<div\s+class="code-object-title"[\s\S]*?>\s*([\s\S]*?)\s*?<\/div>''',)
""" The pattern used to find the title of the code object. Group 1 is the title."""
g_tag_content_pattern: re.Pattern = re.compile(r'''(?<=>)[^<]+''')
""" The pattern used to extract all the visible text in tags. Group 0 is the text."""
g_extra_whitespace_pattern: re.Pattern = re.compile(r'''\s+''')
""" The pattern used to remove extra whitespace. Group 0 is the whitespace."""
g_module_description_pattern: re.Pattern = re.compile(r'''<div id="module-body-description">([\s\S]*?)<\/div>''')
""" The pattern used to find the description of the module. Group 1 is the description."""
g_generic_title_pattern: re.Pattern = re.compile(r'''<h(?P<num>\d).*?class="page-title".*?>([\s\S]*?)<\/h(?P=num)>|<title>([\s\S]*)<\/title>''')
r""" The pattern used to find the title of the page. Group 1 is the html header title and group 3 is the <h\d> title.
If using findall, group 1 wil be index 1 and group 3 will be index 2., group 2 (named group) will have index 0."""
g_sourcecode_body_pattern: re.Pattern = re.compile(r'''<pre[\s\S]*?>([\s\S]*)</pre>''')
""" The pattern used to find the source code in the sourcecode html files. Group 1 is the source code."""


def _scan_generated_html(filepath: str, file_content: str) -> dict[str, [dict[str, str]]]:
    """ Scans generated code object pages and returns a dict with a href key to the contents of the various parts of the
    html file

    :param filepath: The path to the file
    :param file_content: The content of the file

    :return: A dict with a href key to the contents of the various parts of the html file
    """
    html_content: dict[str, [dict[str, str]]] = {}

    # Get the module title and description
    title: str = filepath
    title_match: list[tuple[str, str, str]] = g_generic_title_pattern.findall(file_content)
    for _, _, page_title in title_match:
        if page_title:
            title: str = ''.join(g_tag_content_pattern.findall(page_title))
            if not title:
                title = page_title
            break
    html_content[filepath] = {
        'title': title,
        'content': g_module_description_pattern.search(file_content).group(1).strip()
    }

    # Get content in each code-object
    code_object_list: list[str] = g_code_object_pattern.findall(file_content)
    for code_object in code_object_list:
        href: str = f'{filepath}#{g_code_object_id_pattern.search(code_object).group(1)}'
        title: str = g_code_object_title_pattern.search(code_object).group(1)
        content: str = ''
        for tag_content in g_tag_content_pattern.findall(code_object):
            content += g_extra_whitespace_pattern.sub(' ', tag_content)

        html_content[href] = {'title': title, 'content': content}

    return html_content


def _scan_generated_sourcecode_html(filepath: str, file_content: str) -> dict[str, [dict[str, str]]]:
    # Get the title
    title: str = filepath
    title_match: list[tuple[str, str, str]] = g_generic_title_pattern.findall(file_content)
    for _, _, page_title in title_match:
        if page_title:
            title = ''.join(g_tag_content_pattern.findall(page_title))
            if not title:
                title = page_title
            break

    # Get the source code
    source_code: str = g_sourcecode_body_pattern.search(file_content).group(1)
    source_code = ''.join(g_tag_content_pattern.findall(source_code)).strip()
    return {filepath: {'title': title, 'content': source_code}}


def _scan_user_html(filepath: str, file_content: str) -> dict[str, [dict[str, str]]]:
    """ Scans a user html file and returns a dict with a href key to the contents of the various parts of the html file

    :param filepath: The path to the file
    :param file_content: The content of the file

    :return: A dict with a href key to the contents of the various parts of the html file
    """
    # Get the title
    title: str = filepath
    title_match: list[tuple[str, str, str]] = g_generic_title_pattern.findall(file_content)
    for _, header_title, page_title in title_match:
        if header_title:
            title = header_title
        elif page_title:
            title = ''.join(g_tag_content_pattern.findall(page_title))
            if not title:
                title = page_title
            break  # First header title got priority

    # Get all visible content
    content: str = ''
    for tag_content in g_tag_content_pattern.findall(file_content):
        content += g_extra_whitespace_pattern.sub(' ', tag_content)

    return {filepath: {'title': title, 'content': content}}


def _scan_html(html_file: tuple[str, str], pipe=None) -> dict[str, [dict[str, str]]]:
    """ Scans an HTML file for content and returns a dict with a href key to the contents of the various parts of the
    html file.

    :param html_file: A tuple containing the path to the html file and the content of the html file.
    :param pipe: A multiprocessing pipe used to send progress updates to the main process.
    :type pipe: Connection

    """
    file_content: str = html_file[1]
    filepath: str = os.path.relpath(html_file[0], conf.get_build_directory())
    html_content: str = ''

    # Skip the search page
    if filepath == os.path.join('html', 'search_page.html'):
        if pipe:
            pipe.send(1)
        return {}

    # Filter the type of html file
    if filepath.startswith(os.path.join('html', 'module-')) \
            or filepath == os.path.join('html', 'Classes.html') or filepath == os.path.join('html', 'Functions.html'):
        html_content = _scan_generated_html(filepath, file_content)

    elif filepath.startswith(os.path.join('html', 'sourcecode-')):
        html_content = _scan_generated_sourcecode_html(filepath, file_content)

    else:
        html_content = _scan_user_html(filepath, file_content)

    if html_content[filepath]['content'] == '':
        pass

    # Send progress update
    if pipe:
        pipe.send(1)
    return html_content


# pylint: disable=pointless-string-statement, unused-variable
def create_datastore(html_files: list[tuple[str, str]]) -> None:
    """ Takes in a list of html files, scans their contents and creates a DataStore.json file that is used when
    searching the documentation.

    :param html_files: A list of tuples containing the name of the html file and its contents.
    """
    # Set up the progress bar
    conn_1, conn_2 = multiprocessing.Pipe()
    progress_bar: ProgressBar = ProgressBar(total=len(html_files), description='Creating DataStore:',
                                            pipe_rec_connection=conn_1, pipe_send_connection=conn_2)
    progress_bar.start()

    # Create a list of scan results
    results: list[dict[str, dict[str, str]]] = []
    """ Format: list[{<html_ref>: {'title': <ref title>, 'content': <ref content>}}] """
    if threads := conf.get_multicore() > 1:
        with ProcessPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(_scan_html, html_files, [conn_2] * len(html_files)))

    else:
        progress_bar.close_listener()
        for html_file in html_files:
            results.append(_scan_html(html_file))
            progress_bar.update(1)

    # Convert to a simple dict
    datastore: dict[str, dict[str, str]] = {}
    for result in results:
        datastore.update(result)

    # Save the datastore
    with open(os.path.join(conf.get_build_directory(), 'data', 'DataStore.json'), 'w', encoding=conf.get_encoding()) \
            as file:
        dump(datastore, file, indent=None, ensure_ascii=False)
# pylint: enable=pointless-string-statement, unused-variable
