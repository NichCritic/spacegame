function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: {'body':JSON.stringify(args)}, dataType: "json", type: "POST",
        success: function(response) {
        callback(response);
    }});
};