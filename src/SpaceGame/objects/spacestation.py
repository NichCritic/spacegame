
def create_spacestation(node_factory, position, radius):
	 node_factory.create_new_node(
        {
            'db_position': position,
            'instance_components': {
                "components": '{\
                    "type":{"type":"spacestation1"},\
                    "position": "db_position",\
                    "area":{"radius":rrr}\
                }'.replace("rrr", str(radius))
            }
        }
    )

