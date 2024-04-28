import os
from dotenv import load_dotenv

load_dotenv('../config.env')

API_KEY = os.getenv("API_KEY")
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": API_KEY
}
