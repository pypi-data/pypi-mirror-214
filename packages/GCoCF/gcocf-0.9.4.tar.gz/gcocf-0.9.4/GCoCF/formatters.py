########################################################################
# Message formatters
########################################################################
import os
import locale
import gettext
from dateutil.parser import parse as dateutil_parse

import pytz
import jdatetime
import discord

from .models import WarStats

_ = gettext.gettext


class MessageFactory(object):
    def __init__(self, coc_api, warinfo, clan_info):
        self.coc_api = coc_api
        self.warinfo = warinfo
        self.warstats = WarStats(warinfo)
        self.clan_info = clan_info

    def create_preparation_msg(self):
        embed = discord.Embed(title=f"{self.warinfo.team_size}-fold war is ahead!", color=0x00ff00)
        embed.set_thumbnail(url=self.clan_info.badge_url)
        embed.add_field(name=f"{self.warinfo.clan_name} L{self.warinfo.clan_level}", value=self.clan_info.description, inline=True)
        embed.add_field(name=f"{self.warinfo.op_name} L{self.warinfo.op_level}", value=self.warinfo.opponent_description, inline=True)
        embed.add_field(name="Game begins at", value=self.format_time(self.warinfo.start_time), inline=False)
        embed.set_footer(text="Have fun!")
        return embed

    def create_players_msg(self):
        embed = discord.Embed(title="Players", description="Position, TH, name", color=0xffffff)
        sorted_players_by_map_position = sorted(
            self.warinfo.clan_members.items(),
            key=lambda x: x[1]['mapPosition'])
        for player_tag, player_info in sorted_players_by_map_position:
            embed.add_field(name=f"{player_info['mapPosition']}. {player_info['name']}", value=f"TH {player_info['townhallLevel']}", inline=True)
        return embed

    def create_war_msg(self):
        return _('War has begun!')

    def create_clan_full_destruction_msg(self, attacker, attack, war_stats):
        return _('We destroyed them 100% boss!')

    def create_clan_attack_msg(self, member, attack, war_stats):
        return self.create_attack_msg(member, attack, war_stats, color=0x00ff00)

    def create_opponent_attack_msg(self, member, attack, war_stats):
        return self.create_attack_msg(member,
    attack, war_stats, color=0xff0000)

    def create_attack_msg(self, member, attack, war_stats, color):
        defender = self.warinfo.get_player_info(attack['defenderTag'])
        embed = discord.Embed(title=f"{self.warinfo.clan_name} vs {self.warinfo.op_name}", color=color)
        embed.add_field(name="Attacker", value=f"TH {member['townhallLevel']} MP {member['mapPosition']} {member['name']}", inline=True)
        embed.add_field(name="Defender", value=f"TH {defender['townhallLevel']} MP {defender['mapPosition']} {defender['name']}", inline=True)
        embed.add_field(name="Result", value=f"{self.format_star_msg(attack)} | {attack['destructionPercentage']}%", inline=False)
        embed.set_footer(text=self.create_war_info_msg(war_stats))
        return embed

    def format_star_msg(self, attack):
        new_stars = self.warstats.get_attack_new_stars(attack)
        cookies = (attack['stars'] - new_stars) * '🍪'
        stars = new_stars * '⭐'
        return cookies + stars

    def create_war_info_msg(self, war_stats):
        template = _("""▪ {clan_attack_count: >{atkwidth}}/{total} ⭐ {clan_stars: <{swidth}} ⚡ {clan_destruction:.2f}%
▪ {opponent_attack_count: >{atkwidth}}/{total} ⭐ {opponent_stars: <{swidth}} ⚡ {opponent_destruction:.2f}%""")

        clan_stars = war_stats['clan_stars']
        op_stars = war_stats['op_stars']
        clan_attack_count = war_stats['clan_used_attacks']
        op_attack_count = war_stats['op_used_attacks']

        return template.format(
            total=self.warinfo.team_size * 2,
            clan_attack_count=clan_attack_count,
            opponent_attack_count=op_attack_count,
            clan_stars=clan_stars,
            clan_destruction=war_stats['clan_destruction'],
            opponent_stars=op_stars,
            opponent_destruction=war_stats['op_destruction'],
            swidth=len(str(max(clan_stars, op_stars))),
            atkwidth=len(str(max(clan_attack_count, op_attack_count))))

    def create_opponent_full_destruction_msg(self, attacker, attack,
                                             war_stats):
        return _('⚫️ They destroyed us 100% boss!')

    def create_war_over_msg(self):
        embed = discord.Embed(title=self.create_win_or_lose_title())
        embed.add_field(name=f"Clan {self.warinfo.clan_name}", value=f"L {self.warinfo.clan_level}", inline=True)
        embed.add_field(name=f"Clan {self.warinfo.op_name}", value=f"L {self.warinfo.op_level}", inline=True)
        embed.add_field(name="War Info", value=self.create_war_info_msg(self.warstats.get_latest_war_stats()), inline=False)
        return embed

    def create_win_or_lose_title(self):
        if self.warinfo.is_win():
            return "{} {}".format('🎉', _('We won!'))
        elif self.warinfo.is_draw():
            return "{} {}".format('🏳', _('It\'s a tie!'))
        else:
            return "{} {}".format('💩', _('We lost!'))

    def format_time(self, timestamp):
        utc_time = dateutil_parse(timestamp, fuzzy=True)
        langs = set([locale.getlocale()[0],
                    os.environ.get('LANG'),
                    os.environ.get('LANGUAGE')])
        if langs.intersection(['fa_IR', 'fa', 'fa_IR.UTF-8', 'Persian_Iran']):
            self.patch_jdatetime()
            tehran_time = utc_time.astimezone(pytz.timezone("Asia/Tehran"))
            fmt = jdatetime.datetime.fromgregorian(
                datetime=tehran_time).strftime("%a، %d %b %Y %H:%M:%S")
            return self.convert_to_persian_numbers(fmt)
        return utc_time.strftime("%a, %d %b %Y %H:%M:%S")

    def patch_jdatetime(self):
        jdatetime.date._is_fa_locale = lambda self: True

    def convert_to_persian_numbers(self, text):
        # Supper intelligent and super efficient :)
        return text.replace('0', '۰')\
                   .replace('1', '۱')\
                   .replace('2', '۲')\
                   .replace('3', '۳')\
                   .replace('4', '۴')\
                   .replace('5', '۵')\
                   .replace('6', '۶')\
                   .replace('7', '۷')\
                   .replace('8', '۸')\
                   .replace('9', '۹')

    def get_clan_extra_info(self, clan_tag):
        return self.coc_api.get_claninfo(clan_tag)
