'use strict';

const http = require('http');
const port = process.env.PORT || 1337;
const host = 'localhost'

const fs = require('fs');
const path =  require('path');

http.createServer(function (req, res) {
    console.log(req.url)
    switch (req.url) {
        case '/style.css':
            res.writeHead(200, { 'Content-Type': 'text/css' });
            fs.readFile('./page/style.css', (err, data) => {
                res.end(data);
            });
            break;

        case '/main_style.ttf':
            res.writeHead(200, { 'Content-Type': 'text/css' });
            fs.readFile('./page/fonts/Gafata-Regular.ttf', (err, data) => {
                res.end(data);
            });
            break;


        case '/':
            //Main
            res.writeHead(200, { 'Content-Type': 'text/html' });

            fs.readFile('./page/html/main.html', (err, data) => {

                res.end(data);
            });
            break;

        case '/main.css':
            res.writeHead(200, { 'Content-Type': 'text/css' });
            fs.readFile('./page/css/main.css', (err, data) => {
                res.end(data);
            });
            break;

        case '/main.js':
            res.writeHead(200, { 'Content-Type': 'text/javascript' });
            fs.readFile('./page/js/main.js', (err, data) => {
                res.end(data);
            });
            break;

    }
    


    
}).listen(port, host);
