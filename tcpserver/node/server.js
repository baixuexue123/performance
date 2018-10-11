const net = require('net');

const host = '127.0.0.1';
const port = 8888;

const server = net.createServer();
server.listen(port, host, () => {
    console.log('Server listening on %j', server.address());
});

const sockets = [];

server.on('connection', function(sock) {
    console.log('A new connection has been established.');
    console.log('CONNECTED - ' + sock.remoteAddress + ':' + sock.remotePort);
    sockets.push(sock);

    sock.on('data', function(data) {
        console.log('DATA - ' + sock.remoteAddress + ': ' + data);
        // Write the data back to all the connected,
        // the client will receive it as data from the server
        sockets.forEach(function(sock, index, array) {
            sock.write(sock.remoteAddress + ':' + sock.remotePort + " said " + data + '\n');
        });
    });

    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        let index = sockets.findIndex(function(o) {
            return o.remoteAddress === sock.remoteAddress && o.remotePort === sock.remotePort;
        });
        if (index !== -1) sockets.splice(index, 1);
        console.log('CLOSED - ' + sock.remoteAddress + ' ' + sock.remotePort);
    });

    // When the client requests to end the TCP connection with the server, the server
    // ends the connection.
    /**
     * 服务端收到客户端发出的关闭连接请求时，会触发end事件
     * 这个时候客户端没有真正的关闭，只是开始关闭；
     * 当真正的关闭的时候，会触发close事件；
     * */
    sock.on('end', function() {
        console.log('Closing connection with the client');
    });

    // When client timeout.
    sock.on('timeout', function () {
        console.log('Client request time out. ');
    });

    // Don't forget to catch error, for your own sake.
    sock.on('error', function(err) {
        console.log(`Error: ${err}`);
    });
});
