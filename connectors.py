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

all_boards = client.list_boards()
last_board = all_boards[-1]
print(last_board.name)
last_board.list_lists()
my_list = last_board.get_list('5fce9f7718a50a1681b1a0c1')

for card in my_list.list_cards():
    print(card.id)