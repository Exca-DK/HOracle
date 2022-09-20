package core

import (
	"fmt"
	"os"
	"reflect"

	logging "github.com/Exca-DK/HoudiniPrometheus/log"
	"go.uber.org/zap"
)

type Backend interface {
	RegisterService(service Service, eset IESet)
	Services() []Service
	Handle(router Router)
}

type ApiBackend struct {
	registry  map[IESet]Service
	validator *Validator
	log       logging.Logger
}

func (b *ApiBackend) RegisterService(service Service, eset IESet) {
	eset.BindService(service)
	for _, endpoint := range eset.Endpoints() {
		endpoint.BindValidator(b.validator)
	}
	b.registry[eset] = service
	b.log.Debug("registered service", zap.String("service", service.Name()))
}

func (b *ApiBackend) Services() []Service {
	services := make([]Service, len(b.registry))
	for _, s := range b.registry {
		services = append(services, s)
	}
	return services
}

func (b *ApiBackend) Handle(router Router) {
	for set := range b.registry {
		eps := set.Endpoints()
		for under, ep := range eps {
			router.Bind(under, ep.Handle)
		}
	}
}

func NewApiBackend() Backend {
	backend := ApiBackend{
		registry: map[IESet]Service{},
	}
	backend.validator = NewValidator()
	ident := reflect.TypeOf(backend).Name()
	logging.NewLogger(ident)
	logger, err := logging.GetLogger(ident)
	if err != nil {
		logging.NewLogger(ident)
		logger, err = logging.GetLogger(ident)
		if err != nil {
			fmt.Print(err)
			os.Exit(1)
		}
	}
	backend.log = logger
	return &backend
}
