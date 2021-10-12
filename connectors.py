from dotenv import load_dotenv
import os

from trello import TrelloClient

load_dotenv()

API_KEY=os.getenv('API_KEY', "")
API_SECRET=os.getenv('API_SECRET', "")

client = TrelloClient(
    api_key=API_KEY,
    api_secret=API_SECRET
)


