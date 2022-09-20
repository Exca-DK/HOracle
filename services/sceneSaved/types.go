package sceneSavedService

type FileSavedGetRequest struct {
	UserId string `json:"userId"`
}

type FileSavedStatusRequest struct{}

type SceneSavedPostRequest struct {
	File string `json:"file"`
	User string `json:"user"`
}
