from dotenv import load_dotenv
import logging
import os


load_dotenv()

SESSION_NAME = os.getenv("SESSION_NAME")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

formatter = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
date_format = "%d-%b-%y %H:%M:%S"
logging.basicConfig(format=formatter, datefmt=date_format, level=logging.INFO)
