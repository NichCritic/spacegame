function locked(fn){
    let lock = false;
    function unlock_fn(){
        lock = false;
    }
    function inner(args){
        if(!lock){
            fn(unlock_fn, args);
            lock = true;
        }
    }
    return inner;
}