import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import requests
import time
import re
import urllib.parse
from var import * 

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '-',intents=intents)

@client.event
async def on_ready():
    print("Bot Ready")
    print("-------------")


@client.command(description = "Robert Says Hello to you")
async def hello(ctx):
    await ctx.send(f"Hi {ctx.author.mention} I am robert.")


@client.command(description = "Dad Jokes")
async def redacted(ctx):
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
	    "X-RapidAPI-Key": JOKE_TOKEN,
	    "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers)
    joke = response.json()
    await ctx.send(joke["body"][0]["setup"])
    time.sleep(2)
    await ctx.send(joke["body"][0]["punchline"])

@client.command(description = "Sends a picture of jason")
async def jason(ctx):
    url = "https://any-anime.p.rapidapi.com/anime"

    headers = {
	    "X-RapidAPI-Key": JASON_TOKEN,
	    "X-RapidAPI-Host": "any-anime.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers)
    anim = response.json()
    await ctx.send(anim["stuff"][0]["image"])

@client.event
async def on_member_join(member):
    await member.send("I don't give a fuck who you are or where you live. You can count on me to be there to bring your fucking life to a hellish end. I'll put you in so much fucking pain that it'll make Jesus being nailed to a cross in the desert look like a fucking back massage on a tropical island. I don't give a fuck how many reps you have or how tough you are IRL, how well you can fight, or how many fucking guns you own to protect yourself. I'll fucking show up at your house when you aren't home. I'll turn all the lights on in your house, leave all the water running, open your fridge door and not close it, and turn your gas stove burners on and let them waste gas. You're going to start stressing the fuck out, your blood pressure will triple, and you'll have a fucking heart attack. You'll go to the hospital for a heart operation, and the last thing you'll see when you're being put under in the operating room is me hovering above you, dressed like a doctor. When you wake up after being operated on, wondering what ticking time bomb is in your chest waiting to go off. You'll recover fully from your heart surgery. And when you walk out the front door of the hospital to go home I'll run you over with my fucking car out of no where and kill you. I just want you to know how easily I could fucking destroy your pathetic excuse of a life, but how I'd rather go to a great fuckng length to make sure your last remaining days are spent in a living, breathing fucking hell. It's too late to save yourself, but don't bother committing suicide either… I'll fucking resuscitate you and kill you again myself you bitch-faced phaggot. Welcome to hell, population: you")


@client.event
async def on_member_remove(member):
    await member.send("LOL GOODBYE LOSER. LOSER! You're a LOSER! Are you feeling sorry for yourself?! Well, you should be, because you are DIRT! You make me sick, you big baby! Baby want a bottle? A big, DIRT bottle?!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    patany = '^.*[R-r]obert.{1,40}$'
    resany = re.match(patany, message.content)
    if resany:
        await message.add_reaction("🙋‍♀️")
        time.sleep(1)     
        await message.channel.send("Heyo thats me! Robba from the Computer Science Major!") 
    patex = '^([R-r]obert|[R-r]obert\s)$'
    resex = re.match(patex, message.content)
    if resex:
        await message.add_reaction("😘")
        time.sleep(0.5)                                             
        await message.channel.send("is the cutest lil muffin on Earth!😊🤗")
    await client.process_commands(message)

@client.group(name="translate",description ="Translate text", invoke_without_command=True)
async def trResponse(ctx):
     await ctx.send(">>> Language lookup: -translate list \nLanguage input: -translate to <language> \"<text to translate>\"\n*Note* - Source language is auto detected.\n\nBroken Languages: Chinese")

@trResponse.command(name="list")
async def trLanguageList(ctx):
    langList = []
    getList = []
    with open('lang.json') as g:
        langList = json.load(g)
        langs = langList['data']['languages']
        for i in langs:
            getList.append(i['name'])
        g.close()
    with open('getList.txt', 'w') as h:
        h.write(', '.join(getList))
        h.close()
    with open('getList.txt', 'r') as j:
        languages = j.read()
        await ctx.send(f">>>  {languages}")
        j.close()

@trResponse.command(name="to")
async def trLanguageInput(ctx, arg1=None, arg2=None):
    langData = []
    with open('lang.json') as f:
        langData = json.load(f)
        langs = langData['data']['languages']
        if arg1 == None:
            await ctx.send(f">>> Usage: '-translate to <language> \"<What you want to translate>\"'\n\n-translate -list for list of languages.")
        for i in langs:
            if (arg1.lower()).capitalize() == i['name']:
                await ctx.send(f">>> You are translating {i['name']}. Code: {i['code']}.")
                time.sleep(0.5)
                code = i['code']
                translation = urllib.parse.quote_plus(arg2)
                url = "https://text-translator2.p.rapidapi.com/translate"
                payload = "source_language=auto&target_language="+code+"&text="+translation
                headers = {
                    "content-type": "application/x-www-form-urlencoded",
                    "X-RapidAPI-Key": TRANSLATE_TOKEN,
                    "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
                }

                response = requests.request("POST", url, data=payload, headers=headers)
                trReply = response.json()
                translation = trReply["data"]["translatedText"]
                await ctx.send(f">>> {translation}")
                f.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "<@" + str(303573908538392576) + ">":
        await message.channel.send(f"Hey {message.author.mention}. Don't @ me!")
    await client.process_commands(message)

@client.command(name="robert",description = "Robert joins the voice call", pass_context = True)
async def _join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await ctx.send(f"{ctx.author.mention} Nobody.live?")
        voice = await channel.connect()
        time.sleep(2)
        source = FFmpegPCMAudio('robert.mp3')
        player = voice.play(source)
    else:
        await ctx.send("Get in vc")

@client.command(name="lua",description = "Robert leaves the voice call", pass_context = True)
async def _leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("bye im busy")
    else:
        await ctx.send("I am not in a voice channel idiot")
    

           

client.run(BOT_TOKEN) 