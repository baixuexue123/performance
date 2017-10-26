const http = require('http');

const hostname = '127.0.0.1';
const port = 8000;

const server = http.createServer((req, res) => {
    console.log(Date.now() + ' : ' + req.headers.host);
    setTimeout(() => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'text/html');
        res.end('<p>Hello World</p>');
    }, 100);
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
