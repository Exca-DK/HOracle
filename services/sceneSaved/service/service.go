package sceneSavedService

import (
	"context"
	"net/http"

	"github.com/Exca-DK/HoudiniPrometheus/core"
	"github.com/Exca-DK/HoudiniPrometheus/metrics"
	types "github.com/Exca-DK/HoudiniPrometheus/services/sceneSaved"
)

type SceneSavedService struct {
	name string
	path string
}

func (s *SceneSavedService) Name() string {
	return s.name
}

func (s *SceneSavedService) Path() string {
	return s.path
}

func (s *SceneSavedService) Post(ctx context.Context, request core.PostRequest) core.PostResponse {
	reqq := request.(*types.SceneSavedPostRequest)
	resp, err := s.NodePost(ctx, reqq.User, reqq.File)
	if err != nil {
		return core.PostResponse{
			Code:  http.StatusBadRequest,
			Error: err,
			Data:  resp,
		}
	}
	return core.PostResponse{
		Code:  http.StatusOK,
		Error: err,
		Data:  resp,
	}
}

func (s *SceneSavedService) NodePost(ctx context.Context, user string, file string) (int, error) {
	metrics.RecordSceneSavedActivity(user, file)
	metrics.RecordUserActivity(user)
	return 1, nil
}

func (s *SceneSavedService) Get(ctx context.Context, request core.GetRequest) core.GetResponse {
	return core.GetResponse{Code: http.StatusNotImplemented}
}

func (s *SceneSavedService) Status(ctx context.Context, request core.StatusRequest) core.StatusResponse {
	return core.StatusResponse{Code: http.StatusNotImplemented}
}

func (s *SceneSavedService) NodeStatus(ctx context.Context) (int, error) {
	return 1234, nil
}

func NewService() core.Service {
	return &SceneSavedService{name: "SceneSaved", path: "SceneSaved"}
}
