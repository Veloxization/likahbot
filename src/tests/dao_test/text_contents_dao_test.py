import asyncio
import unittest
import os
from dao.text_contents_dao import TextContentsDAO

class TestTextContentsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.text_contents_dao = TextContentsDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.text_contents_dao.clear_text_contents_table())

    def test_text_contents_are_created_correctly(self):
        text_contents = asyncio.run(self.text_contents_dao.get_guild_text_contents(1234))
        self.assertEqual(len(text_contents), 0)
        asyncio.run(self.text_contents_dao.create_text_content(1234))
        text_contents = asyncio.run(self.text_contents_dao.get_guild_text_contents(1234))
        self.assertEqual(len(text_contents), 1)

    def test_text_content_is_edited_correctly(self):
        asyncio.run(self.text_contents_dao.create_text_content(1234, "Test", "TEST"))
        text_content = asyncio.run(self.text_contents_dao.get_guild_text_contents_by_type(1234, "TEST"))
        self.assertEqual(text_content["content"], "Test")
        asyncio.run(self.text_contents_dao.edit_text_content(1234, "TEST", "Testing"))
        text_content = asyncio.run(self.text_contents_dao.get_guild_text_contents_by_type(1234, "TEST"))
        self.assertEqual(text_content["content"], "Testing")

    def test_specific_text_contents_are_deleted_correctly(self):
        asyncio.run(self.text_contents_dao.create_text_content(1234, "Test", "TEST"))
        text_content = asyncio.run(self.text_contents_dao.get_guild_text_contents_by_type(1234, "TEST"))
        self.assertIsNotNone(text_content)
        asyncio.run(self.text_contents_dao.delete_text_content(1234, "TEST"))
        text_content = asyncio.run(self.text_contents_dao.get_guild_text_contents_by_type(1234, "TEST"))
        self.assertIsNone(text_content)

    def test_guild_text_contents_are_deleted_correctly(self):
        asyncio.run(self.text_contents_dao.create_text_content(1234))
        asyncio.run(self.text_contents_dao.create_text_content(2345))
        text_contents1 = asyncio.run(self.text_contents_dao.get_guild_text_contents(1234))
        text_contents2 = asyncio.run(self.text_contents_dao.get_guild_text_contents(2345))
        self.assertEqual(len(text_contents1), 1)
        self.assertEqual(len(text_contents2), 1)
        asyncio.run(self.text_contents_dao.delete_guild_text_contents(1234))
        text_contents1 = asyncio.run(self.text_contents_dao.get_guild_text_contents(1234))
        text_contents2 = asyncio.run(self.text_contents_dao.get_guild_text_contents(2345))
        self.assertEqual(len(text_contents1), 0)
        self.assertEqual(len(text_contents2), 1)
