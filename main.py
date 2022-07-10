import os
from dotenv import load_dotenv
import nextcord
from discord import Color
import logging
from SentinelDFI.scanner import Scanner

logging.basicConfig(level=logging.INFO)

def main():

	intents = nextcord.Intents.default()
	intents.message_content = True
	ukozi = nextcord.Client(intents=intents)
	load_dotenv()
	staticAI = Scanner(isVerbose = True)
	@ukozi.event
	async def on_message(message):
		if message.attachments != []:
			for attachment in message.attachments:
				await attachment.save(attachment.filename)
				#await message.reply("Downloaded "+attachment.filename+" to scan...")
				try:
					results = staticAI.scanFile(attachment.filename, maxSize = attachment.size)
				except:
					print("Scanner Failed.")
					os.remove(attachment.filename)
				else:
					if results['Verdict'] == "benign":
						embed = nextcord.Embed(description=attachment.filename, title="✅  This file is benign.", color = Color.green())
					
					elif results['Verdict'] == "suspicious":
						embed = nextcord.Embed(description=attachment.filename, title="⚠️  This file is suspicious.", color = Color.orange())
						embed.add_field(name = "Indicators", value = results['Indicators'], inline=True)
						
					elif results['Verdict'] == "malware":
						embed = nextcord.Embed(description=attachment.filename, title="🚨  This file is malicious.", color = Color.red())
						embed.add_field(name = "Indicators", value = results['Indicators'], inline=True)
					
					embed.set_footer(text=str(message.author) + ' uploaded the scanned file.')
					await message.channel.send(embed=embed)
					#await message.reply(staticAI.scanFile(attachment.filename, maxSize = attachment.size))
					os.remove(attachment.filename)
				
	ukozi.run(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
	main()