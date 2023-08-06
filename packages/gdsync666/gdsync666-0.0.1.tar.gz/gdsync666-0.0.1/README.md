![Google Drive sync logo](https://raw.githubusercontent.com/cyber-barrista/gdsync/master/google-drive-logo-logo.png)
# Google Drive Sync
A Python library to automatically synchronize your Google Drive content with local storage folder

# Install

```
pip install gdsync666
```

# Usage

```python
from google_drive_sync import upload, download

path_to_my_credentials = "credentials.json"
local_folder = "./local-storage"
google_drive_folder = "local-storage-backup"

# Puts all files from the local folder up to the drive one
upload(
    creds_file=path_to_my_credentials,
    local_folder=local_folder,
    remote_folder=google_drive_folder
)

# Gets additional files added to the drive folder later downloaded down to the local replica
download(
    creds_file=path_to_my_credentials,
    local_folder=local_folder,
    remote_folder=google_drive_folder
)
```
