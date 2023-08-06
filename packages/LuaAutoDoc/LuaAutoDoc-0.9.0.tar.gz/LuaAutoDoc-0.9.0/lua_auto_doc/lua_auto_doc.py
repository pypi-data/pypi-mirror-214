""" Main module for LuaAutoDoc, running it will execute main program and configured in Config_LuaAutoDoc.py. """

import os
import re
import sys
import shutil
import getopt
import traceback
from importlib import resources
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.lua_parser.lua_documentation_parser import parse_lua_folder
from lua_auto_doc.modules.html_handler.doc_maker import build_html, init_build_directory, clean_build_directory
from lua_auto_doc.modules.tools.misc import g_error_colour, g_end_colour, g_code_field_colour,\
    g_code_field_end_colour, g_success_colour, g_warning_colour


# Regex patterns
g_css_colour_vars_pattern: re.Pattern = re.compile(r'''--[\w-]*-(?:colour|background)[\w-]*:\s*.*;''',
                                                   re.IGNORECASE | re.MULTILINE)
""" A pattern that matches css colour variable declaration lines."""


# Modified from Tobias Kienzler's answer on StackOverflow:
# https://stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python
def _full_stack() -> str:
    """ Returns a string containing the most recent stacktrace.

    :return: The stacktrace as a string.
    """
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be _full_stack()
    if exc is not None:  # i.e. an exception is present remove call of _full_stack,
        del stack[-1]    # the printed exception will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + re.sub(r'^Traceback \(most recent call last\):\n', '', traceback.format_exc())
    return stackstr


def _cmd_option_search() -> str:
    """ Searches current directory and subdirectories for a Config_LuaAutoDoc.json file and returns the folder path to
    it. Exits the program if it cannot find one.

    :return: The folder path to the Config_LuaAutoDoc.json file.
    """
    for root, _, files in os.walk(os.getcwd()):
        if 'Config_LuaAutoDoc.json' in files:
            return root
    print(f'{g_error_colour}Could not locate Config_LuaAutoDoc.json file in current directory or subdirectories.'
          f'{g_end_colour}')
    sys.exit(1)


def _get_css_colour_vars(file_path: str) -> set[str]:
    """ Will capture every css colour variable in a css file and return them in a set.

    :param file_path: The path to the css file.

    :return: The set of colour variables.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(g_css_colour_vars_pattern.findall(file.read()))


def _init_default(path: str, override_set) -> None:
    """ Sets up the default initialisation files for a LuaAutoDoc folder.

    :param path: The path to initialise the files to.
    :param override_set: Whether to override existing files.
    """
    # Init config file
    if not os.path.isfile(os.path.join(path, 'Config_LuaAutoDoc.json')) or override_set:
        config_path = resources.files('lua_auto_doc').joinpath('Config_LuaAutoDoc.json')
        shutil.copy2(src=config_path, dst=os.path.join(path, 'Config_LuaAutoDoc.json'))
        print(f'{g_success_colour}Config file created successfully.{g_end_colour}')
    else:
        print(f'{g_warning_colour}Config file already exists and was not overwritten.'
              f'Use the -o option to override it.{g_end_colour}')

    # Init HTML fragments
    for root, _, files in os.walk(os.path.join(conf.get_default_html_fragment_directory(), 'user_essentials')):
        for file in files:
            if not os.path.isdir(os.path.join(path, 'HTMLFragments')):
                os.makedirs(os.path.join(path, 'HTMLFragments'), exist_ok=True)

            if not os.path.isfile(os.path.join(path, 'HTMLFragments', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'HTMLFragments', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_config(path: str, override_set: bool) -> None:
    """ Sets up the config file for a LuaAutoDoc folder.

    :param path: The path to initialise the config file to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isfile(os.path.join(path, 'Config_LuaAutoDoc.json')) or override_set:
        config_path = resources.files('lua_auto_doc').joinpath('Config_LuaAutoDoc.json')
        shutil.copy2(src=config_path, dst=os.path.join(path, 'Config_LuaAutoDoc.json'))
        print(f'{g_success_colour}Config file created successfully.{g_end_colour}')
    else:
        print(f'{g_warning_colour}Config file already exists and was not overwritten.'
              f'Use the -o option to override it.{g_end_colour}')


