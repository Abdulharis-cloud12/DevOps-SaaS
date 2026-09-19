import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")

GITHUB_API_URL = "https://api.github.com"
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_workflow_runs(limit=10):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    response = requests.get(
        url,
        headers=headers,
        params={"per_page": limit},
        timeout=10,
    )

    response.raise_for_status()

    return response.json()["workflow_runs"]
