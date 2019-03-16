function do_physics(node, control, dt) {
	let mass = node.mass.mass;
	let rotation = node.rotation.rotation;

	let rot_left = (rotation - 1/200 * dt);
	let rot_right = (rotation + 1/200 * dt);

	node.rotation.rotation = control.left ? rot_left : (control.right ? rot_right : rotation);

	rotation = node.rotation.rotation
	
	let thrust = node.thrust.thrust;

	node.force.x = control.thrust ? dt * thrust * Math.sin(rotation) + (-0.03*node.velocity.x*dt): 0;
	node.force.y = control.thrust ? -dt * thrust * Math.cos(rotation) + (-0.03*node.velocity.y*dt) : 0;

	node.acceleration.x = node.force.x/mass;
    node.acceleration.y = node.force.y/mass;

    node.velocity.x = node.velocity.x + node.acceleration.x * dt;
    node.velocity.y = node.velocity.y + node.acceleration.y * dt;

    if(!control.brake){
    	node.velocity.x *= Math.pow(0.99, dt);
    	node.velocity.y *= Math.pow(0.99, dt);
    }

    node.position.x = node.position.x + node.velocity.x * dt;
    node.position.y = node.position.y + node.velocity.y * dt;
}