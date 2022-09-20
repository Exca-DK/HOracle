package main

import (
	"context"
	"log"

	"github.com/Exca-DK/HoudiniPrometheus/app"
	"github.com/Exca-DK/HoudiniPrometheus/config"
	logging "github.com/Exca-DK/HoudiniPrometheus/log"
)

func main() {
	config, err := config.LoadAppConfig()
	if err != nil {
		log.Fatal(err)
	}
	log.SetFlags(log.LstdFlags | log.Lmicroseconds | log.Lshortfile)
	logging.SetupLogging(false, true, logging.LoggingLevel(config.Verbosity))

	application := app.NewHoudiniOracle(config)
	application.Setup()
	application.Run(context.Background())
}
