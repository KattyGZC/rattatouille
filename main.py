from connectors import client, API_KEY, API_SECRET
import requests, json

headers = {
   "Accept": "application/json"
}

list_luch = []
list_dinner = []

def get_board():
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == "Recursos Culinarios":             
            return board

def delete_old_cards(list_week_menu):
    list_week_menu.archive_all_cards()

def all_cards_in_list(list_recipes):
    return list_recipes.list_cards()

def sort_recipes(days, dinner_list, luch_list):
    import random
    menu = []
    for day in range(days):
        random.shuffle(luch_list)
        menu.append(luch_list.pop())
        random.shuffle(dinner_list)
        menu.append(dinner_list.pop())
    return menu

week_menu_list = get_board().get_list('5fce9f77a78d601655ebcf13')
recipes_list = get_board().get_list('5fce9f7718a50a1681b1a0c1')
recipes = all_cards_in_list(recipes_list)


for recipe in recipes:
    id = recipe.id
    url = f"https://api.trello.com/1/cards/{id}/customFieldItems?key={API_KEY}&token={API_SECRET}"
    response = requests.get(url)
    custom_fields = response.json()
    for custom_field in custom_fields:
        if custom_field['idCustomField'] == '6164d583705eab3eec690053' and custom_field['idValue'] == '6164d5b3167ff713455b8ada':
            list_dinner.append(recipe)
            list_luch.append(recipe)
        else:
            if custom_field['idCustomField'] == '6164d583705eab3eec690053' and custom_field['idValue'] == '6164d597427cfc142b542f7e':
                list_luch.append(recipe)
            if custom_field['idCustomField'] == '6164d583705eab3eec690053' and custom_field['idValue'] == '6164d59c317db9464a4558f5':
                list_dinner.append(recipe)

print(sort_recipes(5, list_dinner, list_luch))


#delete_old_cards(week_menu_list)