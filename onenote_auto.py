import msal
import yaml
import requests

def get_access_token( config_filename = 'config.yaml'):
    with open(config_filename) as config_file:
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

def list_notebook_names(access_token):
    response = get_notebook_names(access_token)
    response_json = response.json()
    for i in range(len(response_json["value"])):
        print(response_json["value"][i]["displayName"])

def get_notebook_id(access_token, notebook_name):
    response = get_notebook_names(access_token)
    response_json = response.json()

    for i in range(len(response_json["value"])):
        if response_json["value"][i]["displayName"] == notebook_name :
            return(response_json["value"][i]["id"])

    print(f'Error - Could not find notebook {notebook_name}.')
    return()            

def add_notebook_pages( access_token, page_title_string_list, config_filename = 'config.yaml' ):
    # TODO get rid of this file read.
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)

    section_id = config['section_id']

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
    # Create HTTP POST request headers
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/xhtml+xml',
    }
    # One loop for each title in the title list
    for title in page_title_string_list:
        # Insert the title into the HTML
        final_page_content = page_content_template.format(title)

        # Now post the request
        url = f'https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages'
        response = requests.post(url, headers=headers, data=final_page_content.encode('utf-8'))

        if response.status_code == requests.codes.created :
            print("Page with title " + '"' + title + '" created successfully.' )
        else:
            print("ERROR! - Could not create page with title " + '"' + title + '" .' )
            print(response.status_code)
            print(response.json())
            print( "No further page creations will be attempted.")
            break



    