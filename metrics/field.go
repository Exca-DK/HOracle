package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var fieldUpdate = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "field_updated",
		Help:      "Node field has been updated by an user",
	},
	[]string{"user", "node", "field", "value"},
)

func RegisterPrometheusFieldMetric() {
	prometheus.MustRegister(fieldUpdate)
}

func RecordFieldUpdate(user string, node string, fieldName string, value string) {
	fieldUpdate.WithLabelValues(user, node, fieldName, value).Inc()
}
