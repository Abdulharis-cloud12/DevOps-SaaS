from prometheus_client import start_http_server

from collector.metrics import (
    pipeline_runs_total,
    pipeline_success_total,
    pipeline_failure_total,
    pipeline_duration_seconds,
    pipeline_run_events_total,
    pipeline_success_events_total,
    pipeline_failure_events_total,
    pipeline_last_duration_seconds,
)


def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"Prometheus metrics server started on port {port}")


def record_build(build, emit_event=True):
    """
    Record a completely new pipeline run.

    This increments the total run counter and, when requested,
    emits the corresponding event metrics.
    """

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

    if emit_event:
        pipeline_run_events_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

        if status == "success":
            pipeline_success_events_total.labels(
                pipeline=pipeline,
                provider=provider
            ).inc()

        elif status == "failure":
            pipeline_failure_events_total.labels(
                pipeline=pipeline,
                provider=provider
            ).inc()

        pipeline_last_duration_seconds.labels(
            pipeline=pipeline,
            provider=provider
        ).set(duration)


def record_build_update(build, previous_status):
    """
    Record a status update for an existing pipeline run.

    This is used when an existing run changes from an unfinished
    status such as 'queued', 'in_progress', or 'unknown' to
    'success' or 'failure'.

    IMPORTANT:
    pipeline_runs_total is NOT incremented because this is
    the same pipeline run, not a new run.
    """

    pipeline = build["pipeline"]
    provider = build["provider"]
    status = build["status"]
    duration = build["duration_seconds"]

    if status == "success" and previous_status != "success":
        pipeline_success_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

        pipeline_success_events_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

    elif status == "failure" and previous_status != "failure":
        pipeline_failure_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

        pipeline_failure_events_total.labels(
            pipeline=pipeline,
            provider=provider
        ).inc()

    pipeline_duration_seconds.labels(
        pipeline=pipeline,
        provider=provider
    ).observe(duration)

    pipeline_last_duration_seconds.labels(
        pipeline=pipeline,
        provider=provider
    ).set(duration)


def initialize_metrics(builds):
    """
    Initialize Prometheus counters from existing database records.

    Historical builds are loaded without emitting alert events.
    """

    for build in builds:
        record_build(build, emit_event=False)
