import os
import sys
import discord
import pickle
import secret_token

token = secret_token.token

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} connecté avec succes!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)

    #commands
    # !channelstats
    # !occurences {word1,word2,word3}

    l = message.content.split()
    cmd = l[0]
    args = l[1:]

    if cmd == "!channelstats":
        messages = await message.channel.history(limit=10000).flatten()
        msgCountByAuthor = {}
        maxLen = 0
        maxLenId = None
        linkCount = 0
        ocamlCount = 0
        for i in messages:
            if len(i.content) > maxLen:
                maxLen = len(i.content)
                maxLenId = i.author.id
            if "http://" in i.content or "https://" in i.content:
                linkCount += 1
            if "ocaml" in i.content.lower():
                ocamlCount += 1
            if i.author.id not in msgCountByAuthor:
                msgCountByAuthor[i.author.id] = 1
            else:
                msgCountByAuthor[i.author.id] += 1
        ranks = sorted(msgCountByAuthor, key=msgCountByAuthor.get, reverse=True)
        msg = ":chart_with_upwards_trend:  Statistiques du channel %s  :chart_with_downwards_trend:\n\n"%message.channel.name
        msg += " Nombres de messages analysés: %d\n"%len(messages)
        msg += " Utilisateur ayant envoyé le plus de messages: <@!%s> (%d messages)\n"%(ranks[0], msgCountByAuthor[ranks[0]])
        msg += " Utilisateur ayant envoyé le plus long message: <@!%s> (%d caractères)\n"%(maxLenId, maxLen)
        msg += " Nombre de liens cliquables: %d\n"%linkCount
        msg += " Nombre de mentions d'OCaml: %d\n"%ocamlCount
        await message.channel.send(msg)

    if cmd == "!occurences":
        if len(args) != 1:
            await message.channel.send(":warning: Usage: !occurences mot1,mot2,mot3...")
            return
        words = args[0].lower().split(",")
        counts = [0] * len(words)
        messages = await message.channel.history(limit=10000).flatten()
        for i in messages:
            for j in range(len(words)):
                counts[j] += i.content.lower().count(words[j])
        msg = "Nombre d'occurences des mots suivants dans le channel %s:\n\n"%message.channel.name
        for i in range(len(words)):
            msg += words[i] + " : " + str(counts[i]) + "\n"
        await message.channel.send(msg)




client.run(token)
