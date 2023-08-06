""" This module contains all the classes used for mapping out the documentation. """
import os
import re
from hashlib import sha1
from typing import Union
from enum import Enum, auto
import lua_auto_doc.modules.tools.config_handler as conf
from lua_auto_doc.modules.tools.misc import g_warning_colour, g_end_colour, g_error_colour


# Regex patterns
g_doc_pattern: re.Pattern = re.compile(r'''[ \t]*---[ \t]*(?:@(\w+)[: \t]*((?:[a-zA-Z_\.|][\w|\.]*(?:(?:[<\(]|(?<=fun)[ \t]|(?<=table[ \t]))[<\w, \t>\(\):]*[>\)?])?)*)?(?<!\?)(\?)?(?:(?<=\?)=(\S*))?[: \t]*((?:[a-zA-Z_|][\w\.|]*(?:[< \(][<\w,\. \t>\(\):|]*[>\)])?)*)?[: \t]*(\?)?(.*)|(.*))(?<=\S)''', re.MULTILINE)
""" A pattern that matches doc lines and captures its inputs.
Group 1 captures the tag
Group 2 captures the first follow-up word
Group 3 captures a question mark (optional tag)
Group 4 captures the default value if the Group 3 got a match, requires a preceding "=" sign
Group 5 captures the next follow-up word if Group 2 got a match
Group 6 Captures the optional tag for params
Group 7 captures the remaining text
Group 8 captures all the text if Group 1 got no match
"""
g_property_pattern: re.Pattern = re.compile(r'''[ \t]*---[ \t]*@property[: \t]+\S*[ \t]+(\S*)[ \t]*(.*)''', re.MULTILINE)
""" A pattern that's more fitting for capturing inputs from the @property tag. Group 1 captures the property value,
Group 2 captures the remaining text/description. The property name is presumed to be captured by g_doc_pattern."""
g_superclass_pattern: re.Pattern = re.compile(r'''---[ \t]*@[a-z]*[: \t]*([\w:\.]*)[ \t]*(?:\[([a-z]*)[ \t]*:[ \t]*(.*)\])?[ \t]*(.*)''', re.MULTILINE)
""" A pattern that's more fitting for capturing inputs from the @superclass tag."""
g_link_hint_pattern: re.Pattern = re.compile(r'''---[ \t]*@see[: \t]*"?((?<=").*?(?=")|\S*)"?[ \t]*(?:\[link_text:[ \t]*(.*?)(?<!\\)\])?(?:[ \t]*\[(\w*):[ \t]*(.*)(?<!\\)\])?[ \t]*(.*)''', re.MULTILINE)
""" A pattern to capture link hints.
Group 1 captures the reference,
Group 2 captures hyperlink text (optional)
Group 3 captures the hint type (optional)
Group 4 captures the hint if Group 3 got a match
Group 5 captures the description"""
g_see_reference_pattern: re.Pattern = re.compile(r'''([\w ]*)([:\.])?(\w*)?(\(\))?''', re.MULTILINE)
""" A pattern to capture the reference of a @see tag for further inspection.
Group 1 capture the section before "." or ":"
Group 2 captures the "." or ":" (optional)
Group 3 captures the section after "." or ":" if Group 2 got a match
Group 4 captures the ending parenthesis "()" (optional)"""
g_unescaped_less_than_pattern: re.Pattern = re.compile(r'''((?<!\\)(?:\\{2})*)(<)''', re.MULTILINE)
""" A pattern to capture the unescaped "<" character.
Group 1 captures the preceding escaped escape characters
Group 2 captures the "<" character."""
g_escaped_less_than_pattern: re.Pattern = re.compile(r'''((?<!\\)(?:\\{2})*)(\\<)''', re.MULTILINE)
r""" A pattern to capture the "<" character that's escaped.
Group 1 captures the preceding escape characters
Group 2 captures the escaped "\<" character."""
g_newline_escape_pattern: re.Pattern = re.compile(r'''(?<!\\)(\\{2})*(\\n)''', re.MULTILINE)
""" A Pattern that matches "visible" newline characters. Group 1 captures preceding escape characters,
Group 2 captures the newline character."""
g_tab_escape_pattern: re.Pattern = re.compile(r'''(?<!\\)(\\{2})*(\\t)''', re.MULTILINE)
""" A Pattern that matches "visible" tab characters. Group 1 captures preceding escape characters,
Group 2 captures the tab character."""
g_unescaped_hash_tag_start_pattern: re.Pattern = re.compile(r'''^#''', re.MULTILINE)
""" A pattern that matches the start of a line that starts with a hash tag."""
g_escaped_hash_tag_start_pattern: re.Pattern = re.compile(r'''^\\#''', re.MULTILINE)
""" A pattern that matches the start of a line that starts with an escaped hash tag."""
g_escape_pattern: re.Pattern = re.compile(r'''(\\\\)''', re.MULTILINE)
r""" A pattern that matches escaped backslashes. Group 1 captures '\\''"""
g_bad_file_characters_pattern: re.Pattern = re.compile(r'''[^\w\-_\.]''', re.MULTILINE)
""" A pattern that matches characters not allowed in file names that LuaAutoDoc generates. No capture groups."""
g_raise_level_pattern: re.Pattern = re.compile(r'''---[ \t]*@raise[ \t]+\w+[ \t]+(\w*)[ \t]*(.*)''')
""" A pattern for ---@raise tags that captures the error level and description. Group 1 captures the error level,
Group 2 captures the description."""
g_function_parameters_pattern: re.Pattern = re.compile(r'''function[ \t]+[\S]+?\((.*?)\)''')
""" A pattern that captures the parameters of a function. Group 1 captures the parameters."""


