from Systems.system import TimedSystem


class ProjectileSystem(TimedSystem):
    manditory = ['projectile']
    handles = []

    def handle(self, node, curr_time):
        last_trigger = node.projectile.last_trigger
        timeout = node.projectile.timeout

        if last_trigger is None:
            node.projectile.last_trigger = curr_time

        if self.is_timed_out(last_trigger, curr_time, timeout):
            fn = node.projectile.on_hit
            fn(**node.projectile.args)

            node.remove_component('projectile')


class ProjectileDodgingSystem(TimedSystem):
    manditory = ['dodging']
    optional = ['projectile']

    def handle(self, node, curr_time):
        if node.has('projectile'):
            # AV event for dodging projectiles
            node.remove_component('projectile')
            node.remove_component('dodging')
        else:
            last_trigger = node.dodging.last_trigger
            timeout = node.dodging.timeout

            if not last_trigger:
                # AV event for dodge started
                node.dodging.last_trigger = curr_time

            if self.is_timed_out(last_trigger, curr_time, timeout):

                # AV event for dodge ended
                node.remove_component('dodging')
