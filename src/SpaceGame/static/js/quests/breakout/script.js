var quests = quests ? quests : {};
quests.breakout = quests.breakout ? quests.breakout : {};
quests.breakout.script = (function(){
	var bossman_text_template = ""
	var stage2 = []

	var stage3 = []

	var stage4 = []

	for(var i = 0; i < stage2.length; i++) {
		let line = stage2[i];
		stage2[i] = bossman_text_template.replace('$text$', line);
	}
	for(var i = 0; i < stage3.length; i++) {
		let line = stage3[i];
		stage3[i] = bossman_text_template.replace('$text$', line);
	}
	for(var i = 0; i < stage4.length; i++) {
		let line = stage4[i];
		stage4[i] = bossman_text_template.replace('$text$', line);
	}

	var script = {
		stage2:stage2,
		stage3:stage3,
		stage4:stage4
	};

	return script;
})();