# Classes
# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes, too-many-public-methods
class DocLine:
    """A class to hold comment entries.
    """
    def __init__(self, line: str, line_number: int, file: str):
        """ Initialise a DocLine object.

        :param line: The text of the doc line.
        :param line_number: The line number of the doc line.
        :param file: The file the doc line is in.
        """
        match: re.Match = g_doc_pattern.search(line)
        self.comment_type: str = match.group(1) if match.regs[1][0] != -1 else 'description'
        self.line_number: int = line_number
        self.file: str = file
        self.line = line
        self.hint: str = None
        self.hint_type: str = None
        self.reference: str = None
        self.optional: bool = False
        self.default_value: str = None
        self.value: str = None
        self.name: str = None
        self.parent: str = ''
        self.type: str = None
        self.description: str = None
        self.tags: list[str] = []

        match self.comment_type:
            case 'description':
                self.init_description(match, line)
            case 'usage':
                self.init_usage(match, line)
            case 'module':
                self.init_module(match, line)
            case 'author':
                self.init_author(match, line)
            case 'class':
                self.init_class(match)
            case 'superclass':
                self.init_superclass(line)
            case 'field':
                self.init_field(match, line)
            case 'property':
                self.init_property(match, line)
            case 'member':
                self.init_member(match, line)
            case 'param':
                self.init_param(match, line)
            case 'return':
                self.init_return(match, line)
            case 'raise':
                self.init_raise(match, line)
            case 'deprecated':
                self.init_deprecated(match, line)
            case 'internal':
                self.init_internal(match, line)
            case 'hidden':
                self.init_hidden(match, line)
            case 'see':
                self.init_see(line)
            case 'group':
                self.init_group(match)
            case _:
                known_comment_types: list[str] = ['cast', 'type', 'alias', 'diagnostic', 'ignore', 'listener']
                if self.comment_type not in known_comment_types:
                    print(f'\n{g_warning_colour}ERROR(DC-0): Unknown comment type: {self.comment_type} on line '
                          f'{self.line_number}, File: {self.file}. Line is ignored.{g_end_colour}')

    def init_description(self, match: re.Match, line: str) -> None:
        """ Initialise a description DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        if match.regs[1][0] != -1:
            self.description: str = line[match.regs[2][0]:match.regs[0][1]]
        else:
            self.description: str = match.group(8)

    # Usage doc tag got scrapped, may be introduced again in the future.
    def init_usage(self, match: re.Match, line: str) -> None:
        """ Initialise a usage DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.description: str = line[match.regs[2][0]:match.regs[0][1]]

    def init_module(self, match: re.Match, line: str) -> None:
        """ Initialise a module DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.name: str = match.group(2)
        self.description: str = line[match.regs[2][1]:match.regs[0][1]].strip()

    def init_author(self, match: re.Match, line: str) -> None:
        """ Initialise an author DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.name: str = line[match.regs[2][0]:match.regs[0][1]]

    def init_class(self, match: re.Match) -> None:
        """ Initialise a class DocLine object.

        :param match: The regex match object.
        """
        self.name: str = match.group(2)
        if match.group(5):
            self.parent: str = match.group(5)

    def init_superclass(self, line: str) -> None:
        """ Initialise a superclass DocLine object.

        :param line: The text of the doc line.
        """
        match: re.Match = g_superclass_pattern.search(line)
        self.name: str = line[match.regs[1][0]:match.regs[1][1]]
        self.hint_type: str = match.group(2)
        self.hint: str = match.group(3)

    def init_field(self, match: re.Match, line: str) -> None:
        """ Initialise a field DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.name: str = match.group(2)
        self.type: str = match.group(5)
        self.optional: bool = match.group(6) == '?'
        self.default_value: str = match.group(5) if match.group(5) != '' else 'nil'
        self.description: str = line[match.regs[7][0]:match.regs[7][1]]

        # Special case of varargs
        if self.name == '...':
            self.type = f'vararg<{self.type}>'

    def init_property(self, match: re.Match, line: str) -> None:
        """ Initialise a property DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        property_match: re.Match = g_property_pattern.search(line)
        self.name: str = line[match.regs[2][0]:match.regs[2][1]]
        self.value: str = property_match.group(1)
        self.description: str = property_match.group(2)

    def init_member(self, match: re.Match, line: str) -> None:
        """ Initialise a member DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.init_field(match, line)

    def init_param(self, match: re.Match, line: str) -> None:
        """ Initialise a parameter DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.init_field(match, line)

    def init_return(self, match: re.Match, line: str) -> None:
        """ Initialise a return DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        self.type: str = match.group(2)
        self.optional: bool = match.group(3) == '?'
        self.default_value: str = match.group(4) if match.group(4) != '' else 'nil'
        if match.group(5):
            self.description: str = line[match.regs[5][0]:match.regs[7][1]]
        else:
            self.description: str = match.group(7)

    def init_raise(self, match: re.Match, line: str) -> None:
        """ Initialise a raise DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        raise_match: re.Match = g_raise_level_pattern.search(line)
        self.name: str = line[match.regs[2][0]:match.regs[2][1]]
        self.type: str = line[match.regs[5][0]:match.regs[5][1]]
        if raise_match and raise_match.group(1):
            self.value: str = raise_match.group(1)
            self.description: str = raise_match.group(2)
        else:
            self.value: str = '1'
            self.description: str = ''

    def init_deprecated(self, match: re.Match, line: str) -> None:
        """ Initialize a deprecated DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        if match.regs[2][0] != -1:
            self.description: str = line[match.regs[2][0]:match.regs[6][1]].strip()
        elif match.regs[7][0] != -1:
            self.description: str = line[match.regs[7][0]:match.regs[7][1]].strip()
        if self.description == '':
            self.description = 'Warning: This is deprecated and may be removed soon!'

    def init_internal(self, match: re.Match, line: str) -> None:
        """ Initialise an internal DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        if match.regs[2][0] != -1:
            self.description: str = line[match.regs[2][0]:match.regs[7][1]].strip()
        elif match.regs[7][0] != -1:
            self.description: str = line[match.regs[7][0]:match.regs[7][1]].strip()
        if self.description == '':
            self.description = 'Warning: This is for internal use only!'

    def init_hidden(self, match: re.Match, line: str) -> None:
        """ Initialise a hidden DocLine object.

        :param match: The regex match object.
        :param line: The text of the doc line.
        """
        if match.regs[2][0] != -1:
            self.tags = line[match.regs[2][0]:].replace(',', '').split(' ')
        elif match.regs[7][0] != -1:
            self.tags = line[match.regs[7][0]:].replace(',', '').split(' ')

    def init_see(self, line: str) -> None:
        """ Initialise a see DocLine object.

        :param line: The text of the doc line.
        """
        match: re.Match = g_link_hint_pattern.search(line)
        self.reference: str = match.group(1)
        self.hint_type: str = match.group(2)
        self.hint: str = match.group(3)
        self.description: str = match.group(4)

    def init_group(self, match: re.Match) -> None:
        """ Initialise a group DocLine object.

        :param match: The regex match object.
        """
        self.name: str = match.group(2)

    def __str__(self) -> str:
        """ Get the string representation of the doc line.

        :return: The string representation of the doc line.
        """
        return f'DocLine: {self.comment_type}'

    # getters
    def get_line(self) -> str:
        """ Get the text of the doc line.

        :return: The text of the doc line.
        """
        return self.line

    def get_optionality(self) -> bool:
        """ Get the optionality of the doc line.

        :return: The optionality of the doc line.
        """
        return self.optional

    def get_description(self) -> str:
        """ Get the description of the doc line.

        :return: The description of the doc line.
        """
        parsed_line: str = self.description.strip()
        parsed_line = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
        parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
        return parsed_line

    def get_comment_type(self) -> str:
        """ Get the type of the doc line.

        :return: The type of the doc line.
        """
        return self.comment_type

    def get_name(self) -> str:
        """ Get the name of the doc line.

        :return: The name of the doc line.
        """
        return self.name

    def get_field_name(self) -> str:
        """ Get the field of the doc line.

        :return: The field of the doc line.
        """
        valid_types: list[str] = ['field', 'member', 'param']
        if self.comment_type not in valid_types:
            raise AttributeError(f'Cannot get field/member/param name of DocLine type: {self.comment_type}.')
        return self.name.replace('<', '&lt;')

    def get_param_name(self) -> str:
        """ Get the parameter of the doc line. Wrapper for get_field_name().

        :return: The parameter of the doc line.
        """
        return self.get_field_name()

    def get_field_type(self) -> str:
        """ Get the type of the doc line.

        :return: The type of the doc line.
        """
        valid_types: list[str] = ['field', 'member', 'param']
        if self.comment_type not in valid_types:
            raise AttributeError(f'Cannot get field/member/param type of DocLine type: {self.comment_type}.')
        return self.type.replace('<', '&lt;')

    def get_param_type(self) -> str:
        """ Get the parameter type of the doc line. Wrapper for get_field_type().

        :return: The parameter type of the doc line.
        """
        return self.get_field_type()

    def get_field_description(self) -> str:
        """ Get the description of the doc line.

        :return: The description of the doc line.
        """
        valid_types: list[str] = ['field', 'member', 'param']
        if self.comment_type not in valid_types:
            raise AttributeError(f'Cannot get field/member/param description of DocLine typ: {self.comment_type}.')

        parsed_line: str = self.description.strip()
        parsed_line = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
        parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
        return parsed_line

    def get_param_description(self) -> str:
        """ Get the parameter description of the doc line. Wrapper for get_field_description().

        :return: The parameter description of the doc line.
        """
        return self.get_field_description()

    def get_property_name(self) -> str:
        """ Get the property of the doc line.

        :return: The property of the doc line.
        """
        if self.comment_type != 'property':
            raise AttributeError(f'Cannot get property name of DocLine type: {self.comment_type}.')
        return self.name.replace('<', '&lt;')

    def get_property_value(self) -> str:
        """ Get the property type of the doc line.

        :return: The property type of the doc line.
        """
        if self.comment_type != 'property':
            raise AttributeError(f'Cannot get property type of DocLine type: {self.comment_type}.')
        return self.value

    def get_property_description(self) -> str:
        """ Get the property description of the doc line.

        :return: The property description of the doc line.
        """
        if self.comment_type != 'property':
            raise AttributeError(f'Cannot get property description of DocLine type: {self.comment_type}.')

        parsed_line: str = self.description.strip()
        parsed_line: str = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
        parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
        return parsed_line

    def get_return_type(self) -> str:
        """ Get the return type of the doc line.

        :return: The return type of the doc line.
        """
        if self.comment_type != 'return':
            raise AttributeError(f'Cannot get return type of DocLine type: {self.comment_type}.')

        parsed_line: str = g_unescaped_less_than_pattern.sub(r'\1&lt;', self.type)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        return parsed_line

    def get_return_description(self) -> str:
        """ Get the return description of the doc line.

        :return: The return description of the doc line.
        """
        if self.comment_type != 'return':
            raise AttributeError(f'Cannot get return description of DocLine type: {self.comment_type}.')

        parsed_line: str = self.description.strip()
        parsed_line: str = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
        parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
        return parsed_line

    def get_tags(self) -> list[str]:
        """ Get the tags of the doc line.

        :return: The tags of the doc line.
        """
        if self.comment_type != 'hidden':
            raise AttributeError(f'Cannot get tags of DocLine type: {self.comment_type}.')
        return self.tags

    def get_error_level(self) -> str:
        """ Get the error level of the doc line.

        :return: The error level of the doc line.
        """
        if self.comment_type != 'raise':
            raise AttributeError(f'Cannot get error level of DocLine type: {self.comment_type}.')
        return self.value

    def get_superclass(self) -> str:
        """ Get the superclass of the class.

        :return: The superclass of the class.
        """
        if self.comment_type != 'class':
            raise AttributeError(f'Cannot get superclass of DocLine type: {self.comment_type}.')
        return self.parent


