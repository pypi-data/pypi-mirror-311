# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject -- Prompt implementation
# :Created:   gio 21 apr 2016 18:49:11 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2018, 2024 Lele Gaifax
#

from re import compile

from questionary import ValidationError
from questionary import Validator
from questionary import prompt

from . import Step


class DualValidator(Validator):
    def __init__(self, regexp, regexp_error, validate_expression, validate_error):
        if regexp is None:
            self.regexp = self.regexp_error = None
        else:
            self.regexp = compile(regexp)
            if not regexp_error:
                regexp_error = 'Invalid input, does not match required regexp “%s”'
            if '%s' in regexp_error:
                regexp_error %= regexp
            self.regexp_error = regexp_error
        if validate_expression is None:
            self.validate_function = self.validate_error = None
        else:
            self.validate_function = eval(f'lambda value: {validate_expression}')
            self.validate_error = validate_error or 'Invalid input'

    def validate(self, document):
        if self.regexp is not None:
            if not self.regexp.fullmatch(document.text):
                raise ValidationError(cursor_position=len(document.text),
                                      message=self.regexp_error)
        if self.validate_function is not None:
            if not self.validate_function(document.text):
                raise ValidationError(cursor_position=len(document.text),
                                      message=self.validate_error)


class Prompt(Step):
    def __init__(self, state, config):
        super().__init__(state, config)

        questions = self.questions = []

        if isinstance(config, list):
            # Pre 2.0 format, when the configuration is a list of dictionaries
            # like:
            #
            #  - prompt:
            #      - name_of_the_variable:
            #          message: Tell me the value
            #          default: "default value"
            #
            #      - different_kind_of_input:
            #          message: Select the variant
            #          kind: list
            #          choices:
            #            - Big
            #            - Medium
            #            - Small
            #
            # Let's convert that to the new format, that is:
            #
            #  - prompt:
            #      name_of_the_variable:
            #          message: Tell me the value
            #          default: "default value"
            #
            #      different_kind_of_input:
            #          message: Select the variant
            #          kind: list
            #          choices:
            #            - Big
            #            - Medium
            #            - Small

            new_config = {}
            for question in config:
                items = question.items()
                if len(items) != 1:
                    raise ValueError(f'Bad question config, expected a dictionary with a'
                                     f' single key, got one with {len(items)}: {", ".join(items)}')
                for name, details in items:
                    if name in new_config:
                        raise ValueError(f'Bad prompt config, there is already a question'
                                         f' named {name!r}')
                    new_config[name] = details
            config = new_config
        elif not isinstance(config, dict):
            raise TypeError(f'Bad prompt config, expected either a list of questions'
                            f' or a dictionary, got {type(config)} instead')

        for name, details in config.items():
            if not isinstance(details, dict):
                raise TypeError(f'Bad question config for {name!r}, expected a dictionary,'
                                f' got {type(details)} instead')
            # Make a copy
            prompt = dict(details)
            prompt['name'] = name
            prompt['message'] = prompt['message'] if 'message' in prompt else name.capitalize()
            prompt['message'] += f' ({name})'
            kind = prompt.pop('kind', 'text')
            prompt['type'] = kind
            if 'filter' in prompt:
                prompt['filter'] = eval(f"lambda value: {prompt.pop('filter')}")
            if 'validate' in prompt or 'regexp' in prompt:
                vexpr = prompt.pop('validate', None)
                verror = prompt.pop('validate_error', None)
                rx = prompt.pop('regexp', None)
                rxerror = prompt.pop('regexp_error', None)
                prompt['validate'] = DualValidator(rx, rxerror, vexpr, verror)
            if 'when' in prompt:
                when = prompt.pop('when')
                prompt['when'] = lambda answers, when=when: state.check(when, **answers)
            questions.append(prompt)

    def announce(self):
        pass

    def __call__(self, defaults, prompt_only=False, no_prompt=False):
        if no_prompt:
            return

        result = prompt(self.questions, answers=defaults)
        if not result:
            # questionary.prompt catches KeyboardInterrupt and returns an empty dictionary
            raise KeyboardInterrupt
        return result
