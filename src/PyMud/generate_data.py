'''
Created on 2013-11-10

@author: Nich
'''

import model.base as base
from objects.component_manager import DBComponentSource, ComponentManager, ArrayComponentSource
from objects.node_factory import NodeFactoryDB
from objects.components import db_components, components
from objects.materials import materials
from room.room_components import db_components as db_room_components, components as room_components
from room.room import RoomFactory
from objects.materials import materials


def main():
    engine = base.engine('sqlite:///main.db', echo=True)
    Session = base.create_sessionmaker(engine)
    base.Base.metadata.create_all(engine)

    all_db_components = {}
    all_db_components.update(db_components)
    all_db_components.update(db_room_components)

    all_components = {}
    all_components.update(components)
    all_components.update(room_components)

    session = Session()
    object_db = DBComponentSource(all_db_components, session)
    object_array = ArrayComponentSource(all_components)

    comp_manager = ComponentManager([object_db, object_array])
    node_factory = NodeFactoryDB(comp_manager)

    world_node = node_factory.create_new_node({
        "container": {}
    })

    castle_node = node_factory.create_new_node({
        "container": {"parent_id": world_node.container.id}
    }

    )

    room_factory = RoomFactory(comp_manager)

    gcr = room_factory.create_room(name="Gryffindor Common Room",
                                   width=20,
                                   length=20,
                                   height=20, container_id=castle_node.container.id)

    gcr_node = node_factory.create_node(gcr, ['container'])

    rcr = room_factory.create_room(name="Ravenclaw Common Room",
                                   width=20,
                                   length=20,
                                   height=20, container_id=castle_node.container.id)

    rcr_node = node_factory.create_node(rcr, ['container'])

    chair = comp_manager.create_entity({
        'names': {'name': 'chair', 'identifiers': 'chair'},
        'material': {'material_id': materials.wood},
        'container': {'parent_id': gcr_node.container.id},
        'on_hold': {'callback': 'teleport', 'data': {'new_location': rcr}, 'timeout':5}
    })

    table = comp_manager.create_entity({
        'names': {'name': 'table', 'identifiers': 'table'},
        'material': {'material_id': materials.crystal},
        'container': {'parent_id': rcr_node.container.id},
        'on_hold': {'callback': 'teleport', 'data': {'new_location': gcr}, 'timeout':5}
    })

    session.commit()
    session.close()


if __name__ == "__main__":
    main()
