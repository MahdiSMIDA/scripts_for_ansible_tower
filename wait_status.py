import sys
import requests
import time
from requests.auth import HTTPBasicAuth


def wait_for_job_status(job_id, tower_url, auth_token, auth_username, auth_password):
    headers = {
        'Content-Type': 'application/json'
    }
    auth = None

    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    elif auth_username and auth_password:
        auth = HTTPBasicAuth(auth_username, auth_password)

    url = f'{tower_url}/api/v2/jobs/{job_id}/'
    status_url = f'{tower_url}/api/v2/jobs/{job_id}/job_events/?ordering=-id'

    # Retrieve the initial status of the job
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        print(f"Failed to retrieve job details. Status code: {response.status_code}")
        return

    job_details = response.json()
    current_status = job_details['status']
    print(f"Current status of job (ID {job_id}): {current_status}")

    # Wait until the job status is "successful" or "failed"
    while current_status != "successful" and current_status != "failed":
        time.sleep(5)  # Wait for 5 seconds before checking the status again

        response = requests.get(status_url, headers=headers, auth=auth)
        if response.status_code != 200:
            print(f"Failed to retrieve job events. Status code: {response.status_code}")
            return

        job_events = response.json()['results']
        if job_events:
            latest_event = job_events[0]
            current_status = latest_event['event_data']['res']['status']
            print(f"Current status of job (ID {job_id}): {current_status}")

    # Print the job's standard output (stdout) as plain text in Markdown format
    response = requests.get(f'{url}stdout/?format=ansi', headers=headers, auth=auth)
    if response.status_code == 200:
        job_stdout = response.text
        print(f"Job stdout:\n```\n{job_stdout}\n```")

    if current_status == "failed":
        sys.exit(1)  # Exit with non-zero status code to indicate failure


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide the job ID, Ansible Tower URL, and authentication method as command-line arguments.")
        print("For token authentication: python wait_status.py <job_id> <tower_url> --token <auth_token>")
        print("For basic authentication: python wait_status.py <job_id> <tower_url> --basic-auth <username> <password>")
    else:
        job_id = sys.argv[1]
        tower_url = sys.argv[2]

        if sys.argv[3] == "--token" and len(sys.argv) == 5:
            auth_token = sys.argv[4]
            wait_for_job_status(job_id, tower_url, auth_token, None, None)
        elif sys.argv[3] == "--basic-auth" and len(sys.argv) == 6:
            auth_username = sys.argv[4]
            auth_password = sys.argv[5]
            wait_for_job_status(job_id, tower_url, None, auth_username, auth_password)
        else:
            print("Invalid authentication method or missing authentication details.")

