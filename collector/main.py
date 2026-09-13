import sys

import requests

from collector.collector import collect_recent_builds
from database.queries import get_or_create_pipeline, insert_build


def main():
    try:
        builds = collect_recent_builds(limit=10)

        for build in builds:
            pipeline_id = get_or_create_pipeline(
                build["pipeline"],
                build["provider"]
            )

            insert_build(
                pipeline_id=pipeline_id,
                build_number=build["build_number"],
                status=build["status"],
                duration_seconds=build["duration_seconds"],
                timestamp=build["timestamp"],
                url=build["url"]
            )

        print(f"Successfully processed {len(builds)} Jenkins builds.")

    except requests.exceptions.ConnectionError:
        print("ERROR: Unable to connect to Jenkins.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("ERROR: Jenkins request timed out.")
        sys.exit(1)

    except requests.exceptions.HTTPError as error:
        print(f"ERROR: Jenkins API returned an HTTP error: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
