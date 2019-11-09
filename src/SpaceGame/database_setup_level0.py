from objects.item import Item
from objects.spacestation import create_spacestation
from startup_scripts import setup_objects
from objects.components import components, db_components
import startup_scripts


session_manager = startup_scripts.setup_db('sqlite:///main.db')

all_db_components = {}
all_db_components.update(db_components)

all_components = {}
all_components.update(components)


def create_shop(node_factory, position, session):
    import math
    import gamedata.shop_data
    import json

    shops = gamedata.shop_data.get_shop_data(session)


    component_data = {
        "position": "db_position",
        "shop_spec": shops[0],
        "money":
        {
            "money": 250000000000
        },
        "inventory":
        {
            "inventory": {}
        }
    }

    node_factory.create_new_node(
        {
            'db_position': position,
            'instance_components': {
                "components": json.dumps(component_data)
            }
        }
    )


with session_manager.get_session() as session:
    _, node_factory, node_factory_db, object_db, player_factory, account_utils = setup_objects(
        all_db_components, all_components, session)
    object_db.set_session(session)

    session.add(Item("iron ore"))
    session.add(Item("silver ore"))
    session.add(Item("gold ore"))
    

    create_spacestation(node_factory_db, position={"x":0, "y":-200}, radius=200)
    create_shop(node_factory_db, {"x":0, "y":-200}, session)