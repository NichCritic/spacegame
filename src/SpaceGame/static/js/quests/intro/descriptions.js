var quests = quests ? quests : {};
quests.intro = quests.intro ? quests.intro : {};
quests.intro.descriptions = (function(){
	var quest_desc = "Meet Mr. Bossman and accept your new lot in life"

	var stages_desc = [
		"You need to talk to Mr Bossman",
		"You need to collect 10 iron ore from asteroids and bring them back to the station",
		"You need to sell an iron ore in the shop for credits",
		"Quest complete!"
	]

	var stages_completed_desc = [
		"You met Mr Bossman and learned what your new life entails",
		"You collected 10 iron ore and returned it to Mr Bossman",
		"You exchanged some iron ore for company store credit",

	]


	var descs = {
		quest:quest_desc,
		stages: stages_desc,
		stages_completed:stages_completed_desc
	};

	return descs;
})();
