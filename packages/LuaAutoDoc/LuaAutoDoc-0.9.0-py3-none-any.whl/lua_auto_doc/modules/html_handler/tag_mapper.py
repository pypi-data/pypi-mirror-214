""" This module implements the tag mapper for use on doc_maker"""

import re
import os
import time
from typing import Union
from hashlib import sha1
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.lua_parser.doc_classes import DocLine
from lua_auto_doc.modules.tools.misc import g_error_colour, g_end_colour
from lua_auto_doc.modules.lua_parser.lua_documentation_parser import g_ignore_file_pattern
from lua_auto_doc.modules.html_handler.fragment_reader import get_fragment_from_tag, get_tags_from_fragment
from lua_auto_doc.modules.html_handler.tag_mapper_support_functions import main_page_navbar_href_processor, colour_type


# Regex patterns
# tag_mapper specific patterns
g_href_hash_code_id_pattern: re.Pattern = re.compile(r'''_[\da-z]*\.html$''', re.MULTILINE)
""" A pattern that matches the hash code appended to all project files."""
g_href_link_pattern: re.Pattern = re.compile(r'''<a\s.*href=(?P<quote>["'])(.*?)(?P=quote)''', re.MULTILINE)
""" A pattern that captures the link inside a href tag. Group 2 captures the link."""


def _generate_source_code_map(current_data: dict[str, any]) -> str:
    """ Generates the html for the source code map.

    :param current_data: Data regarding the current file being built.

    :return: The html page as a string.
    """

    def _add_path_to_dict(folder_map: list[Union[str, dict]], path: str) -> None:
        """ Adds a file path to a nested list of dictionaries representing folders and files.

        The format of the folder map created:
        [
        file0.lua,
            {
                'folders': [
                    {
                        'folders': [
                            {'folders': [],
                             'files': ['file1.lua', 'file2.lua']
                             }
                        ],
                        'files': ['file3.lua']
                    },
                    {
                        'folders': [],
                        'files': ['file4.lua']
                    }
                ]
            },
            {
                'folders': [],
                'files': ['file5.lua']
            }
        ]

        :param folder_map: The list to add the path to.
        :param path: The file path to add.
        """
        # Split the path into its individual parts
        path_parts: list[str] = []
        path_copy: str = path
        while path_copy:
            path_copy, tail = os.path.split(path_copy)
            path_parts.append(tail)
        path_parts = path_parts[::-1]

        # Create the href for the file
        # noinspection InsecureHash
        hash_code: str = sha1(path.encode('utf-8')).hexdigest()[:10]
        href = f'sourcecode-{os.path.split(path_parts[-1])[-1]}_{hash_code}.html'

        # If the path is just a file, add it to the root of the folder_map
        if len(path_parts) == 1:
            folder_map.append(href)
            return

        # Traverse the folder_map and add missing parts of the path
        current_list: list[Union[str, dict]] = folder_map
        current_dict: dict[str, Union[str, list]] = None
        for part in path_parts[:-1]:
            # Find the folder part for the current part of the path
            current_dict = None
            for list_entry in current_list:
                if isinstance(list_entry, dict) and list_entry['name'] == part:
                    current_dict = list_entry
                    break
            # If the folder doesn't exist, create it
            if not current_dict:
                current_dict = {'name': part, 'folders': [], 'files': []}
                current_list.append(current_dict)
            # Move to the next level of the folder_map
            current_list = current_dict['folders']

        # Add the file to the current folder_map
        current_dict['files'].append(href)

    def _recursive_add_to_content(folder_node: dict[str, Union[dict, list[str]]], content_string='') -> str:
        """ Recursively adds the contents of a folder to the HTML string.

        :param folder_node: The folder to add.
        :param content_string: The HTML string to add the folder to.
        :type content_string: str

        :return: The HTML string.
        """
        # Add every lua file to the current list of files
        for file_entry in folder_node['files']:
            content_string += '\n' + tag_mapper('SourceCodeFileEntry',
                                                None,
                                                current_data={'entry': file_entry,
                                                               'context': current_data['context'],
                                                               'folder_depth': current_data['folder_depth']})

        # recursively resolve folders
        for folder in folder_node['folders']:
            content_string += _recursive_add_to_content(folder)

        # Get html fragment
        fragment: str = get_fragment_from_tag('SourceCodeFolderList')

        # Replace the tags in the fragment
        fragment = fragment.replace('#LuaAutoDoc-SourceCodeLuaFolderIcon',
                                    f'{"../" * current_data["folder_depth"]}assets/FolderClosed.svg')
        fragment = fragment.replace('#LuaAutoDoc-SourceCodeFolderName', folder_node['name'])
        fragment = fragment.replace('#LuaAutoDoc-SourceCodeFolderContent', content_string)

        return fragment

    # Get all lue file paths that do not contain the @ignoreFile tag
    file_list: list[str] = []
    for root, _, files in os.walk(conf.get_root_directory()):
        for file in files:
            if file.endswith('.lua'):
                with open(os.path.join(root, file), 'r', encoding=conf.get_encoding()) as f:
                    if not g_ignore_file_pattern.search(f.read()):
                        file_path: str = os.path.normpath(os.path.join(os.path.relpath(root, conf.get_root_directory()),
                                                                       file))
                        file_list.append(file_path)

    # Set up data object to loop over
    folder_tree: list[Union[str, dict]] = []
    for file_path in file_list:
        _add_path_to_dict(folder_tree, file_path)

    # Create the HTML string
    html_string: str = ''
    for entry in folder_tree:
        if isinstance(entry, str):
            html_string += tag_mapper('SourceCodeFileEntry', None, current_data={'entry': entry,
                                                                                  'context': 'folder_map',
                                                                                  'folder_depth': 1})
        else:
            html_string += _recursive_add_to_content(entry)

    return html_string


