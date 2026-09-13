import os
import sys
import time

import requests

from collector.collector import collect_recent_builds
from collector.metrics_server import (
    start_metrics_server,
    record_build,
    initialize_metrics,
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
    builds = collect_recent_builds(limit=10)

    new_builds = 0

    for build in builds:
        pipeline_id = get_or_create_pipeline(
            build["pipeline"],
            build["provider"]
        )

        inserted = insert_build(
            pipeline_id=pipeline_id,
            build_number=build["build_number"],
            status=build["status"],
            duration_seconds=build["duration_seconds"],
            timestamp=build["timestamp"],
            url=build["url"]
        )

        if inserted:
            record_build(build)
            new_builds += 1

    print(
        f"Processed {len(builds)} Jenkins builds. "
        f"New builds stored: {new_builds}"
    )


def main():
    historical_builds = get_all_builds()
    initialize_metrics(historical_builds)

    start_metrics_server(8000)

    while True:
        try:
            collect_and_store()

        except requests.exceptions.ConnectionError:
            print("ERROR: Unable to connect to Jenkins.")

        except requests.exceptions.Timeout:
            print("ERROR: Jenkins request timed out.")

        except requests.exceptions.HTTPError as error:
            print(
                f"ERROR: Jenkins API returned an HTTP error: {error}"
            )

        except Exception as error:
            print(f"ERROR: {error}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
