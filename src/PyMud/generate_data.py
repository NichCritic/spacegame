'''
Created on 2013-11-10

@author: Nich
'''

import PyMud.model.base as base
from PyMud.objects.component_manager import DBComponentSource, ComponentManager, ArrayComponentSource
from PyMud.objects.node_factory import NodeFactoryDB
from PyMud.objects.components import db_components, components
from PyMud.room.room_components import db_components as db_room_components, components as room_components
from PyMud.room.room import RoomFactory
from PyMud.objects.materials import materials


def main():
    engine = base.engine('sqlite:///main.db', echo = True)
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
                                        "container":{}
                                       })
    
    castle_node = node_factory.create_new_node({
                                         "container":{"parent_id":world_node.container.id}
                                         }
                                        
                                        )
    
    
    room_factory = RoomFactory(comp_manager)
    
    gcr = room_factory.create_room(name = "Gryffindor Common Room",
                             width = 20,
                             length = 20,
                             height = 20, container_id=castle_node.container.id)
    
    
    
    
    
    
    
    
    session.commit()
    session.close()
    
    


if __name__ == "__main__":
    main()



        