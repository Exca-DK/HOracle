package nodeCreatedService

import (
	"context"
	"net/http"

	"github.com/Exca-DK/HOracle/core"
	"github.com/Exca-DK/HOracle/metrics"
	types "github.com/Exca-DK/HOracle/services/nodeCreated"
)

type ParamUpdatedService struct {
	name string
	path string
}

func (s *ParamUpdatedService) Name() string {
	return s.name
}

func (s *ParamUpdatedService) Path() string {
	return s.path
}

func (s *ParamUpdatedService) Post(ctx context.Context, request core.PostRequest) core.PostResponse {
	data := request.(*types.NodePostRequest)
	node := data.Node
	resp, err := s.NodePost(ctx, node.Name, node.Label, node.Path, data.User)
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

func (s *ParamUpdatedService) NodePost(ctx context.Context, Name string, Label string, Path string, user string) (int, error) {
	metrics.RecordNodeCreation(user, Name, Label, Path)
	metrics.RecordUserActivity(user)
	return 1, nil
}

func (s *ParamUpdatedService) Get(ctx context.Context, request core.GetRequest) core.GetResponse {
	return core.GetResponse{Code: http.StatusNotImplemented}
}

func (s *ParamUpdatedService) Status(ctx context.Context, request core.StatusRequest) core.StatusResponse {
	return core.StatusResponse{Code: http.StatusNotImplemented}
}

func NewService() core.Service {
	return &ParamUpdatedService{name: "NodeCreated", path: "NodeCreated"}
}
