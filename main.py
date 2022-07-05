import os
from dotenv import load_dotenv
import nextcord
import logging

logging.basicConfig(level=logging.DEBUG)

def main():

	intents = nextcord.Intents.default()
	intents.message_content = True
	ukozi = nextcord.Client(intents=intents)
	load_dotenv()
	@ukozi.event
	async def on_message(message):
		if message.attachments != []:
			for attachment in message.attachments:
				await attachment.save(attachment.filename)
				await message.reply("Downloaded "+attachment.filename+" to scan...")
	
	ukozi.run(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
	main()