package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var sceneSaved = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "scene_saved_activity",
		Help:      "Scene has been saved by user",
	},
	[]string{"user", "scene"},
)

func RegisterPrometheusSceneMetric() {
	prometheus.MustRegister(sceneSaved)
}

func RecordSceneSavedActivity(user string, file string) {
	sceneSaved.WithLabelValues(user, file).Inc()
}
