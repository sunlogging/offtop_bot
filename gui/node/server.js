'use strict';

const http = require('http');
const port = 8088;
const host = '127.0.0.1'

const fs = require('fs');
const path =  require('path');

var exec = require('child_process').execFile;

var move_env = function(){
   exec('move_file.bat');
}

function searth_file_for_send(request) {

    var name_file = request[0].split('/')[1];
    var type_file = request[1];


    switch (type_file) {
        case 'css':
            if (name_file == 'style') { return fs.readFileSync('./!node/page/style.css', (err, data) => { console.log(err); return data; });
            } else { return fs.readFileSync('./!node/page/css/' + name_file + '.css', (err, data) => { console.log(err); return data; }); }
            break;

        case 'js':
            if (name_file == 'script') { return fs.readFileSync('./!node/page/script.js', (err, data) => { console.log(err); return data;});
            } else{ return fs.readFileSync('./!node/page/js/' + name_file + '.js', (err, data) => { console.log(err); return data;});}
            break;

        case 'ttf':
            return fs.readFileSync('./!node/page/style/' + name_file + '.ttf', (err, data) => { console.log(err); return data;});
            break;
    }
}

http.createServer(function (req, res) {

    var request = req.url.split('.')
    console.log(req.url)
    if (request.length < 2) {
        switch (req.url) {

            case '/': return fs.readFile('./!node/page/html/main.html', (err, data) => {console.log(err); res.end(data); }); break;
            case '/create': return fs.readFile('./!node/page/html/create.html', (err, data) => {console.log(err); res.end(data); });; break;
            case '/about_us': return fs.readFile('./!node/page/html/about_us.html', (err, data) => {console.log(err); res.end(data); });; break;

            default: return fs.readFile('./!node/page/html/error.html', (err, data) => {console.log(err); res.end(data); });;; break;
        }
    } else res.end(searth_file_for_send(request));
    


}).listen(port, host);
