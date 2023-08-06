import discord
import os
import subprocess
import asyncio
import urllib.parse
import requests
from discord.ext import commands
from discord import Intents
import interactions
from interactions import listen, SlashContext, slash_command, OptionType, slash_option, ChannelType, slash_default_member_permission

import database as db

bot = interactions.Client()

BOT_OWNER_USER_ID = int(os.getenv("BOT_OWNER_USER_ID", "630052168963194885"))  # Use a specific user ID as bot owner
DEV_API_KEY = os.getenv("COC_API_TOKEN", None)

async def run_subprocess(command: str) -> None:
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()

async def send_error_message(ctx: SlashContext, error: Exception):
    print(f"An error occurred: {error}")
    await ctx.send("An error occurred. Please contact the bot owner for assistance.")

@listen()
async def on_startup():
    db.setup_database()
    #db.setup_whitelist_table()

async def verify_player_token(player_tag: str, player_token: str) -> bool:
    headers = {"Authorization": f"Bearer {DEV_API_KEY}"}
    data = {"token": player_token}

    encoded_player_tag = urllib.parse.quote(player_tag)

    try:
        response = requests.post(f"https://api.clashofclans.com/v1/players/{encoded_player_tag}/verifytoken", headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error verifying player token: {e}")
        return False

async def is_whitelisted(ctx: SlashContext) -> bool:
    user_id = ctx.author.id
    if await db.is_user_whitelisted(user_id):
        return True
    else:
        await ctx.send("You are not whitelisted to use this command.")
        return False

async def store(ctx, player_token: str, player_tag: str, webhook_url: str, clan_tag: str):
    user_id = ctx.author.id
    if ctx.guild is not None:
        await ctx.send("Send this command via direct message!")
        return

    if await verify_player_token(player_tag, player_token):
        await db.store_user_data(user_id, player_token, player_tag, webhook_url, clan_tag)
        await ctx.send("The data has been stored successfully.")
    else:
        await ctx.send("Player token verification failed. Please provide a valid token.")

@slash_command(name="store", description="Stores user data")
@slash_option(
    name="player_token",
    description="CoC Player Token",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="player_tag",
    description="CoC Player Tag",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="webhook_url",
    description="Webhook URL",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="clan_tag",
    description="Clan Tag",
    required=True,
    opt_type=OptionType.STRING
)
async def slash_store(ctx: SlashContext, player_token: str, player_tag: str, webhook_url: str, clan_tag: str):
    if not await is_whitelisted(ctx):
        return

    user_id = ctx.author.id
    try:
        await store(ctx, player_token, player_tag, webhook_url, clan_tag)
    except Exception as e:
        await send_error_message(ctx, e)

async def start_instance_for_user(user_id: int):
    user_data = await db.get_user_data(user_id)
    key = DEV_API_KEY
    if user_data and user_data[5] == 0:
        user_id, player_token, player_tag, webhook_url, clan_tag, _ = user_data
        # Check if the saved player token is valid
        if not await verify_player_token(player_tag, player_token):
            return False, "Player token verification failed. Please update your token."

        container_name = f'user_{user_id}_instance'
        run_command = f'docker run -d --pull=always --name {container_name} ghcr.io/gillesmaster/gcocf/gcocf:latest --coc-token {key} --webhook-url {webhook_url} --clan-tag \'{clan_tag}\''
        
        try:
            await run_subprocess(run_command)
            await db.update_instance_count(user_id, 1)
            return True, "Instance started successfully."
        except Exception as e:
            print(f"Error in start_instance_for_user: {e}")
            return False, "Failed to start the instance."

    return False, "Failed to start the instance: Missing data or an instance is already running."

async def stop_instance_for_user(user_id: int):
    user_data = await db.get_user_data(user_id)
    if user_data and user_data[5] == 1:
        container_name = f'user_{user_id}_instance'
        stop_command = f'docker stop {container_name} && docker rm {container_name}'

        try:
            await run_subprocess(stop_command)
            await db.update_instance_count(user_id, 0)
            return True, "Instance stopped successfully."
        except Exception as e:
            print(f"Error in stop_instance_for_user: {e}")
            return False, "Failed to stop the instance."

    return False, "Failed to stop the instance: No instance is running for the user."

@interactions.slash_command(
    name="start_instance",
    description="Starts an instance for the user"
)
async def start_instance(ctx: SlashContext):
    if not await is_whitelisted(ctx):
        return

    user_id = ctx.author.id
    success, message = await start_instance_for_user(user_id)
    try:
        await ctx.send(message, followup=True)
    except HTTPException as e:
        print(f"Error in start_instance command: {e}")

@interactions.slash_command(
    name="stop_instance",
    description="Stops an instance for the user"
)
async def stop_instance(ctx: SlashContext):
    if not await is_whitelisted(ctx):
        return

    user_id = ctx.author.id
    success, message = await stop_instance_for_user(user_id)
    try:
        await ctx.send(message, followup=True)
    except HTTPException as e:
        print(f"Error in stop_instance command: {e}")

@slash_command(
    name="add_to_whitelist",
    description="Add a user to the whitelist"
)
@slash_option(
    name="target_user_id",
    description="The UserID to be whitelisted",
    required=True,
    opt_type=OptionType.STRING  # Change the type back to OptionType.STRING
)
async def add_to_whitelist(ctx: SlashContext, target_user_id: str):  # Update the type of target_user_id to str
    user_id = ctx.author.id

    # Only allow the bot owner to run this command
    if user_id != BOT_OWNER_USER_ID:
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        target_user = await bot.fetch_user(int(target_user_id))  # Fetch the user using the provided user ID
    except Exception as e:
        await send_error_message(ctx, e)
        return

    target_id = target_user.id

    try:
        await db.add_user_to_whitelist(target_id)
        await ctx.send(f"User {target_user.display_name} has been added to the whitelist.")
    except Exception as e:
        await send_error_message(ctx, e)

bot.start(os.getenv("DISCORD_TOKEN", None))