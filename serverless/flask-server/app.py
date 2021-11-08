from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    send_file,
    url_for,
    send_from_directory,
    redirect,
)
from flask_cors import CORS
from flask_cas import CAS, login_required, logout
from flask_s3 import FlaskS3
import os
import boto3
from boto3.dynamodb.conditions import Key
import uuid
from datetime import datetime
from pytz import timezone
import decimal
import simplejson as json
from random_matching import random_matching
from matching.utility import combine_dt
from utils import (
    generate_pairs,
    get_emails,
    get_names,
    sort_by_group,
    send_emails_tentative,
    send_emails_final,
    send_emails_decline,
)
from matching.matching import find_matches
from api_keys import get_api_key, is_key_valid, is_key_valid_match_algo

REQUIRE_KEY = True

# Initialize Flask App
app = Flask(__name__, template_folder="build", static_folder="build/static")
app.config.from_object(__name__)
# app.config['FLASKS3_BUCKET_NAME'] = 'ypool-static'

app.config["CAS_SERVER"] = "https://secure.its.yale.edu"
app.config["CAS_LOGIN_ROUTE"] = "/cas/login"
app.config["CAS_LOGOUT_ROUTE"] = "/cas/logout"
app.config["CAS_AFTER_LOGIN"] = "index"
app.config["CAS_AFTER_LOGOUT"] = "home"
app.secret_key = "YOUR SECRET KEY HERE"

CORS(app)  # enable CORS

cas = CAS(app, "/cas")
# s3 = FlaskS3(app) # used for hosting static assets on S3

USERS_TABLE = os.environ["USERS_TABLE"]
REQUESTS_TABLE = os.environ["REQUESTS_TABLE"]
GROUPS_TABLE = os.environ["GROUPS_TABLE"]
# DESTINATIONS_TABLE = os.environ['DESTINATIONS_TABLE'] # currently not used, destinations are hard coded

IS_OFFLINE = os.environ.get("IS_OFFLINE")
# for local debugging with dynamodb functionality
if IS_OFFLINE:
    client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )
else:
    client = boto3.client("dynamodb")
    dynamodb = boto3.resource("dynamodb")


@app.route("/")
def home():
    """
    landing page not protected by CAS authentication, but redirects to index()
    """
    return render_template("index.html")


@app.route("/<path:path>")
@login_required
def index(path):
    # serve images at top level if needed
    if "png" in path or "ico" in path or "svg" in path or "txt" in path:
        image_path = os.path.join("build", path)
        return send_file(image_path)

    # send over netid and api key - note this is CAS protected
    return render_template(
        "index.html", flask_token=cas.username, api_key=get_api_key()
    )


# static assets should eventually be served from s3, since flask is slow in production environment
@app.route("/images/<filename>")
def image(filename):
    return send_from_directory("build/images", filename)


@app.route("/static/css/<filename>")
def css(filename):
    return send_from_directory("build/static/css", filename)


@app.route("/static/js/<filename>")
def js(filename):
    return send_from_directory("build/static/js", filename)


#####################################################################
# the below routes are API routes and require an api key for access
#####################################################################


