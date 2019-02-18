
'''
Created on 2013-11-02

@author: Nich
'''


#from objects.components import components
from objects.baseobject import Entity

#from room.room_components import room_components

#all_components = {}
# all_components.update(components)
# all_components.update(room_components)


class DBComponentSource():

    def __init__(self, component_list, session=None):
        self.session = session
        self.component_list = component_list

    def set_session(self, session):
        self.session = session

    def get_component(self, oid, component_name):
        Table = self.component_list[component_name]
        return self.session.query(Table).filter(Table.entity_id == oid).one()

    def get_supported_subset(self, component_list):
        return list(filter(self.has, component_list))

    def remove_component(self, entity_id, component_name):
        self.session.delete(self.get_component(entity_id, component_name))

    def has(self, component_name):
        return component_name in self.component_list

    def get_entities_for_component(self, component_name):
        Table = self.component_list[component_name]
        return [component.entity_id for component in self.session.query(Table)]

    def create_component_data(self, component_name, component, entity_id, data):
        c = None
        if data is None:
            c = component(entity_id)
        else:
            c = component(entity_id, **data)
        self.session.add(c)

    def has_entity(self, component_name, entity_id):
        from sqlalchemy.sql import exists
        if self.has(component_name):
            Table = self.component_list[component_name]
            entity_exists = self.session.query(
                exists().where(Table.entity_id == entity_id)).scalar()
            return entity_exists
        else:
            return False

    def add_component_to_object(self, component_name, entity_id, data):
        component = self.component_list[component_name]

        if not self.has_entity(component_name, entity_id):
            self.create_component_data(
                component_name, component, entity_id, data)
            # object.components.add(component_name)
        else:
            raise AttributeError(
                "Can't add a component more than once to the same object")

    def get_entities_with_components(self, component_list, entity_ids=None):
        # import pdb
        # pdb.set_trace()
        if len(component_list) == 0:
            return []

        T0 = self.component_list[component_list[0]]
        q = self.session.query(T0)

        for comp in component_list[1:]:
            Table = self.component_list[comp]
            entities = self.session.query(Table).all()

            q = q.filter(T0.entity_id.in_([e.entity_id for e in entities]))

        entities = q.all()
        return [e.entity_id for e in entities]

    def get_component_for_entities(self, entity_ids, component_name):
        Table = self.component_list[component_name]

        all_comps = []

        limit = 500
        i = 0
        # import pdb
        # pdb.set_trace()

        while True:
            i = i + 1
            if i * limit < len(entity_ids):
                comps = self.session.query(Table).filter(
                    Table.entity_id.in_(entity_ids[(i - 1) * limit: i * limit])).all()
                all_comps += comps
            else:
                comps = self.session.query(Table).filter(
                    Table.entity_id.in_(entity_ids[(i - 1) * limit:])).all()

                all_comps += comps
                break
        return all_comps

    def create_entity(self):
        e = Entity()
        self.session.add(e)
        return e


