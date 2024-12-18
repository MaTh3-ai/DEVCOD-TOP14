import sqlite3
from werkzeug.security import generate_password_hash

class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.connection = sqlite3.connect(db_name)  # Connexion à la base de données
        self.create_table()  # Créer la table si elle n'existe pas

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')  # Créer la table des utilisateurs

    def insert_user(self, username, password, role='public'):
        hashed_password = generate_password_hash(password)  # Hacher le mot de passe
        try:
            with self.connection:
                self.connection.execute('''
                    INSERT INTO users (username, password, role)
                    VALUES (?, ?, ?)
                ''', (username, hashed_password, role))  # Insérer l'utilisateur dans la base de données
            return True
        except sqlite3.IntegrityError:
            return False  # Nom d'utilisateur déjà pris

    def get_user(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()  # Récupérer un utilisateur par son nom d'utilisateur

    def close(self):
        self.connection.close()  # Fermer la connexion à la base de données