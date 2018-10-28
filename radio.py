import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()

import config

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('/usr/local/lib/libopus.so')

@client.event
async def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(client.user))
	voice = await client.join_voice_channel(discord.Object(id=config.channel))
	voice.player = voice.create_ffmpeg_player(config.stream)
	voice.player.start()
	await client.change_presence(game=discord.Game(name=config.playing, type=0))
	await client.send_message(discord.User(id=config.owner), '`{0}` started successfully!'.format(client.user))

@client.event
async def on_message(message):
	if message.author.id == config.owner:
		channel = client.get_channel(config.channel)
		voice = client.voice_client_in(channel.server)
		if message.content.startswith('%pause'):
			voice.player.pause()
			await client.send_message(message.channel, 'The player has been paused.')
		elif message.content.startswith('%resume'):
			voice.player.resume()
			await client.send_message(message.channel, 'The player has been resumed.')
		elif message.content.startswith('%channel'):
			channel = client.get_channel(message.content[9:])
			try:
				await voice.move_to(channel)
				await client.send_message(message.channel, 'The channel has been changed.')
			except:
				await client.send_message(message.channel, 'Must be a voice channel.')
		elif message.content.startswith('%stream'):
			stream = message.content[8:]
			voice.player.stop()
			voice.player = voice.create_ffmpeg_player(stream)
			voice.player.start()
			await client.send_message(message.channel, 'The stream has been changed.')
		elif message.content.startswith('%playing'):
			playing = message.content[9:]
			await client.change_presence(game=discord.Game(name=playing, type=0))
			await client.send_message(message.channel, 'The playing status has been changed.')
		elif message.content.startswith('%logout'):
			await client.send_message(message.channel, '(╯°□°）╯︵ ┻━┻')
			await client.logout()

@client.event
async def on_voice_state_update(before, after):
	if after != client.user:
		if before.voice.voice_channel != after.voice.voice_channel:
			channel = client.get_channel(config.channel)
			voice = client.voice_client_in(channel.server)
			try:
				if before.voice.voice_channel.id == voice.channel.id:
					await client.send_message(discord.User(id=config.owner), '`{0}` left'.format(after))
			except:
				pass
			try:
				if after.voice.voice_channel.id == voice.channel.id:
					await client.send_message(discord.User(id=config.owner), '`{0}` joined'.format(after))
			except:
				pass

client.run(config.token)