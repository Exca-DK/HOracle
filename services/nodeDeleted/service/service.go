package nodeDeletedService

import (
	"context"
	"net/http"

	"github.com/Exca-DK/HoudiniPrometheus/core"
	"github.com/Exca-DK/HoudiniPrometheus/metrics"
	types "github.com/Exca-DK/HoudiniPrometheus/services/nodeDeleted"
)

type NodeDeletedService struct {
	name string
	path string
}

func (s *NodeDeletedService) Name() string {
	return s.name
}

func (s *NodeDeletedService) Path() string {
	return s.path
}

func (s *NodeDeletedService) Post(ctx context.Context, request core.PostRequest) core.PostResponse {
	reqq := request.(*types.NodePostRequest)
	node := reqq.Node
	resp, err := s.NodePost(ctx, node.Name, node.Label, node.Path, reqq.User)
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

func (s *NodeDeletedService) NodePost(ctx context.Context, Name string, Label string, Path string, user string) (int, error) {
	metrics.RecordNodeDeletion(user, Name, Label, Path)
	metrics.RecordUserActivity(user)
	return 1, nil
}

func (s *NodeDeletedService) Get(ctx context.Context, request core.GetRequest) core.GetResponse {
	return core.GetResponse{Code: http.StatusNotImplemented}
}

func (s *NodeDeletedService) Status(ctx context.Context, request core.StatusRequest) core.StatusResponse {
	return core.StatusResponse{Code: http.StatusNotImplemented}
}

func NewService() core.Service {
	return &NodeDeletedService{name: "NodeDeleted", path: "NodeDeleted"}
}
