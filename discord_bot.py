import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageOps 
import sqlite3
import requests
from io import BytesIO
import os

def fetch_background_color(token_id):
    conn = sqlite3.connect('nft_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT color FROM nfts WHERE LOWER(token_id) = LOWER(?) LIMIT 1
    ''', (token_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def fetch_nft_image_link(token_id):
    conn = sqlite3.connect('nft_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT image_link FROM nfts WHERE LOWER(token_id) = LOWER(?) LIMIT 1
    ''', (token_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def create_discord_banner(token_id):

    background_color = fetch_background_color(token_id)
    if not background_color:
        return None, f"NFT with token ID {token_id} not found in the database."
    
    banner_width = 1700
    banner_height = 600
    banner = Image.new('RGB', (banner_width, banner_height), color=background_color)

    nft_image_link = fetch_nft_image_link(token_id)
    if not nft_image_link:
        return None, f"Image link for NFT with token ID {token_id} not found in the database."
   
    try:
        response = requests.get(nft_image_link)
        nft_image = Image.open(BytesIO(response.content))
    except Exception as e:
        return None, f"Error downloading or opening image for NFT with token ID {token_id}: {e}"

    inverted_nft_image = ImageOps.mirror(nft_image)
   
    resized_nft_image = inverted_nft_image.resize((600, 600))

    paste_x = banner_width - resized_nft_image.width
    paste_y = int((banner_height - resized_nft_image.height) / 2)

    banner.paste(resized_nft_image, (paste_x, paste_y))

    file_path = f'discord_banner_token_{token_id}.png'
    banner.save(file_path)
    return file_path, None


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


owner_user_id = {owner_id}
@bot.tree.command(name="generate_banner", description="Generate a banner for a given token ID")
@app_commands.describe(token_id="The token ID for the NFT")
async def generate_banner(interaction: discord.Interaction, token_id: str):
    await interaction.response.defer(ephemeral=True)
    
    file_path, error = create_discord_banner(token_id.lower())
    
    if error:
        await interaction.followup.send(content=error, ephemeral=True)
    else:
        await interaction.followup.send(file=discord.File(file_path), ephemeral=True)

        owner_user = await bot.fetch_user(owner_user_id)
        await owner_user.send(f"{interaction.user.name} created a banner with token ID {token_id}")
        
        os.remove(file_path)  

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')


bot_token = str(os.getenv("BOT_TOKEN"))
bot.run(bot_token)
