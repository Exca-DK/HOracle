package paramUpdatedService

import (
	"context"
	"net/http"

	"github.com/Exca-DK/HOracle/core"
	"github.com/Exca-DK/HOracle/metrics"
	types "github.com/Exca-DK/HOracle/services/paramUpdated"
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
	data := request.(*types.ParamPostRequest)
	resp, err := s.FieldPost(ctx, data.Param.Name, data.Param.Fields, data.Param.Value, data.Param.Source, data.User)
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

func (s *ParamUpdatedService) FieldPost(ctx context.Context, Name string, Fields []types.Field, Value string, Source types.Node, user string) (int, error) {
	for _, field := range Fields {
		metrics.RecordFieldUpdate(user, Source.Label, Name+"_"+field.Name, field.Value)
	}
	if Value != "None" {
		metrics.RecordFieldUpdate(user, Source.Label, Name, Value)

	}
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
	return &ParamUpdatedService{name: "ParmTupleChanged", path: "ParmTupleChanged"}
}
