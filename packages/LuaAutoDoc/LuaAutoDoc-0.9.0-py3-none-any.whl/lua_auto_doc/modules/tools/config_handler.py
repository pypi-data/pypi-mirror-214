""" This module contains functions to save and load configs."""
# pylint: disable=unused-variable
import os
from typing import Union
from json import dump, load
from importlib import resources


g_config: dict[str, str] = None
g_config_dir: str = os.getcwd()

def save_config(configuration: dict[str, str]) -> None:
    """ Saves a config to a file.

    :param configuration: The config to save.
    """
    with open('LAD_config.tmp', 'w', encoding='utf-8') as file:
        dump(configuration, file)


def load_config(file_path='LAD_config.tmp') -> dict[str, str]:
    """ Loads a config from a file.

    :return: The loaded config.
    """
    global g_config_dir
    if file_path != 'LAD_config.tmp':
        g_config_dir = os.path.dirname(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        return load(file)


def remove_config() -> None:
    """ Removes the config file. """
    os.remove('LAD_config.tmp')


def init_config(override=None) -> None:
    """ Initialises the config.

    :param override: The config to override the current config with.
    :type override: dict[str, str]

    """
    global g_config
    if g_config is None:
        if override is None:
            g_config = load_config()
        else:
            g_config = override


def get_root_directory() -> str:
    """ Checks the config for the root directory and returns the default if it is not found.

    :return: The root directory.
    """
    init_config()
    if 'project_folder' in g_config:
        return os.path.normpath(os.path.join(g_config_dir, g_config['project_folder']))

    return os.path.normpath(os.path.join(g_config_dir, '../..'))


def get_html_fragment_directory() -> str:
    """ Checks the config for the HTML fragment directory and returns the default if it is not found.

    :return: The HTML directory.
    """
    init_config()
    if 'html_fragment_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['html_fragment_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'LuaAutoDoc', 'HTMLFragments'))


def get_stylesheet_directory() -> str:
    """ Checks the config for the stylesheet directory and returns the default if it is not found.

    :return: The stylesheet directory.
    """
    init_config()
    if 'stylesheet_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['stylesheet_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'LuaAutoDoc', 'StyleSheets'))


def get_scripts_directory() -> str:
    """ Checks the config for the scripts directory and returns the default if it is not found.

    :return: The scripts directory.
    """
    init_config()
    if 'script_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['script_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'LuaAutoDoc', 'Scripts'))


def get_favicon_directory() -> str:
    """ Checks the config for the favicon directory and returns the default if it is not found.

    :return: The favicon directory.
    """
    init_config()
    if 'favicon_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['favicon_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'LuaAutoDoc', 'Favicon'))


def get_assets_directory() -> str:
    """ Checks the config for the assets directory and returns the default if it is not found.

    :return: The assets directory.
    """
    init_config()
    if 'assets_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['assets_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'LuaAutoDoc', 'Assets'))


def get_build_directory() -> str:
    """ Checks the config for the build directory and returns the default if it is not found.

    :return: The build directory.
    """
    init_config()
    if 'build_directory' in g_config:
        return os.path.normpath(os.path.join(get_root_directory(), g_config['build_directory']))

    return os.path.normpath(os.path.join(get_root_directory(), 'DocBuild'))


def get_lua_version() -> str:
    """ Checks the config for the Lua version and returns the default if it is not found.

    :return: The Lua version.
    """
    init_config()
    if 'lua_version' in g_config:
        return g_config['lua_version']

    return '5.1'


def get_encoding() -> str:
    """ Checks the config for the encoding and returns the default if it is not found.

    :return: The encoding.
    """
    init_config()
    if 'encoding' in g_config:
        return g_config['encoding']

    return 'utf-8'


def get_author() -> str:
    """ Checks the config for the author and returns the default if it is not found.

    :return: The author.
    """
    init_config()
    if 'author' in g_config:
        return g_config['author']

    return ''

def get_version() -> str:
    """ Checks the config for the version and returns the default if it is not found.

    :return: The version.
    """
    init_config()
    if 'version' in g_config:
        return g_config['version']

    return '1.0.0'


def get_project_name() -> str:
    """ Checks the config for the project name and returns the default if it is not found.

    :return: The project name.
    """
    init_config()
    if 'project_name' in g_config:
        return g_config['project_name']

    return 'My Project'


def get_show_hidden() -> bool:
    """ Checks the config for the show hidden setting and returns the default if it is not found.

    :return: The show hidden setting.
    """
    init_config()
    if 'show_hidden' in g_config:
        opt: Union[str, list] = g_config['show_hidden']
        if isinstance(opt, str):
            return opt.lower() == 'true'

        if isinstance(g_config['show_hidden'], list):
            return g_config['show_hidden']

    return False


def get_hide_source_code() -> bool:
    """ Checks the config for the hide source code setting and returns the default if it is not found.

    :return: The hide source code setting.
    """
    init_config()
    if 'hide_source_code' in g_config:
        return str(g_config['hide_source_code']).lower() == 'true'

    return False


def get_main_page() -> str:
    """ Checks the config for the main page and returns the default if it is not found.

    :return: The main page.
    """
    init_config()
    if 'main_page_name' in g_config:
        if g_config['main_page_name'].endswith('.html'):
            return g_config['main_page_name']
        return f'{g_config["main_page_name"]}.html'

    return 'index.html'


def get_multicore() -> int:
    """ Checks the config for the multicore setting and returns the default if it is not found.

    :return: The multicore setting.
    """
    init_config()
    if 'multicore' in g_config:
        if g_config['multicore'].lower() == 'true':
            return 16

        if g_config['multicore'].isdigit():
            return int(g_config['multicore'])

    return 1


def get_footer_links() -> list[dict[str, str]]:
    """ Checks the config for the footer links and returns the default if it is not found.

    :return: The footer links.
    """
    init_config()
    link_list: list[dict[str, str]] = []
    if 'footer_links' in g_config:
        for entry in g_config['footer_links']:
            if entry['url'].strip() != '' and entry['image_link'].strip() != '':
                link_list.append(entry)

    return link_list


def get_native_highlighter() -> bool:
    """ Checks the config for the native highlighter setting and returns the default if it is not found.

    :return: The native highlighter setting.
    """
    init_config()
    if 'native_highlighter' in g_config:
        return str(g_config['native_highlighter']).lower() != 'false' \
               and str(g_config['native_highlighter']).lower() != '0'

    return True


# Not part of the config file, but located here due to proximity to the other config functions.
def get_default_html_fragment_directory() -> str:
    """ Checks the config for the HTML fragment directory and returns the default if it is not found.

    :return: The HTML directory.
    """
    return resources.files('lua_auto_doc').joinpath('HTMLFragments')


def get_default_stylesheet_directory() -> str:
    """ Checks the config for the stylesheet directory and returns the default if it is not found.

    :return: The stylesheet directory.
    """
    return resources.files('lua_auto_doc').joinpath('StyleSheets')


def get_default_scripts_directory() -> str:
    """ Checks the config for the scripts directory and returns the default if it is not found.

    :return: The scripts directory.
    """
    return resources.files('lua_auto_doc').joinpath('Scripts')


def get_default_favicon_directory() -> str:
    """ Checks the config for the favicon directory and returns the default if it is not found.

    :return: The favicon directory.
    """
    return resources.files('lua_auto_doc').joinpath('Favicon')


def get_default_assets_directory() -> str:
    """ Checks the config for the assets directory and returns the default if it is not found.

    :return: The assets directory.
    """
    return resources.files('lua_auto_doc').joinpath('Assets')

# pylint: enable=unused-variable
