""" This module provides support for indexing a lua file."""

import re
# pylint: disable=unused-import, unused-variable
from multiprocessing.connection import Connection
# pylint: enable=unused-import, unused-variable
from lua_auto_doc.modules.highlighter import lua_type_indexer
from lua_auto_doc.modules.html_handler.fragment_reader import get_fragment_from_tag
from lua_auto_doc.modules.highlighter.indexer_support_functions import get_reserved_keywords_dict


# Regex patterns
g_number_pattern: re.Pattern = re.compile(r'''(?<=[\W0-9])(0x[a-fA-F\d]*|\d+\.?\d+|(?<!\.)\.\d+|\d+\.?)''', re.MULTILINE)
""" A pattern that matches all valid Lua numbers, Group 1 captures the entire number."""
g_start_of_line_pattern: re.Pattern = re.compile(r'''(^.*$)''', re.MULTILINE)
""" A pattern that matches an entire line, Group 1 captures the entire line."""
# Special keywords and tokens
g_unique_keyword_pattern: re.Pattern = re.compile(r'''(?<![a-zA-Z_])(#KEYWORD)(?!\w)''', re.MULTILINE)
""" A pattern that matches all unique keywords. #KEYWORD need to be replaced by the actual keywords.
Group 1 captures the keyword."""
g_dot_pattern: re.Pattern = re.compile(r'''(\.{2,3}|(?<!\d)\.(?!\d))''', re.MULTILINE)
""" A pattern that matches all dots that are not part of a number.
Group 1 captures the dots (Up to 3 dots per capture)."""