def _populate_list(tag: str, list_entries: list[str], data_object: dict[str, any], current_data: dict[str, any]) -> str:
    """ Returns the HTML fragment for the given list tag.

    :param tag: The tag to get the HTML fragment for.
    :param list_entries: The list of entries to use for the search.
    :param data_object: The code data to use for the search.
    :param current_data: The current data to use for the search.

    :return: The HTML fragment for the given tag.
    """
    # Create the list entry
    entry_list: list[str] = []
    for entry in list_entries:
        current_data_copy = current_data.copy()
        current_data_copy['entry'] = entry
        entry_list.append(resolve_fragment(_resolve_tag(tag, data_object, current_data_copy)))

    return '\n'.join(entry_list)


def resolve_fragment(fragment: str, data_object=None, current_data=None) -> str:
    """ Recursively depth first resolves LuaAutoTags in the given fragment.

    :param fragment: The fragment to resolve LuaAutoTags in.
    :param data_object: The data object to use for certain tags.
    :type data_object: dict[str, any]
    :param current_data: Data regarding the current file being built.
    :type current_data: dict[str, any]

    :return: The resolved fragment.
    """
    # Get all LuaAutoTags in the fragment
    tags: list[str] = get_tags_from_fragment(fragment)
    # Resolve each LuaAutoTag
    for tag in tags:
        fragment = fragment.replace(f'#LuaAutoDoc-{tag}', tag_mapper(tag, data_object, current_data), 1)

    return fragment


def _resolve_tag(tag: str, data_object=None, current_data=None) -> str:
    """ Wrapper that calls resolve_fragment() with the HTML fragment for the given tag.

    :param tag: The tag to resolve.
    :param data_object: The data object to use for certain tags.
    :type data_object: dict[str, any]
    :param current_data: Data regarding the current file being built.
    :type current_data: dict[str, any]

    :return: The resolved tag.
    """
    html_fragment: str = get_fragment_from_tag(tag)
    return resolve_fragment(html_fragment, data_object, current_data)


