
from objects.item import Item, get_item_by_name
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

    trishot = get_item_by_name(session, 'trishot')
    health = get_item_by_name(session, 'health')

    component_data = {
        "position": "db_position",
        "shop_spec": shops[0],
        "money":
        {
            "money": 250000000000
        },
        "inventory":
        {
            "inventory": {
                trishot.id:{"qty":10000000},
                health.id:{"qty":10000000}
            }
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

    session.add(Item("iron ore", 'ore'))
    session.add(Item("silver ore", 'ore'))
    session.add(Item("gold ore", 'ore'))

    session.add(Item("trishot", 'upgrade'))
    session.add(Item("health", 'upgrade'))
    session.add(Item("heal", 'upgrade'))
    session.add(Item("rootkit", 'upgrade'))

    create_spacestation(node_factory_db, position={
                        "x": 0, "y": -200}, radius=200)
    create_shop(node_factory_db, {"x": 0, "y": -200}, session)
