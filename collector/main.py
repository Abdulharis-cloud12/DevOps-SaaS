```python
import os
import time

import requests

from collector.collector import (
    collect_recent_builds,
    normalize_github_run,
)
from collector.github_actions_client import get_workflow_runs
from collector.metrics_server import (
    start_metrics_server,
    record_build,
    initialize_metrics,
    record_build_update,
)
from database.queries import (
    get_or_create_pipeline,
    insert_build,
    get_all_builds,
)


COLLECTION_INTERVAL = int(
    os.getenv("COLLECTION_INTERVAL", "30")
)


def collect_and_store():
    builds = collect_recent_builds(limit=50)

    new_builds = 0
    updated_builds = 0

    for build in builds:
        pipeline_id = get_or_create_pipeline(
            build["pipeline"],
            build["provider"]
        )

        action, previous_status = insert_build(
            pipeline_id=pipeline_id,
            build_number=build["build_number"],
            status=build["status"],
            duration_seconds=build["duration_seconds"],
            timestamp=build["timestamp"],
            url=build["url"]
        )

        if action == "new":
            record_build(build)
            new_builds += 1

        elif action == "updated":
            record_build_update(build, previous_status)
            updated_builds += 1

    print(
        f"Processed {len(builds)} Jenkins builds. "
        f"New builds stored: {new_builds}, "
        f"Updated builds: {updated_builds}"
    )


def collect_github_and_store():
    runs = get_workflow_runs(limit=50)

    new_runs = 0
    updated_runs = 0

    for run in runs:
        build = normalize_github_run(run)

        pipeline_id = get_or_create_pipeline(
            build["pipeline"],
            build["provider"]
        )

        action, previous_status = insert_build(
            pipeline_id=pipeline_id,
            build_number=build["build_number"],
            status=build["status"],
            duration_seconds=build["duration_seconds"],
            timestamp=build["timestamp"],
            url=build["url"]
        )

        if action == "new":
            record_build(build)
            new_runs += 1

        elif action == "updated":
            record_build_update(build, previous_status)
            updated_runs += 1

    print(
        f"Processed {len(runs)} GitHub Actions runs. "
        f"New runs stored: {new_runs}, "
        f"Updated runs: {updated_runs}"
    )


def main():
    historical_builds = get_all_builds()
    initialize_metrics(historical_builds)

    start_metrics_server(8000)

    while True:
        try:
            collect_and_store()
            collect_github_and_store()

        except requests.exceptions.ConnectionError:
            print("ERROR: Unable to connect to CI provider.")

        except requests.exceptions.Timeout:
            print("ERROR: CI provider request timed out.")

        except requests.exceptions.HTTPError as error:
            print(
                f"ERROR: CI provider API returned an HTTP error: {error}"
            )

        except Exception as error:
            print(f"ERROR: {error}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
```

