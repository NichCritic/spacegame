from objects.item import Item
from startup_scripts import setup_objects
from objects.components import components, db_components
import startup_scripts

session_manager = startup_scripts.setup_db('sqlite:///main.db')

all_db_components = {}
all_db_components.update(db_components)

all_components = {}
all_components.update(components)


def create_planets(node_factory, session):
    import random
    planet_types = ["bolfenn", "planet2", "planet5", "planet3", "planet4"]

    for _ in range(50):
        x_pos = random.randint(-45000, 45000)
        y_pos = random.randint(-45000, 45000)
        type_index = random.randint(0, len(planet_types) - 1)
        typ = planet_types[type_index]

        node_factory.create_new_node(
            {
                'db_position': {'x': x_pos, 'y': y_pos},
                'instance_components': {
                    "components": '{\
                        "type":{"type":"ttt"},\
                        "position": "db_position",\
                        "area":{"radius":750}\
                    }'.replace("ttt", typ)
                }
            }
        )

        for i in range(random.randint(1, 3)):
            create_shop(node_factory, x_pos, y_pos, 750, session)


def create_shop(node_factory, p_x, p_y, p_rad, session):
    import random
    import math
    import gamedata.shop_data
    import json

    shops = gamedata.shop_data.get_shop_data(session)

    x_offset = 0
    y_offset = 0
    while True:
        x_offset = random.randint(-p_rad + 20, p_rad - 20)
        y_offset = random.randint(-p_rad + 20, p_rad - 20)
        l = math.sqrt(x_offset**2 + y_offset**2)
        if l < p_rad and l > p_rad - 500:
            break

    x_pos = p_x + x_offset
    y_pos = p_y + y_offset

    component_data = {
        "type": {"type": "target"},
        "position": "db_position",
        "area": {"radius": 20},
        "shop_spec": random.choice(shops),
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
            'db_position': {'x': x_pos, 'y': y_pos},
            'instance_components': {
                "components": json.dumps(component_data)
            }
        }
    )


def create_asteroids(node_factory, session):
    import math
    count = 1000

    for i in range(count):

        prop = i / count * 2 * math.pi
        radius = 50000

        x_pos = math.sin(prop) * radius
        y_pos = math.cos(prop) * radius

        node_factory.create_new_node(
            {
                "db_position": {"x": x_pos, "y": y_pos},
                "instance_components": {"components": '{\
                    "type": {"type": "asteroid"},\
                    "area": {"radius": 100},\
                    "position": "db_position",\
                    "force": {},\
                    "acceleration": {},\
                    "server_updated": {},\
                    "physics_update": {},\
                    "state_history": {}\
                }'}
            })

        if i % 100:
            print("Created " + str(i) + " asteroids")


with session_manager.get_session() as session:
    _, node_factory, node_factory_db, object_db, player_factory, account_utils = setup_objects(
        all_db_components, all_components, session)
    object_db.set_session(session)

    session.add(Item("iron ore"))
    session.add(Item("silver ore"))
    session.add(Item("gold ore"))
    session.add(Item("iron"))
    session.add(Item("silver"))
    session.add(Item("gold"))
    session.add(Item("gasoline"))

    create_asteroids(node_factory_db, session)
    create_planets(node_factory_db, session)
