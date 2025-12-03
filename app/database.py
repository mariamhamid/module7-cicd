from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy.exc import ArgumentError

# Default (fallback) database URL used when no environment variable is provided.
# You can override this by setting the `DATABASE_URL` environment variable.
DATABASE_URL="postgresql+psycopg2://myuser:mypassword@localhost:5432/new_db"
# Load .env in development only (keeps behavior backward compatible)
load_dotenv()

# Read DATABASE_URL from environment, falling back to DEFAULT_DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL") or DATABASE_URL
# Normalize common mistakes: strip surrounding quotes and whitespace
if isinstance(DATABASE_URL, str):
	DATABASE_URL = DATABASE_URL.strip().strip('"').strip("'")

try:
	engine = create_engine(DATABASE_URL)
except ArgumentError as exc:
	# Provide a clear error message for malformed URLs
	raise RuntimeError(
		f"Invalid DATABASE_URL value: {DATABASE_URL!r}.\n"
		"Set a valid SQLAlchemy database URL in the DATABASE_URL environment variable.\n"
		"Common cause: surrounding quotes in .env (remove quotes so value is unquoted)."
	) from exc

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()