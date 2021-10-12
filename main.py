from connectors import client, API_KEY, API_SECRET
import requests, datetime

headers = {
   "Accept": "application/json"
}

def get_board():
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == "Recursos Culinarios":             
            return board

def delete_old_cards(list_week_menu):
    try:
            list_week_menu.archive_all_cards()
            return True
    except:
        return 'Ha ocurrido un error al archivar las tarjetas antiguas'

def all_cards_in_list(list_recipes):
    return list_recipes.list_cards()

def divider_recipes(recipes):
    try:
        list_luch = []
        list_dinner = []
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
        return list_dinner, list_luch
    except:
        return 'Ha ocurrido un error al dividir la lista'

def sort_recipes(days, dinner_list, luch_list):
    import random
    menu = []
    for day in range(days):
        random.shuffle(luch_list)
        menu.append(luch_list.pop())
        random.shuffle(dinner_list)
        menu.append(dinner_list.pop())
    return menu

def copy_cards_menu(menu):
    try:
        for item in menu:
            week_menu_list.add_card(item.name)
        return "Exito!"
    except ValueError as err:
        return f"Ha ocurrido un error al crear las tarjetas. El error fue:{err} "

def add_date_cards(week_menu, dt):
    try:
        menu_week = all_cards_in_list(week_menu)
        for key, item in enumerate(menu_week):
            item.set_due(dt)
            if key % 2 == 0:
                dt = dt + datetime.timedelta(hours=7)
            else:
                dt = dt + datetime.timedelta(hours=17)
        return "Proceso realizado y finalizado con éxito!!"
    except  Exception as err:
        return f"Algo salió mal... Error: {err}"


week_menu_list = get_board().get_list('5fce9f77a78d601655ebcf13')

if len(week_menu_list.list_cards()) != 0:
    delete_old_cards(week_menu_list)
recipes_list = get_board().get_list('5fce9f7718a50a1681b1a0c1')
recipes = all_cards_in_list(recipes_list)
dinner, lunch = divider_recipes(recipes)
print(copy_cards_menu(sort_recipes(5, dinner, lunch)))
date_init = datetime.datetime(2021, 10, 13, 18, 0, tzinfo=datetime.timezone.utc)
print(add_date_cards(week_menu_list, date_init))


#print(copy_cards_menu(sort_recipes(5, list_dinner, list_luch)))
