import os
import requests
from os.path import join, dirname
import discord
from discord.ext import commands
from dotenv import load_dotenv
import html

dotenv_path = join(dirname(__file__), 'GwerTranslator.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix='!')

import re
from os.path import exists

word_def_link = {}

if not exists("data.txt"):
	a_file = open("data.txt", "w")
else:
	a_file = open("data.txt", "r")
	for line in a_file:
		match = re.search('dictionnaire\/mot\/(.+?)\/(.+)', line)
		word_def_link[match.group(2)] = line
		print(line)

if len(word_def_link) == 0:
	for i in range(329):
		searchAddr =  'https://www.dico2rue.com/dictionnaire/page-' + str(i)
		response = requests.get(searchAddr)

		matches = re.findall('<a href="(\/dictionnaire\/mot\/.+?)">',str(response.content, 'UTF-8'))

		a_file = open("data.txt", "a")

		for match in matches:
			print(match)
			word_def_link.append(match)
			a_file.write(match + '\n')
	
			#a_file.write(str(match + "\n"))



@bot.event
async def on_ready():
	print(f'{bot.user} has connected to discord')
	for guild in bot.guilds:
		if guild.name == GUILD:
			break

	print (
		f'{bot.user} is connected to the following guild:\n'
		f'{guild.name}(id : {guild.id})'
		)

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')




@bot.command(name='GwerTranslator', aliases=['GT'])
async def GwerTranslator(ctx, arg):
	commandAuthor = ctx.author.name
	response = ""
	if arg in word_def_link:
		linkpart = word_def_link[arg]
		link = "https://www.dico2rue.com" + linkpart
		print(link)

		definitionData = requests.get(link)
		definitionText = str(definitionData.content, 'UTF-8')

		definitionmatches = re.search(',"definition":"(.+?)","example":"(.+?)",', definitionText)
		definition = definitionmatches.group(1).encode().decode('unicode-escape').encode('latin1').decode('utf8').replace('<br />','').replace('<br/>', '')
		example = definitionmatches.group(2).encode().decode('unicode-escape').encode('latin1').decode('utf8').replace('<br />','').replace('<br/>', '')
		
		print("Definition : " + definition)
		print("Example : " + example)

		response = f"Salam akhi <@{ctx.author.id}>, la définition de {arg} est :\n{definition}\nExample: {example}?"
	elif arg == "akhi":
		response = f"Salam akhi <@{ctx.author.id}>, la définition de akhi est :Frère\nExample: Salam akhi, ça va?"
	else:
		response = f"Désolé akhi <@{ctx.author.id}>, je n'ai pas la définition de \"{arg}\", viens l'ajouter <@140182302037639168>"

	await ctx.send(response)



#@bot.command(name='GT')
#async def GT(ctx):
#	await GwerTranslator(ctx)


@bot.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a+') as errorFile:
		if event == 'on_message':
			errorFile.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

bot.run(TOKEN)
