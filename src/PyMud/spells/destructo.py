from Systems.AVEvent import AVEvent


def create_av_event_data(location, source_id, messages, target):
    event = AVEvent("reducto", None, location, source_id, messages, target)
    return event


def destructo_fn(player_node, room_node, target_node):
    player_node.add_or_attach_component('location', None)

    av_event_data = create_av_event_data(player_node.location.detach(), player_node.id, destructo[
        "messages"], target_node.id)
    room_node.add_or_attach_component("av_events", None)
    room_node.av_events.events.append(av_event_data)
    print("target: {}".format(target_node.id))
    target_node.remove_component('container')


destructo = {
    "function": destructo_fn,

    "messages": [
        ([("visibility", 50), ("targeted",), ("is_target",)], [
            'You dissolve into a fine mist. You are dead.']),
        ([("visibility", 50), ("targeted",), ],
         ['{target} dissolves into a fine mist, never to be seen again.'])]
}
