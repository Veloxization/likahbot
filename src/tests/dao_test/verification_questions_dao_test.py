import unittest
import os
from dao.verification_questions_dao import VerificationQuestionsDAO

class TestVerificationQuestionsDAO(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.verification_questions_dao = VerificationQuestionsDAO(db_address)

    def tearDown(self):
        self.verification_questions_dao.clear_verification_questions_table()

    def test_guild_verification_questions_are_found_correctly(self):
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        self.verification_questions_dao.add_verification_question(2345, "Test2?")
        questions = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]["question"], "Test1?")

    def test_specific_verification_questions_are_found_correctly(self):
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        question = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        question = self.verification_questions_dao.get_verification_question(question[0]["id"])
        self.assertIsNotNone(question)
        self.assertEqual(question["question"], "Test1?")

    def test_verification_questions_are_edited_correctly(self):
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        questions = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        self.assertEqual(questions[0]["question"], "Test1?")
        self.assertEqual(questions[0]["question_priority"], 0)
        self.verification_questions_dao.edit_verification_question(questions[0]["id"], "Test2?", 1)
        questions = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        self.assertEqual(questions[0]["question"], "Test2?")
        self.assertEqual(questions[0]["question_priority"], 1)

    def test_verification_questions_are_deleted_correctly(self):
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        questions = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        self.assertEqual(len(questions), 1)
        self.verification_questions_dao.delete_verification_question(questions[0]["id"])
        questions = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        self.assertEqual(len(questions), 0)

    def test_guild_verification_questions_are_deleted_correctly(self):
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        self.verification_questions_dao.add_verification_question(2345, "Test2?")
        questions1 = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        questions2 = self.verification_questions_dao.get_all_guild_verification_questions(2345)
        self.assertEqual(len(questions1), 1)
        self.assertEqual(len(questions2), 1)
        self.verification_questions_dao.delete_guild_verification_questions(1234)
        questions1 = self.verification_questions_dao.get_all_guild_verification_questions(1234)
        questions2 = self.verification_questions_dao.get_all_guild_verification_questions(2345)
        self.assertEqual(len(questions1), 0)
        self.assertEqual(len(questions2), 1)
