package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var viewportUpdate = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "viewport_active",
		Help:      "Viewport of user was recently active",
	},
	[]string{"user"},
)

func RegisterPrometheusViewportMetric() {
	prometheus.MustRegister(viewportUpdate)
}

func RecordViewportActivity(user string) {
	viewportUpdate.WithLabelValues(user).Inc()
}
