from flask import render_template, session
from datetime import datetime, timedelta
from functools import wraps
import config, requests


#Authorization code passed into the function, POST request made to obtain the token credentials, 
#which are set as session variables.
def exchange_code(code: str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
    }
    response = requests.post(config.token_url, headers=headers, data=data)

    credentials = response.json()
    
    #Initialise all session variables and expiry times for the tokens.
    session["access_token"] = credentials["access_token"]
    session["refresh_token"] = credentials["refresh_token"]
    session["access_token_expires_in"] = credentials["expires_in"] 
    session["refresh_token_expires_in"] = credentials["refresh_token_expires_in"]
    session["token_expiry_time"] = str((datetime.now()) + timedelta(seconds=session["access_token_expires_in"]))
    session["refresh_token_expiry_time"] = str(datetime.now() + timedelta(seconds=credentials["refresh_token_expires_in"]))
    session["contacts_page_no"] = 1


#Decorator for all functions that require a valid access token. This will be called prior to the 
#function it decorates, and refresh the access token if required, else return an error stating the user must authenticate.
def token_required(f):
  @wraps(f)
  def decorated_function(*args, **kws):
    error_message = refresh_access_token()
    if error_message is None:
        return f(*args, **kws)
    else:
        return render_template("welcome.html", error=error_message)
  return decorated_function


#Function to check the existing expiry time of the access token, if it has expired, refresh it and update the session variables.
def refresh_access_token():
    if session.get("token_expiry_time") is not None:
        if session["token_expiry_time"] < str(datetime.now()):
            try:
                refresh_token = session["refresh_token"]
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                }
                data = {
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                }
                response = requests.post(config.token_url, headers=headers, data=data)
                #Return a message requesting the user to re-authenticate  either due to an error or 
                # an invalid refresh_token.
                if response.status_code == 400 or response.status_code == 401:
                    message = "Your refresh token has expired, you must re-authenticate!"
                    return message
                #If refresh is successful, update the session variables and expiry times.
                elif response.status_code == 200:
                    credentials = response.json()
                    session["access_token"] = credentials["access_token"]
                    session["refresh_token"] = credentials["refresh_token"]
                    session["access_token_expires_in"] = credentials["expires_in"] 
                    session["refresh_token_expires_in"] = credentials["refresh_token_expires_in"]
                    session["token_expiry_time"] = str((datetime.now()) + timedelta(seconds=session["access_token_expires_in"]))
                    session["refresh_token_expiry_time"] = str(datetime.now() + timedelta(seconds=credentials["refresh_token_expires_in"]))
            except Exception as ex:
                return ("Exception message: " + str(ex))
        else:
            print("Token still valid!")
    else:
        # Set message due to error - requiring user to re-auth or authenticate from the start.
        message = "No session found, you must authenticate!"
        return message
        