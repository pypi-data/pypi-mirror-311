# NetBox Authorized Keys Plugin

NetBox Authorized Keys is a plugin for NetBox that allows you to store and manage SSH authorized keys.

## Features

- Store SSH authorized keys
- Assign keys to devices or virtual machines
- Manage keys through the NetBox UI
- API support for managing keys

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/netbox_authorized_keys.git
    ```

2. Navigate to the project directory:
    ```sh
    cd netbox_authorized_keys
    ```

3. Install the plugin:
    ```sh
    pip install .
    ```

4. Add the plugin to your NetBox configuration:
    ```python
    PLUGINS = ["netbox_authorized_keys"]
    PLUGINS_CONFIG = {
        "netbox_authorized_keys": {
            # Add any plugin-specific configuration here
        }
    }
    ```

5. Run the migrations:
    ```sh
    python manage.py migrate
    ```