class DocEntry:
    """A class to hold doc entries.
    """
    def __init__(self, name: str, entry_type: str, locality: bool, comment_entries: list[DocLine], line_number: int,
                 def_line: str, module: Union[str, bool], relative_path: str, hashed_filename: str):
        """ Initialise a DocEntry object.

        :param name: The name of the doc object.
        :param entry_type: The type of the doc object, function, class, etc...
        :param locality: The locality of the doc object, local == True, Global == False.
        :param comment_entries: The list of comment entries preceding the doc object.
        :param line_number: The line number of the doc object.
        :param module: The module the doc object is in.
        :param relative_path: The relative path from source directory the doc object is in.
        :param hashed_filename: The filename of the html mirror of the source code.

        :return: A DocEntry object.
        """
        self.name: str = name
        self.entry_type: str = entry_type
        self.specific_type: str = ''
        self.methods: list[DocEntry] = []
        self.locality: str = 'local' if locality else 'global'
        self.comment_entries: list[DocLine] = comment_entries.copy()
        self.line_number: int = line_number
        self.module: str = module if module else ''
        self.path = relative_path
        self.hashed_filename: str = hashed_filename
        self.parent_id: str = ''
        self.parent: str = None
        self.method_parent: DocEntry = None
        self.children: list[DocEntry] = []
        self.inherited_methods: list[DocEntry] = []
        self.id = f'{hashed_filename}:{self.name}'
        self.see_init_list: list[str] = [line.get_line() for line in self.comment_entries
                                         if line.get_comment_type() == 'see']
        self.see_list: list[tuple[str, str, str]] = []
        self.description: str = '\n'.join([e.get_description() for e in self.comment_entries
                                           if e.get_comment_type() == 'description'])
        self.function_args: list[str] = []

        match self.entry_type:
            case 'class':
                self.init_class_specifics()
            case 'function':
                self.init_function_specifics(def_line)
            case _:
                print(f'\n{g_error_colour}ERROR(DC-1): Unknown entry type: {self.entry_type} from: {self.path} line: '
                      f'{self.line_number}.\nTerminating program{g_end_colour}')
                raise ValueError(f'{self.entry_type} is not a "class" or "function".')

    def init_class_specifics(self) -> None:
        """ Initialise class specific doc entries.
        """
        for entry in self.comment_entries:
            if entry.comment_type == 'superclass':
                self.parent_id = entry.get_name()
                break
            if entry.comment_type == 'class':
                self.parent_id = entry.get_superclass()

    def init_function_specifics(self, def_line: str) -> None:
        """ Initialise function specific doc entries.

        :param def_line: The function definition line.
        """
        # Get parent class if a method
        if ':' in self.name:
            self.parent_id = ':'.join(self.name.split(':')[:-1])
            self.name = self.name.split(':')[-1]
            self.specific_type = 'instance_method'
        elif '.' in self.name:
            self.parent_id = '.'.join(self.name.split('.')[:-1])
            self.name = self.name.split('.')[-1]
            self.specific_type = 'static_method'

        # Get function args
        args: str = g_function_parameters_pattern.search(def_line).group(1)
        if args:
            self.function_args = [arg.strip() for arg in args.split(',')]

    def init_see_list(self, doc_entries: list['DocEntry'], doc_modules: list['DocModule']) -> None:
        """ Initialise the see list of the doc entry.

        :param doc_entries: The list of doc entries.
        :param doc_modules: The list of doc modules.
        """
        for see_line in self.see_init_list:
            href, ref, description = find_see(see_line, doc_entries, doc_modules)
            if href:
                self.see_list.append((href, ref, description))

    def add_method(self, method: 'DocEntry') -> None:
        """ Add a method to the class.

        :param method: The method to add.
        """
        if not isinstance(method, DocEntry):
            raise TypeError(f'Cannot add method of type: {type(method)} to DocEntry object, only DocEntry.')
        if method.get_type() != 'function':
            raise TypeError(f'Cannot add method of type: {method.get_type()} to DocEntry object, only functions.')
        self.methods.append(method)

    def add_inherited_method(self, method: 'DocEntry') -> None:
        """ Add an inherited method to the class.

        :param method: The inherited method to add.
        """
        if not isinstance(method, DocEntry):
            raise TypeError(f'Cannot add inherited method of type: {type(method)} to DocEntry object, only DocEntry.')
        if method.get_type() != 'function':
            raise TypeError(f'Cannot add inherited method of type: {method.get_type()} to DocEntry object, only '
                            f'functions.')
        self.inherited_methods.append(method)

    def add_child(self, child: 'DocEntry') -> None:
        """ Add a child to the class.

        :param child: The child to add.
        """
        if not isinstance(child, DocEntry):
            raise TypeError(f'Cannot add child of type: {type(child)} to DocEntry object, only DocEntry.')
        self.children.append(child)

    def set_parent(self, parent: 'DocEntry') -> None:
        """ Add a parent to the class.

        :param parent: The parent to add.
        """
        if not isinstance(parent, DocEntry):
            raise TypeError(f'Cannot add parent of type: {type(parent)} to DocEntry object, only DocEntry.')
        self.parent = parent

    def set_method_parent(self, method_parent: 'DocEntry') -> None:
        """ Add a parent to the method.

        :param method_parent: The parent to add.
        """
        if not isinstance(method_parent, DocEntry):
            raise TypeError(f'Cannot add parent of type: {type(method_parent)} to DocEntry object, only DocEntry.')
        if self.entry_type != 'function':
            raise TypeError(f'Cannot add method parent to non-method: {self.entry_type}.')
        self.method_parent = method_parent

    def is_hidden(self, tags: Union[list[str], bool]) -> bool:
        """ Check if the doc object is hidden.

        :return: True if the doc object is hidden, False otherwise.
        """
        if tags is True:
            return False

        hidden_flag: bool = False
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'hidden':
                hidden_flag = True
                for entry_tag in entry.get_tags():
                    if tags and entry_tag in tags:
                        return False
        return hidden_flag

    def __str__(self):
        return f'DocEntry: {self.id} ({self.entry_type})'

    # Getters
    def get_source_mirror_ref(self, depth=0) -> str:
        """ Get the html reference for the source code mirror of the doc object.

        :param depth: The depth of the folder structure.

        :return: The html reference for the source code mirror of the doc object.
        """
        folder_depth: str = '../' * depth
        folder_depth += 'html/'
        return f'{folder_depth}sourcecode-{self.hashed_filename}'

    def get_hashed_filename(self) -> str:
        """ Get the hashed filename of the doc object.

        :return: The hashed filename of the doc object.
        """
        return self.hashed_filename

    def get_clean_filename(self) -> str:
        """ Get the filename of the doc object without the hash.

        :return: The filename of the doc object.
        """
        return f'{self.hashed_filename[:-16]}'

    def get_line_number(self) -> str:
        """ Get the line number of the doc object.

        :return: The line number of the doc object.
        """
        return str(self.line_number)

    def get_line_num_href(self, depth=0) -> str:
        """ Get the html reference for declaration of the doc object in the source code mirror.

        :param depth: The depth of the folder structure.

        :return: The html reference for declaration of the doc object in the source code mirror.
        """
        folder_depth: str = '../' * depth
        folder_depth += 'html/'
        return f'{folder_depth}sourcecode-{self.hashed_filename}#line_{self.line_number}'

    def get_module_href(self) -> str:
        """ Get the html reference for the module of the doc object.

        :return: The html reference for the module of the doc object.
        """
        if self.module:
            return f'module-{g_bad_file_characters_pattern.sub("_", self.module)}.html'
        if self.entry_type == 'class':
            return 'Classes.html'
        if self.entry_type == 'function':
            return 'Functions.html'
        raise AttributeError(f'Cannot get module href for doc entry of type: {self.entry_type}')

    def get_href(self, depth=0) -> str:
        """ Get the html reference for the doc object.

        :param depth: The depth of the folder structure.

        :return: The html reference for the doc object.
        """
        folder_depth: str = '../' * depth
        folder_depth += 'html/'
        if self.module != '':
            return f'{folder_depth}{self.get_module_href()}#{self.id}'
        if self.entry_type == 'class':
            return f'{folder_depth}{self.get_module_href()}#{self.id}'
        if self.entry_type == 'function':
            if self.method_parent:
                return f'{folder_depth}{self.method_parent.get_module_href()}#{self.id}'
            return f'{folder_depth}{self.get_module_href()}#{self.id}'

        raise AttributeError(f'Cannot get href for doc entry of type: {self.entry_type}')

    def get_id(self) -> str:
        """ Get the id of the doc object.

        :return: The id of the doc object.
        """
        return self.id

    def get_module(self) -> str:
        """ Get the module the doc object is in.

        :return: The module the doc object is in.
        """
        return self.module.replace('<', '&lt;')

    def get_type(self) -> str:
        """ Get the type of the doc object.

        :return: The type of the doc object.
        """
        return self.entry_type.replace('<', '&lt;').replace(',', ',<wbr>')

    def get_specific_type(self) -> str:
        """ Get the specific type of the doc object.

        :return: The specific type of the doc object.
        """
        if self.specific_type:
            return self.specific_type
        return self.get_type()

    def get_author(self) -> str:
        """ Get the author of the doc object.

        :return: The author of the doc object.
        """
        for entry in self.comment_entries:
            if entry.comment_type == 'author':
                parsed_line: str = g_unescaped_less_than_pattern.sub(r'\1&lt;', entry.name)
                parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
                return parsed_line
        return None

    def get_keywords(self) -> str:
        """ Get the keywords of the doc object.

        :return: The keywords of the doc object.
        """
        if self.method_parent:
            return 'method'
        return f'{self.locality} {self.entry_type}'.replace('<', '&lt;')

    def get_parent_id(self) -> str:
        """ Get the parent id of the doc object.

        :return: The parent id of the doc object.
        """
        return self.parent_id.replace('<', '&lt;')

    def get_parent(self) -> 'DocEntry':
        """ Get the parent of the doc object.

        :return: The parent of the doc object.
        """
        return self.parent

    def get_children(self) -> list['DocEntry']:
        """ Get the children of the doc object.

        :return: The children of the doc object.
        """
        return self.children

    def get_inherited_methods(self) -> list['DocEntry']:
        """ Get the inherited methods of the doc object.

        :return: The inherited methods of the doc object.
        """
        if self.entry_type != 'class':
            raise TypeError(f'Cannot get inherited methods of type: {self.entry_type}, only classes.')
        return self.inherited_methods

    def get_supermethod(self) -> 'DocEntry':
        """ Get the supermethod of the doc object. Wrapper for get_parent() with a type check.

        :return: The supermethod of the doc object.
        """
        if self.entry_type != 'function':
            raise TypeError(f'Cannot get supermethod of type: {self.entry_type}, only functions.')
        return self.get_parent()

    def get_name(self) -> str:
        """ Get the name of the doc object.

        :return: The name of the doc object.
        """
        return self.name

    def get_html_name(self) -> str:
        """ Get the name of the doc object with html breaks.

        :return: The name of the doc object with html breaks.
        """
        if self.entry_type == 'class':
            return self.name.replace('<', '&lt;')

        if self.entry_type == 'function':
            if self.parent_id != '':
                if self.get_specific_type() == 'static_method':  # Use dot separator for static methods.
                    return f'{self.parent_id}.{self.name}()'.replace('<', '&lt;')
                return f'{self.parent_id}:{self.name}()'.replace('<', '&lt;')

            return f'{self.name.replace("<", "&lt;")}()'

        raise AttributeError(f'Cannot get html name for entry type: {self.entry_type}')

    def get_description(self) -> str:
        """ Get the description of the doc object.

        :return: The description of the doc object.
        """
        # Replace whitespace escapes with their associated character.
        if self.description:
            parsed_line: str = self.description.strip()
            parsed_line = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
            parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
            parsed_line = g_newline_escape_pattern.sub(r'\1<br>', parsed_line)
            parsed_line = g_tab_escape_pattern.sub(r'\1&emsp;&emsp;', parsed_line)
            parsed_line = g_escape_pattern.sub(r'\\', parsed_line)
            parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
            parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
            return parsed_line

        return 'No given description.'

    def get_fields(self) -> list[DocLine]:
        """ Get the fields of the doc object.

        :return: The fields of the doc object.
        """
        valid_types: list[str] = ['param', 'member', 'field']
        fields: list[DocLine] = []
        for entry in self.comment_entries:
            if entry.get_comment_type() in valid_types:
                fields.append(entry)

        return fields

    def get_params(self) -> list[DocLine]:
        """ Wrapper for get_fields().

        :return: The fields of the doc object.
        """
        return self.get_fields()

    def get_properties(self) -> list[DocLine]:
        """ Get the properties of the doc object.

        :return: The properties of the doc object.
        """
        properties: list[DocLine] = []
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'property':
                properties.append(entry)

        return properties

    def get_methods(self) -> list['DocEntry']:
        """ Get the methods of the doc object.

        :return: The methods of the doc object.
        """
        if self.entry_type != 'class':
            raise AttributeError(f'DocEntry.get_methods() can only be called on a class. Got called on a '
                                 f'{self.entry_type}.')

        return self.methods

    def get_return_list(self) -> list[DocLine]:
        """ Get the non-optional return list of the doc object.

        :return: The non-optional return list of the doc object.
        """
        return_list: list[DocLine] = []
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'return' and not entry.get_optionality():
                return_list.append(entry)

        return return_list

    def get_return_type(self) -> str:
        """ Get the return type of the doc object.

        :return: The return type of the doc object.
        """
        return_type: str = 'nil'
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'return' and not entry.get_optionality():
                return entry.get_return_type()
        return return_type.replace('<', '&lt;').replace(',', ',<wbr>')

    def get_return_description(self) -> str:
        """ Get the return description of the doc object.

        :return: The return description of the doc object.
        """
        return_description: str = 'This function does not return anything.'
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'return' and not entry.get_optionality():
                return entry.get_description()
        return return_description.replace('<', '&lt;')

    def get_optional_returns(self) -> list[DocLine]:
        """ Get the optional returns of the doc object.

        :return: The optional returns of the doc object.
        """
        optional_returns: list[DocLine] = []
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'return' and entry.get_optionality():
                optional_returns.append(entry)

        return optional_returns

    def get_see_list(self) -> list[tuple[str, str, str]]:
        """ Get the see list of the DocEntry.

        :return: A list of tuples containing the href and name of the see entries.
        """
        return self.see_list

    def get_error_list(self) -> list[tuple[str, str]]:
        """ Get the error list of the DocEntry.

        :return: A list of tuples containing the error name and description.
        """
        error_list: list[DocLine] = []
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'raise':
                error_list.append(entry)
        return error_list

    def get_html_function_name(self) -> str:
        """ Get the function formatted to place nicely in html.

        :return: The function formatted to place nicely in html.
        """
        if self.parent_id != '':
            if self.get_specific_type() == 'static_method':  # Use dot separator for static methods.
                return f'{self.parent_id}.{self.name}({", ".join(self.function_args)})'.replace('<', '&lt;')
            return f'{self.parent_id}:{self.name}({", ".join(self.function_args)})'.replace('<', '&lt;')

        return f'{self.name.replace("<", "&lt;")}({", ".join(self.function_args)})'

    def get_deprecated(self) -> Union[DocLine, None]:
        """ Check if the doc object is deprecated.

        :return: True if the doc object is deprecated with a description, False otherwise.
        """
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'deprecated':
                return entry
        return None

    def get_internal(self) -> Union[DocLine, None]:
        """ Check if the doc object is internal.

        :return: True if the doc object is internal with a description, False otherwise.
        """
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'internal':
                return entry
        return None

    def get_group(self) -> str:
        """ Get the group of the doc object.

        :return: The group of the doc object.
        """
        for entry in self.comment_entries:
            if entry.get_comment_type() == 'group':
                return entry.get_name()
        return ''

    def get_groups(self) -> set[str]:
        """ Get the groups of the doc object class.

        :return: The groups of the doc object.
        """
        if self.entry_type != 'class':
            raise TypeError(f'Cannot get groups of type: {self.entry_type}, only classes.')
        group_list: set[str] = set()
        for entry in self.methods:
            if group := entry.get_group():
                group_list.add(group)
        group_list = list(group_list)
        group_list.sort()

        return group_list

    def get_methods_by_group(self, group_id: str) -> list['DocEntry']:
        """ Get all methods of the class belonging to a group.

        :param group_id: The group id to get the methods for.

        :return: A list of methods belonging to the given group.
        """
        entry_list: list['DocEntry'] = []
        for entry in self.methods:
            if entry.get_group() == group_id:
                entry_list.append(entry)

        return entry_list

    def get_grouped_methods(self) -> list['DocEntry']:
        """ Get all methods of the class grouped by group.

        :return: A dictionary of methods grouped by group.
        """
        grouped_list: list[str] = []
        for entry in self.methods:
            if not entry.get_group():
                grouped_list.append(entry)
        for group in self.get_groups():
            grouped_list.extend(self.get_methods_by_group(group))

        return grouped_list


