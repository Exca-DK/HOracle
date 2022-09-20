package ViewportActivityService

type ParamGetRequest struct {
	UserId string `json:"userId"`
}

type ParamStatusRequest struct{}

type ViewportPostRequest struct {
	User string `json:"user"`
}
