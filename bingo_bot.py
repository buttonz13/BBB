import discord
from discord.ext import commands
import random
from PIL import Image,ImageDraw,ImageFont
import io
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

PHRASES = [
	"A Christian hasn't read their bible",
	"*Thrayle's Sigh*", 
	"A guest doesn't know / understand science", 
	"Guest is unwilling to say 'I don't know'",
	"God is everything", 
	"Someone believes the Earth is flat", 
	"A guest tries to debate", 
	"A guest asks the panel about their beliefs", 
	"Sandwich",
	"A guest thinks their belief is totally unique", 
	"Faith / Divinity", 
	"Crash out", 
	"Someone asserts 'knowing' with no evidence", 
	"A guest doesn't know why they hold a belief", 
	"Panel gets WTF'd", 
	"A guest had a 'spiritual experience'", 
	"Someone learns something",
	"A guest uses a word they can't define", 
	"Brain in a jar / vat", 
	"Critical thought happens", 
	"Everything is energy", 
	"Quantum", 
	"A guest tries to preach",
	"Frequency / Vibrations",
	"Guest avoids a question/ Changes subject",
	"Guest attempts to mimic Thrayle's voice",
	"Christian that doesn't call themselves a Christian",
	"Hammy gets dropped from the panel randomly",
	"Guest assumes the panel is all of the same belief",
	"Someone obsesses over Thrayle's voice",
	"Someone had a personal experience with God / Deity / Jesus",
	"'My Truth' / 'Your Truth' Mentioned",
	"Manifestation",
	"Skeletal Bat Goddess mentioned",
	"Christian that HAS read their bible",
	"Someone says 'This is what they do'",
	"We are all one",
	"Religion of convenience",
	"Aliens mentioned",
	"Anything is possible if you believe hard enough",
	"'Road Trip'",
	"'It's complex'",
	"Everything couldn't be created out of nothing",
	"God day",
	"Thrayle mentions tarocchi",
	"Guest says Google it when asked for source or evidence",
	"Guest gets kicked before finishing their exit speech",
	"Guest says they do not have a belief",
	"End of days mentioned",
	"Guest butchers Thrayle's name"
	]

card_size = 5
square_size = 200
font_size = 25

try:
	font = ImageFont.truetype('Candal.ttf',font_size)
except:
	font = ImageFont.load_default()

def create_bingo_card():
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