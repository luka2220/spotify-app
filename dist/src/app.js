"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const http = require("node:http");
const router_1 = require("./routes/router");
// TODO: Parse out the request url for routing
// Check the url routes for available routing on the server and site
const server = http.createServer((req, res) => {
    const serverResponse = (0, router_1.ParseIncomingURL)({ url: req.url, method: req.method });
    res.statusCode = serverResponse.status;
    res.write(serverResponse.message, () => {
        console.log("response writter callback...");
    });
    res.end();
});
server.listen(8000, () => {
    console.log(`server running on http://127.0.0.1:8000\n`);
});
