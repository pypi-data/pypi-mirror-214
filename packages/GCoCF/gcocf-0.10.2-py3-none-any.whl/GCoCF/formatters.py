import gettext
import locale
import os

import discord
import jdatetime
import pytz
from dateutil.parser import parse as dateutil_parse

from .models import WarStats

_ = gettext.gettext


def sanitize_input(text: str) -> str:
    # Replace markdown characters with their safe counterparts
    return (text.replace("||", "ǁ").replace("*",
                                            "∗").replace("_", "ˍ").replace(
                                                "~", "˜").replace("`", "ˋ"))


class MessageFactory:

    def __init__(self, coc_api, warinfo, clan_info):
        self.coc_api = coc_api
        self.warinfo = warinfo
        self.warstats = WarStats(warinfo)
        self.clan_info = clan_info

    def create_preparation_msg(self):
        embed = discord.Embed(
            title=f"{self.warinfo.team_size}-fold war is ahead!",
            color=0x00FF00)
        embed.set_thumbnail(url=self.clan_info.badge_url)

        home_value = f"Clan {sanitize_input(self.warinfo.clan_name)} L{self.warinfo.clan_level}\n{sanitize_input(self.clan_info.description)}"
        opponent_value = f"Clan {sanitize_input(self.warinfo.op_name)} L{self.warinfo.op_level}\n{sanitize_input(self.warinfo.opponent_description)}"

        embed.add_field(name="Home", value=home_value, inline=True)
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(name="Opponent", value=opponent_value, inline=True)

        embed.add_field(
            name="Game begins at",
            value=self.format_time(self.warinfo.start_time),
            inline=False,
        )
        return embed

    def create_players_msg(self):
        embed = discord.Embed(title="Players",
                              description="Position, name, TH",
                              color=0xFFFFFF)

        # Home clan players
        sorted_home_players_by_map_position = sorted(
            self.warinfo.clan_members.items(),
            key=lambda x: x[1]["mapPosition"])
        home_players_text = "\n".join(
            f"{player_info['mapPosition']}. {player_info['name']} (TH {player_info['townhallLevel']})"
            for player_tag, player_info in sorted_home_players_by_map_position)

        # Opponent clan players
        sorted_op_players_by_map_position = sorted(
            self.warinfo.opponent_members.items(),
            key=lambda x: x[1]["mapPosition"])
        op_players_text = "\n".join(
            f"{player_info['mapPosition']}. {player_info['name']} (TH {player_info['townhallLevel']})"
            for player_tag, player_info in sorted_op_players_by_map_position)

        # Add fields to embed
        embed.add_field(name="Home",
                        value=sanitize_input(home_players_text),
                        inline=True)
        embed.add_field(name="Opponent",
                        value=sanitize_input(op_players_text),
                        inline=True)

        return embed

    def create_war_msg(self):
        embed = discord.Embed(title=_("War has begun!"), color=0x00FF00)
        players_embed = self.create_players_msg()
        embed.add_field(
            name=f"{sanitize_input(self.warinfo.clan_name)}",
            value=sanitize_input(players_embed.fields[0].value),
            inline=True,
        )
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(
            name=f"{sanitize_input(self.warinfo.op_name)}",
            value=sanitize_input(players_embed.fields[1].value),
            inline=True,
        )
        return embed

    def create_clan_full_destruction_msg(self, attacker, attack, war_stats):
        embed = discord.Embed(title=_("⚫️ We achieved the 100% perfect war!"),
                              color=0x00FF00)
        last_attacks_home = self.create_war_summary_msg(
        ).fields[4].value.strip()

        embed.add_field(name=_("Last Attacks"),
                        value=sanitize_input(last_attacks_home),
                        inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Statistics", value="\u200b", inline=False)
        war_info_text = self.create_war_info_msg(
            self.warstats.get_latest_war_stats())
        embed.set_footer(text=war_info_text)
        return embed

    def create_clan_attack_msg(self, member, attack, war_stats):
        return self.create_attack_msg(member,
                                      attack,
                                      war_stats,
                                      color=0x00FF00)

    def create_opponent_attack_msg(self, member, attack, war_stats):
        return self.create_attack_msg(member,
                                      attack,
                                      war_stats,
                                      color=0xFF0000)

    def create_attack_msg(self, member, attack, war_stats, color):
        defender = self.warinfo.get_player_info(attack["defenderTag"])
        embed = discord.Embed(
            title=f"{sanitize_input(self.warinfo.clan_name)} vs {sanitize_input(self.warinfo.op_name)}",
            color=color,
        )
        embed.add_field(
            name="Attacker",
            value=f"TH {member['townhallLevel']} MP {member['mapPosition']} {sanitize_input(member['name'])}",
            inline=True,
        )
        embed.add_field(
            name="Defender",
            value=f"TH {defender['townhallLevel']} MP {defender['mapPosition']} {sanitize_input(defender['name'])}",
            inline=True,
        )
        embed.add_field(
            name="Result",
            value=f"{self.format_star_msg(attack)} | {attack['destructionPercentage']}%",
            inline=False,
        )
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Statistics", value="\u200b", inline=False)
        war_info_text = self.create_war_info_msg(
            self.warstats.get_latest_war_stats())
        embed.set_footer(text=war_info_text)
        return embed

    def format_star_msg(self, attack):
        new_stars = self.warstats.get_attack_new_stars(attack)
        cookies = (attack["stars"] - new_stars) * "✩"
        stars = new_stars * "⭐"
        return cookies + stars

    def create_war_info_msg(self, war_stats):
        template = _(
            """▪ {clan_attack_count: >{atkwidth}}/{total} ⭐ {clan_stars: <{swidth}} ⚡ {clan_destruction:.2f}%
▪ {opponent_attack_count: >{atkwidth}}/{total} ⭐ {opponent_stars: <{swidth}} ⚡ {opponent_destruction:.2f}%"""
        )

        clan_stars = war_stats["clan_stars"]
        op_stars = war_stats["op_stars"]
        clan_attack_count = war_stats["clan_used_attacks"]
        op_attack_count = war_stats["op_used_attacks"]

        return template.format(
            total=self.warinfo.team_size * 2,
            clan_attack_count=clan_attack_count,
            opponent_attack_count=op_attack_count,
            clan_stars=clan_stars,
            clan_destruction=war_stats["clan_destruction"],
            opponent_stars=op_stars,
            opponent_destruction=war_stats["op_destruction"],
            swidth=len(str(max(clan_stars, op_stars))),
            atkwidth=len(str(max(clan_attack_count, op_attack_count))),
        )

    def create_opponent_full_destruction_msg(self, attacker, attack,
                                             war_stats):
        embed = discord.Embed(
            title=_("⚫️ They achieved the 100% perfect war!"), color=0xFF0000)
        last_attacks_op = self.create_war_summary_msg().fields[3].value.strip()

        embed.add_field(name=_("Last Attacks"),
                        value=sanitize_input(last_attacks_op),
                        inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Statistics", value="\u200b", inline=False)
        war_info_text = self.create_war_info_msg(
            self.warstats.get_latest_war_stats())
        embed.set_footer(text=war_info_text)
        return embed

    def create_war_over_msg(self):
        if self.warinfo.is_win():
            color = 0x00FF00  # won
        elif self.warinfo.is_draw():
            color = 0xFFA500  # tie
        else:
            color = 0xFF0000  # lost

        embed = discord.Embed(title=self.create_win_or_lose_title(),
                              color=color)
        players_embed = self.create_players_msg()

        embed.add_field(
            name=f"{sanitize_input(self.warinfo.clan_name)}",
            value=sanitize_input(players_embed.fields[0].value),
            inline=True,
        )
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(
            name=f"{sanitize_input(self.warinfo.op_name)}",
            value=sanitize_input(players_embed.fields[1].value),
            inline=True,
        )
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Statistics", value="\u200b", inline=False)
        war_info_text = self.create_war_info_msg(
            self.warstats.get_latest_war_stats())
        embed.set_footer(text=war_info_text)

        return embed

    def create_win_or_lose_title(self):
        if self.warinfo.is_win():
            return "{} {}".format("🏆", _("We won!"))
        elif self.warinfo.is_draw():
            return "{} {}".format("🏳", _("It's a tie!"))
        else:
            return "{} {}".format("💩", _("We lost!"))

    def create_war_summary_msg(self):
        war_stats = self.warstats.get_latest_war_stats()
        embed = discord.Embed(title="War Summary", color=0xFFA500)

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

        clan_value = f"➥ ({clan_arrow}) {self.warinfo.clan_name[:min(25, len(self.warinfo.clan_name))]}"
        op_value = f"➥ ({op_arrow}) {self.warinfo.op_name[:min(25, len(self.warinfo.op_name))]}"

        embed.add_field(name="Home",
                        value=f"{sanitize_input(clan_value)}\n",
                        inline=True)
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(name="Opponent",
                        value=f"{sanitize_input(op_value)}\n",
                        inline=True)

        home_clan_tags = {
            player["tag"]
            for player in self.warinfo.clan_members.values()
        }
        op_clan_tags = {
            player["tag"]
            for player in self.warinfo.opponent_members.values()
        }

        def filter_attacks(attacks, clan_tags, defending=True):
            return [(player, attack) for player, attack in attacks
                    if (attack["defenderTag"] in clan_tags) == defending]

        all_attacks = list(self.warinfo.ordered_attacks.values())

        last_defences_home = filter_attacks(all_attacks,
                                            home_clan_tags,
                                            defending=True)[-5:]
        last_defences_op = filter_attacks(all_attacks,
                                          op_clan_tags,
                                          defending=True)[-5:]

        last_attacks_home = filter_attacks(all_attacks,
                                           home_clan_tags,
                                           defending=False)[-5:]
        last_attacks_op = filter_attacks(all_attacks,
                                         op_clan_tags,
                                         defending=False)[-5:]

        def format_attack_text(attacks, home_clan_tags, warinfo):
            return "\n".join(
                f"{sanitize_input(player['name'])} -> {sanitize_input(warinfo.clan_members[attack['defenderTag']]['name']) if attack['defenderTag'] in home_clan_tags else sanitize_input(warinfo.opponent_members[attack['defenderTag']]['name'])}"
                for player, attack in attacks)

        home_activity = {
            "defences":
            format_attack_text(last_defences_home, home_clan_tags,
                               self.warinfo),
            "attacks":
            format_attack_text(last_attacks_home, home_clan_tags,
                               self.warinfo),
        }
        opponent_activity = {
            "defences":
            format_attack_text(last_defences_op, home_clan_tags, self.warinfo),
            "attacks":
            format_attack_text(last_attacks_op, home_clan_tags, self.warinfo),
        }

        embed.add_field(name="Last Defences",
                        value=home_activity["defences"],
                        inline=True)
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(name="Last Defences",
                        value=opponent_activity["defences"],
                        inline=True)

        embed.add_field(name="Last Attacks",
                        value=home_activity["attacks"],
                        inline=True)
        embed.add_field(name="\u200b", value="\u200b",
                        inline=True)  # Add an empty field
        embed.add_field(name="Last Attacks",
                        value=opponent_activity["attacks"],
                        inline=True)

        # Add war statistics footer like the other embeds
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Statistics", value="\u200b", inline=False)
        war_info_text = self.create_war_info_msg(war_stats)
        embed.set_footer(text=war_info_text)

        return embed

    def format_time(self, timestamp):
        utc_time = dateutil_parse(timestamp, fuzzy=True)
        langs = {
            locale.getlocale()[0],
            os.environ.get("LANG"),
            os.environ.get("LANGUAGE"),
        }
        if langs.intersection(["fa_IR", "fa", "fa_IR.UTF-8", "Persian_Iran"]):
            self.patch_jdatetime()
            tehran_time = utc_time.astimezone(pytz.timezone("Asia/Tehran"))
            fmt = jdatetime.datetime.fromgregorian(
                datetime=tehran_time).strftime("%a، %d %b %Y %H:%M:%S")
            return self.convert_to_persian_numbers(fmt)
        return utc_time.strftime("%a, %d %b %Y %H;%M;%S")

    @staticmethod
    def patch_jdatetime():
        jdatetime.date._is_fa_locale = lambda self: True

    @staticmethod
    def convert_to_persian_numbers(text):
        # Supper intelligent and super efficient :)
        return (text.replace("0", "۰").replace("1", "۱").replace(
            "2",
            "۲").replace("3", "۳").replace("4", "۴").replace("5", "۵").replace(
                "6", "۶").replace("7", "۷").replace("8",
                                                    "۸").replace("9", "۹"))

    def get_clan_extra_info(self, clan_tag):
        return self.coc_api.get_claninfo(clan_tag)

    @staticmethod
    def create_error_embed(error_message: str) -> discord.Embed:
        return discord.Embed(title=_("Error"),
                             description=error_message,
                             color=0xFF0000)
