function locked(fn){
    let lock = false;
    function unlock_fn(){
        lock = false;
    }
    function inner(args){
        if(!lock){
            ret = fn(unlock_fn, args);
            lock = true;
        }
        return ret;
    }
    return inner;
}

function cubic_bezier(x1, y1, x2, y2, t) {
    let x = 3*t*x1*(1-t)**2 + 3*(1-t)*x2 * t**2 + t**3;
    let y = 3*t*y1*(1-t)**2 + 3*(1-t)*y2 * t**2 + t**3;
    return {x:x, y:y};
}