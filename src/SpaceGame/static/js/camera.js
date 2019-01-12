var camera = {x:0, y:0, w:1200, h:600};
function camera_track(camera, entity) {
	var new_camera = {
	    x: entity.position.x - camera.w /2,
	    y: entity.position.y - camera.h /2,
	    h: camera.h,
	    w: camera.w
	}

	return new_camera;
}