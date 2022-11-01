import re
from tabulate import tabulate
from termcolor import cprint

from .random_colors import color_list_generator


class FormGenerator():
    def __init__(self, title, type, *args):
        self.title = title
        self.type = type
        self.adjusted_width = 59
        self.font_color_printer(self.title)
        if self.type in ["d", "D"]:
            self.definition_generator(args[0])
        elif self.type in ["e", "E"]:
            try:
                self.expression_generator(args[0], args[1])
            except IndexError:
                cprint("Please confirm that a second list has been entered.",
                       self.previous_color, attrs=['blink', 'reverse'])
        elif self.type in ["s", "S"]:
            self.statement_generator(args[0])
        elif self.type in ["v", "V"]:
            try:
                self.variable_generator(args[0], args[1])
            except IndexError:
                cprint("Please confirm that a second list has been entered.",
                       self.previous_color, attrs=['blink', 'reverse'])
        else:
            cprint("Please check that the selection of the form type is correct.",
                   self.previous_color, attrs=['blink', 'reverse'])

    def font_color_printer(self, string):
        global font_colors_list
        try:
            font_colors_list
        except NameError:
            font_colors_list = color_list_generator()
        if font_colors_list == []:
            font_colors_list = color_list_generator()
        self.previous_color = font_colors_list.pop(0)
        cprint(string, self.previous_color, attrs=['underline'], end='\n\n')

    def expression_generator(self, expressions, results):
        table = [["Expression", "Result"]]
        max_length = len(max(expressions, key=len))
        if len("Expression") >= max_length:
            length_expression = len("Expression")
        else:
            length_expression = max_length
        remainder = self.adjusted_width - length_expression - 3
        for expression, result in zip(expressions, results):
            if len(result) > remainder:
                if re.search(r'\n', str(result)):
                    start = 0
                    printable_result = ""
                    string_list = []
                    for match in re.finditer(r'\n', str(result)):
                        nested_string = str(result)[start:match.span()[0]]
                        string_list.append(nested_string)
                        start = match.span()[1]
                    string_list.append(str(result)[start:])
                    for nested_string in string_list:
                        if len(nested_string) > remainder:
                            printable_string = ""
                            printable_line = nested_string
                            while len(nested_string) > remainder:
                                while printable_line.rfind(' ') > remainder:
                                    printable_line = printable_line[:printable_line
                                                                    .rfind(' ')]
                                else:
                                    printable_line = printable_line[:printable_line
                                                                    .rfind(' ')]
                                printable_string += printable_line + "\n"
                                nested_string = nested_string[len(printable_line) +
                                                              1:]
                                printable_line = nested_string
                            else:
                                printable_string += printable_line
                                printable_result += printable_string + "\n"
                        else:
                            printable_result += nested_string + "\n"
                    table.append([expression, printable_result.strip("\n")])
                else:
                    printable_result = ""
                    printable_line = result
                    while len(result) > remainder:
                        while printable_line.rfind(' ') > remainder:
                            printable_line = printable_line[:printable_line.
                                                            rfind(' ')]
                        else:
                            printable_line = printable_line[:printable_line.
                                                            rfind(' ')]
                        printable_result += printable_line + "\n"
                        result = result[len(printable_line) + 1:]
                        printable_line = result
                    else:
                        printable_result += printable_line
                        table.append([expression, printable_result])
            else:
                table.append([expression, result])
        table_list = tabulate(table,
                              headers='firstrow',
                              tablefmt='pretty',
                              colalign=("left", "left")).split('\n')
        for line in table_list:
            cprint('\t'.expandtabs(4) + line,
                   self.previous_color, attrs=['bold'])

    def definition_generator(self, definitions):
        table = [["Definition"]]
        for definition in definitions:
            printable_definition = ""
            for line in definition.strip().split("\n"):
                if len(line) > self.adjusted_width:
                    printable_lines = ""
                    printable_line = line
                    while len(line) > self.adjusted_width:
                        while printable_line.rfind(' ') > self.adjusted_width:
                            printable_line = printable_line[:printable_line.rfind(
                                ' ')]
                        else:
                            printable_line = printable_line[:printable_line.rfind(
                                ' ')]
                        printable_lines += printable_line + \
                            "\n\t".expandtabs(8)
                        line = line[len(printable_line) + 1:]
                        printable_line = line
                    else:
                        printable_lines += printable_line
                        printable_definition += printable_lines + "\n"
                else:
                    printable_definition += line + "\n"
            table.append([printable_definition.strip("\n")])
        table_list = tabulate(table,
                              headers='firstrow',
                              tablefmt='pretty',
                              colalign=('left', )).split('\n')
        for line in table_list:
            cprint('\t'.expandtabs(4) + line,
                   self.previous_color, attrs=['bold'])

    def statement_generator(self, statements):
        table = [["Statement"]]
        for statement in statements:
            if len(statement) > self.adjusted_width:
                printable_statement = ""
                printable_line = statement
                while len(statement) > self.adjusted_width:
                    while printable_line.rfind(' ') > self.adjusted_width:
                        printable_line = printable_line[:printable_line.rfind(
                            ' ')]
                    else:
                        printable_line = printable_line[:printable_line.rfind(
                            ' ')]
                    printable_statement += printable_line + "\n"
                    statement = statement[len(printable_line) + 1:]
                    printable_line = statement
                else:
                    printable_statement += printable_line
                    table.append([printable_statement])
            else:
                table.append([statement])
        table_list = tabulate(table,
                              headers='firstrow',
                              tablefmt='pretty',
                              colalign=('left', )).split('\n')
        for line in table_list:
            cprint('\t'.expandtabs(4) + line,
                   self.previous_color, attrs=['bold'])

    def variable_generator(self, variables, values):
        table = [["Variable", "Value"]]
        max_length = len(max(variables, key=len))
        if len("Variable") >= max_length:
            length_variable = len("Variable")
        else:
            length_variable = max_length
        remainder = self.adjusted_width - length_variable - 3
        for variable, value in zip(variables, values):
            if len(value) > remainder:
                if re.search(r'\n', str(value)):
                    start = 0
                    printable_value = ""
                    string_list = []
                    for match in re.finditer(r'\n', str(value)):
                        nested_string = str(value)[start:match.span()[0]]
                        string_list.append(nested_string)
                        start = match.span()[1]
                    string_list.append(str(value)[start:])
                    for nested_string in string_list:
                        if len(nested_string) > remainder:
                            printable_string = ""
                            printable_line = nested_string
                            while len(nested_string) > remainder:
                                while printable_line.rfind(' ') > remainder:
                                    printable_line = printable_line[:printable_line
                                                                    .rfind(' ')]
                                else:
                                    printable_line = printable_line[:printable_line
                                                                    .rfind(' ')]
                                printable_string += printable_line + "\n"
                                nested_string = nested_string[len(printable_line) +
                                                              1:]
                                printable_line = nested_string
                            else:
                                printable_string += printable_line
                                printable_value += printable_string + "\n"
                        else:
                            printable_value += nested_string + "\n"
                    table.append([variable, printable_value.strip("\n")])
                else:
                    printable_value = ""
                    printable_line = value
                    while len(value) > remainder:
                        while printable_line.rfind(' ') > remainder:
                            printable_line = printable_line[:printable_line.
                                                            rfind(' ')]
                        else:
                            printable_line = printable_line[:printable_line.
                                                            rfind(' ')]
                        printable_value += printable_line + "\n"
                        value = value[len(printable_line) + 1:]
                        printable_line = value
                    else:
                        printable_value += printable_line
                        table.append([variable, printable_value])
            else:
                table.append([variable, value])
        table_list = tabulate(table,
                              headers='firstrow',
                              tablefmt='pretty',
                              colalign=("left", "left")).split('\n')
        for line in table_list:
            cprint('\t'.expandtabs(4) + line,
                   self.previous_color, attrs=['bold'])
