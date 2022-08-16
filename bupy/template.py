# Exception handling derived from
# https://github.com/cidrblock/td4a/blob/master/td4a/models/exception_handler.py
# MIT License
# Copyright (c) 2017 Bradley A. Thornton

from jinja2 import meta, Environment, Template, StrictUndefined, Undefined
import ruamel.yaml as yaml
from typer import Exit
import re
import sys
import traceback


class TemplateException(Exception):
    def __init__(self, value) -> None:
        self.value = value
        super().__init__(self)

    def __str__(self):
        return repr(self.value)


class TemplateExceptionHandler(object):
    """
    Handle YAML and Jinja2 exceptions
    """

    def __init__(self, function):
        self.function = function
        self.error = (
            self.template_file
        ) = self.tback = self.exc_type = self.exc_value = self.exc_traceback = None
        self.error_map = {
            "ruamel.yaml.parser.ParserError": self.parser_error,
            "ruamel.yaml.constructor.ConstructorError": self.constructor_error,
            "ruamel.yaml.constructor.DuplicateKeyError": self.duplicate_key_error,
            "ruamel.yaml.scanner.ScannerError": self.scanner_error,
            "jinja2.exceptions": self.jinja_error,
        }

    def __call__(self, *args):
        try:
            return self.function(*args)
        except Exception as error:
            self.error = error
            self.exc_type, self.exc_value, self.exc_traceback = sys.exc_info()
            self.tback = traceback.extract_tb(self.exc_traceback)

            error_module = getattr(error, "__module__", None)
            if error_module:
                full_error = "%s.%s" % (error.__module__, self.exc_type.__name__)
            else:
                full_error = self.exc_type.__name__
            handler = self.error_map.get(full_error, self.error_map.get(error_module, self.unhandled))
            self.template_file = args[0]
            message = handler()
            raise TemplateException(message)

    def error_response(self, message, line_number):
        if line_number:
            error_payload = f"Issue processing {self.template_file}:{line_number} with the error message of: {message}"
        else:
            error_payload = (
                f"Issue processing {self.template_file} with the error message of: {message}"
            )
        return error_payload

    def constructor_error(self):
        line_number = self.error.problem_mark.line + 1
        message = next(x for x in str(self.error).splitlines() if x.startswith("found"))
        return self.error_response(message=message, line_number=line_number)

    def duplicate_key_error(self):
        line_number = self.error.problem_mark.line + 1
        message = next(x for x in str(self.error).splitlines() if x.startswith("found")).split(
            "with"
        )[0]
        return self.error_response(message=message, line_number=line_number)

    def jinja_error(self):
        message = str(self.error).replace("'ruamel.yaml.comments.CommentedMap object'", "Object")
        line_numbers = [x for x in self.tback if re.search("^<.*>$", x[0])]
        if line_numbers:
            line_number = line_numbers[0][1]
        else:
            line_number = "unknown"
        return self.error_response(message=message, line_number=line_number)

    def parser_error(self):
        line_number = self.error.problem_mark.line + 1
        messages = [x for x in str(self.error).splitlines() if x.startswith("expected")]
        if messages:
            message = messages[0]
        else:
            message = str(self.error)
        return self.error_response(message=message, line_number=line_number)

    def scanner_error(self):
        line_number = self.error.problem_mark.line + 1
        message = str(self.error).splitlines()[0]
        return self.error_response(message=message, line_number=line_number)

    def unhandled(self):
        print(self.exc_type, self.exc_value, self.exc_traceback, self.tback, self.error)
        line_numbers = [x for x in self.tback if re.search("^<.*>$", x[0])]
        if line_numbers:
            line_number = line_numbers[0][1]
        else:
            line_number = None
        message = self.error
        return self.error_response(message=message, line_number=line_number)


@TemplateExceptionHandler
def read_template_vars(file_path: str) -> dict:
    """
    Reads in template vars from a file
    """
    try:
        with open(file_path, "rb") as f:
            template_vars = yaml.load(f, yaml.SafeLoader)
        return template_vars
    except TemplateException as err:
        print(err)


@TemplateExceptionHandler
def verify_template(file_path: str) -> bool:
    """
    Verifies if the loaded file is a valid Jinja2 template
    """
    env = Environment()
    try:
        with open(file_path, "r") as f:
            env.parse(f.read())
        return True
    except TemplateException as err:
        print(err)
        return False


@TemplateExceptionHandler
def rendered_template(file_path: str, template_vars: dict) -> bytes:
    """
    Renders a Jinja2 template from a file
    """
    try:
        with open(file_path, "r") as f:
            rendered_template = Template(f.read()).render(template_vars)
        return rendered_template.encode("utf-8")
    except TemplateException as err:
        print(err)
