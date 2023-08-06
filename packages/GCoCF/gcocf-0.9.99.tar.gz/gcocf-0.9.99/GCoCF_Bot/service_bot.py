import discord
import os
import subprocess
import asyncio
from discord.ext import commands
from discord import Intents
import interactions
from interactions import listen, SlashContext, slash_command, OptionType, slash_option, ChannelType, slash_default_member_permission

import database as db

bot = interactions.Client()

BOT_OWNER_USER_ID = int(os.getenv("BOT_OWNER_USER_ID"))  # Use a specific user ID as bot owner

async def run_subprocess(command: str) -> None:
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()

@listen()
async def on_startup():
    db.setup_database()
    #db.setup_whitelist_table()

async def is_whitelisted(ctx: SlashContext) -> bool:
    user_id = ctx.author.id
    if await db.is_user_whitelisted(user_id):
        return True
    else:
        await ctx.send("You are not whitelisted to use this command.")
        return False

async def store(ctx, api_key: str, webhook_url: str, clan_tag: str):
    user_id = ctx.author.id
    if ctx.guild is not None:
        await ctx.send("Send this command via direct message!")
        return
    await db.store_user_data(user_id, api_key, webhook_url, clan_tag)
    await ctx.send("The data has been stored successfully.")

@slash_command(name="store", description="Stores user data")
@slash_option(
    name="api_key",
    description="CoC API Key",
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
async def slash_store(ctx: SlashContext, api_key: str, webhook_url: str, clan_tag: str):
    if not await is_whitelisted(ctx):
        return

    user_id = ctx.author.id
    await store(ctx, api_key, webhook_url, clan_tag)

async def start_instance_for_user(user_id: int):
    user_data = await db.get_user_data(user_id)
    if user_data and user_data[4] == 0:
        user_id, api_key, webhook_url, clan_tag, _ = user_data
        container_name = f'user_{user_id}_instance'
        run_command = f'docker run -d --name {container_name} ghcr.io/gillesmaster/gcocf/gcocf:latest --coc-token {api_key} --webhook-url {webhook_url} --clan-tag \'{clan_tag}\''
        
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
    if user_data and user_data[4] == 1:
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
    except interactions.HTTPException as e:
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
    except interactions.HTTPException as e:
        print(f"Error in stop_instance command: {e}")

@slash_command(
    name="add_to_whitelist",
    description="Add a user to the whitelist"
)
@slash_option(
    name="target_user",
    description="The user to be whitelisted",
    required=True,
    opt_type=OptionType.USER
)
async def add_to_whitelist(ctx: SlashContext, target_user: discord.User):
    user_id = ctx.author.id

    # Only allow the bot owner to run this command
    if user_id != BOT_OWNER_USER_ID:
        await ctx.send("You do not have permission to use this command.")
        return

    target_id = target_user.id

    await db.add_user_to_whitelist(target_id)

    await ctx.send(f"User {target_user.name} has been added to the whitelist.")

bot.start(os.getenv("DISCORD_TOKEN"))