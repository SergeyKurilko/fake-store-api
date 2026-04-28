import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения при импорте settings
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
BASE_DIR = Path(__file__).resolve().parent