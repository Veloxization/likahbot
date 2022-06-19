"""The classes and functions handling data access objects for the verification_answers table.
The database table keeps track of the verification answers for the guild, if any.
Verification answers are expected answers for specific questions in a verification form.
This is a good way to, for example, have a password that a member has to know before being
verified."""
from db_connection.db_connector import DBConnection

class VerificationAnswersDAO:
    """A data access object for verification answers
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for verification answers
        Args:
            db_address: The address for the database file where the verification answers table
                        resides"""

        self.db_connection = DBConnection(db_address)

    def get_answers_for_question(self, question_id: int):
        """Get a list of possible answer for a specific question
        Args:
            question_id: The database ID of the question whose answers to get
        Returns: A list of Rows containing the answers for the given question"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT a.id, question_id, answer FROM verification_answers AS a " \
              "INNER JOIN verification_questions AS q ON q.id=question_id " \
              "WHERE question_id=?"
        cursor.execute(sql, (question_id,))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def add_verification_answer(self, question_id: int, answer: str):
        """Add a new answer for a specific question
        Args:
            question_id: The database ID of the question this is an answer to
            answer: An expected answer for the question"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO verification_answers (question_id, answer) VALUES (?, ?)"
        cursor.execute(sql, (question_id, answer))
        self.db_connection.commit_and_close(connection)

    def edit_verification_answer(self, answer_id: int, answer: str):
        """Edit a specific verification answer
        Args:
            answer_id: The database ID of the answer to edit
            answer: The new answer"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE verification_answers SET answer=? WHERE id=?"
        cursor.execute(sql, (answer, answer_id))
        self.db_connection.commit_and_close(connection)

    def delete_verification_answer(self, answer_id: int):
        """Delete a specific verification answer
        Args:
            answer_id: The database ID of the answer to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_answers WHERE id=?"
        cursor.execute(sql, (answer_id,))
        self.db_connection.commit_and_close(connection)

    def delete_all_answers_to_question(self, question_id: int):
        """Delete all answers to a specific question
        Args:
            question_id: The database ID of the question whose answers to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_answers WHERE question_id=?"
        cursor.execute(sql, (question_id,))
        self.db_connection.commit_and_close(connection)

    def delete_all_guild_answers(self, guild_id: int):
        """Delete all verification answers of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose answers to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_answers WHERE question_id IN " \
              "(SELECT id FROM verification_questions WHERE guild_id=?)"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_verification_answers_table(self):
        """Delete every single verification answer from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM verification_answers"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
