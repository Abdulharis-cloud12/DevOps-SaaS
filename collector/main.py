import json
import sys

import requests

from collector.collector import collect_recent_builds


def main():
    try:
        builds = collect_recent_builds(limit=10)
        print(json.dumps(builds, indent=4))

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