# Too big/much work to refactor for now
# pylint: disable=too-many-locals, too-many-branches, too-many-statements, unused-variable
def index_code(code: str, lua_version: float) -> dict[int, set[str]]:
    """ Indexes a string of code.

    :param code: The code to index.
    :param lua_version: The version of Lua to use.
    """
    # Initialise global variables
    reserved_lua_keywords_dict: dict[str, list[str]] = get_reserved_keywords_dict(lua_version)

    # Get indexes
    start_end_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code, g_start_of_line_pattern)
    string_indexes: list[dict[str, int]] = lua_type_indexer.get_string_indexes(code)  # Internal filtering with g_comments_and_documentation_non_capture_pattern
    number_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code, g_number_pattern,
                                                                                pattern_filter=True)
    keyword_indexes: list[dict[str, int]] = lua_type_indexer.get_keyword_indexes(code, reserved_lua_keywords_dict)  # Calls get_pattern_indexes() internally
    nil_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code,
                                                            re.compile(g_unique_keyword_pattern.pattern.replace(
                                                                 '#KEYWORD', 'nil'), re.MULTILINE),
                                                            pattern_filter=True)
    true_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code,
                                                             re.compile(g_unique_keyword_pattern.pattern.replace(
                                                                  '#KEYWORD', 'true'), re.MULTILINE),
                                                             pattern_filter=True)
    false_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code,
                                                              re.compile(g_unique_keyword_pattern.pattern.replace(
                                                                   '#KEYWORD', 'false'), re.MULTILINE),
                                                              pattern_filter=True)

    self_indexes: list[dict[str, int]] = lua_type_indexer.get_self_keyword_indexes(code)  # Internal filtering with g_compiled_filter_pattern
    token_indexes: list[dict[str, int]] = lua_type_indexer.get_token_indexes(code, reserved_lua_keywords_dict)  # Calls get_pattern_indexes() internally
    rainbow_token_indexes: list[dict[str, int]] = lua_type_indexer.get_rainbow_token_indexes(code,
                                                                                             reserved_lua_keywords_dict)  # Calls get_pattern_indexes() internally
    dot_indexes: list[dict[str, int]] = lua_type_indexer.get_pattern_indexes(code, g_dot_pattern, pattern_filter=True)

    comment_indexes, doc_type_indexes, doc_name_indexes, doc_param_name_indexes, doc_tag_indexes, \
        documentation_text_indexes,  doc_keyword_indexes, doc_optional_indexes \
        = lua_type_indexer.get_comments_and_documentation_indexes(code)  # Internal filtering with g_string_non_capture_pattern

    built_in_functions_indexes, metamethods_indexes, environment_variables_indexes \
        = lua_type_indexer.get_built_in_indexes(code, lua_version, reserved_lua_keywords_dict)  # Calls get_pattern_indexes() internally

    # Create a master list of comments and strings that overwrites every other tag
    overwrite_list: list[dict[str, int]] = []
    overwrite_list.extend(string_indexes)
    overwrite_list.extend(comment_indexes)
    overwrite_list.extend(doc_type_indexes)
    overwrite_list.extend(doc_name_indexes)
    overwrite_list.extend(doc_param_name_indexes)
    overwrite_list.extend(doc_tag_indexes)
    overwrite_list.extend(documentation_text_indexes)
    overwrite_list.extend(doc_keyword_indexes)
    overwrite_list.extend(doc_optional_indexes)

    # Index fields
    field_indexes: list[dict[str, int]] = lua_type_indexer.get_field_indexes(code)
    # Add field indexes to overwrite list
    overwrite_list.extend(field_indexes)

    # Remove overlapping number indexes
    _, number_indexes = lua_type_indexer.resolve_indexes(overwrite_list, number_indexes, first_list_priority=True)

    # Sort overwrite list by start index
    overwrite_list.sort(key=lambda x: x['start'])

    # Index functions and variables
    local_function_indexes, global_function_indexes, instance_method_indexes, static_method_indexes \
        = lua_type_indexer.get_function_indexes(code, overwrite_list, reserved_lua_keywords_dict)
    local_variable_indexes, param_variable_indexes, global_variable_indexes \
        = lua_type_indexer.get_all_variable_indexes(code, overwrite_list, reserved_lua_keywords_dict)

    # Remove param indexes clashing with dot indexes
    _, param_variable_indexes = lua_type_indexer.resolve_indexes(dot_indexes, param_variable_indexes,
                                                                 first_list_priority=True)
    # Remove duplicate indexes from keywords and tokens that are inside rainbow tokens/keywords
    _, token_indexes = lua_type_indexer.resolve_indexes(rainbow_token_indexes, token_indexes,
                                                        first_list_priority=True)
    _, keyword_indexes = lua_type_indexer.resolve_indexes(rainbow_token_indexes, keyword_indexes,
                                                          first_list_priority=True)

    # Split any multiline strings and comments into single line indexes
    string_indexes = lua_type_indexer.split_multiline_indexes(string_indexes, start_end_indexes)
    comment_indexes = lua_type_indexer.split_multiline_indexes(comment_indexes, start_end_indexes)

    # pylint: disable=use-list-literal
    complete_index: dict[int, set[str]] = {}
    # Add the line start/end indexes to the complete index
    for line_index in start_end_indexes:
        complete_index.setdefault(line_index['start'], list()).append('line-start')
        complete_index.setdefault(line_index['end'], list()).append('line-end')
    # Add the string indexes to the complete index
    for string_index in string_indexes:
        complete_index.setdefault(string_index['start'], list()).append('string-start')
        complete_index.setdefault(string_index['end'], list()).append('end')
    # Add the number indexes to the complete index
    for number_index in number_indexes:
        complete_index.setdefault(number_index['start'], list()).append('number-start')
        complete_index.setdefault(number_index['end'], list()).append('end')
    # Add the keyword indexes to the complete index
    for keyword_index in keyword_indexes:
        complete_index.setdefault(keyword_index['start'], list()).append('keyword-start')
        complete_index.setdefault(keyword_index['end'], list()).append('end')
    # Add the nil indexes to the complete index
    for nil_index in nil_indexes:
        complete_index.setdefault(nil_index['start'], list()).append('nil-start')
        complete_index.setdefault(nil_index['end'], list()).append('end')
    # Add the true indexes to the complete index
    for true_index in true_indexes:
        complete_index.setdefault(true_index['start'], list()).append('true-start')
        complete_index.setdefault(true_index['end'], list()).append('end')
    # Add the false indexes to the complete index
    for false_index in false_indexes:
        complete_index.setdefault(false_index['start'], list()).append('false-start')
        complete_index.setdefault(false_index['end'], list()).append('end')
    # Add the self indexes to the complete index
    for self_index in self_indexes:
        complete_index.setdefault(self_index['start'], list()).append('self-start')
        complete_index.setdefault(self_index['end'], list()).append('end')
    # Add the token indexes to the complete index
    for token_index in token_indexes:
        complete_index.setdefault(token_index['start'], list()).append('token-start')
        complete_index.setdefault(token_index['end'], list()).append('end')
    # Add the rainbow token indexes to the complete index
    for rainbow_token_index in rainbow_token_indexes:
        complete_index.setdefault(rainbow_token_index['start'], list()).append('rainbow-token-start')
        complete_index.setdefault(rainbow_token_index['end'], list()).append('end')
    # Add the dot indexes to the complete index
    for dot_index in dot_indexes:
        complete_index.setdefault(dot_index['start'], list()).append('dot-start')
        complete_index.setdefault(dot_index['end'], list()).append('end')
    # Add the comment indexes to the complete index
    for comment_index in comment_indexes:
        complete_index.setdefault(comment_index['start'], list()).append('comment-start')
        complete_index.setdefault(comment_index['end'], list()).append('end')
    # Add the documentation indexes to the complete index
    for doc_type_index in doc_type_indexes:
        complete_index.setdefault(doc_type_index['start'], list()).append('doc-type-start')
        complete_index.setdefault(doc_type_index['end'], list()).append('end')
    for doc_name__index in doc_name_indexes:
        complete_index.setdefault(doc_name__index['start'], list()).append('doc-name-start')
        complete_index.setdefault(doc_name__index['end'], list()).append('end')
    for doc_param_name_index in doc_param_name_indexes:
        complete_index.setdefault(doc_param_name_index['start'], list()).append('doc-param-name-start')
        complete_index.setdefault(doc_param_name_index['end'], list()).append('end')
    for doc_tag_index in doc_tag_indexes:
        complete_index.setdefault(doc_tag_index['start'], list()).append('doc-tag-start')
        complete_index.setdefault(doc_tag_index['end'], list()).append('end')
    for documentation_text_index in documentation_text_indexes:
        complete_index.setdefault(documentation_text_index['start'], list()).append('documentation-text-start')
        complete_index.setdefault(documentation_text_index['end'], list()).append('end')
    for doc_keyword_index in doc_keyword_indexes:
        complete_index.setdefault(doc_keyword_index['start'], list()).append('doc-keyword-start')
        complete_index.setdefault(doc_keyword_index['end'], list()).append('end')
    for doc_optional_index in doc_optional_indexes:
        complete_index.setdefault(doc_optional_index['start'], list()).append('doc-optional-start')
        complete_index.setdefault(doc_optional_index['end'], list()).append('end')
    # Add the built-in function indexes to the complete index
    for built_in_function_index in built_in_functions_indexes:
        complete_index.setdefault(built_in_function_index['start'], list()).append('built-in-function-start')
        complete_index.setdefault(built_in_function_index['end'], list()).append('end')
    # Add the metamethod indexes to the complete index
    for metamethod_index in metamethods_indexes:
        complete_index.setdefault(metamethod_index['start'], list()).append('metamethod-start')
        complete_index.setdefault(metamethod_index['end'], list()).append('end')
    # Add the environment variable indexes to the complete index
    for environment_variable_index in environment_variables_indexes:
        complete_index.setdefault(environment_variable_index['start'], list()).append('environment-variable-start')
        complete_index.setdefault(environment_variable_index['end'], list()).append('end')
    # Add the field indexes to the complete index
    for field_index in field_indexes:
        complete_index.setdefault(field_index['start'], list()).append('field-start')
        complete_index.setdefault(field_index['end'], list()).append('end')
    # Add the local function indexes to the complete index
    for local_function_index in local_function_indexes:
        complete_index.setdefault(local_function_index['start'], list()).append('local-function-start')
        complete_index.setdefault(local_function_index['end'], list()).append('end')
    # Add the global function indexes to the complete index
    for global_function_index in global_function_indexes:
        complete_index.setdefault(global_function_index['start'], list()).append('global-function-start')
        complete_index.setdefault(global_function_index['end'], list()).append('end')
    # Add the instance method indexes to the complete index
    for instance_method_index in instance_method_indexes:
        complete_index.setdefault(instance_method_index['start'], list()).append('instance-method-start')
        complete_index.setdefault(instance_method_index['end'], list()).append('end')
    # Add the static method indexes to the complete index
    for static_method_index in static_method_indexes:
        complete_index.setdefault(static_method_index['start'], list()).append('static-method-start')
        complete_index.setdefault(static_method_index['end'], list()).append('end')
    # Add the local variable indexes to the complete index
    for local_var_index in local_variable_indexes:
        complete_index.setdefault(local_var_index['start'], list()).append('local-var-start')
        complete_index.setdefault(local_var_index['end'], list()).append('end')
    # Add the parameter variable indexes to the complete index
    for param_var_index in param_variable_indexes:
        complete_index.setdefault(param_var_index['start'], list()).append('param-var-start')
        complete_index.setdefault(param_var_index['end'], list()).append('end')
    # Add the global variable indexes to the complete index
    for global_var_index in global_variable_indexes:
        complete_index.setdefault(global_var_index['start'], list()).append('global-var-start')
        complete_index.setdefault(global_var_index['end'], list()).append('end')
    # pylint: enable=use-list-literal

    # Sort the complete index by the index number
    complete_index = dict(sorted(complete_index.items(), key=lambda item: item[0]))

    return complete_index
