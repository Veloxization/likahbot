import asyncio
import unittest
import os
from services.text_content_service import TextContentService

class TestTextContentService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/test_schema.sql")
        self.text_content_service = TextContentService(db_address)

    def tearDown(self):
        
        asyncio.run(self.text_content_service.clear_text_contents())

    def test_guild_text_contents_are_found_correctly(self):
        asyncio.run(self.text_content_service.create_text_content(1234, "Test", "TEST"))
        text_contents = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        self.assertEqual(len(text_contents), 1)

    def test_guild_text_contents_by_type_are_found_correctly(self):
        asyncio.run(self.text_content_service.create_text_content(1234, "Test1", "TEST1"))
        asyncio.run(self.text_content_service.create_text_content(1234, "Test2", "TEST2"))
        text_content = asyncio.run(self.text_content_service.get_guild_text_contents_by_type(1234, "TEST1"))
        self.assertEqual(text_content.content, "Test1")

    def test_text_contents_are_edited_correctly(self):
        asyncio.run(self.text_content_service.create_text_content(1234, "Test1", "TEST1"))
        text_contents = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        self.assertEqual(text_contents[0].content, "Test1")
        asyncio.run(self.text_content_service.edit_text_content(1234, "TEST1", "Test2"))
        text_contents = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        self.assertEqual(text_contents[0].content, "Test2")

    def test_text_contents_are_deleted_correctly(self):
        asyncio.run(self.text_content_service.create_text_content(1234, "Test", "TEST"))
        text_contents = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        self.assertEqual(len(text_contents), 1)
        asyncio.run(self.text_content_service.delete_text_content(1234, "TEST"))
        text_contents = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        self.assertEqual(len(text_contents), 0)

    def test_guild_text_contents_are_deleted_correctly(self):
        asyncio.run(self.text_content_service.create_text_content(1234))
        asyncio.run(self.text_content_service.create_text_content(2345))
        text_contents1 = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        text_contents2 = asyncio.run(self.text_content_service.get_guild_text_contents(2345))
        self.assertEqual(len(text_contents1), 1)
        self.assertEqual(len(text_contents2), 1)
        asyncio.run(self.text_content_service.delete_guild_text_contents(1234))
        text_contents1 = asyncio.run(self.text_content_service.get_guild_text_contents(1234))
        text_contents2 = asyncio.run(self.text_content_service.get_guild_text_contents(2345))
        self.assertEqual(len(text_contents1), 0)
        self.assertEqual(len(text_contents2), 1)
