import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlashcardDatabase:
    def __init__(self, dbname="japanese_flashcards", user="postgres", password="topsykret", host="localhost"):
        """Initialize database connection parameters"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self._initialize_database()

    def _initialize_database(self):
        """Create database and table if they don't exist"""
        try:
            # Connect to default postgres database to create database
            conn = psycopg2.connect(
                dbname="postgres",
                user=self.user,
                password=self.password,
                host=self.host
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
            logger.info(f"Database {self.dbname} created successfully")
        except psycopg2.Error as e:
            logger.info(f"Database {self.dbname} may already exist: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        # Create table
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id SERIAL PRIMARY KEY,
                    kanji TEXT NOT NULL,
                    hiragana TEXT NOT NULL,
                    english_meaning TEXT NOT NULL,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info("Flashcards table created successfully")
        except psycopg2.Error as e:
            logger.error(f"Error creating table: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def add_flashcard(self, kanji, hiragana, english_meaning):
        """Add a new flashcard to the database"""
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO flashcards (kanji, hiragana, english_meaning)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (kanji, hiragana, english_meaning))
            
            flashcard_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Added flashcard with ID {flashcard_id}")
            return flashcard_id
        except psycopg2.Error as e:
            logger.error(f"Error adding flashcard: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_all_flashcards(self):
        """Retrieve all flashcards from the database"""
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT kanji, hiragana, english_meaning 
                FROM flashcards 
                ORDER BY date_added DESC
            """)
            
            flashcards = cursor.fetchall()
            return flashcards
        except psycopg2.Error as e:
            logger.error(f"Error fetching flashcards: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()