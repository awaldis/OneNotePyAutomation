# %%
import msal
import requests
import yaml

from create_consecutive_date_strings import get_consecutive_days

# %%
with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

# %%
# Initialize the MSAL public client
authority = f'https://login.microsoftonline.com/consumers'
app = msal.PublicClientApplication(
    config['client_id'],
    authority=authority,
)

# %%
# Acquire a token to access Microsoft Graph
scope = ["Notes.ReadWrite"] 
token_response = app.acquire_token_interactive(scopes=scope)
# %%
if "access_token" in token_response :
    access_token = token_response["access_token"]

# %%
# HTML template string
page_content_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{}</title>
    </head>
    <body>
    </body>
    </html>
"""
# %%
consecutive_days = get_consecutive_days(start_date_str="2024-Apr-08", num_days=2)


# %%
# Create HTTP POST request headers
headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/xhtml+xml',
}
# Loop through the dates and modify the HTML
for day in consecutive_days:
    final_page_content = page_content_template.format(day)

    # Now post the request
    section_id = config['section_id']
    url = f'https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages'
    response = requests.post(url, headers=headers, data=final_page_content.encode('utf-8'))
    print(response)

# %%
# Create HTTP GET request headers
headers = {
        'Authorization': 'Bearer ' + access_token,
}
# %%
url = 'https://graph.microsoft.com/v1.0/me/onenote/sections'

response = requests.get(url, headers=headers )

# %%
url = 'https://graph.microsoft.com/v1.0/me/onenote/notebooks?$select=id,displayName'

response = requests.get(url, headers=headers )

# %%
