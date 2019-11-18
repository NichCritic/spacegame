import objects.item


def get_shop_data(session):
    gold_ore = objects.item.get_item_by_name(session, 'gold ore')
    silver_ore = objects.item.get_item_by_name(session, 'silver ore')
    iron_ore = objects.item.get_item_by_name(session, 'iron ore')
    # gasoline = objects.item.get_item_by_name(session, 'gasoline')
    # gold = objects.item.get_item_by_name(session, 'gold')
    # silver = objects.item.get_item_by_name(session, 'silver')
    # iron = objects.item.get_item_by_name(session, 'iron')

    # gold_mine = {"shop_data": {
    #     "name": "Gold mine",
    #     "sale_items": [
    #         {"id": iron_ore.id, "pos": 0, "cost": 10},
    #         {"id": gold_ore.id, "pos": 1, "cost": 1000},
    #     ],
    #     "buy_items": [
    #         {"id": gasoline.id, "pos": 0, "min_price": 1, "max_price": 500}
    #     ],
    #     "process": [
    #         {"id": gasoline.id, "amt": 1, "products": {
    #             iron_ore.id: 10, gold_ore.id: 1}}
    #     ]
    # }}

    # silver_mine = {"shop_data": {
    #     "name": "Silver mine",
    #     "sale_items": [
    #         {"id": iron_ore.id, "pos": 0, "cost": 10},
    #         {"id": silver_ore.id, "pos": 1, "cost": 100},
    #     ],
    #     "buy_items": [
    #         {"id": gasoline.id, "pos": 0, "min_price": 1, "max_price": 500}
    #     ],
    #     "process": [
    #         {"id": gasoline.id, "amt": 1, "products":
    #             {iron_ore.id: 10, silver_ore.id: 10}}
    #     ]
    # }}

    # ore_refinery = {"shop_data": {
    #     "name": "Ore Refinery",
    #     "sale_items": [
    #         {"id": iron.id, "pos": 0, "cost": 100},
    #         {"id": silver.id, "pos": 1, "cost": 1000},
    #         {"id": gold.id, "pos": 2, "cost": 10000}
    #     ],
    #     "buy_items": [
    #         {"id": iron_ore.id, "pos": 0, "min_price": 1, "max_price": 11},
    #         {"id": silver_ore.id, "pos": 1, "min_price": 1, "max_price": 110},
    #         {"id": gold_ore.id, "pos": 2, "min_price": 1, "max_price": 1100}
    #     ],
    #     "process": [
    #         {"id": iron_ore.id, "amt": 5, "products": {iron.id: 1}},
    #         {"id": silver_ore.id, "amt": 5, "products": {silver.id: 1}},
    #         {"id": gold_ore.id, "amt": 5, "products": {gold.id: 1}}
    #     ]
    # }}

    # jeweler = {"shop_data": {
    #     "name": "Jeweler",
    #     "sale_items": [

    #     ],
    #     "buy_items": [
    #         {"id": iron.id, "pos": 0, "min_price": 101, "max_price": 110},
    #         {"id": silver.id, "pos": 1, "min_price": 1001, "max_price": 1100},
    #         {"id": gold.id, "pos": 2, "min_price": 10001, "max_price": 11000}
    #     ],
    #     "process": [

    #     ]
    # }}

    # oil_refinery = {"shop_data": {
    #     "name": "Oil Refinery",
    #     "sale_items": [
    #         {"id": gasoline.id, "pos": 0, "cost": 100},
    #     ],
    #     "buy_items": [],
    #     "process": [{"id": None, "amt": 0, "products": {gasoline.id: 5}}]
    # }}

    ore_shop = {"shop_data": {
        "name": "Shop",
        "sale_items": [
        ],
        "buy_items": [
            {"name":iron_ore.name, "id": iron_ore.id, "pos": 0, "min_price": 11, "max_price": 11},
            {"name":silver_ore.name, "id": silver_ore.id, "pos": 1, "min_price": 110, "max_price": 110},
            {"name":gold_ore.name, "id": gold_ore.id, "pos": 2, "min_price": 1100, "max_price": 1100}
        ]
    }}

    return [ore_shop, ]  # jeweler, oil_refinery, gold_mine, silver_mine]