class DocModule:
    """A class to hold doc module entries.
    """
    def __init__(self, name: str, description_list: list[DocLine]):
        """ Initialise a DocModule object.

        :param name: The name of the doc module.
        :param relative_path: The relative path from source directory the doc module is in.

        :return: A DocModule object.
        """
        self.name: str = name
        self.file_name: str = f'module-{g_bad_file_characters_pattern.sub("_", name)}.html'
        self.classes: list[DocEntry] = []
        self.functions: list[DocEntry] = []

        self.description: str = '\n'.join([line.get_description() for line in description_list
                                           if line.get_comment_type() == 'description'])
        self.see_init_list: list[str] = [line.get_line() for line in description_list
                                         if line.get_comment_type() == 'see']
        self.see_list: list[tuple[str, str, str]] = []
        self.deprecated: DocLine = None
        self.internal: DocLine = None
        for line in description_list:
            if line.get_comment_type() == 'deprecated':
                self.deprecated = line
                continue
            if line.get_comment_type() == 'internal':
                self.internal = line
                continue

    def __str__(self):
        """ Get the string representation of the doc module.

        :return: The string representation of the doc module.
        """
        return f'DocModule: {self.name}'

    def __eq__(self, other):
        """ Check if two doc modules are equal.

        :param other: The other doc module to compare to.

        :return: True if the doc modules are equal or share name with string, false otherwise.
        """
        if isinstance(other, str):
            return self.name == other
        if not isinstance(other, DocModule):
            return False
        return self.name == other.name

    def add_class(self, class_entry: DocEntry):
        """ Add a class to the module.

        :param class_entry: The class to add.
        """
        self.classes.append(class_entry)

    def add_function(self, function_entry: DocEntry):
        """ Add a function to the module.

        :param function_entry: The function to add.
        """
        self.functions.append(function_entry)

    def extend(self, other: 'DocModule'):
        """ Extend the doc module with another doc module.

        :param other: The other doc module to extend with.
        """
        self.classes.extend(other.get_classes())
        self.functions.extend(other.get_functions())
        if other.get_description() != '':
            self.description += f'\n\n{other.get_description()}'

    def init_see_list(self, doc_entries: dict[str, DocEntry], doc_modules: dict[str, 'DocModule']):
        """ Initialise the see list of the doc module.

        :param doc_entries: The dictionary of all doc entries.
        :param doc_modules: The dictionary of all doc modules.
        """
        for see_line in self.see_init_list:
            href, ref, description = find_see(see_line, doc_entries, doc_modules)
            if href:
                self.see_list.append((href, ref, description))

    def sort_entries(self):
        """ Sort the entries of the doc module.
        """
        self.classes.sort(key=lambda x: x.get_name().lower())
        self.functions.sort(key=lambda x: x.get_name().lower())

    # Getters
    def get_name(self) -> str:
        """ Get the name of the doc module.

        :return: The name of the doc module.
        """
        return self.name

    def get_module(self):
        """ Wrapper for get_name() meant for situations where you got a mix of DocEntry and DocModule objects.

        :return: The name of the doc module.
        """
        return self.get_name()

    def get_href(self, depth=0) -> str:
        """ Get the href for the doc module.

        :return: The href for the doc module.
        """
        folder_depth = '../' * depth
        return f'{folder_depth}html/module-{g_bad_file_characters_pattern.sub("_", self.name)}.html'

    def get_file_name(self) -> str:
        """ Get the file name of the doc module.

        :return: The file name of the doc module.
        """
        return self.file_name

    def get_html_name(self) -> str:
        """ Get the name of the doc module with html breaks.

        :return: The name of the doc module with html breaks.
        """
        html_name: str = self.name.replace(':', ':<wbr>').replace('.', '.<wbr>').replace('-', '-<wbr>')
        return os.path.splitext(html_name)[0]

    def get_description(self) -> str:
        """ Get the description of the doc module.

        :return: The description of the doc module.
        """
        # Replace whitespace escapes with their associated character.
        parsed_line: str = self.description.strip()
        parsed_line = g_unescaped_less_than_pattern.sub(r'\1&lt;', parsed_line)
        parsed_line = g_escaped_less_than_pattern.sub(r'\1<', parsed_line)
        parsed_line = g_newline_escape_pattern.sub(r'\1<br>', parsed_line)
        parsed_line = g_tab_escape_pattern.sub(r'\1&emsp;&emsp;', parsed_line)
        parsed_line = g_escape_pattern.sub(r'\\', parsed_line)
        parsed_line = g_unescaped_hash_tag_start_pattern.sub('', parsed_line)
        parsed_line = g_escaped_hash_tag_start_pattern.sub('#', parsed_line)
        return parsed_line

    def get_classes(self) -> list[DocEntry]:
        """ Get the classes of the doc module.

        :return: The classes of the doc module.
        """
        entries = self.classes.copy()
        return entries

    def get_functions(self) -> list[DocEntry]:
        """ Get the functions of the doc module.

        :return: The functions of the doc module.
        """
        entries = self.functions.copy()
        return entries

    def get_entries(self) -> list[DocEntry]:
        """ Get all the entries of the doc module.

        :return: All the entries of the doc module.
        """
        entries: list[DocEntry] = []
        entries.extend(self.classes)
        entries.extend(self.functions)

        return entries

    def get_see_list(self) -> list[tuple[str, str, str]]:
        """ Get the see list of the doc module.

        :return: A list of tuples containing the href and name of the see entries.
        """
        return self.see_list

    def get_deprecated(self) -> Union[DocLine, None]:
        """ Get the deprecated line of the doc module.

        :return: The deprecated line of the doc module.
        """
        if self.deprecated:
            return self.deprecated
        return None

    def get_internal(self) -> Union[DocLine, None]:
        """ Get the internal line of the doc module.

        :return: The internal line of the doc module.
        """
        if self.internal:
            return self.internal
        return None
