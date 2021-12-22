# Google Drive Automatic Backup

This python script uploads all files in a specific folder locally to a specific folder in Google Drive. You can run it automaticaly as a crontab job or when the system boots with systemd. The script was tested on Linux, I don't discard the functionallity on Windows.

## Ussage

The **backup** folder of this repo must be inside of the folder you want to upload to Google Drive. Also you will need an Oauth credential file named as **client_secrets.json** inside **backup** folder of this repo, to generate the **client_secrets.json** file follow this [https://help.talend.com/r/E3i03eb7IpvsigwC58fxQg/Lp096EBnOyWNk33h~CKm~Q](tutorial)
