
function handler() {

    var url = '/send&'


    let inputs = document.querySelectorAll('input');

    for (let i = 0; i < inputs.length; i++) {
        if (typeof (inputs[i].value) == undefined) continue;
        if (inputs[i].type == 'checkbox') {
            url += inputs[i].id.toUpperCase() + '=' + inputs[i].checked + '?';
            continue
        }
        url += inputs[i].id.toUpperCase() + '=' + inputs[i].value + '?';
    }

    const xhr = new XMLHttpRequest();
    console.log(url)
    xhr.open("POST", url);
    xhr.send()
}