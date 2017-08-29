

def projectile(node, time_to_hit, fn, args):
    # A projectile leaves a source arrives at a destination, but since we're dealing with abstract space we just attach the projectile to the target node
    # The target will be informed that the projectile is coming and can
    # attempt a defence
    node.add_or_attach_component(
        "projectile", {"time_to_hit": time_to_hit, "fn": fn, "args": args})


def damage(node, damage, msg):
    node.add_or_attach_component(
        "change_health", {"amount": -damage, "message": msg})


def damage_over_time(node, damage, tick, end):
    node.add_or_attach_component(
        "damage_over_time", {"damage": damage, "tick": tick, "end": end})


def listen_for_target(rune, on_target):
    rune.add_or_attach_component("listening", {"on_message": on_target})
