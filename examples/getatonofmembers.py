'''
another get-members test
this will work on any server..tried it on the official fortnite server and a few other >100k member servers. discord's weird...
if you get an error it's likely cause discord doesnt think you're in that server yet. try again later

also...this doesnt always return all members (because turns out discord doesnt always send back 200 members when you request for them :/ )
yea... the real implementation into the wrapper will ofc return all members.
These are just tests, and tests are meant to show what I need to do on the real wrapper. All in all, I'd say this was a successful test: I learned more about discord's api.

also...I dont condone writing such messy code unless you're doing it for a test
'''

import discum
bot = discum.Client(token=token)

bot.memberlist = []
bot.memberRanges = False
bot.index = -1

#set guild and channel variables
bot.guildID = ""
bot.channelID = "" #you need to specify a channel ID

@bot.gateway.command
def getGuildChannelMembers(resp):
	if resp['t'] == 'READY_SUPPLEMENTAL': #tells the program when to start requesting for guild members
		if bot.gateway.session.guild(bot.guildID).unavailable:
			pass #keep bot.memberRanges equal to False
		else:
			if bot.gateway.session.guild(bot.guildID).memberCount>15000: #15k is pretty big...
				with open('memberdata.txt', 'w+') as initialf:
					initialf.write('[')
				bot.f = open('memberdata.txt', 'a')
			bot.memberRanges = bot.gateway.guildcommands.rangeCalc(bot.gateway.session.guild(bot.guildID).memberCount)
			bot.index += 1
		bot.gateway.guildcommands.listen(bot.guildID,bot.channelID, memberRange=[[0,99]]) #just wraps an op14. we want to listen to this channel, may or may not receive GUILD_MEMBER_LIST_UPDATE
	elif bot.gateway.guildcommands.GuildCreate(resp) and bot.memberRanges==False:
		if bot.gateway.session.guild(bot.guildID).memberCount>15000: #15k is pretty big...
			with open('memberdata.txt', 'w+') as initialf:
				initialf.write('[')
			bot.f = open('memberdata.txt', 'a')
		bot.gateway.session.guild(bot.guildID).setData(resp['d']) #update session data
		bot.index += 1
		bot.memberRanges = bot.gateway.guildcommands.rangeCalc(bot.gateway.session.guild(bot.guildID).memberCount)
	if bot.memberRanges != False:
		if bot.index == 0:
			bot.gateway.guildcommands.listen(bot.guildID,bot.channelID, memberRange=bot.memberRanges[bot.index], typing=None, activities=None, members=None)
			bot.index += 1
		if bot.gateway.guildcommands.GuildMemberListUpdate(resp,'SYNC'):
			if len(bot.gateway.guildcommands.parseSyncData(resp)) == 0 and bot.gateway.session.guild(bot.guildID).memberCount>15000:
				bot.f.write(']')
				bot.f.close()
				bot.gateway.close()
			elif bot.gateway.session.guild(bot.guildID).memberCount>15000: #15k is pretty big...
				bot.f.write(str(bot.gateway.guildcommands.parseSyncData(resp))+',')
			else:
				bot.memberlist.extend(bot.gateway.guildcommands.parseSyncData(resp))
			if bot.index == len(bot.memberRanges): #because we want to end it on the last SYNC
				if bot.gateway.session.guild(bot.guildID).memberCount>15000:
					bot.f.write(']')
					bot.f.close()
				bot.gateway.close()
			elif bot.index != len(bot.memberRanges):
				bot.gateway.guildcommands.listen(bot.guildID,bot.channelID, memberRange=bot.memberRanges[bot.index], typing=None, activities=None, members=None)
				bot.index += 1

bot.gateway.run()

if bot.gateway.session.guild(bot.guildID).memberCount>15000:
	with open('memberdata.txt', 'r') as f:
		memberstring = f.read()
	import ast
	membereval = ast.literal_eval(memberstring)
	import itertools
	bot.memberlist = list(itertools.chain(*membereval)) #all this does is flatten the list

memberlist = list({i['user']['id']:i for i in bot.memberlist}.values()) #remove duplicates, just in case