# pylint: enable=too-many-instance-attributes, too-many-public-methods


class ReferenceType(Enum):
    """ Enum for the type of reference. """
    CLASS_or_MODULE = auto()
    INSTANCE_METHOD = auto()
    STATIC_METHOD = auto()
    CLASS_FIELD = auto()
    FUNCTION = auto()

    def __str__(self) -> str:
        """Makes it so the enum name is printed rather than the value assigned to it by auto()"""
        return self.name.lower()

    def __eq__(self, other) -> bool:
        """Create a sensible comparison logic for the enums

        :param Any other: Object to compare with

        :return: Returns True if objects got equal string representation in lower case, otherwise False
        """
        if self is ReferenceType.CLASS_or_MODULE:
            return 'class' == str(other).lower() or 'module' == str(other).lower()

        return str(self).lower() == str(other).lower()


class HintType(Enum):
    """ Enum for the type of hint. """
    ABS_PATH = auto()
    REL_PATH = auto()
    MODULE = auto()

    def __eq__(self, other) -> bool:
        return self.name.lower() == str(other).lower()


# pylint: disable=unused-variable
def _resolve_hit(hit: tuple[str, DocEntry, Union[DocLine, None]], presumed_type: ReferenceType, hint_type: str,
                 hint, hit_options: dict[str, tuple[str, str]]) \
        -> Union[bool, tuple[str, str]]:
    """ Resolves the hit in _search_reference.

    :param hit: The hit to resolve.
    :param presumed_type: The presumed type of the hit.
    :param hint_type: The type of hint.
    :param hint: The hint.
    :param hit_options: The dict to update if not a direct hit.

    :return: False if not a direct hit, otherwise a tuple with the href and reference.
    """
    # Check for hint hit
    if hint_type == HintType.MODULE and hit[1].get_module() == hint \
            or (hint_type in (HintType.REL_PATH, HintType.ABS_PATH)) and hit[1].get_hashed_filename() == hint:
        # Check for direct hit and return immediately if found
        if hit[0] == presumed_type and presumed_type is ReferenceType.CLASS_FIELD:
            href: str = f'{hit[1].get_href()}-{hit[2].get_name()}'
            ref: str = f'{hit[1].get_name()}.{hit[2].get_name()}'
            return href, ref
        if hit[0] == presumed_type:
            return hit[1].get_href(), hit[1].get_html_name()
        # Else we got a hint hit but the type is maybe wrong
        hit_options['hint_hit'] = (hit[1].get_href(), hit[1].get_html_name())

    # Check for near hit
    elif hit[0] == presumed_type and presumed_type is ReferenceType.CLASS_FIELD:
        href: str = f'{hit[1].get_href()}-{hit[2].get_name()}'
        ref: str = f'{hit[1].get_name()}.{hit[2].get_name()}'
        hit_options['near_hit'] = (href, ref)
    elif hit[0] == presumed_type:
        hit_options['near_hit'] = (hit[1].get_href(), hit[1].get_html_name())
    # Else it is a rest hit
    else:
        hit_options['rest_hit'] = (hit[1].get_href(), hit[1].get_html_name())

    return False


