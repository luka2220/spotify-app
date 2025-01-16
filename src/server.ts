import * as http from "node:http";

const server = http.createServer((req, res) => {
	res.statusCode = 200;
	res.write("I am not sure which route this is for...", () => {
		console.log("response writter callback...");
	});
	res.end();
});

server.listen(8000, () => {
	console.log(`server running on http://127.0.0.1:8000\n`);
})
