package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var nodeCreated = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "node_created",
		Help:      "Node has been created by an user",
	},
	[]string{"user", "name", "label", "path"},
)

var nodeDeleted = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Namespace: "houdini",
		Subsystem: "activity",
		Name:      "node_deleted",
		Help:      "Node  has been removed by an user",
	},
	[]string{"user", "name", "label", "path"},
)

func RegisterPrometheusNodeMetric() {
	prometheus.MustRegister(nodeCreated)
	prometheus.MustRegister(nodeDeleted)
}

func RecordNodeCreation(user string, name string, label string, path string) {
	nodeCreated.WithLabelValues(user, name, label, path).Inc()
}

func RecordNodeDeletion(user string, name string, label string, path string) {
	nodeDeleted.WithLabelValues(user, name, label, path).Inc()
}
