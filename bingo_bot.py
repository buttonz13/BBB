from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
	return "Bot is running!"

def run():
	app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()

import discord
from discord.ext import commands
import random
from PIL import Image,ImageDraw,ImageFont
import io
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

PHRASES = {
	"bible": "A Christian hasn't read their bible",
	"sigh": "*Thrayle's Sigh*", 
	"science": "A guest doesn't know / understand science", 
	"idk": "Guest is unwilling to say 'I don't know'",
	"everything": "God is everything", 
	"flat": "Someone believes the Earth is flat", 
	"debate": "A guest tries to debate", 
	"panel": "A guest asks the panel about their beliefs", 
	"sandwich": "Sandwich",
	"unique": "A guest thinks their belief is totally unique", 
	"faith": "Faith / Divinity", 
	"crash": "Crash out", 
	"assert": "Someone asserts 'knowing' with no evidence", 
	"?": "A guest doesn't know why they hold a belief", 
	"wtf": "Panel gets WTF'd", 
	"experience": "A guest had a 'spiritual experience'", 
	"learn": "Someone learns something",
	"define": "A guest uses a word they can't define", 
	"brain": "Brain in a jar / vat", 
	"crit": "Critical thought happens", 
	"energy": "Everything is energy", 
	"quantum": "Quantum", 
	"preach": "A guest tries to preach",
	"vibes": "Frequency / Vibrations" 
	}

card_size = 5
square_size = 200
font_size = 25

try:
	font = ImageFont.truetype('Candal.ttf',font_size)
except:
	font = ImageFont.load_default()

def create_bingo_card(card_number):
	img = Image.new('RGB',(square_size * card_size, square_size * card_size),'white')
	draw = ImageDraw.Draw(img)

	selected_phrases = random.sample(PHRASES,24)
	grid = []
	
	idx = 0
	for row in range(card_size):
		row_data = []
		for col in range(card_size):
			if row==2 and col==2:
				row_data.append('FREE')
			else:
				row_data.append(selected_phrases[idx])
				idx += 1
		grid.append(row_data)

	for row in range(card_size):
		for col in range(card_size):
			x0 = col * square_size
			y0 = row * square_size
			x1 = x0 + square_size
			y1 = y0 + square_size
			draw.rectangle([x0,y0,x1,y1],outline="black",width=3)

			text = grid[row][col]
			
			lines = []
			words = text.split()
			line = ""
			for word in words:
				if font.getlength(line + word + " ") < square_size - 20:
					line += word + " "
				else:
					lines.append(line.strip())
					line = word + " "
			lines.append(line.strip())

			total_text_height = len(lines) * font_size
			for i, line in enumerate(lines):
				w = font.getlength(line)
				draw.text(
					(x0 + (square_size - w)/2, y0 + (square_size - total_text_height)/2 + i * font_size),
					line,
					font=font,
					fill="black"
				)
	return img	

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")

@bot.command(name="card")
async def card(ctx):
	img = create_bingo_card()

	with io.BytesIO() as image_binary:
		img.save(image_binary,"PNG")
		image_binary.seek(0)
		await ctx.send(file=discord.File(fp=image_binary,filename="card.png"))

bot.run(TOKEN)