@app.route("/users", methods=["POST"])
def create_user():
    """
    register a user with netid, first_name, last_name, and email
    all first time users will be prompted to enter this information
    """
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    user_id = request.json.get("netId")  # primary key
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")

    if not user_id or not first_name or not last_name or not email:
        return (
            jsonify({"error": "Please provide netId, first/last name, and email"}),
            400,
        )

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            "netId": {"S": user_id},
            "first_name": {"S": first_name},
            "last_name": {"S": last_name},
            "email": {"S": email},
        },
    )

    return jsonify(
        {
            "netId": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
    )


@app.route("/ride-request", methods=["POST"])
def submit_ride_request():
    """
    submit a ride request with the following required fields:
        - netId (string) - netId of requester
        - date (date object) - date of travel
        - time (time object) - time of travel
        - origin (string) - chosen from dropdown of origins
        - destination (string) - chosen from dropdown of destinations
        - preferred_car_type (string) - "regular" or "XL"
        - preferred_group_size (int) - number of desired riders in group
    """
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netid = request.json.get("netId")
    if not netid:
        return jsonify({"error": "Please provide netId to request a ride"}), 400
    date = request.json.get("date")
    if not date:
        return jsonify({"error": "Please provide date to request a ride"}), 400
    time = request.json.get("time")
    if not time:
        return jsonify({"error": "Please provide time to request a ride"}), 400
    origin = request.json.get("origin")
    if not origin:
        return jsonify({"error": "Please provide origin to request a ride"}), 400
    destination = request.json.get("destination")
    if not destination:
        return jsonify({"error": "Please provide destination to request a ride"}), 400
    preferred_car_type = request.json.get("preferred_car_type")
    if not preferred_car_type:
        return (
            jsonify(
                {"error": "Please provide preferred_car_type to request a ride"}),
            400,
        )
    preferred_group_size = request.json.get("preferred_group_size")
    if not preferred_group_size:
        return (
            jsonify(
                {"error": "Please provide preferred_group_size to request a ride"}),
            400,
        )

    uid = str(uuid.uuid4())  # generate unique identifier for request
    tz = timezone("EST")
    curr_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    resp = client.put_item(
        TableName=REQUESTS_TABLE,
        Item={
            "requestId": {"S": uid},
            "netId": {"S": netid},
            "request_time": {"S": curr_time},
            "date": {"S": date},
            "time": {"S": time},
            "origin": {"S": origin},
            "destination": {"S": destination},
            "preferred_car_type": {"S": preferred_car_type},
            "preferred_group_size": {"N": preferred_group_size},
            "matched": {"BOOL": False},
            "groupId": {"S": ""},
            "confirmed": {"BOOL": False},
            "allConfirmed": {"BOOL": False},
            "rematch": {"BOOL": False},
        },
    )

    return jsonify(
        {
            "requestId": uid,
            "netId": netid,
            "reesponse_time": curr_time,
            "date": date,
            "time": time,
            "origin": origin,
            "destination": destination,
            "preferred_car_type": preferred_car_type,
            "preferred_group_size": preferred_group_size,
            "matched": False,
            "groupId": "",
            "confirmed": False,
            "allConfirmed": False,
        }
    )


# get possible destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    """
    return all possible destinations
    """
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    # currently hardcoded because the list is short, can eventually migrate this to DB if necessary
    return jsonify(
        [
            "Yale",
            "Airport-JFK",
            "Airport-LGA",
            "Airport-EWR",
            "Airport-BDL",
            "Airport-BOS",
            "Airport-HVN",
            "TrainStation-UnionStationNHV",
            "TrainStation-PennStationNYC",
        ]
    )


@app.route("/get-request-status", methods=["POST"])
def get_status():
    '''
    get the status of all ride requests given:
        - netid (string)
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netid = request.json.get("netId")
    if not netid:
        return (
            jsonify({"error": "Please provide netId to query for ride statuses"}),
            400,
        )

    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.query(KeyConditionExpression=Key("netId").eq(netid))

    tz = timezone("EST")
    curr_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    # add status times
    for entry in response["Items"]:
        entry["status_time"] = curr_time

    return json.dumps(response["Items"])


@app.route("/is-registered", methods=["POST"])
def is_registered():
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netid = request.json.get("netId")
    resp = client.get_item(TableName=USERS_TABLE, Key={"netId": {"S": netid}})
    item = resp.get("Item")
    if not item:
        return jsonify({"isRegistered": False})
    else:
        return jsonify({"isRegistered": True, "firstName": item["first_name"]['S'], "lastName": item["last_name"]['S']})


# return group info given a groupId, also returns whether everyone has been confirmed
@app.route("/get-group-info", methods=["POST"])
def group_info():
    '''
    given groupId, return the following group info:
        - emails (list of emails of group members)
        - names (list of names of group members)
        - deparatureDate (string)
        - deparatureTime (string)
        - origins (list of pairs -> (origin, # people))
        - destinations (list of pairs -> (destination, # people))
        - groupSize (int)
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    groupId = request.json.get("groupId")

    if not groupId:
        return jsonify({"error": "Please provide groupId to get group members"}), 400

    table = dynamodb.Table(REQUESTS_TABLE)
    table_users = dynamodb.Table(USERS_TABLE)

    origins = []
    destinations = []

    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    members = []
    departureDateTimes = []
    for req in data:
        if req["groupId"] == groupId:
            members.append(req["netId"])
            departureDateTimes.append(combine_dt(req["date"], req["time"]))
            origins.append(req["origin"])
            destinations.append(req["destination"])

    actual_dt = min(departureDateTimes)

    departureDate = actual_dt.strftime('%Y-%m-%d')
    departureTime = actual_dt.strftime('%H:%M')

    emails = get_emails(members, table_users)
    names = get_names(members, table_users)
    groupSize = len(names)
    origins = generate_pairs(origins)
    destinations = generate_pairs(destinations)

    return jsonify({"emails": emails,
                    "names": names,
                    "groupSize": groupSize,
                    "departureTime": departureTime,
                    "departureDate": departureDate,
                    "origins": origins,
                    "destinations": destinations})


@app.route("/confirm-match", methods=["POST"])
def confirm():
    '''
    Confirms match
    @inputs:
        - nedId
        - requestId
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netId = request.json.get("netId")
    requestId = request.json.get("requestId")

    if not netId or not requestId:
        return (
            jsonify(
                {"error": "Please provide netId and requestId to confirm acceptance"}
            ),
            400,
        )

    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.query(
        KeyConditionExpression=Key("netId").eq(
            netId) & Key("requestId").eq(requestId)
    )

    result = response["Items"]
    print(result)
    if len(result) != 1:
        print("Length of result is %d (expected result is 1)" % (len(result)))
        return jsonify({"error": "Please provide valid netId and requestId"}), 400

    result = result[0]
    if not result["matched"]:
        return (
            jsonify(
                {"error": "Cannot confirm a request that has yet to be matched"}),
            400,
        )

    result["confirmed"] = True
    table.put_item(Item=result)
    print(result["groupId"])

    # if you are last to confirm, make everyone else in group allConfirmed true
    # get all items and update
    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])
    requests = json.loads(json.dumps(data))
    print(requests)

    all_confirmed = True
    for req in requests:
        if req["groupId"] == result["groupId"]:
            if not req["confirmed"]:
                all_confirmed = False
                break

    if all_confirmed:
        netids = []
        for req in requests:
            if req["groupId"] == result["groupId"]:
                netids.append(req["netId"])
                req["allConfirmed"] = True
                table.put_item(Item=req)

        # send out emails
        table_users = dynamodb.Table(USERS_TABLE)
        emails = get_emails(netids, table_users)
        send_emails_final(emails)

    return jsonify("confirmed success")


@app.route("/decline-match", methods=["POST"])
def decline():
    '''
    Declines match
    @inputs:
        - nedId
        - requestId
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netId = request.json.get("netId")
    requestId = request.json.get("requestId")

    if not netId or not requestId:
        return (
            jsonify(
                {"error": "Please provide netId and requestId to decline match"}),
            400,
        )

    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.query(
        KeyConditionExpression=Key("netId").eq(
            netId) & Key("requestId").eq(requestId)
    )

    result = response["Items"]
    if len(result) != 1:
        print("Length of result is %d (expected result is 1)" % (len(result)))
        return jsonify({"error": "Please provide valid netId and requestId"}), 400

    result = result[0]
    if not result["matched"]:
        return (
            jsonify(
                {"error": "Cannot decline a request that has yet to be matched"}),
            400,
        )

    # say that everyone in the group is now unmatched
    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])
    requests = json.loads(json.dumps(data))

    netids = []
    all_confirmed = True
    for req in requests:
        if req["groupId"] == result["groupId"]:
            netids.append(req["netId"])
            req["matched"] = False
            req["confirmed"] = False
            req["allConfirmed"] = False
            req["groupId"] = ""
            req["rematch"] = True
            table.put_item(Item=req)

    print(netids)

    # send out emails
    table_users = dynamodb.Table(USERS_TABLE)
    emails = get_emails(netids, table_users)
    send_emails_decline(emails)

    return jsonify("decline success")


@app.route("/cancel-request", methods=["POST"])
def cancel():
    '''
    cancels request
    @inputs:
        - nedId
        - requestId
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    netId = request.json.get("netId")
    requestId = request.json.get("requestId")

    if not netId or not requestId:
        return (
            jsonify(
                {"error": "Please provide netId and requestId to cancel request"}),
            400,
        )

    table = dynamodb.Table(REQUESTS_TABLE)
    response = table.query(
        KeyConditionExpression=Key("netId").eq(
            netId) & Key("requestId").eq(requestId)
    )

    result = response["Items"]
    if len(result) != 1:
        print("Length of result is %d (expected result is 1)" % (len(result)))
        return jsonify({"error": "Please provide valid netId and requestId"}), 400

    result = result[0]
    if result["matched"]:
        return (
            jsonify(
                {"error": "Cannot decline a request that has been matched"}),
            400,
        )

    try:
        response = table.delete_item(
            Key={
                'netId': netId,
                'requestId': requestId
            }
        )
    except:
        return (
            jsonify(
                {"error": "Could not delete request"}),
            501,
        )

    return (
        jsonify(
            {"success": "Deleted request successfully"}),
        200,
    )


@app.route("/run-algo", methods=["GET"])
def match():
    '''
    run the matching algo - this is manually invoked now but should be scheduled 
    to run every 15 - 30 min, depending on volume
    '''
    if REQUIRE_KEY:
        try:
            key = request.headers["api-key"]
        except:
            return jsonify({"error": "No API key provided - permission denied"}), 403
        if not is_key_valid_match_algo(key):
            return jsonify({"error": "Invalid API key - permission denied"}), 403

    # get everything from the db, pass it to algo, send out emails if needed
    table = dynamodb.Table(REQUESTS_TABLE)
    table_groups = dynamodb.Table(GROUPS_TABLE)
    table_users = dynamodb.Table(USERS_TABLE)
    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    requests = json.loads(json.dumps(data))

    print("Here are the requests before the algo:")
    print(requests)
    # updated_requests = random_matching(requests) # run the algo
    updated_requests = find_matches(requests)  # run the algo
    print("Here are the requests after the algo:")
    print(updated_requests)

    print("Here are the original requests:")
    print(requests)

    groups_table = dynamodb.Table(GROUPS_TABLE)

    # update db - this may be inefficient, not sure how this scales
    for req in updated_requests:
        table.put_item(Item=req)

    new_groups = sort_by_group(updated_requests)
    print(new_groups)

    for group in new_groups:
        # send out emails
        emails = get_emails(group, table_users)
        send_emails_tentative(emails)

    return json.dumps(updated_requests)


if __name__ == "__main__":
    app.run()
