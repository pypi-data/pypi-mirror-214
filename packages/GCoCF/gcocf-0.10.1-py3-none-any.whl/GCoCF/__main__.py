#!/usr/bin/env python
"""GCoCF - Clash of Clans war moniting for Discord."""
import os
import time
import discord
import shelve
import gettext
import hashlib
import logging

import click

from .models import WarStats
from .formatters import MessageFactory
from .api import CoCAPI
from .notifiers import DiscordNotifier, DummyNotifier
from .utils import SimpleKVDB


gettext.bindtextdomain('messages',
                       localedir=os.path.join(
                           os.path.dirname(os.path.realpath(__file__)),
                           'locales'))
gettext.textdomain('messages')
_ = gettext.gettext

POLL_INTERVAL = 60


@click.command()
@click.option('--coc-token',
              help='CoC API token. Reads COC_API_TOKEN env var.',
              envvar='COC_API_TOKEN',
              prompt=True)
@click.option('--clan-tag',
              help='Tag of clan without hash. Reads COC_CLAN_TAG env var.',
              envvar='COC_CLAN_TAG',
              prompt=True)
@click.option('--webhook-url',
              help='Discord webhook URL. Reads DISCORD_WEBHOOK_URL env var.',
              envvar='DISCORD_WEBHOOK_URL',
              prompt=True)
@click.option('--mute-attacks',
              is_flag=True,
              help='Do not send attack updates.')
@click.option('--warlog',
              help='Warlog file path.',
              envvar='WARLOG',
              default='warlog.db',
              type=click.Path())
@click.option('--loglevel',
              default='WARNING',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL']),
              help="Set the logging level")
@click.option('--dryrun',
              is_flag=True,
              help='Do not save and send anything.')
def main(coc_token, clan_tag, webhook_url, mute_attacks, warlog,
         loglevel, dryrun):
    """Publish war updates to Discord."""
    if loglevel:
        logging.basicConfig(level=loglevel)

    coc_api = CoCAPI(coc_token)
    notifier = DiscordNotifier(webhook_url)

    if dryrun:
        warlog = 'dryrun.db'
        notifier = DummyNotifier()

    with shelve.open(warlog, writeback=True) as db:
        dbwrapper = SimpleKVDB(db)
        monitor = WarMonitor(dbwrapper, coc_api, clan_tag, notifier)
        monitor.mute_attacks = mute_attacks
        try:
            monitor.start()
        finally:
            db.sync()
            db.close()


def serverless(db, coc_token, clan_tag, webhook_url):
    """Publish war updates to Discord."""
    coc_api = CoCAPI(coc_token)
    notifier = DiscordNotifier(webhook_url)
    monitor = WarMonitor(db, coc_api, clan_tag, notifier)
    monitor.update()


########################################################################
# Main war monitor class
########################################################################

