import msal
import requests
import yaml


class OneNoteClient:
    """For reading and writing Microsoft OneNote notebooks via the Graph API."""

    def __init__(self, config_filename="config.yaml"):
        self.config_filename = config_filename
        self.access_token = self._get_access_token()
        if self.access_token is None:
            raise Exception("Failed to obtain access token.")

    def _get_access_token(self):
        """
        Use MSAL library and Microsoft endpoint to get a token interactively.
        This method is not intended to be called from outside the class.

        Args:
            None but self.

        Returns:
            Access token.
        """
        # Read configuration parameters from the config file.
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

    def get_notebook_names_and_ids(self):
        """
        Using an already existing access token, get a list of names of
        notebooks and their corresponding identification numbers.

        Args:
            None but self.

        Returns:
            A requests response object containing the list of notebook names and ids.
        """
        headers = {"Authorization": "Bearer " + self.access_token}
        url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks?$select=id,displayName"
        return requests.get(url, headers=headers)

    def get_section_names_and_ids(self, notebook_id):
        """
        Using an already existing access token and a notebook ID number, get
        a list of the names of the sections in the notebook and their
        corresponding identification numbers.

        Args:
            None but self.

        Returns:
            A requests response object containing the list of section names and ids.
        """
        headers = {"Authorization": "Bearer " + self.access_token}
        url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections?$select=id,displayName"
        return requests.get(url, headers=headers)

    def list_notebook_names(self):
        """
        Using an already existing access token, print the list of notebooks
        associated with that token. 

        Args:
            None but self.

        Returns:
            None - this function only prints to standard output.
        """
        response = self.get_notebook_names_and_ids()
        response_json = response.json()
        for item in response_json["value"]:
            print(item["displayName"])

    def list_section_names(self, notebook_name):
        """
        Using an already existing access token and the notebook name,
        print the list of sections associated with that token. 

        Args:
            None but self.

        Returns:
            None - this function only prints to standard output.
        """
        notebook_id = self.get_notebook_id(notebook_name)
        
        if notebook_id is None:
            return      

        response = self.get_section_names_and_ids(notebook_id)
        response_json = response.json()
        for item in response_json["value"]:
            print(item["displayName"])

    def get_notebook_id(self, notebook_name):
        """
        Return the notebook id number associated with the name of of the
        notebook provided in the inputs.

        Args:
            notebook_name - a string containing the notebook name.

        Returns:
            The notebook id associated with the input name.
        """
        response = self.get_notebook_names_and_ids()
        response_json = response.json()

        for item in response_json["value"]:
            if item["displayName"] == notebook_name:
                return item["id"]

        print(f"Error - Could not find notebook {notebook_name}.")
        return None

    def get_section_id(self, notebook_name, section_name):
        """
        Return the section id number associated with the name of the
        notebook and section provided in the inputs.

        Args:
            notebook_name - a string containing the notebook name.
            section_name - a string containing the section name.

        Returns:
            The section id associated with the input name.
        """
        response = self.get_section_names_and_ids(self.get_notebook_id(notebook_name))
        response_json = response.json()

        for item in response_json["value"]:
            if item["displayName"] == section_name:
                return item["id"]

        print(f"Error - Could not find notebook {section_name}.")
        return None

    def add_notebook_pages(self, notebook_name, section_name, page_title_string_list):
        """
        Add one blank notebook page for each title specified in the the input
        to the notebook and section named in the input.  

        Args:
            notebook_name - a string containing the notebook name.
            section_name - a string containing the section name.
            page_title_string_list - list of titles for each page to add.

        Returns:
            None except for status and error messages printed to standard
            output.
        """
        section_id = self.get_section_id(notebook_name, section_name)

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