def _add_module_hits(prefix: str, doc_modules: list[DocModule], presumed_type: ReferenceType,
                     hits: list[tuple[str, DocEntry, Union[DocLine, None]]]) -> None:
    """ Adds all module hits to the hits list.

    :param prefix: The prefix of the entry.
    :param doc_modules: The list of all doc modules.
    :param presumed_type: The presumed type of the entry.
    :param hits: The list to add the hits to.
    """
    # Check for module hits if the type could be a module
    if presumed_type is ReferenceType.CLASS_or_MODULE:
        for doc_module in doc_modules:
            if doc_module.get_name() == prefix:
                hits.append(('module', doc_module, None))


def _add_entry_hits(prefix: str, suffix: str, doc_entries: dict[str, DocEntry],
                    hits: list[tuple[str, DocEntry, Union[DocLine, None]]]) -> None:
    """ takes in a list and add all possible reference hits to it.

    :param prefix: The prefix of the entry.
    :param suffix: The suffix of the entry.
    :param doc_entries: The dictionary of all doc entries.
    :param doc_modules: The list of all doc modules.
    :param presumed_type: The presumed type of the entry.
    :param hits: The list to add the hits to.
    """
    for doc_entry in doc_entries.values():
        if doc_entry.get_name() == prefix:
            if suffix is None:
                hits.append((doc_entry.get_type(), doc_entry, None))
            elif doc_entry.get_type() == 'class':
                for method in doc_entry.get_methods():
                    if method.get_name() == suffix:
                        hits.append((method.get_specific_type(), method, None))

                for field in doc_entry.get_fields():
                    if field.get_field_name() == suffix:
                        hits.append(('class_field', doc_entry, field))
                for class_property in doc_entry.get_properties():
                    if class_property.get_property_name() == suffix:
                        hits.append(('class_field', doc_entry, class_property))


