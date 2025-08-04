import discord
from discord.ext import commands
import random
import os
import json
from collections import defaultdict

STATS_FILE = "banana_stats.json"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# List of banana image URLs
banana_images = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bb/Banana_on_whitebackground.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/4e/Bananen_Frucht.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1c/Bananas_white_background.jpg",
    # Add more links here
]

# List of random banana facts
banana_facts = [
    "Bananas are berries, but strawberries aren't!",
    "Bananas float in water because they are less dense than water.",
    "Humans share about 60% of their DNA with bananas.",
    "Bananas can help improve your mood thanks to their vitamin B6.",
    "There are more than 1,000 varieties of bananas worldwide!",
    # Add more fun facts
    "Bananas don't grow on trees — they're actually giant herbs!",
    "The inside of a banana peel can help polish leather shoes.",
    "Rubbing banana peel on your skin may help reduce itching and irritation.",
    "Bananas are naturally radioactive due to their potassium-40 content.",
    "Over 100 billion bananas are eaten each year — more than any other fruit!",
    "Uganda has the highest per-capita banana consumption in the world.",
    "A cluster of bananas is called a 'hand,' and a single banana is a 'finger.'",
    "The Cavendish is the most common banana variety worldwide.",
    "Bananas were first domesticated in Southeast Asia over 7,000 years ago.",
    "Refrigerating bananas slows ripening but may cause the peel to turn black.",
    "Bananas produce more ethylene gas than most fruits, speeding ripening.",
    "There’s a banana museum in California with over 20,000 banana-related items!",
    "Bananas can help athletes avoid cramps due to their potassium content.",
    "The word 'banana' comes from the Arabic word 'banan,' meaning finger.",
    "Bananas were first introduced to the U.S. at the 1876 Philadelphia World’s Fair."
]

def load_stats():
    if not os.path.exists(STATS_FILE):
        return defaultdict(int)
    with open(STATS_FILE, "r") as f:
        data = json.load(f)
        return defaultdict(int, {int(k): v for k, v in data.items()})

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def banana(ctx):
    image_url = random.choice(banana_images)
    fact = random.choice(banana_facts)
    embed = discord.Embed(description=fact, color=0xffff00)
    embed.set_image(url=image_url)
    
    # Load stats, update usage, and save
    stats = load_stats()
    stats[ctx.author.id] += 1
    save_stats(stats)
    
    await ctx.send(embed=embed)
    
@bot.command()
async def bananaboard(ctx):
    stats = load_stats()
    if not stats:
        await ctx.send("No banana fans yet 🍌")
        return

    # Sort users by banana count, descending
    top_users = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Rank icons
    rank_emojis = ["🥇", "🥈", "🥉"]

    description = ""
    for i, (user_id, count) in enumerate(top_users, start=1):
        try:
            member = await ctx.guild.fetch_member(user_id)
            display_name = member.nick or member.name
        except discord.NotFound:
            display_name = f"User ID {user_id}"
        except discord.Forbidden:
            display_name = f"Hidden User"
        except discord.HTTPException:
            display_name = f"Error loading user"

        # Add emoji for top 3, otherwise just number
        rank = rank_emojis[i - 1] if i <= 3 else f"{i}."

        description += f"{rank} **{display_name}** — {count} bananas\n"

    embed = discord.Embed(title="🍌 Banana Leaderboard:", description=description, color=0xffff00)
    await ctx.send(embed=embed)

bot.run(os.getenv("BOT_TOKEN"))
