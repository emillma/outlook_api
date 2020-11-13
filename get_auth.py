"""
The code is taken from https://github.com/Azure-Samples/ms-identity-python-devicecodeflow
The configuration file would look like this:
{
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "your_client_id",
    "scope": ["User.ReadBasic.All"],
    "endpoint": "https://graph.microsoft.com/v1.0/users"
}
    # You can find the other permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    # To restrict who can login to this app, you can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer
You can then run this sample with a JSON configuration file:

    python sample.py parameters.json
"""

import json
import logging

import os
import atexit
import msal


# Optional logging
# logging.basicConfig(level=logging.DEBUG)
def get_auth():
    with open('parameters.json', 'r') as file:
        config = json.load(file)
    cache_file = '/private/my_cache.bin'
    cache = msal.SerializableTokenCache()
    if os.path.exists(cache_file):
        cache.deserialize(open(cache_file, "r").read())

    atexit.register(lambda:
                    open(cache_file, "w").write(cache.serialize())
                    if cache.has_state_changed else None
                    )

    app = msal.PublicClientApplication(
        config["client_id"], authority=config["authority"], token_cache=cache

    )

    result = None

    accounts = app.get_accounts()
    if accounts:
        # for a in accounts:
        #     print(a["username"])
        chosen = accounts[0]
        result = app.acquire_token_silent(config["scope"], account=chosen)

    if not result:
        logging.error(
            "No suitable token exists in cache. Let's get a new one from AAD.")

        flow = app.initiate_device_flow(scopes=config["scope"])
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
    return result['access_token']


if __name__ == "__main__":
    auth = get_auth()
    print(auth)
