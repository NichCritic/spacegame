

var QuestMenu = (function() {

    function QuestMenu() {
        var inv_menu = $("#quest_menu").dialog({
            autoOpen:false, 
            open:this.loadData.bind(null, this),
            close: this.cancelTimer.bind(null, this),
            width:600,
            height:400
        });
        var quest_list = $("#quest_list").menu();
    }

    QuestMenu.prototype.cancelTimer = function(menu) {
        
    }; 
   
    QuestMenu.prototype.loadData = function (self, event, ui) {
        $.getJSON("/quests", function success(data){
            var menu = $("#quest_list");
            menu.empty();
            
            for(let qname in data.quests) {
                let quest = data.quests[qname];
                let li = $("<li></li>")
                li.append($("<div>"+qname+"</div>"))
                li.append($("<div>"+"A short description of the quest"+"</div>"))
                let stage_list = $("<ul class='stage_list'></ul>")
                li.append(stage_list)
                for(var i = 0; i < 4; i++) {
                    stage_list.append($("<li><div>"+"A short description of the stage contents"+"</div></li>"))
                }

                li.appendTo(menu);
            }

            // $(".stage_list").menu();

            menu.menu("refresh");
            
        });
    }

    return QuestMenu;
})();