class WarMonitor(object):
    def __init__(self, db, api, tag, notifier):
        """Scan warlog for war updates.

        This is the top most class that puts everything together.
        Calling `start` method will block forever. Calling `update`
        will fetch one update, notify the changes and return.

        Arguments:
            db -- A persistant dictionary-like object.
            api -- Api object
            tag -- Clantag
            notifier -- Notifier object
        """
        self.db = db
        self.clan_tag = tag
        self.coc_api = api
        self.notifier = notifier
        self.warinfo = None
        self.msg_factory = None
        self.warstats = None
        self._mute_attacks = False

    @property
    def mute_attacks(self):
        return self._mute_attacks

    @mute_attacks.setter
    def mute_attacks(self, value):
        self._mute_attacks = value

    def update(self, wartag=None):
        warinfo = self.coc_api.get_currentwar(self.clan_tag, wartag)
        # save_latest_data(warinfo.data, monitor)
        if warinfo.is_not_in_war():
            logging.debug('Not in a war.')
            if self.warinfo is not None:
                self.send_war_over_msg()
            self.reset()
            return

        self.populate_warinfo(warinfo)
        if warinfo.is_in_preparation():
            logging.debug('War preparation.')
            self.send_preparation_msg()
        elif warinfo.is_in_war():
            logging.debug('In a war.')
            self.send_war_msg()
            if not self.mute_attacks:
                self.send_attack_msgs()
        elif warinfo.is_war_over():
            logging.debug('War is over.')
            if not self.mute_attacks:
                self.send_attack_msgs()
            self.send_war_over_msg()
            self.reset()
        else:
            print("Current war status is uknown. We stay quiet.")

    def populate_warinfo(self, warinfo):
        self.clan_tag = warinfo.clan_tag
        self.clan_info = self.coc_api.get_claninfo(self.clan_tag)
        self.warinfo = warinfo
        self.warstats = WarStats(warinfo)
        self.msg_factory = MessageFactory(self.coc_api, warinfo, self.clan_info)
        if self.get_war_id() not in self.db:
            self.db[self.get_war_id()] = {}

    def get_war_id(self):
        if not self.warinfo:
            raise ValueError('Warinfo is empty.')
        return self.warinfo.create_war_id()

    def send_preparation_msg(self):
        self.send_once(
            self.msg_factory.create_preparation_msg(),
            msg_id='preparation_msg')
        self.send_once(
            self.msg_factory.create_players_msg(),
            msg_id='players_msg')

    def send_war_msg(self):
        self.send_once(self.msg_factory.create_war_msg(), 'war_msg')

    def send_attack_msgs(self):
        for order, items in sorted(self.warinfo.ordered_attacks.items()):
            player, attack = items
            self.send_single_attack_msg(player, attack)

    def send_single_attack_msg(self, player, attack):
        war_stats = self.warstats.calculate_war_stats_sofar(attack['order'])
        if self.warinfo.is_clan_member(player):
            self.send_clan_attack_msg(player, attack, war_stats)
        else:
            self.send_opponent_attack_msg(player, attack, war_stats)

    def send_clan_attack_msg(self, attacker, attack, war_stats):
        self.send_once(
            self.msg_factory.create_clan_attack_msg(
                attacker, attack, war_stats),
            msg_id=self.get_attack_id(attack))
        if war_stats['clan_destruction'] == 100:
            self.send_once(
                self.msg_factory.create_clan_full_destruction_msg(
                    attacker, attack, war_stats),
                msg_id='clan_full_destruction')

    def is_msg_sent(self, msg_id):
        return self.db[self.get_war_id()].get(msg_id, False)

    def mark_msg_as_sent(self, msg_id):
        tmp = self.db[self.get_war_id()]
        tmp[msg_id] = True
        self.db[self.get_war_id()] = tmp

    def get_attack_id(self, attack):
        return "attack{}{}".format(attack['attackerTag'][1:],
                                   attack['defenderTag'][1:])

    def send_opponent_attack_msg(self, attacker, attack, war_stats):
        self.send_once(self.msg_factory.create_opponent_attack_msg(
            attacker, attack, war_stats),
            msg_id=self.get_attack_id(attack))
        if war_stats['op_destruction'] == 100:
            self.send_once(
                self.msg_factory.create_opponent_full_destruction_msg(
                    attacker, attack, war_stats),
                msg_id='op_full_destruction')

    def send_war_over_msg(self):
        self.send_once(
            self.msg_factory.create_war_over_msg(), msg_id='war_over_msg')

    def reset(self):
        self.warinfo = None
        self.warstats = None
        self.msg_factory = None

    def send_once(self, msg, msg_id=None):
        if not msg_id:
            msg_id = hashlib.md5(msg.encode('utf-8')).hexdigest()

        if not self.is_msg_sent(msg_id):
            self.send(msg)
            self.mark_msg_as_sent(msg_id)

    def send(self, msg):
        self.notifier.send(msg)

    def start(self):
        """Send war news to Discord."""

        last_summary_send_time = 0
        msg_factory = MessageFactory(None, None, None)

        while True:
            try:
                current_time = time.time()
                leagueinfo = self.coc_api.get_currentleague(self.clan_tag)
                if leagueinfo:
                    for previous_wartag in leagueinfo.get_previous_wartags():
                        self.update(wartag=previous_wartag)
                    current_war_tag = leagueinfo.get_current_wartag()
                    next_war_tag = leagueinfo.get_next_wartag()
                    if current_war_tag:
                        self.update(wartag=current_war_tag)
                    if next_war_tag:
                        self.update(wartag=next_war_tag)
                else:
                    self.update()

                # Send a summary message after 6 hours have passed within the war
                if current_time - last_summary_send_time >= 21600:
                    if self.warinfo and self.warinfo.is_in_war():
                        self.notifier.send(self.msg_factory.create_war_summary_msg())
                        last_summary_send_time = current_time

                time.sleep(POLL_INTERVAL)

            except Exception as err:
                try:
                    error_message = None
                    if '403' in str(err):
                        # Check whether warlog is public
                        if not self.coc_api.get_claninfo(self.clan_tag).is_warlog_public:
                            error_message = _('Warlog must be public boss! ☠️')
                    elif '500' in str(err):
                        error_message = _('CoC internal server error, retrying.')
                    elif '502' in str(err):
                        error_message = _('CoC bad gateway, retrying.')
                    elif '503' in str(err):
                        error_message = _('CoC maintenance error, retrying.')
                    elif '504' in str(err):
                        error_message = _('504 Gateway Timeout, retrying.')

                    if error_message:
                        self.notifier.send(msg_factory.create_error_embed(error_message))
                    else:
                        self.notifier.send(msg_factory.create_error_embed(_("☠️ 😵 App is broken boss! Come over and fix me please!")))

                except Exception as e:
                    raise Exception(str(e))
                raise


if __name__ == '__main__':
    main()
