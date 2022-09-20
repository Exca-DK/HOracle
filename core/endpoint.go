package core

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"reflect"
	"time"

	logging "github.com/Exca-DK/HoudiniPrometheus/log"
	metrics "github.com/Exca-DK/HoudiniPrometheus/metrics"

	"go.uber.org/zap"
)

type EndpointRestriction uint8

var (
	None  EndpointRestriction = 0
	TOKEN EndpointRestriction = 1
	PSSWD EndpointRestriction = 2
)

type EndpointType uint8

var (
	Stats EndpointType = 1
	POST  EndpointType = 2
	GET   EndpointType = 3
)

var EndpointTypeStringers = map[EndpointType]string{
	Stats: "stats",
	POST:  "post",
	GET:   "get",
}

func (e EndpointType) String() string {
	return EndpointTypeStringers[e]
}

type RestrictionHandler func(r *http.Request, validator interface{}) (bool, error)
type msgHandler func(svc Service, obj reflect.Type, restrictions []RestrictionHandler) *Endpoint

var ROUTE = map[EndpointType]msgHandler{
	Stats: MakeStatusEndpoint,
	POST:  MakePostEndpoint,
	GET:   MakeGetEndpoint,
}

type IEndpoint interface {
	Handle(w http.ResponseWriter, r *http.Request)
	Type() EndpointType
	BindValidator(v *Validator)
}

type Endpoint struct {
	Method func(ctx context.Context, request Request) Response
	Body   reflect.Type
	t      EndpointType
	v      *Validator
	r      []RestrictionHandler
	log    logging.Logger
}

func (e *Endpoint) BindValidator(validator *Validator) {
	e.v = validator
}

func (e *Endpoint) Type() EndpointType {
	return e.t
}

func (e *Endpoint) Handle(w http.ResponseWriter, r *http.Request) {
	code := 401
	defer func(ts time.Time, status *int) {
		since := time.Since(ts)
		e.log.Debug("served endpoint",
			zap.String("runtime", since.String()),
			zap.Bool("okay", *status == http.StatusOK),
			zap.String("type", e.t.String()),
			zap.String("endpoint", r.URL.String()),
			zap.String("ip", r.RemoteAddr))
		metrics.RecordRequest(r.URL.String(), *status, since)
	}(time.Now(), &code)

	//validate all of restrictions applied to endpoint
	for _, rhandler := range e.r {
		ok, err := rhandler(r, e.v)
		if err != nil {
			log.Print(err)
			http.Error(w, err.Error(), http.StatusForbidden)
			return
		}
		if !ok {
			http.Error(w, err.Error(), http.StatusForbidden)
			return
		}
	}

	// parse and validate the body
	obj := reflect.New(e.Body).Interface()
	err := json.NewDecoder(r.Body).Decode(&obj)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if err := ValidateBody(obj); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		log.Print(err)
		return
	}

	//run the service method and send feedback
	resp := e.Method(context.Background(), obj)
	code = resp.Code
	json.NewEncoder(w).Encode(resp)
}

func MakeEndpointType(svc Service, obj reflect.Type, t EndpointType, restrictions []RestrictionHandler) IEndpoint {
	endpoint := ROUTE[t](svc, obj, restrictions)
	name := svc.Name() + "_endpoint"
	logger, err := logging.GetLogger(name)
	if err != nil {
		logging.NewLogger(name)
		logger, err = logging.GetLogger(name)
		if err != nil {
			fmt.Print(err)
			os.Exit(1)
		}
	}
	endpoint.log = logger
	return endpoint
}

func MakeGetEndpoint(svc Service, obj reflect.Type, restrictions []RestrictionHandler) *Endpoint {
	endpoint := Endpoint{t: GET, r: restrictions}
	endpoint.Method = func(ctx context.Context, request Request) Response {
		resp := svc.Get(ctx, request)
		return Response(resp)
	}
	endpoint.Body = obj
	return &endpoint
}

func MakePostEndpoint(svc Service, obj reflect.Type, restrictions []RestrictionHandler) *Endpoint {
	endpoint := Endpoint{t: POST, r: restrictions}
	endpoint.Method = func(ctx context.Context, request Request) Response {
		resp := svc.Post(ctx, request)
		return Response(resp)
	}
	endpoint.Body = obj
	return &endpoint
}

func MakeStatusEndpoint(svc Service, obj reflect.Type, restrictions []RestrictionHandler) *Endpoint {
	endpoint := Endpoint{t: Stats}
	endpoint.Method = func(ctx context.Context, request Request) Response {
		resp := svc.Status(ctx, request)
		return Response(resp)
	}
	endpoint.Body = obj
	return &endpoint
}

type IESet interface {
	Endpoints() map[string]IEndpoint
	BindService(service Service)
}
