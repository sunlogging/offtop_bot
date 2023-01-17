function handler(){
var token = document.getElementById("token").value;
var chat_id_main = document.getElementById("chat_id_main").value;
var chat_url_main = document.getElementById("chat_url_main").value;
var chat_id_offtopic = document.getElementById("chat_id_offtopic").value;
var chat_url_offtopic = document.getElementById("chat_url_offtopic").value;

var path_session = document.getElementById("path_session").value;
var path_json = document.getElementById("path_json").value;
var path_db = document.getElementById("path_db").value;

var webhook = document.getElementById("webhook").value;
var statistics = document.getElementById("statistics").value;
var note_user = document.getElementById("note_user").value;
var database_auto = document.getElementById("database_auto").value;

var webhook_path = document.getElementById("webhook_path").value;
var webhook_url = document.getElementById("webhook_url").value;
var webhook_host = document.getElementById("webhook_host").value;
var webhook_post = document.getElementById("webhook_post").value;

var url = '/send&' + '?' +
'token=' + token + '?' +
'chat_id_main=' + chat_id_main + '?' +
'chat_url_main=' + chat_url_main +  '?' +
'chat_id_offtopic=' + chat_id_offtopic + '?' +
'chat_url_offtopic=' + chat_url_offtopic + '?' +
'path_session=' + path_session + '?' +
'path_json=' + path_json + '?' +
'path_db=' + path_db + '?' +
'webhook=' + webhook + '?' +
'statistics=' + statistics + '?' +
'note_user=' + note_user + '?' +
'database_auto=' + database_auto + '?' +
'webhook_path=' + webhook_path + '?' +
'webhook_url=' + webhook_url + '?' +
'webhook_host=' + webhook_host + '?' +
'webhook_post=' + webhook_post

window.open(url, '_blank');
}