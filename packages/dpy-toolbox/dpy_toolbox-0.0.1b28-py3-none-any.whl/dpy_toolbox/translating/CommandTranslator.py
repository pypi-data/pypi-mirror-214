from typing import Any
from discord import app_commands
from discord.ext import commands
from ..core.default import get_multiattr

__all__ = (
    "CommandTranslator",
    "translate_command",
    "default_language",
    "translate_polyglot",
    "translate_params_description",
    "translate_params_name",
    "translate_command_description"
)

class CommandTranslator(app_commands.Translator):
    """
    A Translator that will translate the command using this submodule's decorators

    """
    RELEVANT = {
        "TranslationContextLocation.command_name": "__translating",
        "TranslationContextLocation.command_description": "__translating_desc",
        "TranslationContextLocation.parameter_name": "_Parameter__parent.__translating_name",
        "TranslationContextLocation.parameter_description":  "_Parameter__parent.__translating_desc"
    }

    def __init__(self, default=None):
        self.default = default
        super().__init__()

    def get_default(self, ctx):
        if isinstance(ctx.data, app_commands.Parameter):
            return getattr(ctx.data._Parameter__parent, "__translating_default", None)
        else:
            return getattr(ctx.data, "__translating_default", None)

    # string: what to translate (might be arg, command, description, ...)
    # locale: the string of the local (in the language that should be translated)
    # context: discord.app_commands.translator.TranslationContext
    async def translate(self, string: str, locale: str, context):
        s = str(string)
        search_for_param = self.RELEVANT.get(str(context.location), "")
        default = self.get_default(context) or self.default
        trans_to_lang = locale[1]
        translation = get_multiattr(context.data, *search_for_param.split("."), default={})
        if not translation:
            return translation.get(default, s)
        for lang, trans in translation.items():
            if trans_to_lang.startswith(lang):
                return trans
        return translation.get(default, s)


def default_language(lang: str) -> Any:
    """
    Set a default language for a command. If not given the HelpCommand's default will be used.

    :param lang: The default language of your command
    :return: The translated command
    """
    def decorator(command: commands.Command):
        command.__translating_default = lang
        for param in command._params.values():
            param.__translating_default = lang
        return command
    return decorator


def translate_params_description(lang, **kwargs: str) -> Any:
    """
    Translate a parameter's description into one language

    :param lang: The language you want to translate the params for
    :param kwargs: key being the parameter's name; value being the new description
    :return: The translated command
    """
    def decorator(command: commands.Command):
        for k, v in kwargs.items():
            parameter = command._params.get(k, None)
            if not parameter:
                continue
            if getattr(parameter, "__translating_desc", None) is None:
                parameter.__translating_desc = {}
            parameter.__translating_desc[lang] = v
            command._params[k] = parameter
        return command
    return decorator


def translate_params_name(lang, **kwargs: str) -> Any:
    """
    Translate a parameter's name into one language

    :param lang: The language you want to translate the params for
    :param kwargs: key being the parameter's name; value being the new name
    :return: The translated command
    """
    def decorator(command: commands.Command):
        for k, v in kwargs.items():
            parameter = command._params.get(k, None)
            if not parameter:
                continue
            if getattr(parameter, "__translating_name", None) is None:
                parameter.__translating_name = {}
            parameter.__translating_name[lang] = v
            command._params[k] = parameter
        return command
    return decorator


def translate_command(lang, name) -> Any:
    """
    Translate a command's name into one languages (use translate_polyglot for multiple)

    :param lang: The language
    :param name: The translation of the command in the given language
    :return: The translated command
    """
    def decorator(command: commands.Command):
        if getattr(command, '__translating', None) is None:
            command.__translating = {}
        command.__translating[lang] = name
        return command
    return decorator


def translate_command_description(lang, *description: str) -> Any:
    """
    Translate a command's description into one languages (use translate_polyglot_description for multiple)

    :param lang: The language you want to translate to
    :param description: The translated description
    :return: The translated command
    """
    def decorator(command: commands.Command):
        if getattr(command, '__translating_desc', None) is None:
            command.__translating_desc = {}
        command.__translating_desc[lang] = " ".join(description)
        return command
    return decorator


def translate_polyglot_description(**kwargs) -> Any:
    """
    Translate a command's description into multiple languages

    :param kwargs: key being the language; value being the translation
    :return: The translated command
    """

    def decorator(command: commands.Command):
        if getattr(command, '__translating_desc', None) is None:
            command.__translating_desc = {}
        for k, v in kwargs.items():
            command.__translating_desc[k] = v
        return command

    return decorator

def translate_polyglot(**kwargs) -> Any:
    """
    Translate a command's name into multiple languages

    :param kwargs: key being the language; value being the translation
    :return: The translated command
    """
    def decorator(command: commands.Command):
        if getattr(command, '__translating', None) is None:
            command.__translating = {}
        for k, v in kwargs.items():
            command.__translating[k] = v
        return command
    return decorator
