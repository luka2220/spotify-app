import { IncomingRequest, OutgoingResponse, } from "./types";


const RegisteredRoutes = {
	Home: { path: "/", methods: ["GET"] },
	Login: { path: "/login", methods: ["GET"] },
	Logout: { path: "/logout", methods: ["GET"] },
	HomeAuthenticated: { path: "/home/authenticated", methods: ["GET"] },
	Profile: { path: "/profile", methods: ["GET"] },
}

export function ParseIncomingURL({ url, method }: IncomingRequest): OutgoingResponse {
	if (url === undefined) throw new Error("URL is not defined on incoming request");
	if (method === undefined) throw new Error("HTTP method is not defined on incoming request")

	url = clean(url);

	if (url.includes("?")) {
		// TODO: process the request for url parameters
	}

	const route = Object.values(RegisteredRoutes).find((val) => val.path === url);

	if (route) {
		return { route: route.path, message: "This is a valid route for some reason", status: 200 }
	}

	return { message: "This is an invalid route...", status: 404 }
}

function clean(url: string): string {
	if (url === RegisteredRoutes.Home.path) return url;

	console.log(`before cleaned value: ${url}`);
	url = url[url.length - 1] === '/' ? url.slice(0, url.length - 1) : url;
	console.log(`cleaned value: ${url}`);

	return url === '/' ? `${url}/` : url;
}
