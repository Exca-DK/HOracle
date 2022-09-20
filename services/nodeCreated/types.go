package nodeCreatedService

type ParamGetRequest struct {
	UserId string `json:"userId"`
}

type ParamStatusRequest struct{}

type Node struct {
	Name  string `json:"name"`
	Label string `json:"label"`
	Path  string `json:"path"`
}

type NodePostRequest struct {
	Node Node   `json:"node"`
	User string `json:"user"`
}