# pylint: disable=too-many-locals, too-many-return-statements, too-many-branches, too-many-statements
def tag_mapper(tag: str, data_object: dict[str, any], current_data: dict[str, any]) -> str:
    """ Returns the HTML fragment for the given tag.

    :param tag: The tag to get the HTML fragment for.
    :param data_object: The data object to use for certain tags.
    :param current_data: Data regarding the current file being built.

    :return: The HTML fragment for the given tag.
    """
    match tag:
        case 'ModulePage':
            # Retrieves the CodeObject HTML fragment
            return _resolve_tag('HTMLCodeObjectPage', data_object, current_data)

        case 'ClassPage':
            # Retrieves the CodeObject HTML fragment
            return _resolve_tag('HTMLCodeObjectPage', data_object, current_data)

        case 'FunctionPage':
            # Retrieves the CodeObject HTML fragment
            return _resolve_tag('HTMLCodeObjectPage', data_object, current_data)

        case 'ModuleTitle':
            # Retrieves the title of the module
            if current_data['context'] == 'module':
                return f'Module: {current_data["entry"].get_name()}'
            if current_data['context'] == 'class':
                return 'Classes'
            if current_data['context'] == 'function':
                return 'Functions'
            if current_data['context'] == 'custom':
                return current_data['page_name'][:-4]

        case 'FileName':
            # Returns the relative path of a file
            return f'<span class="source-code-title">Code path: </span>{current_data["filepath"]}'

        case 'ModuleDescription':
            # Retrieves the docstring description of the module, or a default description
            if current_data['context'] == 'module':
                return current_data['entry'].get_description()
            if current_data['context'] == 'class':
                return 'All classes not belonging to a module.'
            if current_data['context'] == 'function':
                return 'All functions not belonging to a module.'

        case 'ProjectName':
            # Retrieves the configured project name
            return conf.get_project_name()

        case 'ProjectVersion':
            # Retrieves the configured project version
            return conf.get_version()

        case 'Favicon':
            # Returns the html favicon list for the html header
            favicon_text: str = _resolve_tag('Favicon', data_object, current_data)
            favicon_path: str = f'{"../" * current_data["folder_depth"]}favicon/'
            favicon_text = favicon_text.replace('href="favicon/', f'href="{favicon_path}')
            return favicon_text

        case 'StylesheetEntry':
            # Retrieves the html list of all stylesheets for the html header
            html_stylesheet_list: list[str] = []
            folder_path: str = f'{"../" * current_data["folder_depth"]}stylesheets/'
            for stylesheet in data_object['stylesheets']:
                html_stylesheet_list.append(_resolve_tag('StylesheetEntry',
                                                         current_data,
                                                         current_data={'entry': f'{folder_path}{stylesheet}',
                                                                       'folder_depth': current_data['folder_depth'],
                                                                       }))
            return '\n'.join(html_stylesheet_list)

        case 'ScriptEntry':
            # Retrieves the html list of all scripts for the html header
            html_script_list: list[str] = []
            folder_path: str = f'{"../" * current_data["folder_depth"]}scripts/'
            for script in data_object['scripts']:
                html_script_list.append(_resolve_tag('ScriptEntry',
                                                     current_data,
                                                     current_data={'entry': f'{folder_path}{script}',
                                                                   'folder_depth': current_data['folder_depth'],
                                                                   }))
            return '\n'.join(html_script_list)

        case 'MainPageLink':
            # Retrieves the html link to the main page
            folder_depth: str = '../' * current_data['folder_depth']
            return f'{folder_depth}{conf.get_main_page()}'

        case 'NavBarCurrentPageEntries':
            # Generates the list of all sections of the current page for the navbar
            if current_data['context'] == 'module':
                # Set up a structure similar to case: NavBarClassPageContent and case: NavBarFunctionPageContent
                current_data_copy: dict[str, any] = current_data.copy()
                current_data_copy['navbar_classes'] = current_data['entry'].get_classes()
                current_data_copy['navbar_functions'] = current_data['entry'].get_functions()

                # Get the results from case: NavBarClassPageContent and case: NavBarFunctionPageContent
                current_page_list: list[str] = []
                current_page_list.append(tag_mapper('NavBarClassPageEntries', data_object, current_data_copy))
                current_page_list.append(tag_mapper('NavBarFunctionPageEntries', data_object, current_data_copy))
                return '\n'.join(current_page_list)

            if current_data['context'] == 'class':
                # Set up a structure similar to case: NavBarClassPageContent
                current_data_copy: dict[str, any] = current_data.copy()
                current_data_copy['navbar_classes'] = data_object['classes']

                return tag_mapper('NavBarClassPageEntries', data_object, current_data_copy)

            if current_data['context'] == 'functions':
                # Set up a structure similar to case: NavBarFunctionPageContent
                current_data_copy: dict[str, any] = current_data.copy()
                current_data_copy['navbar_functions'] = data_object['functions']

                return tag_mapper('NavBarFunctionPageEntries', data_object, current_data_copy)

            return ''

        case 'NavBarModulePageContent':
            # Generates the list of all modules for the navbar
            if len(data_object['doc_modules']):
                return _resolve_tag('NavBarModulePageContent', data_object, current_data)
            return ''

        case 'NavBarModulePageEntries':
            # Loops through the list of all modules and returns the html list of all modules for the navbar
            return _populate_list('NavBarModulePageEntries', data_object['doc_modules'], data_object, current_data)

        case 'NavBarClassPageContent':
            # Generates the list of all classes for the navbar
            if len(data_object['classes']):
                current_data_copy: dict[str, any] = current_data.copy()
                current_data_copy['navbar_classes'] = data_object['classes']
                return _resolve_tag('NavBarClassPageContent', data_object, current_data_copy)
            return ''

        case 'NavBarClassPageEntries':
            # Loops through the list of all classes and returns the html list of all classes for the navbar
            entry_list: list[str] = []
            for class_entry in current_data['navbar_classes']:
                # Gather all methods for the class
                temp_list: list[str] = []
                temp_list.append(_resolve_tag('NavBarClassPageEntries',
                                              data_object,
                                              current_data={'entry': class_entry,
                                                            'folder_depth': current_data['folder_depth'],
                                                            'context': 'class',
                                                            }))
                for method in class_entry.get_grouped_methods():
                    temp_list.append(_resolve_tag('NavBarClassPageEntries',
                                                  data_object,
                                                  current_data={'entry': method,
                                                                'folder_depth': current_data['folder_depth'],
                                                                'context': 'function',
                                                                }))
                # If we got methods, add another level lists
                if len(temp_list) > 1:
                    # Get the default NavBarSection fragment and replace the value DocTag with the gathered data
                    fragment: str = get_fragment_from_tag('NavBarSection')
                    fragment = fragment.replace('#LuaAutoDoc-GetHTMLName', class_entry.get_html_name())
                    fragment = fragment.replace('#LuaAutoDoc-NavBarSectionEntry', '\n'.join(temp_list))
                    entry_list.append(fragment)
                else:
                    entry_list.extend(temp_list)
            return '\n'.join(entry_list)

        case 'NavBarFunctionPageContent':
            # Generates the list of all functions for the navbar
            if len(data_object['functions']):
                current_data_copy: dict[str, any] = current_data.copy()
                current_data_copy['navbar_functions'] = data_object['functions']
                return _resolve_tag('NavBarFunctionPageContent', data_object, current_data_copy)
            return ''

        case 'NavBarFunctionPageEntries':
            # Loops through the list of all functions and returns the html list of all functions for the navbar
            return _populate_list('NavBarFunctionPageEntries', current_data['navbar_functions'], data_object,
                                  current_data)

        case 'NavBarSourceCodeMap':
            # If the source code is set to visible, return the link to the source code map
            if not conf.get_hide_source_code():
                return _resolve_tag('NavBarSourceCodeMap', data_object, current_data)
            return ''

        case 'SourceCodeFolderMapHref':
            # Returns the link to the source code map
            return f'{"../" * current_data["folder_depth"]}html/sourcecodefoldermap.html'

        case 'SourceCodeFolderMapName':
            # Returns the title of the source code map
            return 'Source Code View'

        case 'NavBarCustomContent':
            # Processes the custom content for the navbar
            # Special case for the main page (top level directory)
            if current_data['page_name'] == 'Main Page':
                fragment: str = get_fragment_from_tag('NavBarCustomContent')
                match_list: list[re.Match] = list(g_href_link_pattern.finditer(fragment))
                # If the fragment is empty, return empty string
                if not match_list:
                    return ''
                # Process the first link to take care of the special case of end=0
                new_fragment, end = main_page_navbar_href_processor(fragment, match_list[0], start=0)
                # Loop through the remaining links
                for link_match in match_list[1:]:
                    temp_str, end = main_page_navbar_href_processor(fragment, link_match, start=end)
                    new_fragment += temp_str
                new_fragment += fragment[end:]
                return new_fragment
            return _resolve_tag('NavBarCustomContent', data_object, current_data)

        case 'HTMLSelf':
            # Returns the link to the current page
            return '#'

        case 'CurrentPageName':
            # Returns the name of the current page
            return current_data['page_name']

        case 'CurrentYear':
            # Returns the current year
            return time.strftime('%Y')

        case 'Author':
            # Returns the configured author
            return conf.get_author()

        case 'FooterLinks':
            # Generates the list of all footer links
            link_list: list[str] = []
            for link in conf.get_footer_links():
                link_list.append(_resolve_tag('FooterLinks',
                                              data_object,
                                              current_data={'entry': link,
                                                            'folder_depth': current_data['folder_depth'],
                                                            'context': current_data['context']}))
            return '\n'.join(link_list)

        case 'FooterLinkHref':
            # Returns the link to the footer link
            return current_data['entry']['url']

        case 'FooterAssetSource':
            # Returns the image link to the footer link
            return f'{"../" * current_data["folder_depth"]}assets/{current_data["entry"]["image_link"]}'

        case 'GetValueHref':
            # Returns the href of the current entry
            return current_data['entry'].get_href(current_data['folder_depth'])

        case 'GetValueId':
            # Returns the id of the current entry
            return current_data['entry'].get_id()

        case 'GetName':
            # Returns the name of the current entry
            return current_data['entry'].get_name()

        case 'GetHTMLName':
            # Returns the html name of the current entry
            return current_data['entry'].get_html_name()

        case 'GetDescription':
            # Returns the description of the current entry
            return current_data['entry'].get_description()

        case 'GetEntry':
            # Returns the current entry
            return current_data['entry']

        case 'GetKeywords':
            # Returns the keywords of the current code object
            return current_data['entry'].get_keywords()

        case 'HighlightFallback':
            # Fallback method in case the SourceCodeHighlighter fails
            return '#LuaAutoDoc-HighlightFallback'

        ### Code Object specific tags###
        case 'CodeObjectList':
            # Generates the list which contains a code object and any methods it may have
            if len(current_data['entries']):
                html_code_object_list: list[str] = []
                for entry in current_data['entries']:
                    html_code_object_list.append(
                        _resolve_tag('CodeObjectList',
                                     data_object,
                                     current_data={'entry': entry,
                                                   'folder_depth': current_data['folder_depth'],
                                                   'context': current_data['context']}))
                return '\n<br>'.join(html_code_object_list)
            return ''

        case 'DeprecatedEntryClass':
            # Returns a css class which changes the background colour to warn user that the entry is deprecated
            if current_data['entry'].get_deprecated():
                return ' code-object-deprecated-bg'
            if current_data['entry'].get_module() in data_object['module_dict'] \
                    and data_object['module_dict'][current_data['entry'].get_module()].get_deprecated():
                return ' code-object-deprecated-bg'
            return ''

        case 'InternalEntryClass':
            # Returns a css class which changes the background colour to warn user that the entry is internal
            if current_data['entry'].get_internal():
                return ' code-object-internal-bg'
            if current_data['entry'].get_module() in data_object['module_dict'] \
                    and data_object['module_dict'][current_data['entry'].get_module()].get_internal():
                return ' code-object-internal-bg'
            return ''

        case 'CodeObjectEntry':
            # Generates the html for a code object entry
            if current_data['entry'].get_type() == 'class':
                return _resolve_tag('CodeObjectClass', data_object, current_data)
            if current_data['entry'].get_type() == 'function':
                return _resolve_tag('CodeObjectFunction', data_object, current_data)

        case 'ObjectAuthor':
            # Returns the author of the current code object if it has one
            if current_data['entry'].get_author():
                return _resolve_tag('ObjectAuthor', data_object, current_data)
            return ''

        case 'EntryAuthor':
            # Returns the author of the current entry
            return current_data['entry'].get_author()

        case 'CodeObjectDeprecated':
            # Return the html marking a code object as deprecated if it is
            if current_data['context'] != 'module':
                return ''
            deprecated: Union[bool, DocLine] = current_data['entry'].get_deprecated()
            if deprecated:
                return _resolve_tag('CodeObjectDeprecated',
                                    data_object,
                                    current_data={'entry': deprecated,
                                                  'folder_depth': current_data['folder_depth'],
                                                  'context': current_data['context']})
            return ''

        case 'DeprecatedImage':
            # Returns the image link to the deprecated image
            return '../' * current_data['folder_depth'] + 'assets/Deprecated.svg'

        case 'CodeObjectInternal':
            # Return the html marking a code object as internal if it is
            if current_data['context'] != 'module':
                return ''
            internal: Union[bool, DocLine] = current_data['entry'].get_internal()
            if internal:
                return _resolve_tag('CodeObjectInternal',
                                    data_object,
                                    current_data={'entry': internal,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'InternalImage':
            # Returns the image link to the internal image
            return '../' * current_data['folder_depth'] + 'assets/Internal.svg'

        case 'CodeObjectSuperclass':
            # Returns the html for the superclass of the current code object if it has one
            if current_data['entry'].get_parent():
                return _resolve_tag('CodeObjectSuperclass', data_object, current_data)
            return ''

        case 'CodeObjectSuperObjectHref':
            # Returns the href of the superclass of the current code object
            return current_data['entry'].get_parent().get_href(current_data['folder_depth'])

        case 'CodeObjectGetSuperclass':
            # Returns the name of the superclass of the current code object
            return current_data['entry'].get_parent().get_name()

        case 'CodeObjectSubclasses':
            # Returns a html list of the subclasses of the current code object if it has any
            if subclasses := current_data['entry'].get_children():
                return _resolve_tag('CodeObjectSubclasses',
                                    data_object,
                                    current_data={'subclasses': subclasses,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'CodeObjectSubclassesEntry':
            # Loops through the subclasses of the current code object and returns the html link for each
            return _populate_list('CodeObjectSubclassesEntry', current_data['subclasses'], data_object, current_data)

        case 'CodeObjectDescriptionText':
            # Returns the description of the current code object
            return current_data['entry'].get_description()

        case 'See':
            # Returns the html for the see section of the current code object if it has one
            if 'entry' not in current_data:
                return ''
            if see := current_data['entry'].get_see_list():
                if len(see) > 1:
                    return _resolve_tag('See', data_object, current_data={'see': see,
                                                                          'folder_depth': current_data['folder_depth']})
                return tag_mapper('SeeSingle',
                                  data_object,
                                  current_data={'see': see[0],
                                                'folder_depth': current_data['folder_depth']})
            return ''

        case 'SeeSingle':
            # Returns the html code for a single see entry if the code object only had one @see reference
            href, value, description = current_data['see']
            # Process description
            if description:
                description = f': {description}'
            # Process href
            if not href.startswith('http') and not href.startswith('https'):
                href = f'{"../" * current_data["folder_depth"]}{href}'
            return f'<span class="code-object-keyword">See: </span><a href="{href}">{value}</a>{description}'

        case 'SeeEntries':
            # Loop through the see entries and return the html code for each
            see_list: str = []
            for href, value, description in current_data['see']:
                # Process description
                if description:
                    description = f': {description}'
                # Process href
                if not href.startswith('http') and not href.startswith('https'):
                    href = f'{"../" * current_data["folder_depth"]}{href}'

                # Add to list
                see_list.append(_resolve_tag('SeeEntries',
                                             data_object,
                                             current_data={'href': href,
                                                           'value': value,
                                                           'description': description,
                                                           'folder_depth': current_data['folder_depth']}))
            return '\n'.join(see_list)

        case 'SeeHref':
            # Returns the href of the current see entry
            return current_data['href']

        case 'SeeRef':
            # Returns the text of the current see entry
            return current_data['value']

        case 'SeeDescription':
            # Returns the description of the current see entry
            return current_data['description']

        case 'CodeObjectErrors':
            # Returns the html list of possible errors the entry can raise
            if errors := current_data['entry'].get_error_list():
                return _resolve_tag('CodeObjectErrors',
                                    data_object,
                                    current_data={'errors': errors,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'CodeObjectErrorsList':
            # Loops through the possible errors and returns the html code for each
            error_list: list[str] = []
            for error in current_data['errors']:
                error_list.append(_resolve_tag('CodeObjectErrorsList',
                                               data_object,
                                               current_data={'entry': error,
                                                             'folder_depth': current_data['folder_depth']}))
            return '<br>'.join(error_list)

        case 'GetErrorLevel':
            # Returns the error level of that the current error will raise
            return current_data['entry'].get_error_level()

        case 'GetErrorDescription':
            # Returns the description of the current error
            description: str = current_data['entry'].get_description()
            if description:
                return f'- {description}'
            return ''

        case 'CodeObjectFields':
            # Returns the html table of the fields of the current code object if it has any
            if fields := current_data['entry'].get_fields():
                return _resolve_tag('CodeObjectFields',
                                    data_object,
                                    current_data={'fields': fields,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'CodeObjectFieldsEntry':
            # Loops through the fields of the current code object and returns the html table row for each
            html_field_list: list[str] = []
            for field in current_data['fields']:
                html_field_list.append(_resolve_tag('CodeObjectFieldsEntry',
                                                    data_object,
                                                    current_data={'field': field,
                                                                  'folder_depth': current_data['folder_depth']}))
            return '\n'.join(html_field_list)

        case 'GetClassFieldName':
            # Returns the name of the current field
            return current_data['field'].get_field_name()

        case 'GetClassFieldType':
            # Returns the type of the current field
            filed_text: str = colour_type(current_data['field'].get_field_type(), data_object, current_data)
            if current_data['field'].get_optionality():
                filed_text += '<span class="code-object-small-keyword">(optional)</span>'
            return filed_text

        case 'GetClassFieldDescription':
            # Returns the description of the current field
            return current_data['field'].get_field_description()

        case 'CodeObjectProperties':
            # Returns the html table of the properties of the current code object if it has any
            if properties := current_data['entry'].get_properties():
                br: str = ''
                if current_data['entry'].get_fields():
                    br = '<br>\n'

                result: str = _resolve_tag("CodeObjectProperties",
                                           data_object,
                                           current_data={"properties": properties,
                                                         "entry": current_data["entry"],
                                                         'folder_depth': current_data['folder_depth']})
                return f'{br}{result}'
            return ''

        case 'CodeObjectPropertiesEntry':
            # Loops through the properties of the current code object and returns the html table row for each
            html_property_list: list[str] = []
            for prop in current_data['properties']:
                html_property_list.append(_resolve_tag('CodeObjectPropertiesEntry',
                                                       data_object,
                                                       current_data={'property': prop,
                                                                     'entry': current_data['entry'],
                                                                     'folder_depth': current_data['folder_depth']}))
            return '\n'.join(html_property_list)

        case 'GetPropertyID':
            # Returns the id of the current property
            return f'{current_data["entry"].get_id()}-{current_data["property"].get_property_name()}'

        case 'GetClassPropertyName':
            # Returns the name of the current property
            return current_data['property'].get_property_name()

        case 'GetClassPropertyValue':
            # Returns the value of the current property
            return colour_type(current_data['property'].get_property_value(), data_object, current_data)

        case 'GetClassPropertyDescription':
            # Returns the description of the current property
            return current_data['property'].get_property_description()

        case 'CodeObjectSource':
            # Returns the html code for the source code of the current code object if enabled
            if not conf.get_hide_source_code():
                return _resolve_tag('CodeObjectSource', data_object, current_data)
            return ''

        case 'CodeObjectSourceMirrorRef':
            # Returns the href to the source code mirror page
            return current_data['entry'].get_source_mirror_ref(current_data['folder_depth'])

        case 'CodeObjectCleanFileName':
            # Returns the original file name the current object was defined in
            return current_data['entry'].get_clean_filename()

        case 'CodeObjectLineHref':
            # Returns the href to the line the current object was defined in
            return current_data['entry'].get_line_num_href(current_data['folder_depth'])

        case 'CodeObjectDeclarationLine':
            # Returns the line number the current object was defined in
            return current_data['entry'].get_line_number()

        case 'CodeObjectCompressedMethodsList':
            # Returns a list of all the methods the current object has
            if methods := current_data['entry'].get_grouped_methods():
                return _resolve_tag('CodeObjectCompressedMethodsList',
                                    data_object,
                                    current_data={'methods': methods,
                                                  'entry': current_data['entry'],
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'CodeObjectCompressedMethodsEntry':
            # Loops through the methods of the current code object and returns a list of all the methods
            return _populate_list('CodeObjectCompressedMethodsEntry', current_data['methods'], data_object,
                                  current_data={'entry': current_data['entry'],
                                               'folder_depth': current_data['folder_depth']})

        case 'CodeObjectClassMethods':
            # Returns the html table of the methods of the current code object if it has any
            if methods := current_data['entry'].get_grouped_methods():
                return _resolve_tag('CodeObjectClassMethods',
                                    data_object,
                                    current_data={'methods': methods,
                                                  'entry': current_data['entry'],
                                                  'folder_depth': current_data['folder_depth'],
                                                  'context': current_data['context']})
            return ''

        case 'ClassMethodsTitle':
            # Returns the title of the methods list
            return f'{current_data["entry"].get_html_name()} Methods:'

        case 'CodeObjectMethods':
            # Loops over and returns the html code for each method of the current code object
            html_method_list: list[str] = []
            group_id: str = ''
            for method in current_data['methods']:
                if method.get_group() != group_id:
                    group_id = method.get_group()
                    html_method_list.append(f'<h2 class="code-object-group-title" id='
                                            f'"{method.get_href()}_group_{method.get_group().replace("<", "&lt;")}">'
                                            f'{group_id}</h2>\n<hr class="code-object-group-title-separator">')
                html_method_list.append(_resolve_tag('CodeObjectFunction',
                                                     data_object,
                                                     current_data={'entry': method,
                                                                   'folder_depth': current_data['folder_depth'],
                                                                   'context': current_data['context']}))
            return '\n<br>'.join(html_method_list)

        case 'GetFunctionName':
            # Returns the name of the current function
            return current_data['entry'].get_html_function_name()

        case 'InheritedMethodList':
            # Returns the html list of all methods the current object inherits
            if inherited_methods := current_data['entry'].get_inherited_methods():
                return _resolve_tag('InheritedMethodList',
                                    data_object,
                                    current_data={'inherited_methods': inherited_methods,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'InheritedMethodEntry':
            # Loops through the inherited methods of the current code object and returns the html list item for each
            html_inherited_method_list: list[str] = []
            for inherited_method in current_data['inherited_methods']:
                html_inherited_method_list.append(
                    _resolve_tag('InheritedMethodEntry',
                                 data_object,
                                 current_data={'entry': inherited_method,
                                               'folder_depth': current_data['folder_depth'],
                                               }))
            return '\n'.join(html_inherited_method_list)

        case 'CodeObjectSuperMethod':
            # Returns a html <a> tag linking to the super method of the current method if it has one
            if method := current_data['entry'].get_supermethod():
                return _resolve_tag('CodeObjectSuperMethod',
                                    data_object,
                                    current_data={'entry': method,
                                                  'folder_depth': current_data['folder_depth']})
            return ''

        case 'CodeObjectReturn':
            # Returns the html code for each mandatory return type the current code object has
            if return_list := current_data['entry'].get_return_list():
                return_html_list: list[str] = []
                for return_entry in return_list:
                    return_html_list.append(_resolve_tag('CodeObjectReturn',
                                                         data_object,
                                                         current_data={'entry': return_entry,
                                                                       'folder_depth': current_data['folder_depth'],
                                                                       'context': current_data['context']}))
                return '<br>\n'.join(return_html_list)
            return ''

        case 'CodeObjectReturnType':
            # Returns a html/css formatted string of the return type(s) of the current code object
            return colour_type(current_data['entry'].get_return_type(), data_object, current_data)

        case 'CodeObjectReturnDescription':
            # Returns the description of the return type of the current code object
            return current_data['entry'].get_return_description()

        case 'CodeObjectOptionalReturn':
            # Returns the html code for optional returns the current code object has
            optional_returns_list: list[str] = []
            # Add a blank line if there are mandatory returns
            if current_data['entry'].get_return_list():
                optional_returns_list.append('')
            if optional_returns := current_data['entry'].get_optional_returns():
                for optional_return in optional_returns:
                    optional_returns_list.append(_resolve_tag('CodeObjectOptionalReturn',
                                                              data_object,
                                                              current_data={'optional_return': optional_return,
                                                                            'folder_depth': current_data['folder_depth']
                                                                            }))
                return '<br>\n'.join(optional_returns_list)
            return ''

        case 'CodeObjectOptionalReturnType':
            # Returns a html/css formatted string of the optional return type(s) of the current code object
            return colour_type(current_data['optional_return'].get_return_type(), data_object, current_data)

        case 'CodeObjectOptionalReturnDescription':
            # Returns the description of the optional return type of the current code object
            return current_data['optional_return'].get_return_description()

        case 'CodeObjectParams':
            # Returns the html table of the parameters of the current code object if it has any
            if params := current_data['entry'].get_params():
                return _resolve_tag('CodeObjectParams',
                                    data_object,
                                    current_data={'params': params,
                                                  'folder_depth': current_data['folder_depth'], })
            return ''

        case 'CodeObjectParamsEntry':
            # Loops through the parameters of the current code object and returns the html table row for each
            html_field_list: list[str] = []
            for param in current_data['params']:
                html_field_list.append(_resolve_tag('CodeObjectParamsEntry',
                                                    data_object,
                                                    current_data={'param': param,
                                                                  'folder_depth': current_data['folder_depth'], }))
            return '\n'.join(html_field_list)

        case 'GetParamName':
            # Returns the name of the current parameter
            return current_data['param'].get_param_name()

        case 'GetParamType':
            # Returns a html/css formatted string of the type of the current parameter
            param_text: str = colour_type(current_data['param'].get_param_type(), data_object, current_data)
            if current_data['param'].get_optionality():
                param_text += '<span class="code-object-small-keyword">(optional)</span>'
            return param_text

        case 'GetParamDescription':
            # Returns the description of the current parameter
            return current_data['param'].get_param_description()

        case 'SourceCodeFolderMapContent':
            # Generates the sourcecodefoldermap.html file if source code is not hidden
            return _generate_source_code_map(current_data)

        case 'SourceCodeFileHref':
            # Returns the href of the current source code file
            return current_data['entry']

        case 'SourceCodeFileName':
            # Returns the name of the current source code file
            # Remove the parts of the entry that is only part of the href
            name: str = current_data['entry'].replace('sourcecode-', '', 1)
            name = g_href_hash_code_id_pattern.sub('', name, 1)
            return name

        case 'SourceCodeLuaFileIcon':
            # Returns the href of the LuaFile.svg icon
            return f'{"../" * current_data["folder_depth"]}assets/LuaFile.svg'

        case 'Skip':
            # Placeholder tag mainly used for fragments where it's expected that the user overwrite the fragment
            return ''

        case _:
            # Default case, resolve the tag as a fragment
            return _resolve_tag(tag, data_object, current_data)

    # Should never get here
    raise RuntimeError(f'\n{g_error_colour}ERROR(DM-1): Tag {tag} got past the tag mapper, this should never happen! '
                       f'Please report this bug!{g_end_colour}')
# pylint: enable=too-many-locals, too-many-return-statements, too-many-branches, too-many-statements
