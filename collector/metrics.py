from prometheus_client import Counter, Gauge, Histogram


pipeline_runs_total = Counter(
    "pipeline_runs_total",
    "Total number of pipeline runs",
    ["pipeline", "provider"]
)


pipeline_success_total = Counter(
    "pipeline_success_total",
    "Total number of successful pipeline runs",
    ["pipeline", "provider"]
)


pipeline_failure_total = Counter(
    "pipeline_failure_total",
    "Total number of failed pipeline runs",
    ["pipeline", "provider"]
)


pipeline_duration_seconds = Histogram(
    "pipeline_duration_seconds",
    "Pipeline execution duration in seconds",
    ["pipeline", "provider"]
)


pipeline_run_events_total = Counter(
    "pipeline_run_events_total",
    "Total number of newly detected completed pipeline runs",
    ["pipeline", "provider"]
)

pipeline_success_events_total = Counter(
    "pipeline_success_events_total",
    "Total number of newly detected successful pipeline runs",
    ["pipeline", "provider"]
)

pipeline_failure_events_total = Counter(
    "pipeline_failure_events_total",
    "Total number of newly detected failed pipeline runs",
    ["pipeline", "provider"]
)

pipeline_last_duration_seconds = Gauge(
    "pipeline_last_duration_seconds",
    "Duration of the most recently detected pipeline run in seconds",
    ["pipeline", "provider"]
)

pipeline_last_failure_timestamp = Gauge(
    "pipeline_last_failure_timestamp",
    "Unix timestamp of the most recently detected failed pipeline run",
    ["pipeline", "provider"]
)
