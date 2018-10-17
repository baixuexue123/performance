const net = require('net');

const host = '127.0.0.1';
const port = 8888;

const server = net.createServer();

server.listen(port, host, () => {
    console.log('Server listening on %j', server.address());
});

server.on('connection', function(sock) {
    let peername = sock.remoteAddress + ':' + sock.remotePort;
    console.log(`A new connection(${peername}) has been established.`);

    sock.on('data', function(data) {
        let msg = data.toString();
        if (msg !== 'ping\r\n') {
            console.log('Connection - ' + peername + 'ERROR: ' + msg);
            sock.end();
        } else {
            sock.write('pong\r\n');
        }
    });

    sock.on('close', function() {
        console.log('CLOSED - ' + peername);
    });
});
