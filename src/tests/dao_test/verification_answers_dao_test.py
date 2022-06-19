import unittest
import os
from dao.verification_answers_dao import VerificationAnswersDAO
from dao.verification_questions_dao import VerificationQuestionsDAO

class TestVerificationAnswersDAO(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.verification_answers_dao = VerificationAnswersDAO(db_address)
        self.verification_questions_dao = VerificationQuestionsDAO(db_address)
        self.verification_questions_dao.add_verification_question(1234, "Test1?")
        self.verification_questions_dao.add_verification_question(2345, "Test2?")
        self.question1 = self.verification_questions_dao.get_all_guild_verification_questions(1234)[0]
        self.question2 = self.verification_questions_dao.get_all_guild_verification_questions(2345)[0]

    def tearDown(self):
        self.verification_answers_dao.clear_verification_answers_table()
        self.verification_questions_dao.clear_verification_questions_table()

    def test_answers_for_a_question_are_found_correctly(self):
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1!")
        self.verification_answers_dao.add_verification_answer(self.question2["id"], "Test2!")
        answers = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]["answer"], "Test1!")

    def test_verification_answers_are_edited_correctly(self):
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1!")
        answers = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        self.assertEqual(answers[0]["answer"], "Test1!")
        self.verification_answers_dao.edit_verification_answer(answers[0]["id"], "Test2!")
        answers = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        self.assertEqual(answers[0]["answer"], "Test2!")

    def test_verification_answers_are_deleted_correctly(self):
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1!")
        answers = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        self.assertEqual(len(answers), 1)
        self.verification_answers_dao.delete_verification_answer(answers[0]["id"])
        answers = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        self.assertEqual(len(answers), 0)

    def test_all_answers_to_a_verification_question_are_deleted_correctly(self):
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1.0!")
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1.1!")
        self.verification_answers_dao.add_verification_answer(self.question2["id"], "Test2!")
        answers1 = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        answers2 = self.verification_answers_dao.get_answers_for_question(self.question2["id"])
        self.assertEqual(len(answers1), 2)
        self.assertEqual(len(answers2), 1)
        self.verification_answers_dao.delete_all_answers_to_question(self.question1["id"])
        answers1 = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        answers2 = self.verification_answers_dao.get_answers_for_question(self.question2["id"])
        self.assertEqual(len(answers1), 0)
        self.assertEqual(len(answers2), 1)

    def test_all_guild_verification_answers_are_deleted_correctly(self):
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1.0!")
        self.verification_answers_dao.add_verification_answer(self.question1["id"], "Test1.1!")
        self.verification_answers_dao.add_verification_answer(self.question2["id"], "Test2!")
        answers1 = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        answers2 = self.verification_answers_dao.get_answers_for_question(self.question2["id"])
        self.assertEqual(len(answers1), 2)
        self.assertEqual(len(answers2), 1)
        self.verification_answers_dao.delete_all_guild_answers(1234)
        answers1 = self.verification_answers_dao.get_answers_for_question(self.question1["id"])
        answers2 = self.verification_answers_dao.get_answers_for_question(self.question2["id"])
        self.assertEqual(len(answers1), 0)
        self.assertEqual(len(answers2), 1)