# pylint: enable=too-many-locals, too-many-branches, too-many-statements


# pylint: disable=too-many-return-statements
def _resolve_rainbow_keyword(keyword: str, rainbow_keyword_queue: list[str], rainbow_loop: int) -> tuple[str, int]:
    """ Function that keeps track of rainbow characters and the amount of nesting.

    :param keyword: The keyword to check
    :param rainbow_keyword_queue: The list of current open rainbow characters
    :param rainbow_loop: The current level of nesting

    :return: The resolved keyword and the new level of nesting
    """
    rainbow_starts: list[str] = [
        '(',
        '{',
        '[',
        'if',
        'elseif',
        'else',
        'for',
        'while',
        'do',
        'repeat',
    ]
    rainbow_ends: list[str] = [
        'end',
        ')',
        '}',
        ']',
        'until',
    ]

    do_predecessors: list[str] = ['for', 'while']
    then_predecessors: list[str] = ['if', 'elseif']
    end_predecessors: list[str] = ['do', 'then', 'if', 'elseif', 'else', 'for', 'while']

    # Check if keyword should not create a new rainbow nest
    if keyword == 'do' and len(rainbow_keyword_queue) and rainbow_keyword_queue[-1] in do_predecessors:
        return f'rainbow_{rainbow_loop % 5}', rainbow_loop
    if keyword == 'then' and rainbow_keyword_queue[-1] in then_predecessors:
        return f'rainbow_{rainbow_loop % 5}', rainbow_loop
    if keyword == 'elseif':
        rainbow_keyword_queue.append('elseif')
        return f'rainbow_{rainbow_loop % 5}', rainbow_loop
    if keyword == 'else':
        return f'rainbow_{rainbow_loop % 5}', rainbow_loop
    if keyword == 'end' and len(rainbow_keyword_queue) == 0 \
            or keyword == 'end' and rainbow_keyword_queue[-1] not in end_predecessors:
        return 'keyword', rainbow_loop
    if keyword == 'function':
        rainbow_keyword_queue.append('function')
        return 'keyword', rainbow_loop
    # Check if keyword should create a new rainbow nest
    if keyword in rainbow_starts:
        rainbow_keyword_queue.append(keyword)
        rainbow_loop += 1
        return f'rainbow_{rainbow_loop % 5}', rainbow_loop
    # Check if keyword should close a rainbow nest
    if keyword in rainbow_ends:
        # Track back to pop the root "if", if the first entry in the queue is "elseif"
        while len(rainbow_keyword_queue) and rainbow_keyword_queue[-1] == 'elseif':
            rainbow_keyword_queue.pop()

        rainbow_keyword_queue.pop()
        class_name = f'rainbow_{rainbow_loop % 5}'
        rainbow_loop -= 1
        return class_name, rainbow_loop

    # If keyword not caught by any if statements, raise an error
    raise ValueError(f'Keyword {keyword} is not a valid rainbow keyword.')
