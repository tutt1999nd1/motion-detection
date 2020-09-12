var app = require('express')();
var http = require('http').Server(app);
var ioIn = require('socket.io')(http);
var ioOut = require('socket.io-client');
var socketOut = ioOut.connect('http://localhost:9090/motion');

var nsp = ioIn.of('/my-namespace');
nsp.on('connection', function(socket) {
	socketOut.on('id1234', function(msg) {
    nsp.emit('hi', msg);
	});
});



app.get('/', function(req, res) {
   res.sendfile('check.html');
});
http.listen(3000, function() {
   console.log('listening on localhost:3000');
});