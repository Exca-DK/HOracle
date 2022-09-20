package renderActivityService

import (
	"context"
	"net/http"
	"time"

	"github.com/Exca-DK/HOracle/core"
	"github.com/Exca-DK/HOracle/metrics"
	types "github.com/Exca-DK/HOracle/services/renderActivity"
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

func (s *ViewportActivity) Post(ctx context.Context, irequest core.PostRequest) core.PostResponse {
	request := irequest.(*types.RenderPostRequest)
	resp, err := s.NodePost(ctx, *request)
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

func (s *ViewportActivity) NodePost(ctx context.Context, request types.RenderPostRequest) (int, error) {
	if request.RenderActivityParams != nil {
		gs_ts := time.Unix(request.RenderActivityParams.Start, 0)
		ge_ts := time.Unix(request.RenderActivityParams.End, 0)
		g_elapsed := ge_ts.Sub(gs_ts)
		frames := request.RenderActivityParams.Frames
		metrics.RecordRenderActivity(request.User, gs_ts, ge_ts, frames, g_elapsed, request.Scene, int64(request.Type))
	}
	if request.Frame != nil {
		l_start := time.Unix(request.Frame.Start, 0)
		l_end := time.Unix(request.Frame.End, 0)
		l_duration := l_end.Sub(l_start)
		metrics.RecordRenderedFrame(metrics.Frame{
			Start:    l_start,
			End:      l_end,
			Duration: l_duration,
			Number:   request.Frame.Number,
			Scene:    request.Scene,
			User:     request.User,
			Type:     int(request.Type),
		})
	}
	return 1, nil
}

func (s *ViewportActivity) Get(ctx context.Context, request core.GetRequest) core.GetResponse {
	return core.GetResponse{Code: http.StatusNotImplemented}
}

func (s *ViewportActivity) Status(ctx context.Context, request core.StatusRequest) core.StatusResponse {
	return core.StatusResponse{Code: http.StatusNotImplemented}
}

func NewService() core.Service {
	return &ViewportActivity{name: "RenderActivity", path: "RenderActivity"}
}
