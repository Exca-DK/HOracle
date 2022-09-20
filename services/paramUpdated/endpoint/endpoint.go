package endpoint

import (
	"reflect"

	"github.com/Exca-DK/HOracle/core"
	"github.com/Exca-DK/HOracle/internal"
	types "github.com/Exca-DK/HOracle/services/paramUpdated"
)

type Set struct {
	Path           string
	PostEndpoint   core.IEndpoint
	GetEndpoint    core.IEndpoint
	StatusEndpoint core.IEndpoint
}

func (s *Set) Endpoints() map[string]core.IEndpoint {
	return map[string]core.IEndpoint{
		"/" + s.Path + "/" + "status/": s.StatusEndpoint,
		"/" + s.Path + "/" + "post/":   s.PostEndpoint,
		"/" + s.Path + "/" + "get/":    s.GetEndpoint,
	}
}

func (s *Set) BindService(service core.Service) {
	s.PostEndpoint = core.MakeEndpointType(service, reflect.TypeOf(types.ParamPostRequest{}), core.POST, []core.RestrictionHandler{internal.ValidateRequest})
	s.GetEndpoint = core.MakeEndpointType(service, reflect.TypeOf(types.ParamGetRequest{}), core.GET, []core.RestrictionHandler{internal.ValidateRequest})
	s.StatusEndpoint = core.MakeEndpointType(service, reflect.TypeOf(types.ParamStatusRequest{}), core.Stats, []core.RestrictionHandler{internal.ValidateRequest})
	s.Path = service.Name()
}

func NewEndpointSet() core.IESet {
	return &Set{}
}
