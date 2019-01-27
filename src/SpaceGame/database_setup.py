from objects.item import Item
import startup_scripts

session_manager = startup_scripts.setup_db('sqlite:///main.db')

with session_manager.get_session() as session:
    session.add(Item("gold"))
    session.add(Item("silver"))
    session.add(Item("copper"))
    session.add(Item("crystal"))
