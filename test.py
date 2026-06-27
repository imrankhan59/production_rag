from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql+psycopg://rag_user:password@localhost:5432/rag_db"
)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connected Successfully!")
        print(result.scalar())

except Exception as e:
    print("Connection Failed!")
    print(e)