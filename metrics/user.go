package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var userUpdate = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "user_active",
		Help:      "User activity",
	},
	[]string{"user"},
)

func RegisterPrometheusUserMetric() {
	prometheus.MustRegister(userUpdate)
}

func RecordUserActivity(user string) {
	userUpdate.WithLabelValues(user).Inc()
}
