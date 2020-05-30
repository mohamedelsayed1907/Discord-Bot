import random
import covid19_data
import datetime
import json
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix = "!")

URL = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'

@bot.event
async def on_ready():
    print("Bot is on ready state")


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
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Your ping is {round(bot.latency * 1000)}ms")


bot.run('NzE1MDM4NjIyNzQyNDc4OTAw.Xs3Zqg.ztPGkNLpYYZyLubJpy7HCU6s2fM')