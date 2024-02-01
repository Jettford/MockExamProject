import sys
import mariadb

from typing import Optional

from .structs import Article, User, AdviceTrigger

conn = None

class Database:
    def connect(host: str, port: int, user: str, password: str, database: str):
        try:
            global conn

            # connect to database using mariadb connector
            conn = mariadb.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        except mariadb.Error as e:
            # catch anything and panic
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def cursor():
        if not conn:
            # if not connected, raise exception
            raise Exception("Database not connected")
            
        # TODO: check for any caching args
        return conn.cursor()
    
    def get_article(id: int) -> Optional[Article]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM articles WHERE article_id = ?", (id,))
        article = cursor.fetchone()

        if not article:
            return None
        
        return Article(*article)
    
    def get_articles() -> Optional[list[Article]]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM articles")
        articles = cursor.fetchall()

        if not articles:
            return None
        
        return [Article(*article) for article in articles]
    
    def create_article(title: str, search_keys: str, content: str) -> None:
        cursor = Database.cursor()
        cursor.execute("INSERT INTO articles (title, search_keys, content) VALUES (?, ?, ?)", (title, search_keys, content))
        conn.commit()

    def get_article_by_title(title: str) -> Optional[Article]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        article = cursor.fetchone()

        if not article:
            return None
        
        return Article(*article)
    
    def get_user(username: str) -> Optional[User]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return None
        
        return User(*user)
    
    def create_user(username: str, password: str) -> None:
        cursor = Database.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

    def get_triggers() -> Optional[list[AdviceTrigger]]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM advice_triggers")
        triggers = cursor.fetchall()

        if not triggers:
            return None

        return [AdviceTrigger(*trigger) for trigger in triggers]
    
    def create_trigger(lhs: str, rhs: str, logic: str, article_id: int) -> None:
        cursor = Database.cursor()
        cursor.execute("INSERT INTO advice_triggers (lhs, rhs, logic, article_id) VALUES (?, ?, ?, ?)", (lhs, rhs, logic, article_id))
        conn.commit()

    def delete_trigger(trigger_id: int) -> None:
        cursor = Database.cursor()
        cursor.execute("DELETE FROM advice_triggers WHERE trigger_id = ?", (trigger_id,))
        conn.commit()

    def get_trigger(trigger_id: int) -> Optional[AdviceTrigger]:
        cursor = Database.cursor()
        cursor.execute("SELECT * FROM advice_triggers WHERE trigger_id = ?", (trigger_id,))
        trigger = cursor.fetchone()

        if not trigger:
            return None
        
        return AdviceTrigger(*trigger)
    
    def delete_article(article_id: int) -> None:
        cursor = Database.cursor()
        cursor.execute("DELETE FROM articles WHERE article_id = ?", (article_id,))
        conn.commit()