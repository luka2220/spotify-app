import { IncomingRequest, OutgoingResponse } from "./types";

export enum RegisteredRoutes {
	Home = "/",
	Login = "/login",
	Logout = "/logout",
	Redirect = "home/authenticated",
	Profile = "/profile"
}

export function ParseIncomingURL({ url, method }: IncomingRequest): OutgoingResponse {
	if (url === undefined) throw new Error("URL is not defined on incoming request");
	if (method === undefined) throw new Error("HTTP method is not defined on incoming request")

	console.log(`current url = ${url}`);
	console.log(`current http method = ${method}`)


	//NOTE: use array.find()
	const route = Object.values(RegisteredRoutes).find((val) => val === url);

	if (route) {
		console.log(route);
		return { message: "This is a valid route for some reason", status: 200 }
	}

	return { message: "This is an invalid route...", status: 404 }
}
