import time
from cassandra.cluster import Cluster
import uuid

CASSANDRA_HOST = "cassandra"  # Remplace "localhost" par "cassandra"

def wait_for_cassandra(host, retries=10, delay=5):
    """Attend que Cassandra soit prêt avant de se connecter."""
    for i in range(retries):
        try:
            cluster = Cluster([host])
            session = cluster.connect()
            print("✅ Cassandra est prêt !")
            return session
        except Exception as e:
            print(f"⏳ Cassandra non prêt ({i+1}/{retries}) : {e}")
            time.sleep(delay)
    raise Exception("🚨 Impossible de se connecter à Cassandra après plusieurs tentatives.")

# Connexion avec retry
session = wait_for_cassandra(CASSANDRA_HOST)

# Création de la base de données
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS my_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")
session.set_keyspace('my_keyspace')

# Création de la Table Users
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        name TEXT,
        age INT,
        email TEXT
    )
""")

# Insertion de données
def insert_user(session, name, age, email):
    user_id = uuid.uuid4()
    session.execute("""
        INSERT INTO users (id, name, age, email) VALUES (%s, %s, %s, %s)
    """, (user_id, name, age, email))
    print(f"✅ Inséré: {name}, Age: {age}, Email: {email}")

# Récupération des utilisateurs
def fetch_users(session):
    rows = session.execute("SELECT * FROM users")
    for row in rows:
        print(f"🆔 {row.id}, 👤 {row.name}, 🎂 {row.age}, 📧 {row.email}")

# Exécuter les opérations
insert_user(session, "Alice", 30, "alice@ynov.com")
insert_user(session, "Hugo", 30, "hugo@ynov.com")
insert_user(session, "Ousmane", 30, "ousmane@ynov.com")

fetch_users(session)
