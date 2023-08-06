from typing import Any, Union, Type, Iterable, Callable, Coroutine
from ..core import tokenize, Tokenizer, MISSING
import discord
import inspect


class QuestioningModal(discord.ui.Modal):
    """
    Ask multiple questions at the same time

    :param title: The title of the modal
    :param questions: If not kwargs: All questions that the modal will include
    :param lengths: The questions' max lengths
    :param requireds: Wether a question is required or not
    :param styles: The questions' styles
    :param callback: The on_submit callback
    :param timeout: The max amount of time the modal will remain open
    :param submit_message: The message the user receives when they submit their modal
    :param error_message: The message the user receives when an exception occurs
    :param custom_id: The custom id of the modal
    :param kwargs: All questions that the modal will include
    """

    def __init__(
            self,
            title: str,
            questions: Iterable[str] = MISSING,
            lengths: dict[Union[int, str], int] = MISSING,
            requireds: dict[Union[int, str], bool] = MISSING,
            styles: dict[Union[int, str], discord.TextStyle] = MISSING,
            callback: Callable = None,
            timeout: float = None,
            submit_message: str = "Your modal has been submit and is being processed {user}!",
            error_message: str = "Exception in `QuestioningModal`. Please contact Wever#3255\n{exception}",
            custom_id: str = None,
            **kwargs: str
    ):
        super().__init__(**dict(list(filter(lambda item: item[1], {"title": title, "timeout": timeout, "custom_id": custom_id}.items()))))
        self.callback = callback
        self.submit_message = submit_message
        self.error_message = error_message
        self.questions = kwargs or {i: v for i, v in enumerate(questions)}
        for k, q in self.questions.items():
            length, required, style = (
                lengths.get(k, 300),
                requireds.get(k, True),
                styles.get(q, discord.TextStyle.long)
            )
            inp = discord.ui.TextInput(
                label=q,
                style=style,
                required=required,
                max_length=length,
            )
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction) -> Any:
        if not self.callback:
            return await interaction.response.send_message(tokenize(self.submit_message, **Tokenizer(user=interaction.user)), ephemeral=True)
        return await self.callback(self, interaction)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(tokenize(self.error_message, **Tokenizer(error=error, exception=error)), ephemeral=True)

    @property
    def result(self):
        """
        The modal's result

        :rtype: dict
        :return: The question and its corresponding value
        """
        return {x.label: x.value for x in self.children}

    @property
    def values(self):
        """
        The modal's result

        :rtype: tuple
        :return: All values entered by the user
        """
        return tuple(self.result.values())

class SingleQuestion(discord.ui.Modal):
    """
    Ask a single question

    :param question: The question
                Will replace the questions title if no title is given
    :param max_length: The max length of the answer
    :param style: The style of the field
    :param callback: The on_submit function
    :param title: The title of the question
                If given the question will not be title but the prompts label
    :param submit_message: The on_submit function
    :param interaction_check: The interaction_check function

    """
    def __init__(
            self,
            question: str = "",
            max_length: int = 30,
            style: discord.TextStyle = discord.TextStyle.short,
            callback: Callable = None,
            title: str = None,
            submit_message: str = None,
            interaction_check: Union[Callable[[discord.Interaction], Coroutine[bool]], Callable[[discord.Interaction], bool], None] = None
    ):
        # tokenize("Your modal has been submit and is being processed!", **Tokenizer(user=interaction.user))
        self.submit_message = submit_message or "Your modal has been submit and is being processed!"
        self.interaction_check_func = interaction_check
        self.callback = callback
        super().__init__(title=question if not title else title)
        self.add_item(
            discord.ui.TextInput(
                label="Answer: "if not title else question,
                style=style,
                required=True,
                max_length=max_length
            )
        )

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if self.interaction_check_func:
            if inspect.iscoroutinefunction(self.interaction_check_func):
                return await self.interaction_check_func(interaction)
            return self.interaction_check_func(interaction)
        return True

    async def on_submit(self, interaction: discord.Interaction) -> Any:
        if not self.callback:
            return await interaction.response.send_message(self.submit_message, ephemeral=True)
        return await self.callback(self, interaction)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message("Exception in `SingleQuestion`", ephemeral=True)

    @property
    def result(self):
        """
        The result of the question

        :rtype: str
        :return: The result
        """
        return self.children[0].value

    @property
    def value(self):
        """
        .result alias

        :rtype: str
        :return: The result
        """
        return self.result