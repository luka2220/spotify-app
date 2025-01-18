export interface IncomingRequest {
	url: string | undefined;
	method: string | undefined;
}

export interface OutgoingResponse {
	message: string;
	status: number;
	route?: string;
}
