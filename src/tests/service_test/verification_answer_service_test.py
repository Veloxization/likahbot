import unittest
import os
from services.verification_answer_service import VerificationAnswerService
from services.verification_question_service import VerificationQuestionService

class TestVerificationAnswerService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.verification_answer_service = VerificationAnswerService(db_address)
        self.verification_question_service = VerificationQuestionService(db_address)
        self.verification_question_service.add_verification_question(1234, "Test1?")
        self.verification_question_service.add_verification_question(2345, "Test2?")
        self.question1 = self.verification_question_service.get_all_guild_verification_questions(1234)[0]
        self.question2 = self.verification_question_service.get_all_guild_verification_questions(2345)[0]

    def tearDown(self):
        self.verification_answer_service.clear_verification_answers()
        self.verification_question_service.clear_verification_questions()

    def test_answers_to_questions_are_found_correctly(self):
        self.verification_answer_service.add_verification_answer(self.question1.db_id, "Test1!")
        answers = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].answer, "Test1!")

    def test_answers_are_deleted_correctly(self):
        self.verification_answer_service.add_verification_answer(self.question1.db_id, "Test1!")
        answers = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        self.assertEqual(len(answers), 1)
        self.verification_answer_service.delete_verification_answer(answers[0].db_id)
        answers = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        self.assertEqual(len(answers), 0)

    def test_all_answers_to_a_question_are_found_correctly(self):
        self.verification_answer_service.add_verification_answer(self.question1.db_id, "Test1!")
        self.verification_answer_service.add_verification_answer(self.question2.db_id, "Test2!")
        answers1 = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        answers2 = self.verification_answer_service.get_answers_for_question(self.question2.db_id)
        self.assertEqual(len(answers1), 1)
        self.assertEqual(len(answers2), 1)
        self.verification_answer_service.delete_all_answers_to_question(self.question1.db_id)
        answers1 = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        answers2 = self.verification_answer_service.get_answers_for_question(self.question2.db_id)
        self.assertEqual(len(answers1), 0)
        self.assertEqual(len(answers2), 1)

    def test_all_guild_answers_are_deleted_correctly(self):
        self.verification_answer_service.add_verification_answer(self.question1.db_id, "Test1!")
        self.verification_answer_service.add_verification_answer(self.question2.db_id, "Test2!")
        answers1 = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        answers2 = self.verification_answer_service.get_answers_for_question(self.question2.db_id)
        self.assertEqual(len(answers1), 1)
        self.assertEqual(len(answers2), 1)
        self.verification_answer_service.delete_all_guild_answers(1234)
        answers1 = self.verification_answer_service.get_answers_for_question(self.question1.db_id)
        answers2 = self.verification_answer_service.get_answers_for_question(self.question2.db_id)
        self.assertEqual(len(answers1), 0)
        self.assertEqual(len(answers2), 1)
