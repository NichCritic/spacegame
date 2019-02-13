from objects.item import Item
from startup_scripts import setup_objects
from objects.components import components, db_components
import startup_scripts

session_manager = startup_scripts.setup_db('sqlite:///main.db')

all_db_components = {}
all_db_components.update(db_components)

all_components = {}
all_components.update(components)


def create_asteroids(node_factory, session):
    import math
    count = 1000

    for i in range(count):

        prop = i/count * 2 * math.pi
        radius = 50000

        x_pos = math.sin(prop) * radius
        y_pos = math.cos(prop) * radius

        node_factory.create_new_node(
            {
                "db_position" : {"x": x_pos, "y":y_pos},
                "instance_components": {"components":"{\
                    'type': {'type': 'asteroid'},\
                    'area': {'radius': 100},\
                    'position': 'db_position',\
                    'force': {},\
                    'acceleration': {},\
                    'server_updated': {},\
                    'physics_update': {},\
                    'state_history': {}\
                }"}
            })

        if i % 100:
            print("Created "+str(i)+" asteroids")





with session_manager.get_session() as session:
    _, node_factory, object_db, player_factory, account_utils = setup_objects(
        all_db_components, all_components, session)
    object_db.set_session(session)


    session.add(Item("gold"))
    session.add(Item("silver"))
    session.add(Item("copper"))
    session.add(Item("crystal"))


    create_asteroids(node_factory, session)



