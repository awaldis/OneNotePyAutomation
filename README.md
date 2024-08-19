# OneNotePyAutomation
Read and write OneNote notebooks with Python and the Microsoft Graph API

Command to start quickly in the Python REPL:
`python -i onenote_interactive_setup.py`

Currently, you'll need to supply your own client_id in the YAML file.

Here is an example of how one might add journal pages to a notebook section:

```
C:\repos\OneNotePyAutomation> python -i onenote_interactive_setup.py
>>> days = get_consecutive_days('2024-Aug-19')
>>> days
['2024-Aug-19 - Monday', '2024-Aug-20 - Tuesday', '2024-Aug-21 - Wednesday', '2024-Aug-22 - Thursday', '2024-Aug-23 - Friday', '2024-Aug-24 - Saturday', '2024-Aug-25 - Sunday']
>>> onc.add_notebook_pages("Journal Notebook", "Journal Section", days)
Page with title "2024-Aug-19 - Monday" created successfully.
Page with title "2024-Aug-20 - Tuesday" created successfully.
Page with title "2024-Aug-21 - Wednesday" created successfully.
Page with title "2024-Aug-22 - Thursday" created successfully.
Page with title "2024-Aug-23 - Friday" created successfully.
Page with title "2024-Aug-24 - Saturday" created successfully.
Page with title "2024-Aug-25 - Sunday" created successfully.
```