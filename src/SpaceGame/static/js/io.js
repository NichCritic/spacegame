function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback, error) {
    // args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: {'body':JSON.stringify(args)}, dataType: "json", type: "POST",
        success: callback, error: error});
};

var throttledGetServerData =  locked(getServerData);
var throttledSendServerData = locked(sendServerData);

function getServerData(unlock_fn, args){
    let inputs = args.inputs;
    let gamestate_buffer = args.gamestate_buffer;
    $.postJSON('./a/message/updates', {}, function success(result){
        let serverState = result.messages[0];

        for(let i = inputs.length-1; i >= 0; i--){
            let inp = inputs[i];
            if(inp.was_processed){
                break;
            }
            if(inp.time <= serverState.time){
                inp.was_processed = true;
            }
        }
        var new_inputs = []
        for(let i = 0; i < inputs.length; i++){
            let inp = inputs[i];
            if(inp.was_processed === false){
                new_inputs.push(inp);

            }
        }
        inputs= new_inputs
        gamestate_buffer.insert(serverState); 
        unlock_fn();
    }, function error(result){
        unlock_fn();
    });
    
}

function sendServerData(unlock_fn, args){
    let inputs = args.inputs;
    let to_send = []
    for(let i = 0; i < inputs.length; i++){
        let inp = inputs[i];
        if(!inp.was_sent){
            to_send.push(inp)
            inp.was_sent = true
        }
    }
    $.postJSON('./a/message/new', {'inputs':to_send}, function(result){
        unlock_fn();

    }, function error(result){
        unlock_fn();
    });    
}