class ArrayComponentSource():

    def __init__(self, component_list):
        self.component_list = component_list
        self.component_object = {}

        for comp_name in component_list.keys():
            self.component_object[comp_name] = {}

    def get_component(self, entity_id, component_name):
        if self.has_entity(component_name, entity_id):
            return self.component_object[component_name][entity_id]
        else:
            raise AttributeError(
                "{0} has no component named {1}".format(entity_id, component_name))

    def get_supported_subset(self, component_list):
        return list(filter(self.has, component_list))

    def remove_component(self, entity_id, component_name):
        if self.has_entity(component_name, entity_id):
            self.component_object[component_name].pop(entity_id)

    def has(self, component_name):
        return component_name in self.component_list

    def get_entities_for_component(self, component_name):
        return list(self.component_object[component_name].keys())

    def create_component_data(self, component_name, entity_id, data):
        component = self.component_list[component_name]
        if data is None:
            self.component_object[component_name][
                entity_id] = component(entity_id)
        else:
            self.component_object[component_name][
                entity_id] = component(entity_id, **data)

    def has_entity(self, component_name, entity_id):
        return self.has(component_name) and entity_id in self.component_object[component_name]

    def add_component_to_object(self, component_name, entity_id, data):
        if not self.has_entity(component_name, entity_id):
            self.create_component_data(component_name, entity_id, data)
            # object.components.add(component_name)
        else:
            raise AttributeError(
                "Can't add a component more than once to the same object")

    def get_entities_with_components(self, component_list, entity_ids=None):
        entities = [] if entity_ids == None else [entity_ids]
        for component_name in component_list:
            entities.append(self.get_entities_for_component(component_name))

        if len(entities) == 0:
            return []

        e_list = set(entities[0])
        for e in entities[1:]:
            e_list = e_list.intersection(set(e))

        return e_list

    def get_component_for_entities(self, entity_ids, component_name):
        components = []
        for e_id in entity_ids:

            if self.has_entity(component_name, e_id):

                components.append(self.component_object[component_name][e_id])

        return components

    def create_entity(self):
        return Entity()


class ComponentManager(object):

    def __init__(self, component_sources=None):
        self.component_sources = component_sources

    def get_component(self, entity_id, component_name):
        for component_source in self.component_sources:
            if component_source.has(component_name):
                return component_source.get_component(entity_id, component_name)

    def entity_has_component(self, entity_id, component_name):
        return any([s.has_entity(component_name, entity_id) for s in self.component_sources])

    def has_component(self, component_name):
        return any([cs.has(component_name) for cs in self.component_sources])

    def remove_component(self, component_name, entity_id):
        for component_source in self.component_sources:
            if component_source.has(component_name):
                component_source.remove_component(entity_id, component_name)
                break
        else:
            raise AttributeError("Component not found")

    def add_component_to_object(self, component_name, entity_id, data=None):
        for component_source in self.component_sources:
            if component_source.has(component_name):
                component_source.add_component_to_object(
                    component_name, entity_id, data)
                break
        else:
            raise AttributeError(component_name + " was not found in sources")

    def create_entity(self, entity_spec):

        entity = self.component_sources[0].create_entity()

        for component_name, component_data in entity_spec.items():
            self.add_component_to_object(
                component_name, entity.id, component_data)

        return entity

    def get_entities_for_component(self, component_name):
        entities = []
        for component_source in self.component_sources:
            if component_source.has(component_name):
                entities = component_source.get_entities_for_component(
                    component_name)
                break
        return entities

    def get_entities_with_components(self, component_list, entity_ids):
        entities_from_sources = []
        components_covered = []
        num_components_from_source = []

        for component_source in self.component_sources:
            supported_components = component_source.get_supported_subset(
                component_list)
            entities_from_sources.append(
                component_source.get_entities_with_components(supported_components, entity_ids=entity_ids))
            components_covered += supported_components
            num_components_from_source.append(len(supported_components))

        if sorted(components_covered) != sorted(component_list):
            raise AttributeError("One or more components not found in one of the lists. Got: " +
                                 str(components_covered) + " Expected: " + str(component_list))

        # If a source doesn't provide any entities, don't count that as empty when considering if entities should be returned
        # To do that, filter them from the lists of sources (those sources
        # should return 0 entities regardless)
        entities_from_sources = [
            es for i, es in enumerate(entities_from_sources) if num_components_from_source[i] > 0]

        entities = entities_from_sources[0]
        for entity_list in entities_from_sources[1:]:
            if entity_list != []:
                entities = list(set(entities).intersection(set(entity_list)))

        return entities

    def get_components_for_entities(self, entity_ids, component_name):
        components = []
        for component_source in self.component_sources:
            if component_source.has(component_name):
                components += component_source.get_component_for_entities(
                    entity_ids, component_name)

        return components
