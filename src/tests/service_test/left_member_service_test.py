import unittest
import os
from services.left_member_service import LeftMemberService

class TestLeftMemberService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.left_member_service = LeftMemberService(db_address)

    def tearDown(self):
        self.left_member_service.clear_left_members()

    def test_guild_left_members_are_found_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        members = self.left_member_service.get_all_guild_left_members(9876)
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].user_id, 1234)

    def test_all_left_members_are_found_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(2345, 8765)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 2)

    def test_guild_left_member_is_found_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(2345, 9876)
        member = self.left_member_service.get_guild_left_member(1234, 9876)
        self.assertEqual(member.user_id, 1234)

    def test_left_member_is_found_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(1234, 8765)
        members = self.left_member_service.get_left_member(1234)
        self.assertEqual(len(members), 2)

    def test_left_member_record_is_removed_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(2345, 9876)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 2)
        self.left_member_service.remove_left_member(1234, 9876)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].user_id, 2345)

    def test_all_member_records_are_removed_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(1234, 8765)
        self.left_member_service.add_left_member(2345, 9876)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 3)
        self.left_member_service.remove_all_member_records(1234)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].user_id, 2345)

    def test_guild_left_member_records_are_removed_correctly(self):
        self.left_member_service.add_left_member(1234, 9876)
        self.left_member_service.add_left_member(1234, 8765)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 2)
        self.left_member_service.remove_guild_left_member_records(9876)
        members = self.left_member_service.get_all_left_members()
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].guild_id, 8765)
