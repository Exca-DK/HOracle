package paramUpdatedService

type ParamGetRequest struct {
	UserId string `json:"userId"`
}

type ParamStatusRequest struct{}

type Node struct {
	Name  string `json:"name"`
	Label string `json:"label"`
	Path  string `json:"path"`
}

type Field struct {
	Name  string `json:"name"`
	Value string `json:"value"`
}

type Param struct {
	Name   string  `json:"name"`
	Fields []Field `json:"fields"`
	Value  string  `json:"value"`
	Source Node    `json:"source"`
}

type ParamPostRequest struct {
	Param Param  `json:"param"`
	User  string `json:"user"`
}
