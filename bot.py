# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json
import logging.config
import os
import sys
import traceback

import discord
from discord.ext import commands


class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix, help_command=None)

        self.INITIAL_COGS = [
            filename[:-3] for filename in os.listdir("./cogs") if filename.endswith(".py")]

        for cog in self.INITIAL_COGS:
            try:
                self.load_extension(f'cogs.{cog}')
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('-----')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        logging.info('rebooted')
        await bot.change_presence(activity=discord.Game(name="リアクション集計中"))


def read_token():
    file = currentpath + "/token"
    try:
        for line in open(file, 'r'):
            temp = line.replace(" ", "").strip().split("=")
            token = temp[1]
    except FileNotFoundError:
        print("ファイルが見つかりません・・・。")
        print(sys.exc_info())
        return

    return token


if __name__ == '__main__':
    currentpath = os.path.dirname(os.path.abspath(__file__))

    token = read_token()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.FileHandler(
        currentpath + "/data/log/logger.log", 'a', 'utf-8')
    formatter = logging.Formatter(
        '%(levelname)s : %(asctime)s : %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    bot = MyBot(command_prefix="/")
    bot.run(token)
