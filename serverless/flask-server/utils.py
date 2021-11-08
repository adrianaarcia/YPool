from collections import defaultdict
import os
import smtplib
from email.message import EmailMessage
from boto3.dynamodb.conditions import Key

def generate_pairs(location_list):
    mappings = {}
    for location in location_list:
        if location not in mappings:
            mappings[location] = 0
        mappings[location] += 1

    pairs = []
    for key, value in mappings.items():
        pairs.append((key, value))
    return pairs


def get_emails(netid_list, table):
    """ given list of netids, lookup emails in dynamodb table and return list of emails"""
    email_list = []
    for netid in netid_list:
        response = table.query(KeyConditionExpression=Key("netId").eq(netid))
        assert len(response["Items"]) == 1
        email_list.append(response["Items"][0]["email"])
    return email_list


def get_names(netid_list, table):
    """ given list of netids, lookup names in dynamodb table and return list of names"""
    name_list = []
    for netid in netid_list:
        response = table.query(KeyConditionExpression=Key("netId").eq(netid))
        assert len(response["Items"]) == 1
        fn = response["Items"][0]["first_name"]
        ln = response["Items"][0]["last_name"]
        name_list.append(f"{fn} {ln}")
    return name_list


def sort_by_group(requests):
    """ given a list of requests, returns a list of lists, where the sublists contain netids of each group """
    groups = defaultdict(list)
    for req in requests:
        if req["matched"]:
            groups[req["groupId"]].append(req["netId"])
    return list(groups.values())


def send_emails_tentative(recipients):
    """ given list of email addresses, sends emails to each recipient indicating a match """
    EMAIL_ADDRESS = "ypool.official@gmail.com"
    EMAIL_PASSWORD = "rekcyzrrpcdgfmfl"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        people = "%s\n%s" % ("\n".join(recipients[:-1]), str(recipients[-1]))
        notif = f"Thank you for using YPool! You have successfully been matched. Please accept or decline this match at https://yalepool.com/ridestatus. You can find the contact information of your fellow riders below:\n{people}\n\nPlease note that this match is not finalized until all group members have confirmed. You will receive another email after all members have confirmed."

        msg = EmailMessage()
        msg["Subject"] = "[YPool] Ride Match Found - Please Confirm"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipients
        msg.set_content(notif)

        smtp.send_message(msg)


def send_emails_final(recipients):
    """ given list of email addresses, sends emails to each recipient indicating a match """
    EMAIL_ADDRESS = "ypool.official@gmail.com"
    EMAIL_PASSWORD = "rekcyzrrpcdgfmfl"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        people = "%s\n%s" % ("\n".join(recipients[:-1]), str(recipients[-1]))
        notif = f"Thank you for using YPool! Your ride match group has been confirmed. Please find the contact information of your fellow riders below:\n{people}\n\nHave a great trip!"

        msg = EmailMessage()
        msg["Subject"] = "[YPool] Ride Match Confirmation"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipients
        msg.set_content(notif)

        smtp.send_message(msg)


def send_emails_decline(recipients):
    """ given list of email addresses, sends emails to each recipient indicating a match """
    EMAIL_ADDRESS = "ypool.official@gmail.com"
    EMAIL_PASSWORD = "rekcyzrrpcdgfmfl"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        people = "%s\n%s" % ("\n".join(recipients[:-1]), str(recipients[-1]))
        notif = f"Thank you for using YPool! Unfortunately, someone in your group has declined the match, and the match has been dissolved. Your request has been reentered into the match pool, and we will send you an email as soon an a new match is found."

        msg = EmailMessage()
        msg["Subject"] = "[YPool] Ride Match Dissolved"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipients
        msg.set_content(notif)

        smtp.send_message(msg)