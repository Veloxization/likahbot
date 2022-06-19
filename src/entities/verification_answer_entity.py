"""Verification answer database rows converted into Python objects"""

class VerificationAnswerEntity():
    """An object derived from the verification answers database table's rows
    Attributes:
        db_id: The database ID of the verification answer
        question_id: The database ID of the question this answer is for
        answer: The expected answer to the question"""

    def __init__(self, db_id: int, question_id: int, answer: str):
        """Create a new verification answer entity
        Args:
            db_id: The database ID of the verification answer
            question_id: The database ID of the question this answer is for
            answer: The expected answer to the question"""

        self.db_id = db_id
        self.question_id = question_id
        self.answer = answer
