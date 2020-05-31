import random
import covid19_data
import datetime
import asyncio
import json
import discord
import requests
from discord.ext import commands
import pprint
import requests
from time import sleep
import time
from discord.ext.commands import ConversionError

bot = commands.Bot(command_prefix = "!")

URL = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'





@bot.event
async def on_ready():
    print("Bot is on ready state")

@bot.event
async def on_member_join(ctx, member):
    await ctx.send('f{member} has joined the server!')

@bot.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context = True)
async def covid19(ctx):
    msg = await ctx.send("Collecting information...")
    total = covid19_data.dataByName("Total")
    egypt = covid19_data.dataByName("Egypt")
    usa = covid19_data.dataByName("US")
    canada = covid19_data.dataByName("Canada")
    india = covid19_data.dataByName("India")
    embed = discord.Embed(title = "COVID 19 OUTBREAK INFORMATION",
                          url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public",
                          description = "Coronavirus disease (COVID-19) is an infectious disease caused by a new virus.",
                          color = ctx.author.color
                          )
    embed.set_author(name="WORLD HEALTH ORGANIZATION",
                     icon_url="https://seeklogo.net/wp-content/uploads/2014/11/who-logo-vector.png")
    embed.set_thumbnail(
        url="https://wpcdn.us-east-1.vip.tn-cloud.net/www.abc6.com/content/uploads/2020/03/coronavirus.png")
    embed.add_field(name="CONFIRMED USA \nCASES", value=usa.cases)
    embed.add_field(name="CONFIRMED CANADA \nCASES", value=canada.cases)
    embed.add_field(name="CONFIRMED INDIA \nCASES", value = india.cases)
    embed.add_field(name="CONFIRMED EGYPT \nCASES", value = egypt.cases)
    embed.add_field(name="TOTAL \nCASES", value=total.cases, inline = True)
    embed.add_field(name="TOTAL \n DEATHS", value = total.deaths, inline = True)
    embed.add_field(name="TOTAL \n RECOVERIES", value= total.recovered, inline = True)
    embed.set_image(url="https://media1.tenor.com/images/16df5b8e9a9487e7a1cc980d9800f78b/tenor.gif?itemid=16521690")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed = embed)
    await msg.delete()

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def news(ctx):
    secret = 'f558a322e478455d80ae71fd77f010ed'
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': 'big data',  # query phrase
        'pageSize': 5,  # maximum is 100
        'apiKey': secret  # your own API key
    }

    response = requests.get(url, params=parameters)
    response_json = response.json()
    for i in response_json['articles']:
        await ctx.send("Fetching news...")
        time.sleep(3)
        await ctx.send(i['url'])
        time.sleep(3)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def bitcoin(ctx):
    url='https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await ctx.send("Bitcoin rate is: " + value)

@bot.command()
async def trivia(ctx):
    counter = 0
    questions = [
        "Who won the UEFA Champions League 2019?",
        "Who won the soccer Ballon D'or 2019?",
        "Who won the NBA 2019?",
        "Who won the English Premier League last year?",
        "What is the first country to have Coronavirus?"
    ]
    answers = ["Liverpool", "Messi", "Toronto Raptors", "Manchester City", "China"]
    rand_question = questions[random.randrange(len(questions))]
    await ctx.send(rand_question)


@bot.command()
@commands.has_role('Admin')
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("Not an administrator")
    elif isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        msg2 = await ctx.send(msg)
        await asyncio.sleep(2.5)
        await msg2.delete()
    else:
        raise error

@news.error
@commands.cooldown(1, 5, commands.BucketType.user)
async def news_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        msg2 = await ctx.send(msg)
        await asyncio.sleep(2.5)
        await msg2.delete()
    else:
        raise error

@bitcoin.error
@commands.cooldown(1, 5, commands.BucketType.user)
async def bitcoin_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        msg2 = await ctx.send(msg)
        await asyncio.sleep(2.5)
        await msg2.delete()
    else:
        raise error

@clear.error
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear_error_countdown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        msg2 = await ctx.send(msg)
        await asyncio.sleep(2.5)
        await msg2.delete()
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f"Pong! Your ping is {round(bot.latency * 1000)}ms")


@ping.error
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        msg2 = await ctx.send(msg)
        await asyncio.sleep(2.5)
        await msg2.delete()
    else:
        raise error

bot.run('NzE1MDM4NjIyNzQyNDc4OTAw.XtMI6A.SpIT0wsj4ekrEP1m_C_vi7ECw6U')