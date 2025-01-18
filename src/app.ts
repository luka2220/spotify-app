import * as http from "node:http";

import { ParseIncomingURL } from "./routes/router";


// TODO: Parse out the request url for routing
// Check the url routes for available routing on the server and site

const server = http.createServer((req, res) => {
	const serverResponse = ParseIncomingURL({ url: req.url, method: req.method });

	res.statusCode = serverResponse.status;
	res.write(serverResponse.message);
	if (serverResponse.route !== undefined) {
		res.write(`\nroute: ${serverResponse.route}`);
	}

	res.end();
});

server.listen(8000, () => {
	console.log(`server running on http://127.0.0.1:8000\n`);
})
