package renderActivityService

import (
	"encoding/json"
	"strconv"
)

type ParamGetRequest struct {
	UserId string `json:"userId"`
}

type RenderType int

func (b *RenderType) UnmarshalJSON(data []byte) error {
	var v string
	if err := json.Unmarshal(data, &v); err != nil {
		return err
	}

	value, err := strconv.Atoi(v)
	if err != nil {
		return err
	}
	*b = RenderType(value)
	return nil
}

var (
	CACHING   RenderType = 1
	RENDERING RenderType = 2
)

type ParamStatusRequest struct{}

type RenderFrame struct {
	Number int   `json:"number"`
	Start  int64 `json:"start"`
	End    int64 `json:"end"`
}

type RenderActivityParams struct {
	Start  int64  `json:"start"`
	Frames uint32 `json:"frames"`
	End    int64  `json:"end"`
}

type RenderPostRequest struct {
	RenderActivityParams *RenderActivityParams `json:"render,omitempty"`
	Frame                *RenderFrame          `json:"frame,omitempty"`
	User                 string                `json:"user"`
	Type                 RenderType            `json:"t"`
	Scene                string                `json:"scene"`
}
