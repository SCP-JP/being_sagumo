# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
from cogs.utils.reaction_aggregation_manager import ReactionParameter
import discord

from .setting_manager import SettingManager


class CommonUtil():
    def __init__(self):
        self.setting_mng = SettingManager()

    async def is_bot_user(self, guild: discord.Guild, command_user: discord.Member) -> bool:
        """そのサーバーのBOT_user役職を持っているか判定する関数

        Args:
            guild (discord.Guild): サーバーのギルドオブジェクト
            command_user (discord.Member): コマンド使用者のメンバーオブジェクト

        Returns:
            bool: 入ってたらTrue、入ってなかったらFalse

        Memo:
            管理者は使用者の権限も持つことにする
        """
        guild_DB = await self.setting_mng.get_guild(guild.id)
        if guild_DB is None:
            return False
        bot_user_role = guild.get_role(guild_DB.bot_user_id)
        bot_manager_role = guild.get_role(guild_DB.bot_manager_id)

        if any([role in command_user.roles for role in [
                bot_manager_role, bot_user_role]]):
            return True
        else:
            return False

    async def is_bot_manager(self, guild: discord.Guild, command_user: discord.Member) -> bool:
        """そのサーバーのBOT_manager役職を持っているか判定する関数

        Args:
            guild (discord.Guild): サーバーのギルドオブジェクト
            command_user (discord.Member): コマンド使用者のメンバーオブジェクト

        Returns:
            bool: 入ってたらTrue、入ってなかったらFalse
        """
        guild_DB = await self.setting_mng.get_guild(guild.id)
        if guild_DB is None:
            return False
        bot_manager_role = guild.get_role(guild_DB.bot_manager_id)
        if bot_manager_role in command_user.roles:
            return True
        else:
            return False

    @staticmethod
    async def autodel_msg(msg: discord.Message, second: int = 5):
        """渡されたメッセージを指定秒数後に削除する関数

        Args:
            msg (discord.Message): 削除するメッセージオブジェクト
            second (int, optional): 秒数. Defaults to 5.
        """
        try:
            await msg.delete(delay=second)
        except discord.Forbidden:
            pass

    @staticmethod
    def get_msgurl_from_reaction(reaction: ReactionParameter) -> str:
        """msgurlをリアクションから生成する関数

        Args:
            reaction (ReactionParameter): リアクションオブジェクト

        Returns:
            str: discordのURL
        """
        url = f'https://discord.com/channels/{reaction.guild_id}/{reaction.channel_id}/{reaction.message_id}'
        return url

    @staticmethod
    def return_member_or_role(guild: discord.Guild,
                              id: int) -> typing.Union[discord.Member,
                                                       discord.Role,
                                                       None]:
        """メンバーか役職オブジェクトを返す関数

        Args:
            guild (discord.guild): discordのguildオブジェクト
            id (int): 役職かメンバーのID

        Returns:
            typing.Union[discord.Member, discord.Role]: discord.Memberかdiscord.Role
        """
        user_or_role = guild.get_role(id)
        if user_or_role is None:
            user_or_role = guild.get_member(id)

        return user_or_role
