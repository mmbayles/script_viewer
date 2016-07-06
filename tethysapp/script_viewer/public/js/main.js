function find_query_parameter(name) {
    url = location.href;
    //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(url);
    return results == null ? null : results[1];
}
var popupDiv = $('#welcome-popup');
$('document').ready(function () {
    var res_id = find_query_parameter("res_id");
    var src = find_query_parameter("src");
    if (res_id == null) {
        if (document.referrer == "https://apps.hydroshare.org/apps/") {
            $('#extra-buttons').append('<a class="btn btn-default btn" href="https://apps.hydroshare.org/apps/">Return to HydroShare Apps</a>');
        }
        popupDiv.modal('show');
    }

    $('#editor_div').hide()
    if(res_id != null)
    {
        $('#loading').show()
        add_script(res_id, src);
    }


    document.title = 'Script Viewer';
});

function getNumberOfLines(str) {
    //get the number of lines
    var lines = str.split(/\r\n|\r|\n/);
    return lines.length;
}
function finishloading(callback) {
    $('#editor_div').show()
    $('#loading').hide()

}
function add_script(res_id, src) {
    current_url = location.href;
    index = current_url.indexOf("script-viewer");
    base_url = current_url.substring(0, index);

    // in the start we show the loading...
    // the res_id can contain multiple IDs separated by comma
    data_url = base_url + 'script-viewer/chart_data/' + src + '/' + res_id + '/';
    $.ajax({
        url: data_url,
        success: function (json) {
            //console.log(json)
            //decode = encodeURI(json)
            //console.log(decode)
            //happy = decodeURIComponent(jQuery.param(json.script))
            //console.log(happy)
            //$('#editor_div').html(json)
            var editor = ace.edit("editor_div");
            editor.setTheme("ace/theme/chaos");
            editor.getSession().setMode("ace/mode/r");
            editor.$blockScrolling = Infinity
            editor.getSession().setValue(json.script)
            finishloading();
        }
    })


}


