import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import database as db

DB_NAME = "test_service_bot.db"


def setup_test_database():
    db.DB_NAME = DB_NAME
    db.setup_database()


def remove_test_database():
    os.remove(DB_NAME)


def mock_start(*args, **kwargs):
    """Dummy function."""
    pass  # skipcq


class MockClient:
    start = mock_start


with patch("interactions.Client", MockClient):
    from service_bot import is_whitelisted


class TestIsWhitelisted(unittest.IsolatedAsyncioTestCase):
    async def test_is_whitelisted(self):
        ctx = MagicMock()
        ctx.author.id = 12345
        ctx.send = AsyncMock()  # Make ctx.send an AsyncMock
        db.is_user_whitelisted = AsyncMock(return_value=True)

        result = await is_whitelisted(ctx)
        self.assertTrue(result)

        db.is_user_whitelisted.return_value = False

        result = await is_whitelisted(ctx)
        self.assertFalse(result)
        ctx.send.assert_called_once_with(
            "You are not whitelisted to use this command.")


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_test_database()

    @classmethod
    def tearDownClass(cls):
        remove_test_database()

    async def test_whitelist_functions(self):
        test_user_id = 630052168963194885

        await db.add_user_to_whitelist(test_user_id)

        self.assertTrue(await db.is_user_whitelisted(test_user_id))

    async def test_user_data_storage(self):
        test_user_id = 630052168963194885
        player_token = "grdfgrd5"
        player_tag = "#PPUYPYYPL"
        webhook_url = "https://test-webhook-url.com"
        clan_tag = "#2QJ8Q09J8"

        await db.store_user_data(
            test_user_id, player_token, player_tag, webhook_url, clan_tag
        )

        user_data = await db.get_user_data(test_user_id)

        expected_data = (
            test_user_id,
            player_token,
            player_tag,
            webhook_url,
            clan_tag,
            0,
        )

        self.assertEqual(user_data, expected_data)

        new_player_token = "r34re5t4"
        new_player_tag = "#PPUYWYFWM"
        new_webhook_url = "https://new-webhook-url.com"
        new_clan_tag = "#46GSYR63J"

        await db.store_user_data(
            test_user_id,
            new_player_token,
            new_player_tag,
            new_webhook_url,
            new_clan_tag,
        )

        updated_user_data = await db.get_user_data(test_user_id)

        expected_updated_data = (
            test_user_id,
            new_player_token,
            new_player_tag,
            new_webhook_url,
            new_clan_tag,
            0,
        )

        self.assertEqual(updated_user_data, expected_updated_data)


if __name__ == "__main__":
    unittest.main()
