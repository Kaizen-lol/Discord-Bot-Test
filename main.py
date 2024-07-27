import discord
from discord.ext import commands
import requests
import json

from apikeys import key

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

class Utils:
    @staticmethod
    def check_tiktok_username(username: str):
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url)
            if '"followerCount":' in response.text:
                stats_start = response.text.find('"stats":{')
                stats_end = response.text.find('}', stats_start) + 1
                stats_text = response.text[stats_start:stats_end]
                stats = json.loads(stats_text.split(":", 1)[1])
                return True, stats
            else:
                return False, None
        except:
            return False, None

@client.event
async def on_ready():
    print("Running\n--------------------")

@client.command()
async def check(ctx, username: str):
    giturl = f"https://api.github.com/users/{username}"
    response = requests.get(giturl)

    embed = discord.Embed(title=f"Profile Check for {username}", color=discord.Color.blue())

    if response.status_code == 200:
        user_data = response.json()
        
        embed.add_field(name="GitHub Profile", value=f"[{user_data['login']}](https://github.com/{user_data['login']})", inline=False)
        embed.set_thumbnail(url=user_data['avatar_url'])
        embed.add_field(name="Name", value=user_data.get('name', 'N/A'), inline=True)
        embed.add_field(name="Bio", value=user_data.get('bio', 'N/A'), inline=False)
        embed.add_field(name="Public Repos", value=user_data['public_repos'], inline=True)
        embed.add_field(name="Followers", value=user_data['followers'], inline=True)
        embed.add_field(name="Following", value=user_data['following'], inline=True)
    else:
        embed.add_field(name="GitHub Profile", value="No GitHub account found.", inline=False)

    embed.add_field(name="--------------------------------------------", value="\u200b", inline=False)

    tik_tok_taken, tik_tok_stats = Utils.check_tiktok_username(username)
    tik_tok_status = "Available"
    tik_tok_embed_fields = []

    if tik_tok_taken:
        tik_tok_status = f"[{username}](https://www.tiktok.com/@{username}) was found\n"
        tik_tok_embed_fields.append(("Follower Count", tik_tok_stats.get('followerCount', 'N/A')))
        tik_tok_embed_fields.append(("Following Count", tik_tok_stats.get('followingCount', 'N/A')))
        tik_tok_embed_fields.append(("Heart Count", tik_tok_stats.get('heart', 'N/A')))
        tik_tok_embed_fields.append(("Video Count", tik_tok_stats.get('videoCount', 'N/A')))
        tik_tok_embed_fields.append(("Digg Count", tik_tok_stats.get('diggCount', 'N/A')))
        tik_tok_embed_fields.append(("Friend Count", tik_tok_stats.get('friendCount', 'N/A')))
    
    embed.add_field(name="TikTok Username Status", value=tik_tok_status, inline=False)
    
    for name, value in tik_tok_embed_fields:
        embed.add_field(name=name, value=value, inline=True)
    
    await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    await ctx.send("Test worked")

client.run(key)
