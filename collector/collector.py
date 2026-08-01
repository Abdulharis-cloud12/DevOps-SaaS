from datetime import datetime, timezone

from collector.jenkins_client import get_job_info, get_build_info


def normalize_build(job_name, build):
    return {
        "provider": "jenkins",
        "pipeline": job_name,
        "build_number": build.get("number"),
        "status": (build.get("result") or "UNKNOWN").lower(),
        "duration_seconds": round(build.get("duration", 0) / 1000, 3),
        "timestamp": datetime.fromtimestamp(
            build.get("timestamp", 0) / 1000,
            tz=timezone.utc
        ).isoformat(),
        "url": build.get("url")
    }


def collect_latest_build():
    job = get_job_info()

    latest_build = job.get("lastCompletedBuild")

    if not latest_build:
        raise RuntimeError("No completed Jenkins builds found.")

    build = get_build_info(latest_build["number"])

    return normalize_build(job["name"], build)

def collect_recent_builds(limit=10):
    job = get_job_info()

    normalized_builds = []

    for build_reference in job.get("builds", [])[:limit]:
        build = get_build_info(build_reference["number"])

        normalized_builds.append(
            normalize_build(job["name"], build)
        )

    return normalized_builds
