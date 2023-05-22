# Script

This is the documentation for waiting status for Ansible Automation platform Job script using API V2.

## Installation

To install the script, follow these steps:

1. Install the required dependencies: requests
2. Download the script file: `wait_status.py`.

## Usage

To use the script, run the following command:

python wait_status.py <job_id> <tower_url> [options]

markdown
Copy code

**Arguments:**

- `<job_id>`: The ID of the job.
- `<tower_url>`: The URL of the Ansible Tower.

**Options:**

- `--token <auth_token>`: Use token authentication with the provided authentication token.
- `--basic-auth <username> <password>`: Use basic authentication with the provided username and password.

## Examples

Here are some examples of using the script:

1. Run the script with token authentication:

   ```shell
   python wait_status.py 1234 https://tower.example.com --token ABCDEFGHIJKLMNOP
Run the script with basic authentication:

shell
Copy code
python wait_status.py 1234 https://tower.example.com --basic-auth username password
API Reference
The script provides the following functions:

wait_for_job_status(job_id, tower_url, auth_token, auth_username, auth_password): Waits for the job status to be "successful" or "failed".
## License
This script is licensed under the MIT License. See LICENSE file for more details.

## Author
Script authored by Mahdi SMIDA.
