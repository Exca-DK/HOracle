package metrics

import (
	"strconv"
	"time"

	"github.com/prometheus/client_golang/prometheus"
)

var requestDurationMetric = prometheus.NewHistogramVec(
	prometheus.HistogramOpts{
		Namespace: "rest",
		Subsystem: "houdini",
		Name:      "request",
		Help:      "duration of the request",
	},
	[]string{"endpoint", "status"},
)

func RegisterPrometheusRequestMetric() {
	prometheus.MustRegister(requestDurationMetric)
}

func RecordRequest(endpoint string, status int, duration time.Duration) {
	requestDurationMetric.WithLabelValues(endpoint, strconv.Itoa(status)).Observe(duration.Seconds())
}
