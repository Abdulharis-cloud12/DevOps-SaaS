import os
import requests
from dotenv import load_dotenv


load_dotenv()


JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")
JENKINS_JOB = os.getenv("JENKINS_JOB")


def get_job_info():
    url = f"{JENKINS_URL}/job/{JENKINS_JOB}/api/json"

    response = requests.get(
        url,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_build_info(build_number):
    url = f"{JENKINS_URL}/job/{JENKINS_JOB}/{build_number}/api/json"

    response = requests.get(
        url,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        timeout=10
    )

    response.raise_for_status()

    return response.json()
