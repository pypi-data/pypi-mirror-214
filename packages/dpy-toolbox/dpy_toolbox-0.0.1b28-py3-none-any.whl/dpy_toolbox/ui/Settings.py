import asyncio
from typing import Union, Iterable, Optional, Callable, Coroutine, Any, Tuple
import discord
from itertools import chain
from ..ui.core import ButtonDisplay, DropdownDisplay, SelectOptionDisplay
from ..ui.Modal import SingleQuestion
from ..core import MISSING


class SimpleMultiToggler(discord.ui.View):
    def __init__(
            self,
            callback: Callable,
            options: Tuple[Any, Any],
            *,
            timeout: Optional[float] = 180.0,
            **kwargs
    ):
        """
        A menu to allow users to simply toggle settings

        :param  buttons: A book that will be used as an iterator
        :return: The view
        :rtype: discord.ui.View
        """
        self._callback = callback
        super().__init__(timeout=timeout)
        for d in options:
            label, value = d[0], d[1]
            default = False
            params = {"label": label, **(d[3:] if len(d) >= 4 else kwargs)}
            if len(d) == 3:
                default = d[2]
            btn = discord.ui.Button(**params)
            btn.callback = self.get_callback(btn)
            btn.__state__ = default
            btn.__value__ = value
            self.add_item(btn)
        for child in self.children:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self._callback(self, inter, child, child.__state__, child.__value__)
            )

    def get_callback(self, button: discord.ui.Button):
        async def child_callback(inter: discord.Interaction):
            button.__state__ = not button.__state__
            return await self._callback(self, inter, button, button.__state__, button.__value__)
        return child_callback

