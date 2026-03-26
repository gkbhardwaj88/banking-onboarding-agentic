import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET", "dev")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
SUREPASS_TOKEN = os.getenv("SUREPASS_TOKEN")