def _init_templates(path: str, override_set: bool) -> None:
    """ Sets up the HTML user_essentials files for a LuaAutoDoc folder.

    :param path: The path to initialise the HTML files to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isdir(os.path.join(path, 'HTMLFragments')):
        os.makedirs(os.path.join(path, 'HTMLFragments'), exist_ok=True)
    for root, _, files in os.walk(os.path.join(conf.get_default_html_fragment_directory(), 'user_essentials')):
        for file in files:
            if not os.path.isfile(os.path.join(path, 'HTMLFragments', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'HTMLFragments', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_favicon(path: str, override_set: bool) -> None:
    """ Sets up the favicon files for a LuaAutoDoc folder.

    :param path: The path to initialise the favicon files to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isdir(os.path.join(path, 'Favicon')):
        os.makedirs(os.path.join(path, 'Favicon'), exist_ok=True)

    for root, _, files in os.walk(os.path.join(conf.get_default_favicon_directory())):
        for file in files:
            if not os.path.isfile(os.path.join(path, 'Favicon', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'Favicon', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_assets(path: str, override_set: bool) -> None:
    """ Sets up the assets files for a LuaAutoDoc folder.

    :param path: The path to initialise the assets files to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isdir(os.path.join(path, 'Assets')):
        os.makedirs(os.path.join(path, 'Assets'), exist_ok=True)

    for root, _, files in os.walk(os.path.join(conf.get_default_assets_directory())):
        for file in files:
            if not os.path.isfile(os.path.join(path, 'Assets', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'Assets', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_stylesheets(path: str, override_set: bool) -> None:
    """ Sets up the stylesheets files for a LuaAutoDoc folder.

    :param path: The path to initialise the stylesheets files to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isdir(os.path.join(path, 'StyleSheets')):
        os.makedirs(os.path.join(path, 'StyleSheets'), exist_ok=True)

    for root, _, files in os.walk(os.path.join(conf.get_default_stylesheet_directory())):
        for file in files:
            if not os.path.isfile(os.path.join(path, 'StyleSheets', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'StyleSheets', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_javascript(path: str, override_set: bool) -> None:
    """ Sets up the javascript files for a LuaAutoDoc folder.

    :param path: The path to initialise the javascript files to.
    :param override_set: Whether to override existing files.
    """
    if not os.path.isdir(os.path.join(path, 'Scripts')):
        os.makedirs(os.path.join(path, 'Scripts'), exist_ok=True)

    for root, _, files in os.walk(os.path.join(conf.get_default_scripts_directory())):
        for file in files:
            if not os.path.isfile(os.path.join(path, 'Scripts', file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(path, 'Scripts', file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


def _init_html_fragments(path: str, override_set: bool) -> None:
    """ Sets up the HTML fragments files for a LuaAutoDoc folder.

    :param path: The path to initialise the HTML fragments files to.
    :param override_set: Whether to override existing files.
    """
    for root, _, files in os.walk(conf.get_default_html_fragment_directory()):
        for file in files:
            # Get the relative path to the destination folder from root directory
            folder_dst: str = os.path.join(path, 'HTMLFragments',
                                           os.path.relpath(root, conf.get_default_html_fragment_directory()))

            if not os.path.isdir(folder_dst):
                os.makedirs(folder_dst, exist_ok=True)

            if not os.path.isfile(os.path.join(folder_dst, file)) or override_set:
                shutil.copy2(src=os.path.join(root, file), dst=os.path.join(folder_dst, file))
                print(f'{g_success_colour}{file} copied successfully.{g_end_colour}')
            else:
                print(f'{g_warning_colour}{file} already exists and was not overwritten.'
                      f'Use the -o option to override it.{g_end_colour}')


# pylint: disable=too-many-branches, too-many-statements
def _init(argv=()) -> None:
    """ Initialises a LuaAutoDoc folder for a project.

    :param argv: The command line arguments.
    """
    # Keep track of if a file specific setting has been given
    file_specific: bool = False
    # Init settings
    path: str = os.path.join(os.getcwd(), 'LuaAutoDoc')
    override_set: bool = False
    config_set: bool = False
    templates_set: bool = False
    reset_set: bool = False
    favicon_set: bool = False
    assets_set: bool = False
    html_set: bool = False
    css_set: bool = False
    js_set: bool = False

    opts, args = getopt.getopt(argv, 'p:ctorah', ['path=', 'config', 'templates', 'override', 'reset', 'all', 'help',
                                                  'favicon', 'assets', 'html', 'css', 'js'])
    for opt, args in opts:
        if opt in ('-h', '--help'):
            print(f'\n{g_code_field_colour}LuaAutoDoc init{g_code_field_end_colour} can be called without any '
                  'arguments for a standard setup. This includes creation of a LuaAutoDoc folder with a config file '
                  'and essential folders/templates added, like the main page description html file.\n\n'
                  f'Usage: {g_code_field_colour}LuaAutoDoc init -options{g_code_field_end_colour}\n'
                  'Options:\n'
                  f'{g_code_field_colour}-p, --path <path>{g_code_field_end_colour}: Specifies the path to initialise '
                  'the files to. Defaults to LuaAutoDoc/ if no option is given.\n'
                  f'{g_code_field_colour}-c, --config{g_code_field_end_colour}: Initialises the config file.\n'
                  f'{g_code_field_colour}-t, --templates{g_code_field_end_colour}: Initialises the essential '
                  'template files.\n'
                  f'{g_code_field_colour}-o, --override{g_code_field_end_colour}: Overrides existing files.\n'
                  f'{g_code_field_colour}-r, --reset{g_code_field_end_colour}: Cleans up the config folder and '
                  'initialises it again.\n'
                  f'{g_code_field_colour}-a, --all{g_code_field_end_colour}: Copy every source file to the config '
                  f'folder. Not recommended unless you want heavily customised documentation.\n'
                  f'{g_code_field_colour}--favicon{g_code_field_end_colour}: Copies the favicon folder to the config '
                  'folder.\n'
                  f'{g_code_field_colour}--assets{g_code_field_end_colour}: Copies the assets folder to the config '
                  'folder.\n'
                  f'{g_code_field_colour}--html{g_code_field_end_colour}: Copy all html fragments the config folder. '
                  'Not recommended unless you want to heavily '
                  'customise the documentation.\n'
                  f'{g_code_field_colour}--css{g_code_field_end_colour}: Copy all css files to the config folder.\n'
                  f'{g_code_field_colour}--js{g_code_field_end_colour}: Copy all js files to the config folder.\n'
                  f'{g_code_field_colour}-h, --help{g_code_field_end_colour}: Displays this message.')
            sys.exit(0)

        elif opt in ('-p', '--path'):
            path = os.path.normpath(os.path.join(os.getcwd(), args))

        elif opt in ('-c', '--config'):
            config_set = True
            file_specific = True

        elif opt in ('-t', '--templates'):
            templates_set = True
            file_specific = True

        elif opt in ('-o', '--override'):
            override_set = True

        elif opt in ('-r', '--reset'):
            reset_set = True

        elif opt in ('-a', '--all'):
            config_set = True
            favicon_set = True
            assets_set = True
            html_set = True
            css_set = True
            js_set = True
            file_specific = True

        elif opt == '--favicon':
            favicon_set = True
            file_specific = True

        elif opt == '--assets':
            assets_set = True
            file_specific = True

        elif opt == '--html':
            html_set = True
            file_specific = True

        elif opt == '--css':
            css_set = True
            file_specific = True

        elif opt == '--js':
            js_set = True
            file_specific = True

        else:
            print(f'{g_error_colour}Unknown argument: {opt}{g_end_colour}')
            sys.exit(1)

    # Make sure the path exists
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

    # Reset the config folder if requested
    if reset_set:
        shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    # If not file specific settings are given, initialise the standard setup
    if not file_specific:
        _init_default(path, override_set)
        sys.exit(0)

    # Init config file
    if config_set:
        _init_config(path, override_set)

    # Init HTML fragments
    if templates_set and not html_set:
        _init_templates(path, override_set)

    # Init Favicon
    if favicon_set:
        _init_favicon(path, override_set)

    # Init Assets
    if assets_set:
        _init_assets(path, override_set)

    # Init CSS
    if css_set:
        _init_stylesheets(path, override_set)

    # Init JS
    if js_set:
        _init_javascript(path, override_set)

    # Init all HTMLFragments
    if html_set:
        _init_html_fragments(path, override_set)
# pylint: enable=too-many-branches, too-many-statements


def _clean_build() -> None:
    """ Removes the configured DocBuild folder
    """
    if os.path.isdir(conf.get_build_directory()):
        shutil.rmtree(conf.get_build_directory())
        print(f'{g_success_colour}DocBuild removed successfully.{g_end_colour}')
    else:
        print(f'{g_error_colour}DocBuild not found at configured path: '
              f'{conf.get_build_directory()}{g_end_colour}')


def _clean_config(path) -> None:
    """ Removes the configured Config folder

    :param path: The path to the config folder.
    """
    try:
        shutil.rmtree(os.path.dirname(path))
        print(f'{g_success_colour}Config folder removed successfully.{g_end_colour}')
    except FileNotFoundError as e:
        print(e)


def _clean(argv=()) -> None:
    """ Removes generated LuaAutoDoc files from the project.

    :param argv: The command line arguments.
    """
    # Init settings
    path: str = 'Config_LuaAutoDoc.json'
    build_set: bool = False
    config_set: bool = False
    all_set: bool = False

    opts, args = getopt.getopt(argv, 'hp:sbca', ['help', 'path=', 'search', 'build', 'config', 'all'])
    for opt, args in opts:
        if opt in ('-h', '--help'):
            print(f'\n{g_code_field_colour}LuaAutoDoc clean{g_code_field_end_colour} can only be called with an option '
                  'specifier. Requires a Config_LuaAutoDoc.json file in the current directory unless -p or -s is used.'
                  '\n\n'
                  f'Usage: {g_code_field_colour}LuaAutoDoc clean -options{g_code_field_end_colour}\n'
                  'Options:\n'
                  f'{g_code_field_colour}-p, --path <path>{g_code_field_end_colour}: Specifies the path to the config '
                  'file. If not specified, it will only check current directory.\n'
                  f'{g_code_field_colour}-s, --search{g_code_field_end_colour}: Searches for a Config_LuaAutoDoc.json '
                  'file in the current directory and all subdirectories. If found, it will use that file as the config '
                  'file.\n'
                  f'{g_code_field_colour}-b, --build{g_code_field_end_colour}: Removes the generated Docbuild.\n'
                  f'{g_code_field_colour}-c, --config{g_code_field_end_colour}: Removes the config folder. This will '
                  'delete the ALL content in the config folder, including files not generated by LuaAutoDoc.\n'
                  f'{g_code_field_colour}-a, --all{g_code_field_end_colour}: Removes the generated DocBuild and the '
                  'config folder. This will delete the ALL content in the config folder, including files not generated '
                  'by LuaAutoDoc.\n'
                  f'{g_code_field_colour}-h, --help{g_code_field_end_colour}: Displays this help message.')
            sys.exit(0)

        elif opt in ('-p', '--path'):
            path = os.path.relpath(args, os.getcwd())

        elif opt in ('-s', '--search'):
            path = os.path.join(_cmd_option_search(), 'Config_LuaAutoDoc.json')

        elif opt in ('-b', '--build'):
            build_set = True

        elif opt in ('-c', '--config'):
            config_set = True

        elif opt in ('-a', '--all'):
            all_set = True

        else:
            print(f'{g_error_colour}Unknown option: {opt}{g_end_colour}')
            sys.exit(1)

    if not os.path.isfile(path):
        print(f'{g_error_colour}No config file found.{g_end_colour}')
        sys.exit(1)

    conf.init_config(conf.load_config(path))

    # Remove the build directory
    if build_set or all_set:
        _clean_build()

    # Remove the config directory
    if config_set or all_set:
        _clean_config(path)


def _template_theme() -> None:
    """ Generates a ThemeTemplate.css file containing every css colour variable in the configured stylesheet directory.
    """
    theme_list: list[str] = []
    for root, _, files in os.walk(conf.get_default_stylesheet_directory()):
        for file in files:
            if file.endswith('.css'):
                theme_list.extend(_get_css_colour_vars(os.path.join(root, file)))
                theme_list.append('')  # A blank line between each file
    css_string: str = ':root {\n\t' + '\n\t'.join(theme_list) + '\n}'
    if not os.path.isdir(conf.get_stylesheet_directory()):
        os.makedirs(conf.get_stylesheet_directory())
    with open(os.path.join(conf.get_stylesheet_directory(), 'ThemeTemplate.css'), 'w', encoding='utf-8') as css_file:
        css_file.write(css_string)
    print(f'{g_success_colour}ThemeTemplate.css generated successfully.{g_end_colour}')


def _template_code() -> None:
    """ Generates a CodeThemeTemplate.css file containing every css colour variable in SourceCode.css.
    """
    source_code_path = resources.files('lua_auto_doc').joinpath('StyleSheets/SourceCode.css')

    css_string: str = ':root {\n\t' + '\n\t'.join(_get_css_colour_vars(str(source_code_path))) + '\n}'
    if not os.path.isdir(conf.get_stylesheet_directory()):
        os.makedirs(conf.get_stylesheet_directory())
    with open(os.path.join(conf.get_stylesheet_directory(), 'CodeThemeTemplate.css'), 'w', encoding='utf-8') \
            as css_file:
        css_file.write(css_string)
    print(f'{g_success_colour}CodeThemeTemplate.css generated successfully.{g_end_colour}')


def _template_html() -> None:
    """ Generates a Template.html file containing the default HTML template for creating your own documentation page.
    """
    html_file_path = resources.files('lua_auto_doc').joinpath('HTMLFragments/templates/template.html')
    destination_path: str = os.path.join(conf.get_html_fragment_directory(), 'templates')
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)

    shutil.copy2(src=html_file_path, dst=os.path.join(destination_path, 'Template.html'))
    print(f'{g_success_colour}Template.html generated successfully.{g_end_colour}')


def _template(argv=()) -> None:
    """ Generates a template file.

    :param argv: The command line arguments.
    """
    # Init settings
    path: str = 'Config_LuaAutoDoc.json'
    theme_set: bool = False
    code_set: bool = False
    html_set: bool = False

    opts, args = getopt.getopt(argv, 'hp:s', ['help', 'path=', 'search', 'theme', 'code', 'html'])
    for opt, args in opts:
        if opt in ('-h', '--help'):
            print(f'\n{g_code_field_colour}LuaAutoDoc template{g_code_field_end_colour} can only be called with an '
                  'option specifier. Requires a Config_LuaAutoDoc.json file in the current directory unless -p or -s '
                  'is used.\n\n'
                  f'Usage: {g_code_field_colour}LuaAutoDoc template -options{g_code_field_end_colour}\n'
                  'Options:\n'
                  f'{g_code_field_colour}-p, --path <path>{g_code_field_end_colour}: Specifies the path to the config '
                  f'file. If not specified, it will only check current directory.\n'
                  f'{g_code_field_colour}-s, --search{g_code_field_end_colour}: Searches for a '
                  'Config_LuaAutoDoc.json file in the current directory and all '
                  'subdirectories. If found, it will use that file as the config file.\n'
                  f'{g_code_field_colour}--theme{g_code_field_end_colour}: Will generate a css file for conveniently '
                  'changing the colour theme of the  documentation.\n'
                  f'{g_code_field_colour}--code{g_code_field_end_colour}: Will generate a css file for conveniently '
                  'changing the colour theme of code blocks.\n'
                  f'{g_code_field_colour}--html{g_code_field_end_colour}: Will generate a template html file '
                  'containing the standard LuaAutoDoc tags like navbar, '
                  'header, footer, etc...\nRecommended if you want to add additional pages to your documentation.\n'
                  f'{g_code_field_colour}-h, --help{g_code_field_end_colour}: Displays this help message.')
            sys.exit(0)

        elif opt in ('-p', '--path'):
            path = args

        elif opt in ('-s', '--search'):
            os.chdir(_cmd_option_search())

        elif opt == '--theme':
            theme_set = True

        elif opt == '--code':
            code_set = True

        elif opt == '--html':
            html_set = True

        else:
            print(f'{g_error_colour}Unknown option: {opt}{g_end_colour}')
            sys.exit(1)

    if not os.path.isfile(path):
        print(f'{g_error_colour}No config file found.{g_end_colour}')
        sys.exit(1)

    conf.init_config(conf.load_config(path))

    # Generate theme file
    if theme_set:
        _template_theme()

    # Generate code file
    if code_set:
        _template_code()

    # Generate html file
    if html_set:
        _template_html()


def _build_config_setup(config_path: str, show_hidden: bool, hide_source_code: bool, overrides: dict[str, str]) -> None:
    """ Loads up the config file and applies the given overrides.

    :param config_path: The path to the config file.
    :param show_hidden: Whether to show hidden functions.
    :param hide_source_code: Whether to hide the source code.
    :param overrides: The overrides to apply to the config file.
    """
    # Load config file
    if not os.path.isfile(config_path):
        print(f'{g_error_colour}Error: config file not found.\nPath: {config_path}{g_end_colour}')
        sys.exit(1)

    config: dict[str, str] = conf.load_config(config_path)
    if show_hidden:
        config['show_hidden'] = show_hidden
    if hide_source_code:
        config['hide_source_code'] = hide_source_code
    for key, value in overrides.items():
        if key not in config:
            print(f'{g_error_colour}Error: invalid config key: {key}{g_end_colour}')
            sys.exit(1)
        config[key] = value
    conf.save_config(config)


# pylint: disable=broad-except, too-many-branches
def _build(argv=()) -> None:
    """ Builds the documentation for the given project.

    :param argv: The command line arguments.
    """
    config_path: str = os.path.join(os.getcwd(), 'Config_LuaAutoDoc.json')
    show_hidden: bool = None
    hide_source_code: bool = None
    overrides: dict[str, str] = {}

    opts, args = getopt.getopt(argv, 'hp:so:', ['path=', 'search', 'show_hidden', 'hide_source_code', 'override=',
                                                'help'])
    for opt, args in opts:
        if opt in ('-h', '--help'):
            print(f'\n{g_code_field_colour}LuaAutoDoc build{g_code_field_end_colour} can be called without any '
                  f'arguments if a config file is found in the current directory. A config file can be generated with '
                  f'the command {g_code_field_colour}LuaAutoDoc init -options{g_code_field_end_colour}.\n\n'
                  f'Usage: {g_code_field_colour}LuaAutoDoc build -options{g_code_field_end_colour}\n'
                  'Options:\n'
                  f'{g_code_field_colour}-p, --path <path>{g_code_field_end_colour}: The path to the config file. '
                  f'(must be given before other options)\n'
                  f'{g_code_field_colour}-s, --search{g_code_field_end_colour}: Will search for the config file in '
                  'the current directory and all subdirectories. Exits if none is found.\n'
                  'A more convenient alternative to -c. (must be given before other options)\n'
                  f'{g_code_field_colour}--show_hidden{g_code_field_end_colour}: Will ignore @hidden tags and include '
                  'hidden classes and functions in the documentation.\n'
                  f'{g_code_field_colour}--hide_source_code{g_code_field_end_colour}: If set, the source code will '
                  f'not be included in the documentation.\n'
                  f'{g_code_field_colour}-o, --override <arg>{g_code_field_end_colour}: format '
                  f'{g_code_field_colour}-o key=value{g_code_field_end_colour} can be used to override a specific'
                  f' config value. Can be used multiple times.\n'
                  f'{g_code_field_colour}-h, --help{g_code_field_end_colour}: Displays this help message.')
            sys.exit(0)

        elif opt in ('-p', '--path'):
            config_path = args
            os.chdir(os.path.dirname(args))

        elif opt in ('-s', '--search'):
            config_path = os.path.join(_cmd_option_search(), 'Config_LuaAutoDoc.json')
            # Change cwd to the config file's directory
            os.chdir(os.path.dirname(config_path))

        elif opt == '--show_hidden':
            show_hidden = 'True'

        elif opt == '--hide_source_code':
            hide_source_code = 'True'

        elif opt in ('-o', '--override'):
            key, value = args.split('=', 1)
            overrides[key] = value

        else:
            print(f'{g_error_colour}Unknown option: {opt}{g_end_colour}')
            sys.exit(1)

    # Setup config file
    _build_config_setup(config_path, show_hidden, hide_source_code, overrides)

    # noinspection PyBroadException
    try:
        init_build_directory()
        module_list, doc_entry_list = parse_lua_folder(conf.get_root_directory())
        build_html(module_list, doc_entry_list)
    # Catch all exceptions end clean build directory
    except KeyboardInterrupt:
        print(f'{g_error_colour}\nKeyboard interrupt, cleaning build directory and terminating program.'
              f'{g_end_colour}')
    except SystemExit:
        print(f'{g_error_colour}\nEncountered SystemExit, cleaning build directory and terminating program.'
              f'{g_end_colour}')
    except Exception:
        print(f'{g_error_colour}\nError: encountered unexpected error, cleaning build directory and terminating '
              f'program.\nTraceback: {_full_stack()}{g_end_colour}')
        clean_build_directory(conf.get_build_directory())
    finally:
        # Remove config file
        conf.remove_config()
# pylint: enable=broad-except, too-many-branches


def main() -> None:
    """ Main terminal interface for LuaAutoDoc. """
    # noinspection Assert
    argv: list[str] = sys.argv[1:]

    # Make sure the user is using Python 3.10 or higher
    # noinspection Assert
    assert sys.version_info >= (3, 10), '\nLuaAutoDoc requires Python 3.10 or higher.'
    if len(argv) < 1:
        print(f'\n{g_error_colour}LuaAutoDoc requires at least one argument.\nUse {g_end_colour}'
              f'{g_code_field_colour}LuaAutoDoc --help{g_code_field_end_colour}'
              f'{g_error_colour} to get help with calling LuaAutoDoc.{g_end_colour}')
        sys.exit()

    # Get command
    command: str = argv[0].lower()
    if command == 'init':
        _init(argv[1:])
    elif command == 'clean':
        _clean(argv[1:])
    elif command == 'build':
        _build(argv[1:])
    elif command == 'template':
        _template(argv[1:])
    elif command in ('-h', '--help'):
        print('\nLuaAutoDoc is a documentation generator for Lua.\n'
              'To use the program, you must first create a config directory with the command:\n'
              'LuaAutoDoc init -options\n'
              'You can then build the documentation with the command: '
              f'{g_code_field_colour}LuaAutoDoc build -options{g_code_field_end_colour}\n\n'
              'All available commands:\n'
              f'{g_code_field_colour}init -options{g_code_field_end_colour}: Creates a config file.\n'
              f'{g_code_field_colour}clean -options{g_code_field_end_colour}: Removes generated files.\n'
              f'{g_code_field_colour}build -options{g_code_field_end_colour}: Generates documentation.\n'
              f'{g_code_field_colour}template -options{g_code_field_end_colour}: Creates a template specified by '
              f'-options.\n'
              f'For more in-depth information you can run '
              f'{g_code_field_colour}LuaAutoDoc <command> --help{g_code_field_end_colour} or read the documentation at '
              f'https://gitlab.com/UlrikHD/LuaAutoDoc')
        sys.exit()
    else:
        print(f'{g_error_colour}Unknown command: {command}{g_end_colour}\n'
              f'Use {g_code_field_colour}LuaAutoDoc --help{g_code_field_end_colour} to read the documentation.')
        sys.exit(1)


if __name__ == '__main__':
    main()
