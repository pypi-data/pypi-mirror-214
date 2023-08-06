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
        embed.set_footer(text=self.create_war_info_msg(self.warstats.get_latest_war_stats()))
        return embed

    def create_players_msg(self):
        embed = discord.Embed(title="Players", description="Position, name, TH", color=0xffffff)

        # Home clan players
        sorted_home_players_by_map_position = sorted(
            self.warinfo.clan_members.items(),
            key=lambda x: x[1]['mapPosition'])
        home_players_text = "\n".join(f"{player_info['mapPosition']}. {player_info['name']} (TH {player_info['townhallLevel']})" for player_tag, player_info in sorted_home_players_by_map_position)

        # Opponent clan players
        sorted_op_players_by_map_position = sorted(
            self.warinfo.opponent_members.items(),
            key=lambda x: x[1]['mapPosition'])
        op_players_text = "\n".join(f"{player_info['mapPosition']}. {player_info['name']} (TH {player_info['townhallLevel']})" for player_tag, player_info in sorted_op_players_by_map_position)

        # Add fields to embed
        embed.add_field(name="Home", value=home_players_text, inline=True)
        embed.add_field(name="Opponent", value=op_players_text, inline=True)

        return embed

    def create_war_msg(self):
        embed = discord.Embed(description=_("War has begun!"), color=0x00ff00)
        embed.add_field(name=_("Players"), value="\n" + "=" * 40 + "\n", inline=True)
        players_embed = self.create_players_msg()
        embed.add_field(name=_("Home"), value=players_embed.fields[0].value, inline=True)
        embed.add_field(name=_("Opponent"), value=players_embed.fields[1].value, inline=True)
        embed.set_footer(text=self.create_war_info_msg(self.warstats.get_latest_war_stats()))
        return embed

    def create_clan_full_destruction_msg(self, attacker, attack, war_stats):
        embed = discord.Embed(description=_("⚫️ We achieved the 100% perfect war!"), color=0x00ff00)
        last_attacks_home = self.create_war_summary_msg().fields[2].value.strip()

        embed.add_field(name=_("Last Attacks"), value=last_attacks_home, inline=True)
        embed.set_footer(text=self.create_war_info_msg(war_stats))
        return embed

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
        cookies = (attack['stars'] - new_stars) * '✩'
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

    def create_opponent_full_destruction_msg(self, attacker, attack, war_stats):
        embed = discord.Embed(description=_("⚫️ They achieved the 100% perfect war!"), color=0xff0000)
        last_attacks_op = self.create_war_summary_msg().fields[3].value.strip()

        embed.add_field(name=_("Last Attacks"), value=last_attacks_op, inline=True)
        embed.set_footer(text=self.create_war_info_msg(war_stats))
        return embed

    def create_war_over_msg(self):
        embed = discord.Embed(title=self.create_win_or_lose_title())
        embed.add_field(name=f"Clan {self.warinfo.clan_name}", value=f"L {self.warinfo.clan_level}", inline=True)
        embed.add_field(name=f"Clan {self.warinfo.op_name}", value=f"L {self.warinfo.op_level}", inline=True)
        embed.add_field(name="War Info", value=self.create_war_info_msg(self.warstats.get_latest_war_stats()), inline=False)
        return embed

    def create_win_or_lose_title(self):
        if self.warinfo.is_win():
            return "{} {}".format('🏆', _('We won!'))
        elif self.warinfo.is_draw():
            return "{} {}".format('🏳', _('It\'s a tie!'))
        else:
            return "{} {}".format('💩', _('We lost!'))

    def create_war_summary_msg(self):
        war_stats = self.warstats.get_latest_war_stats()
        embed = discord.Embed(title="War Summary", color=0xffa500)

        # Determine the winning and losing clans
        if self.warinfo.clan_stars > self.warinfo.op_stars:
            clan_arrow = "🟢"
            op_arrow = "🔴"
        elif self.warinfo.clan_stars < self.warinfo.op_stars:
            clan_arrow = "🔴"
            op_arrow = "🟢"
        else:  # Equal stars
            clan_arrow = "🟡"
            op_arrow = "🟡"

        # Display long clan names without wrapping
        clan_value = f"➥ ({clan_arrow}) {self.warinfo.clan_name[:min(25, len(self.warinfo.clan_name))]}"
        op_value = f"➥ ({op_arrow}) {self.warinfo.op_name[:min(25, len(self.warinfo.op_name))]}"

        embed.add_field(value=clan_value, name="Home", inline=True)
        embed.add_field(value=op_value, name="Opponent", inline=True)

        home_clan_tags = [player["tag"] for player in self.warinfo.clan_members.values()]
        op_clan_tags = [player["tag"] for player in self.warinfo.opponent_members.values()]
        match = {"home": self.warinfo.clan_members, "away": self.warinfo.opponent_members}

        def filter_attacks(ordered_attacks, defender_clan_tags):
            return [(player, attack) for player, attack in ordered_attacks if attack["defenderTag"] in defender_clan_tags]

        all_attacks = list(self.warinfo.ordered_attacks.values())

        last_defences_home = filter_attacks(all_attacks, home_clan_tags)[-5:]
        last_defences_text_home = "\n".join(f"{player['name']} -> {match['home' if attack['defenderTag'] in home_clan_tags else 'away'][attack['defenderTag']]['name']}" for player, attack in last_defences_home)

        last_defences_op = filter_attacks(all_attacks, op_clan_tags)[-5:]
        last_defences_text_op = "\n".join(f"{player['name']} -> {match['home' if attack['defenderTag'] in home_clan_tags else 'away'][attack['defenderTag']]['name']}" for player, attack in last_defences_op)

        last_attacks_home = filter_attacks(all_attacks, home_clan_tags)[:5]
        last_attacks_text_home = "\n".join(f"{player['name']} -> {match['home' if attack['defenderTag'] in home_clan_tags else 'away'][attack['defenderTag']]['name']}" for player, attack in last_attacks_home)

        last_attacks_op = filter_attacks(all_attacks, op_clan_tags)[:5]
        last_attacks_text_op = "\n".join(f"{player['name']} -> {match['home' if attack['defenderTag'] in home_clan_tags else 'away'][attack['defenderTag']]['name']}" for player, attack in last_attacks_op)

        embed.add_field(name="Last Defences", value=last_defences_text_home.strip(), inline=True)
        embed.add_field(name="Last Defences", value=last_defences_text_op.strip(), inline=True)
        embed.add_field(name="Last Attacks", value=last_attacks_text_home.strip(), inline=True)
        embed.add_field(name="Last Attacks", value=last_attacks_text_op.strip(), inline=True)

        # Add war statistics footer like the other embeds
        war_info_text = self.create_war_info_msg(war_stats)
        embed.set_footer(text=war_info_text)

        return embed

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
        return utc_time.strftime("%a, %d %b %Y %H.%M.%S")

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

    @staticmethod
    def create_error_embed(error_message: str) -> discord.Embed:
        return discord.Embed(title=_("Error"), description=error_message, color=0xFF0000)
