import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "https://narrify.dev")
    GENERATE_SERVICE_URL = os.getenv("GENERATE_SERVICE_URL", "https://narrify.dev")

config = Config()
