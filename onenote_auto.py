import msal
import yaml
import requests

def get_access_token():
    with open('config.yaml') as config_file:
        config = yaml.safe_load(config_file)

    # Initialize the MSAL public client
    authority = f'https://login.microsoftonline.com/consumers'
    app = msal.PublicClientApplication(
        config['client_id'],
        authority=authority,
    )

    # Acquire a token to access Microsoft Graph
    scope = ["Notes.ReadWrite"] 
    token_response = app.acquire_token_interactive(scopes=scope)

    if "access_token" in token_response :
        return(token_response["access_token"])

    # If we get here then we failed to get an access token.
    return(None)

def get_notebook_names(access_token):
    # Create HTTP GET request header
    headers = {
            'Authorization': 'Bearer ' + access_token,
    }

    url = 'https://graph.microsoft.com/v1.0/me/onenote/notebooks?$select=id,displayName'

    return(requests.get(url, headers=headers ))