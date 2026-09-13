from prometheus_client import start_http_server

from collector.metrics import (
    pipeline_runs_total,
    pipeline_success_total,
    pipeline_failure_total,
    pipeline_duration_seconds,
)


def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"Prometheus metrics server started on port {port}")


def record_build(build):
    pipeline = build["pipeline"]
    provider = build["provider"]
    status = build["status"]
    duration = build["duration_seconds"]

    pipeline_runs_total.labels(
        pipeline=pipeline,
        provider=provider
    ).inc()

    if status == "success":
        pipeline_success_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

    elif status == "failure":
        pipeline_failure_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

    pipeline_duration_seconds.labels(
        pipeline=pipeline,
        provider=provider
    ).observe(duration)

def initialize_metrics(builds):
    for build in builds:
        record_build(build)
