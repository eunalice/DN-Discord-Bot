import discord
from discord import app_commands
from discord.ext import commands
from patchInfo import getPatchInfo
from luckyzone import getLuckyzoneWeek
from uistring import getCdata
from DNmath import bonus_spilt
from Gemini import getTextGeneration
from luckyzoneAnnouncement import check_next_announcement_time, write_next_announcement_time, read_next_announcement_time, next_friday_six_pm
from datetime import datetime, timedelta, timezone
from dnt_csv import search_item
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN_YUI')
prefix = "."
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

async def schedule_announcement():
    now = datetime.now(timezone(timedelta(hours=8)))

    if check_next_announcement_time():
        announcement_channel = bot.get_channel(1197177232158888057)
        message = await announcement_channel.send(content=getLuckyzoneWeek(1))
        await message.publish()

        next_announcement_time = next_friday_six_pm()

        write_next_announcement_time(next_announcement_time)
        delay = (next_announcement_time - now).total_seconds()
        await asyncio.sleep(delay)

        if check_next_announcement_time():
            await schedule_announcement()
    else:
        next_announcement_time = read_next_announcement_time()
        delay = (next_announcement_time - now).total_seconds()
        await asyncio.sleep(delay)

        if check_next_announcement_time():
            await schedule_announcement()


@bot.event
async def on_ready():
  print("目前登入身份：", bot.user)
  
  try:
    synced = await bot.tree.sync()
    print(f'[on_ready()] Synced {len(synced)} commands.')
  except Exception as e:
    print(f'[on_ready()] Error syncing commands: {e}')

  await schedule_announcement()

@bot.group()
async def lz(ctx):
  if ctx.invoked_subcommand is None:
    message = await ctx.send("正在獲取幸運關卡資訊...")
    await message.edit(content=getLuckyzoneWeek(0))


@lz.command()
async def week(ctx, week: int):
  message = await ctx.send("正在獲取幸運關卡資訊...")
  await message.edit(content=getLuckyzoneWeek(week))


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  else:
    print(error)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
  pass


@bot.tree.command(name="help", description="呼喚小唯")
async def 小唯(interaction: discord.Interaction):
  await interaction.response.send_message("是的，請問您有什麼事情想要我幫忙的嗎？",
                                          ephemeral=True)


@bot.tree.command(name="patch", description="獲取版本資訊")
async def patch(interaction: discord.Interaction):
  await interaction.response.defer()
  patchInfo = await getPatchInfo()
  embed = discord.Embed(title="版本資訊", description=patchInfo, color=0x665ba9)
  await interaction.followup.send(embed=embed)


@bot.tree.command(name="uistring", description="文本查詢")
@app_commands.describe(mid='請輸入mid')
async def uistring(interaction: discord.Interaction, mid: str):
  await interaction.response.defer(ephemeral=True)
  cData = getCdata(mid)
  embed = discord.Embed(title="文本查詢", description=cData, color=0x665ba9)
  await interaction.followup.send(embed=embed, ephemeral=True)


@bot.tree.command(name="bonusspilt", description="均分金幣")
@app_commands.describe(gold='請輸入金幣量')
@app_commands.describe(count='請輸入人數')
async def bonusspilt(interaction: discord.Interaction,
                     gold: int,
                     count: int = None):
  await interaction.response.defer()
  if count is None:
    count = 8
  goldspilt = bonus_spilt(gold, count)
  text = f"總金額：{gold}金\n每人分：{goldspilt}"
  embed = discord.Embed(title=f"均分金幣({count}人)",
                        description=text,
                        color=0x665ba9)
  await interaction.followup.send(embed=embed)


@bot.tree.command(name="luckyzone", description="幸運關卡查詢")
@app_commands.describe(week='欲查詢週次(1等於下週，-1等於上週)')
async def luckyzone(interaction: discord.Interaction, week: int = None):
  await interaction.response.defer()
  if week is None:
    week = 0
  lz = getLuckyzoneWeek(week)
  embed = discord.Embed(title="幸運關卡查詢", description=lz, color=0x665ba9)
  await interaction.followup.send(embed=embed)


@bot.tree.command(name="says", description="文字生成測試")
@app_commands.describe(prompt='是的，請問您有什麼事情想要我幫忙的嗎？')
async def textGeneration(interaction: discord.Interaction, prompt: str):
  await interaction.response.defer()
  text = "您：" + prompt + "\n小唯：" + getTextGeneration(prompt)
  embed = discord.Embed(title="文字生成測試", description=text, color=0x665ba9)
  await interaction.followup.send(embed=embed)


@bot.tree.command(name="itemid", description="道具ID查詢")
@app_commands.describe(id='透過道具ID來查詢道具的詳細資訊')
async def searchItemByID(interaction: discord.Interaction, id: int):
  await interaction.response.defer()
  text = search_item(id)
  embed = discord.Embed(title="道具查詢(ID)", description=text, color=0x665ba9)
  await interaction.followup.send(embed=embed)

bot.run(bot_token)
