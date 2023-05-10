"""The verification answer service is used to call methods in the verification answers DAO
class."""

from dao.verification_answers_dao import VerificationAnswersDAO
from entities.verification_answer_entity import VerificationAnswerEntity

class VerificationAnswerService:
    """A service for calling methods from verification answers DAO
    Attributes:
        verification_answers_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for verification answers DAO
        Args:
            db_address: The address for the database file where the verification answers table
                        resides"""

        self.verification_answers_dao = VerificationAnswersDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a verification answer entity
        Args:
            row: The database row to convert to a verification answer entity
        Returns: A verification answer entity equivalent to the database row"""

        if not row:
            return None
        return VerificationAnswerEntity(row["id"], row["question_id"], row["answer"])

    async def get_answers_for_question(self, question_id: int):
        """Get a list of possible answer for a specific question
        Args:
            question_id: The database ID of the question whose answers to get
        Returns: A list of verification answer entities"""

        rows = await self.verification_answers_dao.get_answers_for_question(question_id)
        return [self._convert_to_entity(row) for row in rows]

    async def add_verification_answer(self, question_id: int, answer: str):
        """Add a new answer for a specific question
        Args:
            question_id: The database ID of the question this is an answer to
            answer: An expected answer for the question"""

        await self.verification_answers_dao.add_verification_answer(question_id, answer)

    async def edit_verification_answer(self, answer_id: int, answer: str):
        """Edit a specific verification answer
        Args:
            answer_id: The database ID of the answer to edit
            answer: The new answer"""

        await self.verification_answers_dao.edit_verification_answer(answer_id, answer)

    async def delete_verification_answer(self, answer_id: int):
        """Delete a specific verification answer
        Args:
            answer_id: The database ID of the answer to delete"""

        await self.verification_answers_dao.delete_verification_answer(answer_id)

    async def delete_all_answers_to_question(self, question_id: int):
        """Delete all answers to a specific question
        Args:
            question_id: The database ID of the question whose answers to delete"""

        await self.verification_answers_dao.delete_all_answers_to_question(question_id)

    async def delete_all_guild_answers(self, guild_id: int):
        """Delete all verification answers of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose answers to delete"""

        await self.verification_answers_dao.delete_all_guild_answers(guild_id)

    async def clear_verification_answers(self):
        """Delete every single verification answer"""

        await self.verification_answers_dao.clear_verification_answers_table()
