import discord
from discord.ext import commands
from patchInfo import getPatchInfo
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')
prefix = "."
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents = intents)

@bot.event
async def on_ready():
    print("目前登入身份：", bot.user)
    
@bot.command()
async def 小唯(ctx):
    await ctx.send("是的，我在!")    

@bot.command()
async def patch(ctx):
    message = await ctx.send("正在獲取版本資訊...")
    await message.edit(content=getPatchInfo())

bot.run(bot_token)