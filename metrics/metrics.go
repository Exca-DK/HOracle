package metrics

func InitMetrics() {
	RegisterPrometheusFieldMetric()
	RegisterPrometheusUserMetric()
	RegisterPrometheusNodeMetric()
	RegisterPrometheusViewportMetric()
	RegisterPrometheusSceneMetric()
	RegisterPrometheusRenderMetric()
	RegisterPrometheusRequestMetric()
}
