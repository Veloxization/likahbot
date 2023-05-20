import asyncio
import unittest
import os
from dao.left_members_dao import LeftMembersDAO

class TestTextContentsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.left_members_dao = LeftMembersDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.left_members_dao.clear_left_members_table())

    def test_left_members_are_added_correctly(self):
        left_members = asyncio.run(self.left_members_dao.get_all_guild_left_members(1234))
        self.assertEqual(len(left_members), 0)
        asyncio.run(self.left_members_dao.add_left_member(9876, 1234))
        left_members = asyncio.run(self.left_members_dao.get_all_guild_left_members(1234))
        self.assertEqual(len(left_members), 1)

    def test_left_members_are_deleted_correctly(self):
        asyncio.run(self.left_members_dao.add_left_member(9876, 1234))
        left_member = asyncio.run(self.left_members_dao.get_guild_left_member(9876, 1234))
        self.assertIsNotNone(left_member)
        asyncio.run(self.left_members_dao.remove_left_member(9876, 1234))
        left_member = asyncio.run(self.left_members_dao.get_guild_left_member(9876, 1234))
        self.assertIsNone(left_member)

    def test_records_of_a_left_member_are_deleted_correctly(self):
        asyncio.run(self.left_members_dao.add_left_member(9876, 1234))
        asyncio.run(self.left_members_dao.add_left_member(9876, 2345))
        left_member_records = asyncio.run(self.left_members_dao.get_left_member(9876))
        self.assertEqual(len(left_member_records), 2)
        asyncio.run(self.left_members_dao.remove_all_member_records(9876))
        left_member_records = asyncio.run(self.left_members_dao.get_left_member(9876))
        self.assertEqual(len(left_member_records), 0)

    def test_records_of_a_guild_are_deleted_correctly(self):
        asyncio.run(self.left_members_dao.add_left_member(9876, 1234))
        asyncio.run(self.left_members_dao.add_left_member(9876, 2345))
        left_members1 = asyncio.run(self.left_members_dao.get_all_guild_left_members(1234))
        left_members2 = asyncio.run(self.left_members_dao.get_all_guild_left_members(2345))
        self.assertEqual(len(left_members1), 1)
        self.assertEqual(len(left_members2), 1)
        asyncio.run(self.left_members_dao.remove_guild_left_member_records(1234))
        left_members1 = asyncio.run(self.left_members_dao.get_all_guild_left_members(1234))
        left_members2 = asyncio.run(self.left_members_dao.get_all_guild_left_members(2345))
        self.assertEqual(len(left_members1), 0)
        self.assertEqual(len(left_members2), 1)
