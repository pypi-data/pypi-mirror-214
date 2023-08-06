""" This module provides modules for fetching HTML fragments."""

import os
import re
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.misc import g_error_colour, g_end_colour


# Regex patterns
g_html_fragment_pattern: re.Pattern = re.compile(r'''^#LuaAutoDoc-(\w*)\n([\w\W]*?)\n*(?:(?=^#LuaAutoDoc-)|\Z)''', re.MULTILINE)
""" Captures HTML fragments, first group captures the tag, second group captures the associated HTML fragment."""
g_lua_auto_doc_tag_pattern: re.Pattern = re.compile(r'''#LuaAutoDoc-(\w*)''', re.MULTILINE)
""" Captures LuaAutoDoc tags, 1 capture group."""


# pylint: disable=unused-variable
g_tag_dict: dict[str, str] = {}
def _get_tag_dict() -> dict[str, str]:
    """ Returns a dictionary of HTML fragments from the HTMLFragments module.

    :return: A dictionary of HTML fragments.
    """
    if g_tag_dict:
        return g_tag_dict

    # Get default HTML fragments
    for root, _, files in os.walk(conf.get_default_html_fragment_directory()):
        for file in files:
            if file.lower().endswith('.html'):
                with open(os.path.join(root, file), 'r', encoding=conf.get_encoding()) as html_file:
                    contents: str = html_file.read()
                fragments: list[tuple[str, str]] = g_html_fragment_pattern.findall(contents)
                for fragment in fragments:
                    g_tag_dict[fragment[0]] = fragment[1]

    # Get custom HTML fragments and overwrite default fragments
    if os.path.isdir(conf.get_html_fragment_directory()):
        for root, _, files in os.walk(conf.get_html_fragment_directory()):
            for file in files:
                if file.lower().endswith('.html'):
                    with open(os.path.join(root, file), 'r', encoding=conf.get_encoding()) as html_file:
                        contents: str = html_file.read()
                    fragments: list[tuple[str, str]] = g_html_fragment_pattern.findall(contents)
                    for fragment in fragments:
                        g_tag_dict[fragment[0]] = fragment[1]

    return g_tag_dict


def get_html_fragment_path(filename: str) -> str:
    """ Returns the path to the HTML fragment with the given filename.

    :param filename: The unique filename of the HTML fragment.e

    :return: The path to the HTML fragment with the given filename.
    """
    for root, _, files in os.walk(conf.get_html_fragment_directory()):
        for file in files:
            if file.lower() == filename.lower():
                return os.path.normpath(os.path.join(root, file))

    for root, _, files in os.walk(conf.get_default_html_fragment_directory()):
        for file in files:
            if file.lower() == filename.lower():
                return os.path.normpath(os.path.join(root, file))

    raise FileNotFoundError(f'\n{g_error_colour}ERROR(FR-1): HTML root file "{filename}" not found.{g_end_colour}')


def get_fragment_from_tag(tag: str) -> str:
    """ Returns the HTML fragment for the given tag.

    :param tag: The tag to get the HTML fragment for.

    :return: The HTML fragment for the given tag.
    """
    tag_dict: dict[str, str] = _get_tag_dict()
    try:
        return tag_dict[tag]
    except KeyError as e:
        print(f'\n{g_error_colour}ERROR(FR-0): Tag "{tag}" not found in HTML fragments.\n Please ensure your HTML '
              f'fragments follows all guidelines, and your call is written correctly. Tags are case-sensitive.'
              f'{g_end_colour}')
        raise KeyError(e) from e


def get_tags_from_fragment(fragment: str) -> list[str]:
    """ Returns a list of tags found in the given HTML fragment.

    :param fragment: The HTML fragment to get tags from.

    :return: A list of tags found in the given HTML fragment.
    """
    return g_lua_auto_doc_tag_pattern.findall(fragment)
# pylint: enable=unused-variable
