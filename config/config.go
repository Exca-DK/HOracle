package config

import (
	"fmt"
	"log"

	"github.com/Exca-DK/HOracle/core"
	"github.com/spf13/viper"
)

type Config struct {
	//app config

	Port string `json:"port"`

	//logging config

	Verbosity uint8 `json:"verbosity"` // lvl of logging. 1 = Debug, 2 = Info, 3 = Warn, 4 = Error
}

func LoadAppConfig() (Config, error) {
	vp := viper.New()
	var cfg Config
	vp.SetConfigName("config")
	vp.SetConfigType("json")
	vp.AddConfigPath(".")
	err := vp.ReadInConfig()
	if err != nil {
		return cfg, err
	}
	err = vp.Unmarshal(&cfg)
	if err != nil {
		return cfg, err
	}
	err = core.ValidateBody(&cfg)
	if err != nil {
		log.Printf("d: %+v", cfg)
		return cfg, fmt.Errorf("invalid config specified, error: %v", err.Error())
	}
	return cfg, nil
}
