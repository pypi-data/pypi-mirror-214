import discord
import os
import subprocess
from discord.ext import commands

import database as db

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    db.setup_database()

@bot.command()
async def store(ctx, api_key: str, webhook_url: str, clant_tag: str):
    user_id = ctx.author.id
    if ctx.guild is not None:
        await ctx.message.delete()
        await ctx.send("Send this command via direct message!")
        return
    await db.store_user_data(user_id, api_key, webhook_url, clant_tag)

@bot.command()
async def start_instance(ctx):
    user_id = ctx.author.id
    success, msg = await start_instance_for_user(user_id)
    await ctx.send(msg)

@bot.command()
async def stop_instance(ctx):
    user_id = ctx.author.id
    success, msg = await stop_instance_for_user(user_id)
    await ctx.send(msg)

async def start_instance_for_user(user_id: int):
    user_data = await db.get_user_data(user_id)
    if user_data and user_data[4] == 0:
        user_id, api_key, webhook_url, clan_tag, _ = user_data
        container_name = f'user_{user_id}_instance'
        run_command = f'docker run -e COC_API_KEY={api_key} -e WEBHOOK_URL={webhook_url} -e CLAN_TAG={clan_tag} --name {container_name} your_container_image'

        try:
            subprocess.run(run_command, shell=True, check=True)
            await db.update_instance_count(user_id, 1)
            return True, "Instance started successfully."
        except subprocess.CalledProcessError:
            print(run_command)
            return False, "Failed to start the instance."

    return False, "Failed to start the instance: Missing data or an instance is already running."

async def stop_instance_for_user(user_id: int):
    user_data = await db.get_user_data(user_id)
    if user_data and user_data[4] == 1:
        container_name = f'user_{user_id}_instance'
        stop_command = f'docker stop {container_name} && docker rm {container_name}'

        try:
            subprocess.run(stop_command, shell=True, check=True)
            await db.update_instance_count(user_id, 0)
            return True, "Instance stopped successfully."
        except subprocess.CalledProcessError:
            return False, "Failed to stop the instance."

    return False, "Failed to stop the instance: No instance is running for the user."

bot.run(os.getenv("DISCORD_TOKEN"))