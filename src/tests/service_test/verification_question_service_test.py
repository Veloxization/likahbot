import asyncio
import unittest
import os
from services.verification_question_service import VerificationQuestionService

class TestVerificationQuestionService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.verification_question_service = VerificationQuestionService(db_address)

    def tearDown(self):
        asyncio.run(self.verification_question_service.clear_verification_questions())

    def test_all_guild_verification_questions_are_found_correctly(self):
        asyncio.run(self.verification_question_service.add_verification_question(1234, "Test1?"))
        asyncio.run(self.verification_question_service.add_verification_question(2345, "Test2?"))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].question, "Test1?")

    def test_specific_verification_questions_are_found_correctly(self):
        asyncio.run(self.verification_question_service.add_verification_question(1234, "Test?"))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        questions = asyncio.run(self.verification_question_service.get_verification_question(questions[0].db_id))
        self.assertEqual(questions.question, "Test?")

    def test_verification_questions_are_edited_correctly(self):
        asyncio.run(self.verification_question_service.add_verification_question(1234, "Test1?"))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        self.assertEqual(questions[0].question, "Test1?")
        self.assertEqual(questions[0].question_priority, 0)
        asyncio.run(self.verification_question_service.edit_verification_question(questions[0].db_id, "Test2?", 1))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        self.assertEqual(questions[0].question, "Test2?")
        self.assertEqual(questions[0].question_priority, 1)

    def test_verification_question_is_deleted_correctly(self):
        asyncio.run(self.verification_question_service.add_verification_question(1234, "Test?"))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        self.assertEqual(len(questions), 1)
        asyncio.run(self.verification_question_service.delete_verification_question(questions[0].db_id))
        questions = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        self.assertEqual(len(questions), 0)

    def test_guild_verification_questions_are_deleted_correctly(self):
        asyncio.run(self.verification_question_service.add_verification_question(1234, "Test1?"))
        asyncio.run(self.verification_question_service.add_verification_question(2345, "Test2?"))
        questions1 = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        questions2 = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(2345))
        self.assertEqual(len(questions1), 1)
        self.assertEqual(len(questions2), 1)
        asyncio.run(self.verification_question_service.delete_guild_verification_questions(1234))
        questions1 = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(1234))
        questions2 = asyncio.run(self.verification_question_service.get_all_guild_verification_questions(2345))
        self.assertEqual(len(questions1), 0)
        self.assertEqual(len(questions2), 1)
