########################################################################
# Notifiers
########################################################################
# notifier.py
import requests
import json
import discord

class DiscordNotifier(object):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, msg, silent=False):
        payload = {}

        if isinstance(msg, str):
            payload = {
                "content": msg,
                "tts": not silent
            }
        elif isinstance(msg, discord.Embed):
            payload = {
                "embeds": [msg.to_dict()],  # Convert the discord.Embed object to JSON format
                "tts": not silent
            }

        headers = {
            "Content-Type": "application/json"
        }

        requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)

class DummyNotifier(object):
    def send(self, msg, silent=False):
        if not silent:
            print(msg)