package logging

import (
	"errors"
	"log"
	"os"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

type Logger interface {
	Warn(msg string, items ...zapcore.Field)
	Debug(msg string, items ...zapcore.Field)
	Info(msg string, items ...zapcore.Field)
	Fatal(msg string, items ...zapcore.Field)
	Error(msg string, items ...zapcore.Field)
}

type LoggingLevel int

var (
	DEBUG LoggingLevel = 1
	INFO  LoggingLevel = 2
	WARN  LoggingLevel = 3
	FATAL LoggingLevel = 4
)

var filesF bool = false
var consoleF bool = false
var initialized bool = false
var lvl LoggingLevel
var loggers map[string]*zap.Logger

func SetupLogging(files bool, console bool, level LoggingLevel) {
	filesF = files
	consoleF = console
	lvl = level
	loggers = make(map[string]*zap.Logger)
	initialized = true
}

func SetLoggingLevel(level LoggingLevel) {
	lvl = level
}

func GetCurrentLogingLevel() LoggingLevel {
	if !initialized {
		return INFO
	}
	return lvl
}

func newLogger(module string, toFile bool, toConsole bool) *zap.Logger {

	config := zap.NewProductionEncoderConfig()
	config.EncodeTime = zapcore.ISO8601TimeEncoder
	fileName := module + ".log"
	var log_lvl zapcore.LevelEnabler
	switch GetCurrentLogingLevel() {
	case DEBUG:
		log_lvl = zapcore.DebugLevel
	case INFO:
		log_lvl = zapcore.InfoLevel
	case WARN:
		log_lvl = zapcore.WarnLevel
	case FATAL:
		log_lvl = zapcore.FatalLevel
	}

	consoleEncoder := zapcore.NewConsoleEncoder(config)
	fileEncoder := zapcore.NewJSONEncoder(config)
	var core zapcore.Core
	if toFile && toConsole {
		logFile, _ := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		writer := zapcore.AddSync(logFile)
		c1 := zapcore.NewCore(fileEncoder, writer, log_lvl)
		c2 := zapcore.NewCore(consoleEncoder, zapcore.AddSync(os.Stdout), log_lvl)
		core = zapcore.NewTee(c1, c2)
	}
	if toFile && !toConsole {
		logFile, _ := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		writer := zapcore.AddSync(logFile)
		c1 := zapcore.NewCore(fileEncoder, writer, log_lvl)
		core = zapcore.NewTee(c1)
	}
	if !toFile && toConsole {
		c2 := zapcore.NewCore(consoleEncoder, zapcore.AddSync(os.Stdout), log_lvl)
		core = zapcore.NewTee(c2)
	}

	return zap.New(core, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel))
}

func newFileLogger(module string) *zap.Logger {
	return newLogger(module, true, false)
}

func newConsoleLogger() *zap.Logger {
	return newLogger("", false, true)
}

func newFileAndConsoleLogger(module string) *zap.Logger {
	return newLogger(module, true, true)
}

func NewLogger(module string) {
	_, err := GetLogger(module)
	if err == nil {
		log.Fatal(err)
		os.Exit(1)
	}
	var logger *zap.Logger
	if filesF && consoleF {
		logger = newFileAndConsoleLogger(module)
	}
	if filesF && !consoleF {
		logger = newFileLogger(module)
	}
	if !filesF && consoleF {
		logger = newConsoleLogger()
	}
	loggers[module] = logger
}

func GetLogger(module string) (*zap.Logger, error) {
	logger, ok := loggers[module]
	if !ok {
		return nil, errors.New("logger %v doesn't exist")
	}
	return logger, nil
}
