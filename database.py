import peewee
import json
db = peewee.SqliteDatabase('bot.db')

def init_views():

    with open('sql_views.json', 'r') as json_file:
        views= json.load(json_file)
        
    for view in views:

        try:
            db.execute_sql(views[view])

        except peewee.OperationalError as e:

            print(f'Error creating view {view}: {e}')
        
        print(f'View {view} created successfully')
