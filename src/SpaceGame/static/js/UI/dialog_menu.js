

var DialogMenu = (function() {
    var page = 0;
    var data = [];

    function DialogMenu() {
        this.dialog = $("#dialog_menu").dialog({autoOpen:false});
        this.next_button = $("#dialog_next_button").button();
        this.next_button.click( function( event ) {
            event.preventDefault();
            page = Math.min(page+1, data.length-1);
            showPage(data, page);
        } ).css('visibility', 'hidden');
        this.prev_button = $("#dialog_prev_button").button();
        this.prev_button.click( function( event ) {
            event.preventDefault();
            page = Math.max(page-1, 0);
            showPage(data, page);
        } ).css('visibility', 'hidden');
    } 
   
    DialogMenu.prototype.open = function(my_data, my_page) {
        var page = my_page ? my_page : 0;
        data = my_data;
        showPage(data, page);
        this.dialog.dialog("open");        
    }

    function showPage(data, page) {
        $("#dialog_menu_content").html(data[page]);
        $("#dialog_next_button").css('visibility', 'hidden');
        $("#dialog_prev_button").css('visibility', 'hidden');



        if(page > 0) {
            $("#dialog_prev_button").css('visibility', 'visible');            
        }
        if(page < data.length-1) {
            $("#dialog_next_button").css('visibility', 'visible');            
        }

    }

    return DialogMenu;
})();