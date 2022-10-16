# Key details required for the authorization process.

# In production you would ensure important details such as client_id and client_secret are stored securely.

#ENTER YOUR REGISTERED CLIENT ID, CLIENT SECRET AND CALLBACK URL:
client_id = "{{CLIENT_ID}}"
client_secret = "{{CLIENT_SECRET}}"
redirect_uri = "{{CALLBACK_URL}}"

#Remaining details required to build the intial request URI to initiate the OAuth2.0 flow.
response_type = "code"
auth_url = "https://www.sageone.com/oauth2/auth/central?filter=apiv3.1"
token_url = "https://oauth.accounting.sage.com/token"
scope = "full_access"
state = "AABBCCDD"

#Completed request URI.
request_uri = auth_url + "&response_type=" + response_type + "&client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&scope=" + scope + "&state=" + state

#API Base URL.
base_url = "https://api.accounting.sage.com/v3.1"


