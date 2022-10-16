from flask import Flask, render_template, redirect, request, redirect, session
import config, auth, requests, os, json

app = Flask(__name__)

#Set secret key for encrypting the session - this uses os to retrieve a set environment variable. 
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")



#Define the route for the main homepage
@app.route("/")
def welcome():
    return render_template("welcome.html")

#Redirect the app to the SBCA OAUTH2.0 flow using the request_uri string built in config.py.
@app.route("/authenticate")
def get_code():
    return redirect(config.request_uri)

#SBCA authorization server redirects here (registered callback_url of localhost:5000/redirect), authorization code is
#retrieved and a call made to exchange the code for token credentials.
@app.route("/redirect")
def login_redirect():
    code = request.args.get("code")
    auth.exchange_code(code)
    return redirect("/businesses")


#Make the required GET Request to obtain a list of businesses the authenticated user is allowed to access.
#Return the list to the authenticated.html template to use as the datasource for an HTML selection element.

#This is the first function decorated with the token_required decorator. This function is called before get_businesses()
#ensuring a valid access token is present, and if not uses the refresh_token to refresh it. The function definitions are in auth.py.
@app.route("/businesses", methods=["GET"])
@auth.token_required
def get_businesses():
    if session.get("access_token") == None:
        return render_template("welcome.html", text="Authenticate first!")
    else:
        response = requests.get(
            config.base_url + "/businesses",
            headers={
                "Authorization": "Bearer %s" % session["access_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        businesses = response.json()
        return render_template("authenticated.html", businesses=businesses["$items"])

#When the business has been chosen, the business_id is set in the session as the selected business.
#You would likely be using a database to store all businesses and their ids etc. in your application.
@app.route("/business-selected", methods=["GET", "POST"])
@auth.token_required
def select_business():
    selection = request.form.get("business-select")
    session["business_id"] = selection
    #This function returns the user to a template ready to make a get request via the /contacts endpoint.
    #The initial page number is passed to the template in this instance as we aren't using a database in this example and it is
    # required by Jinja2 for the page to render successfully.
    return render_template("contacts.html", page=1)

#If a POST request to create a contact is made, pass the user to a new page displaying a confirmation
#of the posted values.
@app.route("/contact")
@auth.token_required
def contact():
    return render_template("contact.html")

#A GET request to retrieve a list of contacts from the business including an initial page number. 
@auth.token_required
def get_contacts_request(page_no):
    response = requests.get(
        config.base_url + "/contacts",
        headers={
            "Authorization": "Bearer %s" % session["access_token"],
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Business": session["business_id"],
        },
        params={"page": str(page_no),
            "items_per_page": "20",

                },
    )
    return response.json()

#As no database is used, this function handles calling the contacts endpoint, checking the paging and rendering the correct pages.
# The contents of the $items array are returned to the contacts.html template to be rendered.
@app.route('/contacts/page/<int:page>', methods=["GET"])
@auth.token_required
def get_contacts(page):
    contacts = get_contacts_request(page)

    #determine if prev or next page should be available. 
    def check_back(contacts):
        if contacts['$back'] == None:
            back_page = False
        else:
            back_page = True
        return back_page
    
    def check_next(contacts):
        if contacts['$next'] == None:
            next_page = False
        else:
            next_page = True
        return next_page
    
    #set boolean to pass to contacts template.
    next_page = check_next(contacts)
    back_page = check_back(contacts)
    
    return render_template("contacts.html", contacts=contacts['$items'], back=back_page, next=next_page, page=contacts['$page'])

#Page to render a form in order to create a new contact.
@app.route("/create-contact")
@auth.token_required
def create_contact():
    return render_template("contact-form.html")


#POST request to create a new contact and setting some attributes, returning the user to a page displaying
# the details posted.
@app.route("/contact", methods=["GET", "POST"])
@auth.token_required
def contact_post():
    if request.method == "POST":
        try:
            headers = {
            "Authorization": "Bearer %s" % session["access_token"],
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Business": session["business_id"],
            }
            data = json.dumps({
                "contact": {
                    "name": str(request.form.get("name")),
                    "contact_type_ids": [str(request.form.get("contact_type_id"))],
                    "main_address": {
                        "address_line_1": str(request.form.get("address_line_1")),
                        "address_line_2": str(request.form.get("address_line_2")),
                        "city": str(request.form.get("city")),
                        "region": str(request.form.get("region")),
                        "postal_code": str(request.form.get("postal_code"))
                    },
                    "reference": str(request.form.get("ref")),
                    "notes": str(request.form.get("notes"))   
                }
            })
            response = requests.post(config.base_url + "/contacts", headers=headers, data=data)
        except Exception as e:
            return render_template("welcome.html", str(e))
        print(response)
    contact = response.json()
    return render_template("contact.html", contact=contact)
