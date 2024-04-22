import msal
import requests
import yaml


class OneNoteClient:
    """For reading and writing Microsoft OneNote notebooks via the Graph API."""    
    def __init__(self, config_filename="config.yaml"):
        self.config_filename = config_filename
        self.access_token = self.get_access_token()
        if self.access_token is None:
            raise Exception("Failed to obtain access token.")

    def get_access_token(self):
        with open(self.config_filename) as config_file:
            config = yaml.safe_load(config_file)

        # Initialize the MSAL public client
        authority = "https://login.microsoftonline.com/consumers"
        app = msal.PublicClientApplication(
            config["client_id"],
            authority=authority,
        )

        # Acquire a token to access Microsoft Graph
        scope = ["Notes.ReadWrite"]
        token_response = app.acquire_token_interactive(scopes=scope)

        return token_response.get("access_token")

    def get_notebook_names(self):
        headers = {"Authorization": "Bearer " + self.access_token}
        url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks?$select=id,displayName"
        return requests.get(url, headers=headers)

    def get_section_names(self, notebook_id):
        headers = {"Authorization": "Bearer " + self.access_token}
        url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections?$select=id,displayName"
        return requests.get(url, headers=headers)

    def list_notebook_names(self):
        response = self.get_notebook_names()
        response_json = response.json()
        for item in response_json["value"]:
            print(item["displayName"])

    def get_notebook_id(self, notebook_name):
        response = self.get_notebook_names()
        response_json = response.json()

        for item in response_json["value"]:
            if item["displayName"] == notebook_name:
                return item["id"]

        print(f"Error - Could not find notebook {notebook_name}.")
        return None

    def add_notebook_pages(self, page_title_string_list):
        # Load section_id from config
        with open(self.config_filename) as config_file:
            config = yaml.safe_load(config_file)
        section_id = config["section_id"]

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

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/xhtml+xml",
        }

        for title in page_title_string_list:
            final_page_content = page_content_template.format(title)
            url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages"
            response = requests.post(
                url, headers=headers, data=final_page_content.encode("utf-8")
            )

            if response.status_code == requests.codes.created:
                print(f'Page with title "{title}" created successfully.')
            else:
                print(f'ERROR! - Could not create page with title "{title}".')
                print(response.status_code)
                print(response.json())
                break
