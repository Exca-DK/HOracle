package app

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"reflect"
	"sync"
	"syscall"
	"time"

	"github.com/Exca-DK/HOracle/config"
	"github.com/Exca-DK/HOracle/core"
	logging "github.com/Exca-DK/HOracle/log"
	"github.com/Exca-DK/HOracle/metrics"
	"github.com/Exca-DK/HOracle/services"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"go.uber.org/zap"
)

var (
	HOracle_Version string = "0.0"
)

type HoudiniOracle struct {
	//info
	ident   string
	version string
	config  config.Config

	wait   chan struct{}
	done   chan string
	server *http.Server

	//internal
	backend core.Backend
	router  core.Router

	//sync primitives
	wg *sync.WaitGroup

	log logging.Logger
}

func (app *HoudiniOracle) Setup() {
	app.log.Debug("setting up application")
	defer func(ts time.Time) { app.log.Info("setup info", zap.String("runtime", time.Since(ts).String())) }(time.Now())

	graceful := make(chan os.Signal, 1)
	signal.Notify(graceful, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		for {
			select {
			case <-graceful:
				app.log.Info("Stopping Application", zap.String("reason", "os.kill"))
				app.Cleanup()
				return
			case reason := <-app.done:
				app.log.Info("Stopping Application", zap.String("reason", reason))
				app.Cleanup()
				return
			}
		}
	}()
	app.router = core.NewRouter()
	app.backend = core.NewApiBackend()
	for _, service := range services.GetAllServices() {
		app.backend.RegisterService(service.Service, service.Set)
	}
	app.backend.Handle(app.router)

	app.server = &http.Server{Addr: "0.0.0.0:" + app.config.Port, Handler: app.router.Handler()}
}

func (app *HoudiniOracle) Run(ctx context.Context) {
	defer func(ts time.Time) { app.log.Info("run info", zap.String("runtime", time.Since(ts).String())) }(time.Now())
	app.router.Handle("/metrics", promhttp.Handler())
	metrics.InitMetrics()

	go func() {
		app.log.Info("server listening", zap.String("under", app.server.Addr))
		if err := app.server.ListenAndServe(); err != nil {
			app.done <- err.Error()
			return
		}
	}()
	app.Wait()
}

func (app *HoudiniOracle) Cleanup() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err := app.server.Shutdown(ctx)
	if err != nil {
		app.log.Warn("server shutdown error", zap.String("err", err.Error()))
	} else {
		app.log.Info("server spinned down")
	}
	app.wait <- struct{}{}
}

func (app *HoudiniOracle) Wait() {
	<-app.wait
}
func (s *HoudiniOracle) Version() string {
	return s.version
}

func (s *HoudiniOracle) Identity() string {
	return reflect.TypeOf(*s).Name()
}

func (app *HoudiniOracle) Stats(ctx context.Context) {
	panic("not implemented") // TODO: Implement
}

func NewHoudiniOracle(config config.Config) IApp {
	app := HoudiniOracle{
		wg:      &sync.WaitGroup{},
		version: HOracle_Version,
		done:    make(chan string),
		wait:    make(chan struct{}),
		config:  config,
	}
	app.ident = reflect.TypeOf(app).Name()
	logging.NewLogger(app.ident)
	logger, err := logging.GetLogger(app.ident)
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
	app.log = logger
	return &app
}
