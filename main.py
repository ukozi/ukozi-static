import os
import nest_asyncio
import string
from dotenv import load_dotenv
import nextcord
from discord import Color
import logging
import SentinelDFI.scanner as SentinelOne
from SentinelDFI.scanner import Scanner
import vt

logging.basicConfig(level=logging.INFO)
load_dotenv()
nest_asyncio.apply()

def trimTime(strTime, trim):
	strTime = strTime[:len(strTime)-trim]
	return str(strTime)

async def getAnalysisStats(hash):
	client = vt.Client(os.getenv("VT_API"))
	strHash = str(hash[:2])
	print(strHash)
	file = client.get_object("/files/"+str(hash))
	return file

def main():

	intents = nextcord.Intents.default()
	intents.message_content = True
	ukozi = nextcord.Client(intents=intents)
	staticAI = Scanner(isVerbose = True)


	@ukozi.event
	async def on_message(message):
		if message.attachments != []:
			for attachment in message.attachments:
				await attachment.save(attachment.filename)
				#await message.reply("Downloaded "+attachment.filename+" to scan...")
				try:
					results = staticAI.scanFileWithDepth(attachment.filename, maxSize = attachment.size, maxDepth = 5)
				except SentinelOne.ScannerUnknownFileTypeException:
					fileName, fileType = os.path.splitext(attachment.filename)
					fileType = fileType.translate(str.maketrans('', '', string.punctuation))
					embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine doesn't scan this file type because it is unlikely to pose a threat. Always exercise vigilance when downloading files.", title= fileType.upper()+" not scanned.", color = Color.blue())
					embed.set_footer(text=str(attachment.filename)+' was uploaded by '+str(message.author)+ " at "+ trimTime(str(message.created_at), 13)+" UTC")
					await message.channel.send(embed=embed)
					os.remove(attachment.filename)
				except SentinelOne.ScannerInvalidArchiveException:
					embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine couldn't scan this file because it is most likely encrypted. This is a common tactic used to bypass detections. Always exercise vigilance when downloading files.", title="Archive encrypted.", color = Color.red())
					embed.set_footer(text=str(attachment.filename)+' was uploaded by '+str(message.author)+ " at "+ trimTime(str(message.created_at), 13)+" UTC")
					await message.channel.send(embed=embed)
					os.remove(attachment.filename)
				except SentinelOne.ScannerFailedException:
					embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine couldn't scan this file for an unknown reason. Always exercise vigilance when downloading files.",title="Couldn't scan file.", color = Color.red())
					embed.set_footer(text=str(attachment.filename)+' was uploaded by '+str(message.author)+ " at "+ trimTime(str(message.created_at), 13)+" UTC")
					await message.channel.send(embed=embed)
					os.remove(attachment.filename)
				else:
					if results['Verdict'] == "benign":
						embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine found no issues with this file.", title="No detections.", color = Color.green())
					
					elif results['Verdict'] == "suspicious":
						file = await getAnalysisStats(results['SHA1'])
						embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine found this file suspicious. Therefore, Ukozi Static checked with over 70 other AV and EDR engines to help you decide if you would like to interact with this file.", title="Suspicious detection.", color = Color.orange())
						embed.add_field(name = "Harmless", value = file.last_analysis_stats['harmless'], inline=True)
						embed.add_field(name = "Suspicious", value = file.last_analysis_stats['suspicious'], inline=True)
						embed.add_field(name = "Malicious", value = file.last_analysis_stats['malicious'], inline=True)
						embed.add_field(name = "Undetected", value = file.last_analysis_stats['undetected'], inline=True)
						embed.add_field(name = "Unsupported", value = file.last_analysis_stats['type-unsupported'], inline=True)
						embed.add_field(name = "Failed", value = file.last_analysis_stats['failure'], inline=True)
						
					elif results['Verdict'] == "malware":
						embed = nextcord.Embed(description="The <:s1:955538101424521226>**Nexus** engine found this file malicious.", title="Malicious detection.", color = Color.red())
						embed.add_field(name = "Indicators", value = results['Indicators'], inline=True)
						
					embed.set_footer(text=str(attachment.filename)+' was uploaded by '+str(message.author)+ " at "+ trimTime(str(message.created_at), 13)+" UTC")
					await message.channel.send(embed=embed)
					#await message.reply(staticAI.scanFile(attachment.filename, maxSize = attachment.size))
					os.remove(attachment.filename)

	ukozi.run(os.getenv("BOT_TOKEN"))
	
	
if __name__ == "__main__":
	main()