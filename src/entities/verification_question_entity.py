"""Verification question database rows converted into Python objects"""

class VerificationQuestionEntity():
    """An object derived from the verification question database table's rows
    Attributes:
        db_id: The database ID of the utility channel
        question: The verification question
        question_priority: The priority of the question, lower number means higher priority"""

    def __init__(self, db_id: int, question: str, question_priority: int):
        """Create a new verification question entity
        Args:
            db_id: The database ID of the utility channel
            question: The verification question
            question_priority: The priority of the question"""

        self.db_id = db_id
        self.question = question
        self.question_priority = question_priority
