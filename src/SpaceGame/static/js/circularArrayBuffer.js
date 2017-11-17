var circularArrayBuffer = (function() {
	
	function CAB(maxlen){
		this.array = [];
		this.index = -1;
		this.maxlen = maxlen || 50;
	}

	CAB.prototype.top = function(){
		return this.array[this.index];
	}

	CAB.prototype.insert = function(item) {
		let new_position = this.index + 1
		if(new_position >= this.maxlen) {
			new_position -= this.maxlen
		}
		this.array[new_position] = item;
		this.index = new_position;
	}

	CAB.prototype.find = function(findfn) {
		if(this.array.length === 0){
			return null;
		}

		for(var i = this.index; i >= 0; i--) {
			let item = this.array[i];
			if(findfn(item)){
				return this.array[i];
			}
		}

		for(i = this.array.length-1; i > this.index; i--){
			let item = this.array[i];
			if(findfn(item)){
				return this.array[i];
			}
		} 
		return null;

	}


	return CAB
})()