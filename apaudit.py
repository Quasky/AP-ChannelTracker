
import discord
import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
discord_client = discord.Client(intents=intents)

with open('config.json') as f:
    config = json.load(f)

DiscordToken = config["DiscordToken"]
DiscordGuildID = int(config["DiscordGuild"])
AgentID = int(config["YourID"])

@discord_client.event
async def on_ready():
    await discord_client.get_user(AgentID).send("Starting Audit!")
    
    for forum in discord_client.get_guild(DiscordGuildID).forums:
        #print("=== Found forum: "+ str(forum.name) + " with "+ str(len(forum.members)) + " members...")
        with open("summary.csv", "a") as f:
            f.write(forum.name + "|||" + str(len(forum.members)) + "\n")
            
        for thread in forum.threads:
            #print("=== Found active thread: "+ str(thread.name) + " with "+ str(len(await thread.fetch_members())) + " members...")
            with open("listing.csv", "a") as f:
                f.write(forum.name + "|||" + thread.name + "|||" + str(len(await thread.fetch_members())) + "|||" + str(thread.id) + "|||active\n")
        async for archthread in forum.archived_threads():
            #print("=== Found archived thread: "+ str(archthread.name) + " with "+ str(len(await archthread.fetch_members())) + " members...")
            with open("listing.csv", "a") as f:
                f.write(forum.name + "|||" + archthread.name + "|||" + str(len(await archthread.fetch_members())) + "|||" + str(archthread.id) + "|||archived\n")
                
    audits = [
    discord.File('listing.csv'),
    discord.File('summary.csv')
    ]
    await discord_client.get_user(AgentID).send("Finished Audit!", files=audits)
    await discord_client.close()

def main():
    discord_client.run(DiscordToken)

if __name__ == '__main__':
    main()
