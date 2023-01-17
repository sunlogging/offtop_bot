function handler(){

var url = '/send&' + '?' +
'token=' + document.getElementById("token").value + '?' +
'chat_id_main=' + document.getElementById("chat_id_main").value + '?' +
'chat_url_main=' + document.getElementById("chat_url_main").value +  '?' +
'chat_id_offtopic=' + document.getElementById("chat_id_offtopic").value + '?' +
'chat_url_offtopic=' + document.getElementById("chat_url_offtopic").value + '?' +
'path_session=' + document.getElementById("path_session").value + '?' +
'path_json=' + document.getElementById("path_json").value + '?' +
'path_db=' + document.getElementById("path_db").value + '?' +
'webhook=' + document.getElementById("webhook").checked + '?' +
'statistics=' + document.getElementById("statistics").checked + '?' +
'note_user=' + document.getElementById("note_user").checked + '?' +
'database_auto=' + document.getElementById("database_auto").checked + '?' +
'webhook_path=' + document.getElementById("webhook_path").value + '?' +
'webhook_url=' + document.getElementById("webhook_url").value + '?' +
'webhook_host=' + document.getElementById("webhook_host").value + '?' +
'webhook_post=' + document.getElementById("webhook_post").value;

const xhr = new XMLHttpRequest();

xhr.open("POST", url);
xhr.send()
}