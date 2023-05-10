"""The classes and functions handling data access objects for the verification_questions table.
The database table keeps track of the verification questions for the guild, if any.
Verification questions are a form that a new member has to fill out to gain access to the guild."""
from db_connection.db_connector import DBConnection

class VerificationQuestionsDAO:
    """A data access object for verification questions
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for verification questions
        Args:
            db_address: The address for the database file where the verification questions table
                        resides"""

        self.db_connection = DBConnection(db_address)

    async def get_all_guild_verification_questions(self, guild_id: int):
        """Get all verification questions of a given guild
        Args:
            guild_id: The Discord ID of the guild whose verification questions to get
        Returns: A list of Rows with the found verification questions"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM verification_questions WHERE guild_id=? " \
              "ORDER BY question_priority ASC"
        await cursor.execute(sql, (guild_id,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def get_verification_question(self, question_id: int):
        """Get a specific verification question
        Args:
            question_id: The database ID of the question to get
        Returns: A Row object with the found question, or None if none are found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM verification_questions WHERE id=?"
        await cursor.execute(sql, (question_id,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def add_verification_question(self, guild_id: int, question: str, priority: int = 0):
        """Add a new verification question for a given guild
        Args:
            guild_id: The Discord ID of the guild to which the question is added
            question: The question itself
            priority: The priority number of the question. Lower numbers are displayed first."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO verification_questions (guild_id, question, question_priority) " \
              "VALUES (?, ?, ?)"
        await cursor.execute(sql, (guild_id, question, priority))
        await self.db_connection.commit_and_close(connection)

    async def edit_verification_question(self, question_id: int, question: str, priority: int):
        """Edit an existing verification question
        Args:
            question_id: The database ID of the question to edit
            question: The new question
            priority: The new priority number for the question"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE verification_questions SET question=?, question_priority=? WHERE id=?"
        await cursor.execute(sql, (question, priority, question_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_verification_question(self, question_id: int):
        """Delete a specific verification question
        Args:
            question_id: The database ID of the question to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_questions WHERE id=?"
        await cursor.execute(sql, (question_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_verification_questions(self, guild_id: int):
        """Delete all verification questions of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose verification questions to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_questions WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_verification_questions_table(self):
        """Delete every single verification question from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_questions"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
