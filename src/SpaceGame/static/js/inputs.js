function Input(data){
	this.left = data.left || false;
	this.right = data.right || false;
	this.thrust = data.thrust || false;
	this.brake = data.brake || false;
    this.shoot = data.shoot || false;
    this.mining = data.mining || false;
    this.time = data.time || 0;
    this.dt = data.dt || 0;
    this.was_processed = false;
    this.was_sent = false;
}

function InputList(data){
	this.list = [];
}

InputList.prototype = {
	getUnprocessedInput:function(){
		let last_processed = 0;
        for(let i = this.list.length-1; i >= 0; i--){
            let inp  = this.list[i];
            if(inp.was_processed){
	            last_processed = i + 1;
            	break;
        	}
            
    	}
    	return this.list.slice(last_processed);
	},
	push: function(item){
		this.list.push(item)
	},
    update: function(time) {
        for(let i = this.list.length-1; i >= 0; i--){
            let inp = this.list[i];
            if(inp.was_processed){
                break;
            }
            if(inp.time <= time){
                inp.was_processed = true;
            }
        }
        var new_inputs = [];
        for(let i = 0; i < this.list.length; i++){
            let inp = this.list[i];
            if(inp.was_processed === false){
                new_inputs.push(inp);
            }
        }
        this.list = new_inputs
    }

}