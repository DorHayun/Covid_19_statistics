import requests
from flask import Flask, jsonify, request

# create an instance of the Flask object.
app = Flask(__name__)
app.url_map.strict_slashes = False

# defining the external API url
path_api = "https://disease.sh/v3/covid-19/historical"

# defining the parameter for the API call
payload = {"lastdays": "31"}

# defining a dictionary response for the status endpoint
response_success = {"status": "success"}
response_failure = {"status": "failed"}


def highest_peak(method_name: str):

    # get the country parameter from the request
    country = request.args.get('country')
    print(country)

    # making a get request for the external API
    request_url = f'{path_api}/{country}'
    response = requests.get(request_url, params=payload)
    data = response.json()
    print(request_url)

    # parsing the data
    key = None
    if method_name == "newCasesPeak":
        key = "cases"
    elif method_name == "recoveredPeak":
        key = "recovered"
    
    elif method_name == "deathsPeak":
        key = "deaths"

    #assign the specific dictionary from the api as JSON    
    cases = data["timeline"][key]

    #variables definitions for looping through dictionary items and subtract prev value from current value
    prev = None
    max_diff = 0
    diff_key = None

    #loop throgh the items while calculating the highest peak
    for key, value in cases.items():
        if prev == None:
            prev = value
            continue

        current_diff = value - prev
        prev = value

        if current_diff > max_diff:
            max_diff = current_diff
            diff_key = key

    
    print(max_diff, diff_key)

    #send back response JSON as requested
    return jsonify(country=country,
                   date=diff_key,
                   method=method_name,
                   value=max_diff)


# defining newCasesPeak endpoint
@app.route("/newCasesPeak")
def newCasesPeak():
    return highest_peak(method_name="newCasesPeak")

# defining recoveredPeak endpoint


@app.route("/recoveredPeak")
def recoveredPeak():
    return highest_peak(method_name="recoveredPeak")

# defining deathsPeak endpoint


@app.route("/deathsPeak")
def deathsPeak():
    return highest_peak(method_name="deathsPeak")

# defining status endpoint


@app.route("/status")
def status():
    # making a get request for the external API
    r = requests.get("https://disease.sh/v3/covid-19/all")

    # checking wheter the request succeed or not and return it
    if (r.status_code == requests.codes.ok):
        return response_success
    else:
        return response_failure


# defining an error handling
@app.errorhandler(404)
def page_not_found(error):
    return {}, 404
