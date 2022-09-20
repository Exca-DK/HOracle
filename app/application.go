package app

import "context"

type IApp interface {
	Setup()
	Run(ctx context.Context)
	Cleanup()
	Wait()
	Version() string
	Identity() string
	Stats(ctx context.Context)
}
