from prometheus_client import Counter, Histogram


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
