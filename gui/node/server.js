'use strict';

const http = require('http');
const port = 8088;
const host = '127.0.0.1'

const fs = require('fs');
const path = require('path');

var exec = require('child_process').execFile;

function searth_file_for_send(request) {

    var name_file = request[0].split('/')[1];
    var type_file = request[1];


    switch (type_file) {
        case 'css':
            if (name_file == 'style') {
                return fs.readFileSync('./gui/node/page/style.css', (err, data) => { console.log(err); return data; });
            } else { return fs.readFileSync('./gui/node/page/css/' + name_file + '.css', (err, data) => { console.log(err); return data; }); }
            break;

        case 'js':
            if (name_file == 'script') {
                return fs.readFileSync('./gui/node/page/script.js', (err, data) => { console.log(err); return data; });
            } else { return fs.readFileSync('./gui/node/page/js/' + name_file + '.js', (err, data) => { console.log(err); return data; }); }
            break;

        case 'ttf':
            return fs.readFileSync('./gui/node/page/style/' + name_file + '.ttf', (err, data) => { console.log(err); return data; });
            break;
    }
}

http.createServer(function (req, res) {

    var request_type = req.url.split('.')
    var request_args = req.url.split('&')
    console.log(req.url)
    if (request_type.length < 2) {
        console.log(request_type, request_args, request_args.length < 2)
        if (request_args.length > 1) {
            switch (request_args[0]) {
                case '/send':
                    var args = request_args[1].split('?');
                    args.pop()
                    fs.writeFileSync('./.env', '')
                    for (let index = 0; index < args.length; index++) {
                        console.log(args[index].split('='))
                        fs.appendFileSync('./.env', args[index].split('=')[0].toUpperCase() + "=" + args[index].split('=')[1] + '\n')
                    }
                    exec('move_file.bat')
                    break;

            }
        } else {
            switch (req.url) {

                case '/': return fs.readFile('./gui/node/page/html/main.html', (err, data) => { console.log(err); res.end(data); }); break;
                case '/create': return fs.readFile('./gui/node/page/html/create.html', (err, data) => { console.log(err); res.end(data); }); break;
                case '/about_us': return fs.readFile('./gui/node/page/html/about_us.html', (err, data) => { console.log(err); res.end(data); }); break;

                default: return fs.readFile('./gui/node/page/html/error.html', (err, data) => { console.log(err); res.end(data); }); break;
            }
        }


    } else res.end(searth_file_for_send(request_type));



}).listen(port, host);
