export enum RegisteredRoutes {
	Home = "/",
	Login = "/login",
	Logout = "/logout",
	Redirect = "home/authenticated",
	Profile = "/profile"
}

export interface IncomingRequest {
	url: string | undefined;
	method: string | undefined;
}

export interface OutgoingResponse {
	message: string;
	status: number;
}
