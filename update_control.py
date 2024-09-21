import requests
import os

# GitHub API token and repository information
GITHUB_API_TOKEN = os.getenv('PAT')
OWNER = 'axs6'
REPO = 'repo'

# Headers for authentication
headers = {
    'Authorization': f'token {PAT}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get the latest release information
response = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/releases/latest', headers=headers)
release_info = response.json()

# Extract download count and release date
download_count = release_info['assets'][0]['download_count']
release_date = release_info['published_at']

# Path to your control file
control_file_path = 'control'

# Read the control file
with open(control_file_path, 'r') as file:
    control_content = file.readlines()

# Write the updated control file
with open(control_file_path, 'w') as file:
    for line in control_content:
        if line.startswith('Download-Count:'):
            file.write(f'Download-Count: {download_count}\n')
        elif line.startswith('Release-Date:'):
            file.write(f'Release-Date: {release_date}\n')
        else:
            file.write(line)
