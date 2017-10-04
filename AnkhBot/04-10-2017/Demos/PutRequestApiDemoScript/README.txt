To use/test this script one needs their own CLIENT-ID to use the Twitch APIv5

Register an application to get an client ID on the bottom of the following page;

# https://www.twitch.tv/settings/connections

When registering you can use the following link as Redirect URI

# http://localhost/


After you got a client-id you need to generate an OAuth with an user with the following scopes:

# user_read       > Used to get the user-id of the authorized user
# channel_editor  > Used to demonstrate the PUT Request to push new data to twitch

You can generate an OAuth with the following link;
**REPLACE YOUR_CLIENT_ID WITH THE CLIENT ID YOU GOT AFTER REGISTERING AN APPLICATION**

# https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&scope=user_read+channel_editor&force_verify=true

One you navigate to the above link (after replacing YOUR_CLIENT_ID) you need to login with your account.
The account you login with will have the user_read and channel_editor scopes so that channel will be used in the example script.

After login you will be redirected to localhost, which most likely your browser cannot find.
BUT look in the address bar and you will see the link containing your access_token or OAuth

# http://localhost/#access_token=yiba5s5vi2qxvngurgh3j2y56qsp83&scope=user_read+channel_editor

so your access_token is: yiba5s5vi2qxvngurgh3j2y56qsp83

