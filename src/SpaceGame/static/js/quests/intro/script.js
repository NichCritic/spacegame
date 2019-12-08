var quests = quests ? quests : {};
quests.intro = quests.intro ? quests.intro : {};
quests.intro.script = (function(){
	var bossman_text_template = "<div class='quest_img_box'><img src='./static/assets/bossman.png'/></div><div class='quest_text'>$text$</div>"
	var script = [
		"Hey! You're awake!",
		"Good, we were starting to worry!",
		"You're probably wondering what's going on. Don't worry, I'll explain.",
		"You were part of one of those freezing experiments that were popular in the 2000's.",
		"The good news is, you were right! It's possible to revive a consciousness just from the contents of it's frozen brain.",
		"So now you're in the future! Whee!",
		"The bad news is, well, it's the future. Life is cheap. 21st century life, well, that's cheaper than dirt, literally",
		"The other bad news is, you probably set aside assets. Hoping inflation would keep them worth an equivalent amount in the future...",
		"NOPE! WRONG! They're totally worthless now",
		"So let me break down your situation:",
		"You're in a tremendous amount of debt.",
		"Your frozen head was bought for - what's the  21st century expression - pennies on the dollar",
		"Now you work for Minecore. Slavery was made illegal for conscious beings, but 21st century brains fall into a bit of a <i>legal gray area</i>. That is to say, you're not provably conscious in the way us advanced life forms are. So this is totally ok",
		"Now have a look at your body. Try to move it around a little bit. You might have noticed a few changes from the body you used to have",
		"You're a spaceship! More specifically, you're a G48-1204 class mining spacecraft.",
		"Now you might be thinking, 'HEY WTF WHERE IS MY BODY'. That's totally normal ^_^",
		"I promise you'll get used to it",
		"Now, time to get used to the controls.",
		"Use the arrow keys to fly left to find some asteroids.",
		"When you find one, get close and hold the SPACE key to start mining. Be patient, it might take a while!",
		"Come back to the space station when you've mined <b>10 pieces of iron ore</b>",
		"And you might be thinking, 'screw this I'll just fly away'. And you can do that, and if you do we'll blow you up and put you in a new ship",
		"You can keep blowing up again and again and you won't deplete our resources one bit. That ship you're in is every bit as cheap as you are",
		"Have fun! Remember, <b>Come back with 10 iron ore</b>. Press Q to check your progress, if you forget"
	]

	for(var i = 0; i < script.length; i++) {
		let line = script[i];
		script[i] = bossman_text_template.replace('$text$', line);
	}

	return script;
})();
