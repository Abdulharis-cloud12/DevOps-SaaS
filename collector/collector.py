from datetime import datetime, timezone

from collector.jenkins_client import get_job_info, get_build_info


def normalize_build(job_name, build):
    """Normalize a Jenkins build into the PipelinePulse build model."""

    return {
        "provider": "jenkins",
        "pipeline": job_name,
        "build_number": build.get("number"),
        "status": (build.get("result") or "UNKNOWN").lower(),
        "duration_seconds": round(
            build.get("duration", 0) / 1000,
            3
        ),
        "timestamp": datetime.fromtimestamp(
            build.get("timestamp", 0) / 1000,
            tz=timezone.utc
        ).isoformat(),
        "url": build.get("url"),
    }


def normalize_github_run(run):
    """Normalize a GitHub Actions workflow run into the PipelinePulse build model."""

    started_at = datetime.fromisoformat(
        run["run_started_at"].replace("Z", "+00:00")
    )

    updated_at = datetime.fromisoformat(
        run["updated_at"].replace("Z", "+00:00")
    )

    duration_seconds = round(
        (updated_at - started_at).total_seconds(),
        3
    )

    conclusion = run.get("conclusion")

    if conclusion == "success":
        status = "success"
    elif conclusion == "failure":
        status = "failure"
    else:
        status = (
            conclusion
            or run.get("status")
            or "unknown"
        ).lower()

    return {
        "provider": "github_actions",
        "pipeline": run["name"],
        "build_number": run["run_number"],
        "status": status,
        "duration_seconds": duration_seconds,
        "timestamp": started_at.isoformat(),
        "url": run["html_url"],
    }


def collect_latest_build():
    """Collect the latest completed Jenkins build."""

    job = get_job_info()

    latest_build = job.get("lastCompletedBuild")

    if not latest_build:
        raise RuntimeError(
            "No completed Jenkins builds found."
        )

    build = get_build_info(
        latest_build["number"]
    )

    return normalize_build(
        job["name"],
        build
    )


def collect_recent_builds(limit=50):
    """Collect recent completed Jenkins builds."""

    job = get_job_info()

    normalized_builds = []

    for build_reference in job.get("builds", [])[:limit]:
        build = get_build_info(
            build_reference["number"]
        )

        # Skip builds that are still running.
        if build.get("result") is None:
            continue

        normalized_builds.append(
            normalize_build(
                job["name"],
                build
            )
        )

    return normalized_builds
