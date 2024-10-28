import discord
from random import randint
from discord.ext import commands
from dotenv import load_dotenv
import os
from scp_scrapping import SCP_SCRAPPING

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')

intents = discord.Intents.all()
intents.messages = True
intents.members = True

BOT = commands.Bot(command_prefix='!',intents=intents)

@BOT.command()
#Creacion de sufijo 'info' para llamar a esta funcion
#Valor por defecto del idioma en ingles si el usuario no pasa ningun parametro
async def web(ctx,lang:str = 'eng'):
    URL_WEB = "https://fsurvive.online"
    lang = lang.lower()
    if lang == 'eng':
        await ctx.send(f'Visit our official website of the project right now!.\n{URL_WEB}')
    elif lang == 'esp':
        await ctx.send(f'Visita la pagina web oficial del proyecto y enterate mas sobre el proyecto.\n{URL_WEB}')
    else:
        canal_bot = BOT.get_channel(1294559090655232021)
        await ctx.send(f"We couldn't detected your specified languague.\nRemember that you can see the commands bot in {canal_bot.mention}")

@BOT.command()
async def scp(ctx,scp_number,lang = 'eng'):
    scrapping = SCP_SCRAPPING(refactorNumber(str(scp_number)),getPREURL(lang),lang)
    
    await ctx.send(scrapping.getContent())

@BOT.command()
async def random_scp(ctx,lang = 'eng'):
    number = randint(2,7999)
    print("Numero aleatorio dado: "+str(number))
    scrapping = SCP_SCRAPPING(refactorNumber(str(number)),getPREURL(lang),lang)

    await ctx.send(scrapping.getContent())

@BOT.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Ups. It seems that you have entered an invalid or non-existent command. Please verified")

def refactorNumber(number):
    return str(number).zfill(3)

def getPREURL(lang):
    ENG_PRE_URL = "https://scp-wiki.wikidot.com/scp-"
    ESP_PRE_URL = "http://scp-es.com/scp-"

    return ENG_PRE_URL if lang == 'eng' else ESP_PRE_URL

BOT.run(TOKEN)