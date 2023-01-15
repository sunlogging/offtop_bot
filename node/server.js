'use strict';

const http = require('http');
const port = process.env.PORT || 1337;
const host = 'localhost'

const fs = require('fs');
const path =  require('path');

http.createServer(function (req, res) {
    console.log(req.url)
    switch (req.url) {
        case '/':
            //Main
            res.writeHead(200, { 'Content-Type': 'text/html' });
            fs.readFile('./page/html/main.html', (err, data) => {
                console.log(data)
                console.log(err)
                res.end(data);
            })
            break;

        case '/login':
            //login
            res.writeHead(200, { 'Content-Type': 'text/html' });
            fs.readFile('./page/html/login.html', (err, data) => {
                res.end(data);
            })
            break;

        case '/create':
            //Create
            res.writeHead(200, { 'Content-Type': 'text/html' });
            fs.readFile('./page/html/create.html', (err, data) => {
                res.end(data);
            })
            break;

    }
    


    
}).listen(port, host);
