"""The verification question service is used to call methods in the verification questions DAO
class."""

from dao.verification_questions_dao import VerificationQuestionsDAO
from entities.verification_question_entity import VerificationQuestionEntity

class VerificationQuestionService:
    """A service for calling methods from verification questions DAO
    Attributes:
        verification_questions_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for verification questions DAO
        Args:
            db_address: The address for the database file where the verification questions table
                        resides"""

        self.verification_questions_dao = VerificationQuestionsDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a verification question entity
        Args:
            row: The database row to convert to a verification question entity
        Returns: A verification question entity equivalent to the database row"""

        if not row:
            return None
        return VerificationQuestionEntity(row["id"], row["question"], row["question_priority"])

    async def get_all_guild_verification_questions(self, guild_id: int):
        """Get all verification questions of a given guild
        Args:
            guild_id: The Discord ID of the guild whose verification questions to get
        Returns: A list of verification question entities"""

        rows = await self.verification_questions_dao.get_all_guild_verification_questions(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    async def get_verification_question(self, question_id: int):
        """Get a specific verification question
        Args:
            question_id: The database ID of the question to get
        Returns: A verification question entity"""

        row = await self.verification_questions_dao.get_verification_question(question_id)
        return self._convert_to_entity(row)

    async def add_verification_question(self, guild_id: int, question: str, priority: int = 0):
        """Add a new verification question for a given guild
        Args:
            guild_id: The Discord ID of the guild to which the question is added
            question: The question itself
            priority: The priority number of the question. Lower numbers are displayed first."""

        await self.verification_questions_dao.add_verification_question(guild_id, question,
                                                                        priority)

    async def edit_verification_question(self, question_id: int, question: str, priority: int):
        """Edit an existing verification question
        Args:
            question_id: The database ID of the question to edit
            question: The new question
            priority: The new priority number for the question"""

        await self.verification_questions_dao.edit_verification_question(question_id, question,
                                                                         priority)

    async def delete_verification_question(self, question_id: int):
        """Delete a specific verification question
        Args:
            question_id: The database ID of the question to delete"""

        await self.verification_questions_dao.delete_verification_question(question_id)

    async def delete_guild_verification_questions(self, guild_id: int):
        """Delete all verification questions of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose verification questions to delete"""

        await self.verification_questions_dao.delete_guild_verification_questions(guild_id)

    async def clear_verification_questions(self):
        """Delete every single verification question"""

        await self.verification_questions_dao.clear_verification_questions_table()
