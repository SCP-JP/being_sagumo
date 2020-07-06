# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
import typing

import discord
from discord.ext import commands


def is_server_owner():  # botのオーナーのみが実行できるコマンド
    async def predicate(ctx):
        return ctx.guild and ctx.author.id == ctx.author.id
    return commands.check(predicate)


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.master_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.is_owner(self.bot.user)

    @commands.group(aliases=['re'], hidden=True)
    @is_server_owner()
    async def reload(self, ctx, cogname: typing.Optional[str] = "ALL"):
        if cogname == "ALL":
            for cog in self.bot.INITIAL_COGS:
                try:
                    self.bot.unload_extension(f'cogs.{cog}')
                    self.bot.load_extension(f'cogs.{cog}')
                except Exception as e:
                    print(e)
            await ctx.send(f"{(self.bot.INITIAL_COGS)}をreloadしました")
        else:
            try:
                self.bot.unload_extension(f'cogs.{cogname}')
                self.bot.load_extension(f'cogs.{cogname}')
                await ctx.send(f"{cogname}をreloadしました")
            except Exception as e:
                print(e)
                await ctx.send(e)

    @commands.command(aliases=['st'], hidden=True)
    @is_server_owner()
    async def status(self, ctx, word: str):
        try:
            await self.bot.change_presence(activity=discord.Game(name=word))
            await ctx.send(f"ステータスを{word}に変更しました")
            self.bot.status = word
        except BaseException:
            pass
        

    @commands.command(aliases=['p'], hidden=True)
    async def ping(self, ctx):
        start_time = time.time()
        mes = await ctx.send("Pinging....")
        await mes.edit(content="pong!\n" + str(round(time.time() - start_time, 3) * 1000) + "ms")

    @commands.command(aliases=['wh'], hidden=True)
    @is_server_owner()
    async def where(self, ctx):
        await ctx.send("現在入っているサーバーは以下です")
        for s in ctx.cog.bot.guilds:
            await ctx.send(f"{s}")

    @commands.command(aliases=['mem'], hidden=True)
    @is_server_owner()
    async def num_of_member(self, ctx):
        await ctx.send(f"{ctx.guild.member_count}")

    @commands.command(aliases=['send'], hidden=True)
    @is_double_owner()
    async def send_json(self, ctx):
        json_files = [
            filename for filename in os.listdir(self.master_path + "/data")
            if filename.endswith(".json")]

        my_files = [discord.File(f'{self.master_path}/data/{i}') for i in json_files]

        await ctx.send(files=my_files)


def setup(bot):
    bot.add_cog(admin(bot))
