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
        $('#loading').hide()
        if (document.referrer == "https://apps.hydroshare.org/apps/") {
            $('#extra-buttons').append('<a class="btn btn-default btn" href="https://apps.hydroshare.org/apps/">Return to HydroShare Apps</a>');
        }
        popupDiv.modal('show');
    }
    $('#tabs').hide()
    $('#content_tab').hide()
    if(res_id != null)
    {
        $('#loading').show()
        add_script(res_id, src);
    }

    document.title = 'Script Viewer';
});

function add_script(res_id, src) {
    current_url = location.href;
    index = current_url.indexOf("script-viewer");
    base_url = current_url.substring(0, index);
    ext = []
    // in the start we show the loading...
    // the res_id can contain multiple IDs separated by comma
    data_url = base_url + 'script-viewer/chart_data/' + src + '/' + res_id + '/';
    $.ajax({
        url: data_url,
        success: function (json) {
            script_type = json.script_type
            counter =0
            counter1 =0
            var size = Object.keys(json).length;
             for(item in json) {
                 tab_name = Object.keys(json)[counter]
                 id = 'editor_div' + counter
                 //console.log(json[item])

                 ext_name = tab_name.split('.').pop()
                 console.log(ext_name)
                 if(ext_name =='py'){

                     ext.push('python')
                     console.log(ext)
                 }
                 else if(ext_name =='r'){
                     ext.push('r')
                 }
                 else if(ext_name =='m'){
                     ext.push('matlab')
                 }
                 else {
                     ext.push('text')
                 }
                 list_string = '<li><a href="#" id="'+counter+'" class="tablinks"  onclick= "openCity(event,\'' + id + '\',\''+tab_name+'\' )">' + tab_name + '</a></li>'
                 $('#list').append(list_string)
                 $('#content_tab').append('<div  id="' + id + '" class="tabcontent">' +
                     '</div>')
                 counter = counter +1

             }

            $('#0').click()
            for(item in json)
            {
                mode = ext[counter1]
                console.log (mode)
                var editor = ace.edit("editor_div"+counter1);
                editor.setTheme("ace/theme/chaos");
                editor.getSession().setMode("ace/mode/"+mode);
                editor.$blockScrolling = Infinity
                editor.getSession().setValue(json[item])
                counter1 = counter1 +1
            }
            finishloading();
        }
    })
}

function openCity(evt, cityName,file_name) {
    // Declare all variables
    $("#hydroshare").remove();
    $('#save').append('<button id = "hydroshare"  type="button" name ="'+file_name+'" class="btn btn-primary" onclick= "save_file(\''+file_name+'\',\''+cityName+'\')">Save to HydroShare</button>')
    var i, tabcontent, tablinks;
    console.log(file_name)
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(cityName).style.display = "block";
    //evt.currentTarget.className += " active";
}
function save_file(file_name,div_name){
    console.log(file_name)
    $('#loading').show()
    $('#tabs').toggle()
    $('#content_tab').toggle()
    $('#hydroshare').hide()
    var res_id = find_query_parameter("res_id");
    var src = find_query_parameter("src");
    var editor = ace.edit(div_name);
    var code = editor.getValue();
    console.log(code)
    var csrf_token = getCookie('csrftoken');
    data_url = base_url + 'script-viewer/save_file/' + src + '/' + res_id + '/'+file_name +'/';
    $.ajax({
            type:"POST",
            headers:{'X-CSRFToken':csrf_token},
            dataType: 'json',
            data:{'script':code},
            url: data_url,
            success: function (json) {
                console.log(json)
                finishloading()
            }
    }
    )}
function finishloading(callback) {
    $('#editor_div').show()
    $('#loading').hide()
     $('#tabs').show()
    $('#content_tab').show()
    $('#hydroshare').show()
}
$("#theme").click( function() {
   var obj = document.getElementById("theme");
   x= obj.options[obj.selectedIndex].text;
    console.log("selected")
    console.log(x)
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
