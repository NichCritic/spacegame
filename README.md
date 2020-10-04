# Spacegame

This is a browser based MMO written in Python and Javascript. It builds upon my previous work on [Pymud](https://github.com/NichCritic/pymud) but uses websockets and a more robust frontend to deliver a responsive experience.

## Installation

### Requirements
Python 3+, SQLAlchemy and Tornado

### Initialisation
1. Create a file called keys.py with the following info:
```python
cookie_secret="YOURCOOKIESECRET"
google_oauth_key="your-google-oath-key"
google_oauth_secret="your-oauth-secret"
```
2. In `network\chatserver.py` in the AuthLoginHandler, change naelick.com:8888 to your host. If you are running locally, make up a hostname and configure your system hosts file to reroute it to 127.0.0.1

3. Run `python database_setup_level0.py` to initialize the database

### Running
1. Run main.py. A server is set up at http://<yourhost>:8888/
2. Visit that site, authorize with google, and create a character
3. You should be redirected to the main page and be able to play

## Controls
Up Arrow key: Thrust
Right/Left Arrow key: Turn
F key: Shoot
D key: Brake
C key: Enter shop
SPACE key: Mine from asteroids
I key: View inventory
U key: View and apply upgrades
M key: View minimap
Q key: View Quest status

## Architecture
The game logic is divided into Systems (found in the Systems folder). At each game tick, each system gets access to the Component data for every entity it is interested in, specified in the mandatory and optional arrays at the top of each System, performs operations on it, and adds or removes Components as needed to complete its task.
Typically a System will be related to some component which doesn't contain any data, which acts as a flag. If that flag doesn't exist on any components the System doesn't run.

Data for entities are divided into Components, found in the objects/components.py file. Components are data classes with little to no logic, except where it makes sense to extrapolate from some data or store the component's creation time. Components are stored in dictionaries indexed by component name and entity id. This provides the ability to quickly fetch all entities with a specific component, for Systems, while also allowing the quick access of the components of a known entity.

Data access is facilitated by the NodeFactory and Node classes. A Node is an entity and associated collection of components. A Node only has data for components attached to it, but provides helper methods to add and remove components, as well as query if a component is available to be attached. The NodeFactory is responsible for creating Nodes and lists of Nodes with specific components. A typical use pattern is to create a Node and then use the "add_or_attach_component" method to attach components to the Node if they already exist or create them if they don't.

Network communication is done by the GameStateRequestSystem, which gathers information about the player entity and other entities that are relevant and then sends them to the player once per tick. Incoming messages are recieved by the command/command_handler.py class and transformed from keypress inputs to Components read by the physics Systems. Other networking tasks are performed by the classes in network/chatserver.py, such as sending data for shops and player inventory when those screens are open.
