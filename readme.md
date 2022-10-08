![alt text](https://github.com/chuml1/ukozi-static/blob/master/screenshot.jpg?raw=true)

# Ukozi Static Bot for Discord
 Ukozi Static is a Discord bot that scans attachments to messages using SentinelOne's Static AI engine to determine if they pose any threat. The bot then posts the outcome. In the case of "suspicious" detections, the bot will also poll VirusTotal to assist in making any decision around removing messages (or users) that are posting files. While Discord offers *some* malicious file detection natively, it's pretty minimal and although it automatically removes files it deems to be malicious, the bot has (so far) been able to scan and post results faster than Discord can remove the file. I've also implemented some quality of life messages around things like encrypted archives and feedback on the types of files that won't be scanned.

## Note: You will need to supply your own copy of SentinelOne's NEXUS. 

### About Nexus:
The Nexus Embedded AI software development kit (SDK), enables organizations to prevent malicious threats from entering non-endpoint attack surfaces. The SDK embeds SentinelOne’s Static AI engine to provide real-time threat prevention. The Static AI engine is consistently ranked in the top VT engines and third party tests for efficacy and lowest FPs.

The SDK’s portable technology can be leveraged to protect and scan all traffic in cloud services like email and web gateways, CASBs, file sync and share services, traditional file servers, USB scanning kiosks, medical devices, SCADA/ICS instances, containers and many more use cases.

## If you don't want to install...
Prefer to just use the bot, rather than run your own? [Here's the invite](https://discord.com/api/oauth2/authorize?client_id=992267176524382209&permissions=536890368&scope=bot)