# pylint: enable=too-many-locals, too-many-branches, too-many-statements, unused-variable


# Too big/much work to refactor for now
# pylint: disable=too-many-locals, too-many-statements, unused-variable
def indexed_code_to_html(source_code: str, indexed_code: dict[int, set[str]], default_linenum=True) -> str:
    """ Converts an index dict into formatted html code fragment.

    :param source_code: The source code to convert to html.
    :param indexed_code: The index to use for formatting the source code.
    :param default_linenum: Whether to include default line numbers.
    :type default_linenum: bool

    :return: The html code fragment.
    """
    # Get list of all keys in the index
    index_keys: list[int] = list(indexed_code.keys())
    index_counter: int = 0
    # Init string variables
    html_code: str = ''
    start_fragment: str = '''<li class="li-code-field-line-entry #ROWTYPE" id="#LINENUMBER"><code class="code-text">'''
    end_fragment: str = '''</code></li>'''
    span_start: str = '<span class="#CLASSNAME">'
    span_end: str = '</span>'
    css_class_link: dict[str, str] = {
        'string': 'code-string',
        'number': 'code-number',
        'keyword': 'code-keyword',
        'nil': 'code-nil',
        'true': 'code-true',
        'false': 'code-false',
        'self': 'code-self',
        'token': 'code-token',
        'rainbow_0': 'code-rainbow-1',
        'rainbow_1': 'code-rainbow-2',
        'rainbow_2': 'code-rainbow-3',
        'rainbow_3': 'code-rainbow-4',
        'rainbow_4': 'code-rainbow-5',
        'dot': 'code-dot',
        'comment': 'code-comment',
        'doc_type': 'code-doc-type',
        'doc_name': 'code-doc-name',
        'doc_param_name': 'code-doc-param-name',
        'doc_tag': 'code-doc-tag',
        'doc_text': 'code-doc-text',
        'doc_keyword': 'code-doc-keyword',
        'doc_optional': 'code-doc-optional',
        'built-in': 'code-built-in',
        'metamethods': 'code-metamethods',
        'environment': 'code-environment-var',
        'global_var': 'code-global-var',
        'instance_method': 'code-instance-method',
        'static_method': 'code-static-method',
        'local_var': 'code-local-var',
        'parameter': 'code-param-var',
        'global_function': 'code-global-function',
        'local_function': 'code-local-function',
        'fields': 'code-fields',
    }

    # Loop through the indexed code and create the html code fragment
    line_counter: int = 1
    # Rainbow loop trackers
    rainbow_loop: int = -1  # _resolve_rainbow_keyword() increments this value by 1 before calculating the class name
    rainbow_keyword_queue: list[str] = []
    for string_index, value in indexed_code.items():
        # The strings starting and ending html code lines
        line_start: str = ''
        line_end: str = ''
        line_start_flag: bool = False
        line_end_flag: bool = False
        # The strings starting and ending span tags
        line_entry_start: str = ''
        line_entry_end: str = ''
        for word in value:
            match word:
                case 'end':
                    line_entry_end += span_end
                case 'line-start':
                    line_start_flag = True
                case 'line-end':
                    line_end_flag = True
                case 'string-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['string'])
                case 'number-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['number'])
                case 'keyword-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['keyword'])
                case 'nil-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['nil'])
                case 'true-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['true'])
                case 'false-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['false'])
                case 'self-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['self'])
                case 'token-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['token'])
                case 'rainbow-token-start':
                    class_name, rainbow_loop = _resolve_rainbow_keyword(
                        source_code[string_index:index_keys[index_counter + 1]],
                        rainbow_keyword_queue,
                        rainbow_loop
                    )
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link[class_name])
                case 'dot-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['dot'])
                case 'comment-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['comment'])
                case 'doc-type-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_type'])
                case 'doc-name-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_name'])
                case 'doc-param-name-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_param_name'])
                case 'doc-tag-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_tag'])
                case 'documentation-text-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_text'])
                case 'doc-keyword-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_keyword'])
                case 'doc-optional-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['doc_optional'])
                case 'built-in-function-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['built-in'])
                case 'metamethod-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['metamethods'])
                case 'environment-variable-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['environment'])
                case 'global-var-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['global_var'])
                case 'local-var-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['local_var'])
                case 'param-var-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['parameter'])
                case 'field-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['fields'])
                case 'global-function-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['global_function'])
                case 'local-function-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['local_function'])
                case 'instance-method-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['instance_method'])
                case 'static-method-start':
                    line_entry_start += span_start.replace('#CLASSNAME', css_class_link['static_method'])
                case _:
                    print('################# ERROR (INDEX-0 #################\n'
                          'Please report this error to the developer.\n')

        if line_start_flag:
            row_type: str = f'row-{line_counter % 2}'
            line_start = start_fragment.replace('#ROWTYPE', row_type).replace('#LINENUMBER', f'line_{line_counter}')
            line_counter += 1

        if line_end_flag:
            line_end = end_fragment

        # Get the next index
        source_code_index: int
        index_counter += 1
        if index_counter < len(index_keys):
            source_code_index = index_keys[index_counter]
        else:
            source_code_index = len(source_code)

        html_code += line_entry_end + line_start + line_entry_start \
            + source_code[string_index:source_code_index].replace('<', '&lt;') + line_end

    if default_linenum:
        return f'<ol id="ol-linenum">{html_code}</ol>'
    return html_code
# pylint: enable=too-many-locals, too-many-statements, unused-variable


# pylint: disable=unused-variable
def index_fallback(source_code: str, html_template: str) -> tuple[str, str]:
    """ Fallback method if the source code could not be indexed. Can't be indexed with
    index_code()/indexed_code_to_html(). Relies on https://highlightjs.org and JSDeliver to colourise the code.

    :param source_code: The source code to colourise.
    :param html_template: The html template to edit:

    :return: The html code fragment.
    """
    source_code = source_code.replace('<', '&lt;')
    html_code = f'<code class="language-lua">{source_code}</code>'
    html_template = html_template.replace('#LuaAutoDoc-HighlightFallback', get_fragment_from_tag('HighlightFallback'))

    return html_code, html_template
# pylint: enable=unused-variable
