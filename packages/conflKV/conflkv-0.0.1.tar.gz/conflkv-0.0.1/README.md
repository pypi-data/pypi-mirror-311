# ConflKV

**ConflKV** is a Python library for managing key-value pairs stored in Confluence pages using the Confluence REST API. It simplifies working with the storage format of Confluence pages, enabling operations like fetching, updating, inserting, deleting, and searching for key-value pairs.

This can be especially useful for automating documentation updates from a CI/CD pipelines to proactively preventing documentation drift. 

---

## Features

- Fetch all key-value pairs from a Confluence page.
- Insert new key-value pairs while avoiding duplicates.
- Update or replace existing key-value pairs.
- Delete key-value pairs with optional error handling for missing keys.
- Search for specific keys with configurable error handling.
- Set a custom HTML header with an associated key-value table.

---

## Usage

Below is an example of how to use **ConflKV** to manage key-value pairs in a Confluence page.

```python
import os  # For managing environment variables
from conflkv import PageManager

# Initialize the PageManager with your Confluence credentials and page details
app1_doc_page = PageManager(
    page_id="25559043",  # Replace with your Confluence page ID
    server_url=f'https://{os.environ["CONFLUENCE_INSTANCE"]}.atlassian.net',
    auth_username=os.environ["CONFLUENCE_USERNAME"],
    auth_token=os.environ["CONFLUENCE_TOKEN"],
)

# Set up the page with an HTML header and a key-value table
app1_doc_page.set_html_header(
    header="About",
    paragraph="This webpage is sample key-value store related to App1.",
    table_key="Key",
    table_value="Value",
)

data = confluence.fetchall()  # Retrieve all key-value pairs as a dictionary
confluence.replaceall(data)  # Replace all key-value pairs with a new dictionary

key_data = confluence.search("key", ok_if_missing=True)  # Search for a key; ignores missing keys if 'ok_if_missing' is True

confluence.insert("key", "value")  # Insert a new pair; raises an error if the key exists
confluence.replace("key", "new_value")  # Replace an existing pair; raises an error if the key doesn't exist
confluence.upsert("key", "value")  # Insert or update a key-value pair
confluence.delete("key", ok_if_missing=True)  # Delete a key; ignores missing keys if 'ok_if_missing' is True

# Close the connection when done
confluence.close()
```

---

## Configuration

### Required Parameters
- **`page_id`**: The ID of the Confluence page to manage.
- **`server_url`**: The base URL of your Confluence instance (e.g., `https://your-instance.atlassian.net`).
- **`auth_username`**: Your Confluence username or email.
- **`auth_token`**: A personal access token generated in Confluence for API access.

### Environment Variables (Optional)
For secure handling of credentials, it is recommended to set the following environment variables:
- `CONFLUENCE_INSTANCE`
- `CONFLUENCE_USERNAME`
- `CONFLUENCE_TOKEN`

---

## Trademarks

Confluence is a registered trademark of Atlassian. This library is not affiliated with, endorsed by, or sponsored by Atlassian.
