var quests = quests ? quests : {};
quests.breakout = quests.breakout ? quests.breakout : {};
quests.breakout.descriptions = (function(){
	var quest_desc = "Find a way out of this hellish slavery"

	var stages_desc = [
		"You need to find someone who can help you escape Minecorp's grasp",
		"Quest complete!"
	]

	var stages_completed_desc = [
		"You met The Hacker, who offered to sell you a special upgrade",
	]


	var descs = {
		quest:quest_desc,
		stages: stages_desc,
		stages_completed:stages_completed_desc
	};

	return descs;
})();