# noinspection InsecureHash
def _search_reference(prefix: str, suffix: str, presumed_type: ReferenceType, doc_entries: dict[str, DocEntry],
                      doc_modules: list[DocModule], hint_type=None, hint=None) -> tuple[str, str]:
    """ Searches through all doc entries and returns the doc entry with the given name.

    :param prefix: The prefix of the entry.
    :param suffix: The suffix of the entry.
    :param presumed_type: The presumed type of the entry.
    :param doc_entries: The dictionary of all doc entries.
    :param doc_modules: The list of all doc modules.
    :param hint_type: The type of hint.
    :type hint_type: str
    :param hint: The hint to use for the search.
    :type hint: str

    :return: the href and name of the entry.
    """
    if hint_type == HintType.ABS_PATH:
        hint = os.path.normpath(hint)
        hash_code: str = sha1(os.path.relpath(hint, conf.get_root_directory()).encode('utf-8')).hexdigest()[:10]
        hint: str = f'{os.path.split(hint)[-1]}_{hash_code}.html'
    elif hint_type == HintType.REL_PATH:
        hint = os.path.join(conf.get_root_directory(), hint)
        hint = os.path.normpath(hint)
        hash_code: str = sha1(os.path.relpath(hint, conf.get_root_directory()).encode('utf-8')).hexdigest()[:10]
        hint: str = f'{os.path.split(hint)[-1]}_{hash_code}.html'

    hits: list[tuple[str, DocEntry, Union[DocLine, None]]] = []
    _add_entry_hits(prefix, suffix, doc_entries, hits)
    _add_module_hits(prefix, doc_modules, presumed_type, hits)

    # near_hit: The hit that matches the entry, but not the hint, highest priority hit
    # hint_hit: The hit that matches the hint, but not the entry, second-highest priority hit
    # rest_hit: The hit that matches the entry the closest, lowest priority hit
    hit_options: dict[str, tuple[str, str]] = {'near_hit': None, 'hint_hit': None, 'rest_hit': None}
    for hit in hits:
        result: Union[bool, tuple[str, str]] = _resolve_hit(hit, presumed_type, hint_type, hint, hit_options)
        if result is not False:
            return result

    if hit_options['near_hit']:
        return hit_options['near_hit']
    if hit_options['hint_hit']:
        return hit_options['hint_hit']
    if hit_options['rest_hit']:
        return hit_options['rest_hit']

    return None, None


def _get_presumed_see_type(ref_separator: str, ref_function_symbol: str) -> ReferenceType:
    """ Returns the presumed type of see entry.

    :param ref_separator: The separator of the see entry.
    :param ref_function_symbol: The function symbol of the see entry.

    :return: The presumed type of the see entry.
    """
    if ref_separator == ':' and ref_function_symbol:
        return ReferenceType.INSTANCE_METHOD
    if ref_separator == ':' and ref_function_symbol:
        return ReferenceType.STATIC_METHOD
    if ref_separator:
        return ReferenceType.CLASS_FIELD
    if ref_function_symbol:
        return ReferenceType.FUNCTION

    return ReferenceType.CLASS_or_MODULE


