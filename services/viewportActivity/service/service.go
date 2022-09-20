package sceneSavedService

import (
	"context"
	"net/http"

	"github.com/Exca-DK/HOracle/core"
	"github.com/Exca-DK/HOracle/metrics"
	types "github.com/Exca-DK/HOracle/services/viewportActivity"
)

type ViewportActivity struct {
	name string
	path string
}

func (s *ViewportActivity) Name() string {
	return s.name
}

func (s *ViewportActivity) Path() string {
	return s.path
}

func (s *ViewportActivity) Post(ctx context.Context, request core.PostRequest) core.PostResponse {
	reqq := request.(*types.ViewportPostRequest)
	s.NodePost(ctx, reqq.User)
	return core.PostResponse{Code: http.StatusOK}
}

func (s *ViewportActivity) NodePost(ctx context.Context, user string) {
	metrics.RecordViewportActivity(user)
	metrics.RecordUserActivity(user)
}

func (s *ViewportActivity) Get(ctx context.Context, request core.GetRequest) core.GetResponse {
	return core.GetResponse{Code: http.StatusNotImplemented}
}

func (s *ViewportActivity) Status(ctx context.Context, request core.StatusRequest) core.StatusResponse {
	return core.StatusResponse{Code: http.StatusNotImplemented}
}

func NewService() core.Service {
	return &ViewportActivity{name: "ViewportActivity", path: "ViewportActivity"}
}