def _get_see_reference(ref_match: re.Match, doc_entries: dict[str, DocEntry], doc_modules: list[DocModule],
                       hint_type: str, hint: str) -> tuple[str, str]:
    """ Returns the reference of a see entry.

    :param ref_match: The match of the see entry.
    :param doc_entries: The dictionary of all doc entries.
    :param doc_modules: The list of all doc modules.
    :param hint_type: The type of hint.
    :param hint: The hint to use for the search.

    :return: The href and name of the entry.
    """
    ref_name: str = ref_match.group(1)
    ref_separator: str = ref_match.group(2) if ref_match.group(2) else None
    ref_addon: str = ref_match.group(3) if ref_match.group(3) else None
    ref_function_symbol: str = ref_match.group(4) if ref_match.group(4) else None

    presumed_type: ReferenceType = _get_presumed_see_type(ref_separator, ref_function_symbol)

    return _search_reference(ref_name, ref_addon, presumed_type, doc_entries, doc_modules, hint_type, hint)


def find_see(line: str, doc_entries: dict[str, DocEntry], doc_modules: list[DocModule],
             ignore_miss=False) -> tuple[str, str, str]:
    """ Searches through a list of all doc_entries and returns the href and name of the see entry.

    :param line: The line containing the see entry.
    :param doc_entries: The dictionary of all doc entries.
    :param doc_modules: The list of all doc modules.
    :param ignore_miss: If true, will not print a warning message when not finding a reference.
    :type ignore_miss: bool

    :return: A tuple containing the href, name and description of the @see entry.
    """
    match: re.Match = g_link_hint_pattern.search(line)

    if not match:
        return None, None, None

    reference: str = match.group(1)
    hyperlink_text: str = match.group(2) if match.group(2) else reference
    hint_type: str = match.group(3) if match.group(3) else None
    hint: str = match.group(4) if match.group(4) else None
    description: str = match.group(5)

    # No search needed if the reference is already a link
    if reference.startswith(r'https://') or reference.startswith(r'http://'):
        return reference, hyperlink_text, description

    # Determine the type of the reference, class, function, class method, class, field, etc...
    ref_match: re.Match = g_see_reference_pattern.search(reference)
    if not ref_match:
        print(f'{g_end_colour}Invalid @see reference: {reference}. Reference must either by a weblink starting with'
              f' http:// or https:// or a valid Lua name.{g_end_colour}')

    href, ref = _get_see_reference(ref_match, doc_entries, doc_modules, hint_type, hint)

    if ref:
        ref = ref.replace('<', '&lt;').replace('>', '&gt;')

    if href is None:
        if not ignore_miss:
            print(f'\n{g_warning_colour}WARNING: Could not find @see reference from line: "{line}"{g_end_colour}')
        return None, None, None

    # If we got an "overwrite text", use that instead of the reference
    # handle escaping of <
    if hyperlink_text:
        ref = g_unescaped_less_than_pattern.sub(r'\1&lt;', hyperlink_text)
        ref = g_escaped_less_than_pattern.sub(r'\1<', ref)
    else:
        ref = g_unescaped_less_than_pattern.sub(r'\1&lt;', ref)
        ref = g_escaped_less_than_pattern.sub(r'\1<', ref)

    return href, ref, description


def init_see_lists(doc_entries: dict[str, DocEntry], doc_modules: list[DocModule]) -> None:
    """ Loops through every DocEntry and DocModule and initialises their see lists.

    :param doc_entries: The dictionary of all DocEntries.
    :param doc_modules: The list of all DocModules.
    """
    for entry in doc_entries.values():
        entry.init_see_list(doc_entries, doc_modules)
        if entry.get_type() == 'class':
            for method in entry.get_methods():
                method.init_see_list(doc_entries, doc_modules)
    for module in doc_modules:
        module.init_see_list(doc_entries, doc_modules)


def link_class_child_parents(doc_entries: dict[str, DocEntry]) -> None:
    """ Loops through all the doc entries and links DocEntry classes to their parents.

    :param doc_entries: The list of doc entries to update.
    """
    for entry in doc_entries.values():
        # Filter out entries without a parent and entries that are not classes
        if not entry.get_parent_id():
            continue
        if entry.get_type() != 'class':
            continue

        # Search DocEntries with priority file -> module -> rest
        module_entry: DocEntry = None
        rest_entry: DocEntry = None
        file_entry_flag: bool = False
        for doc_entry in doc_entries.values():
            if entry.get_parent_id() == doc_entry.get_name():
                if entry.get_hashed_filename() == doc_entry.get_hashed_filename():
                    # Update immediately if the file is the same
                    entry.set_parent(doc_entry)
                    doc_entry.add_child(entry)
                    file_entry_flag = True
                    break
                if doc_entry.get_module() == entry.get_module():
                    module_entry = doc_entry
                else:
                    rest_entry = doc_entry

        if file_entry_flag:
            continue
        if module_entry:
            entry.set_parent(module_entry)
            module_entry.add_child(entry)
        elif rest_entry:
            entry.set_parent(rest_entry)
            rest_entry.add_child(entry)
        else:
            print(f'{g_warning_colour}WARNING: Could not find parent ({entry.get_parent_id()}) for {entry.get_name()} '
                  f'in file {entry.get_clean_filename()}.{g_end_colour}')


def _recursive_link_method_child_parents(method: DocEntry, parent: DocEntry) -> None:
    """ Recursively searches up the parent tree until a similar method is found or the top is reached.

    :param method: The method to link.
    :param parent: The parent to search.
    """
    for p_method in parent.get_methods():
        if method.get_name() == p_method.get_name():
            method.set_parent(p_method)
            p_method.add_child(method)
            return
    if new_parent := parent.get_parent():
        _recursive_link_method_child_parents(method, new_parent)


def link_method_child_parents(doc_entries: dict[str, DocEntry]) -> None:
    """ Loops through all the doc entries and links DocEntry methods to their parents. Needs to be run after linking
    classes to their parents.

    :param doc_entries: The list of doc entries to update.
    """
    for entry in doc_entries.values():
        if entry.get_type() != 'class':
            continue

        if parent := entry.get_parent():
            # Recursively search up the parent tree until a similar method is found or the top is reached
            for method in entry.get_methods():
                _recursive_link_method_child_parents(method, parent)


def update_inherited_methods(doc_entries: dict[str, DocEntry]) -> None:
    """ Loops through all the doc entries and updates the inherited methods. Needs to be run after linking methods to
    their parents.

    :param doc_entries: The list of doc entries to update.
    """
    for entry in doc_entries.values():
        if entry.get_type() != 'class':
            continue

        parent = entry
        method_list: list[str] = [e.get_name() for e in entry.get_methods()]
        while parent := parent.get_parent():
            for method in parent.get_methods():
                if method.get_name() not in method_list:
                    entry.add_inherited_method(method)
                    method_list.append(method.get_name())
# pylint: enable=unused-variable
