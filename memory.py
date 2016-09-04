from __future__ import print_function
import time
import json
import re
import urllib2
import csv
from datetime import datetime

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getInfoIntent":
        return getInfo(intent, session)
    elif intent_name == "getLengthIntent":
        return getLength(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.NoIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "Memory"

    speech_output = "This is your memory, what do you want to remember?"
    reprompt_text = "I did not hear that, please repeat."
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help():
    session_attributes = {}
    card_title = "Help"
    url = 'https://raw.githubusercontent.com/ekt1701/My-Memory/master/myMemory.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    for row in cr:
        data.append(row[0])
    keywords = ' '.join(data)
    words = keywords.split()
    wordkeys = ", ".join(sorted(set(words), key=words.index))
    speech_output = "Here are your keywords " + str(wordkeys) + "What do you want to remember?"
    reprompt_text = "What do you want to remember?"
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))




def getInfo(intent, session):
    session_attributes = {}
    card_title = "Get info"
    namelookup = intent['slots']['Info']['value'].lower()
    name = str(namelookup)
    today = (time.strftime("%m/%d/%Y"))
    url = 'https://raw.githubusercontent.com/ekt1701/My-Memory/master/myMemory.csv'
    response = urllib2.urlopen(url)
    contents = csv.reader(response)
    records=[]
    element = ""
    for row in contents:
        for element in row:
            if name in element.lower():
                title = row[0]
                description = row[1]
                date = row[2]
                date_format = "%m/%d/%Y"

                summary = str(description) + " on " + str(date)
                records.append(summary)
    temp1 = '. '.join(records)

    speech_output = str(temp1) + " What else do you want to remember?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))


def getLength(intent, session):
    session_attributes = {}
    card_title = "Get info"
    namelookup = intent['slots']['Length']['value'].lower()
    name = str(namelookup)
    today = (time.strftime("%m/%d/%Y"))
    url = 'https://raw.githubusercontent.com/ekt1701/My-Memory/master/myMemory.csv'
    response = urllib2.urlopen(url)
    contents = csv.reader(response)
    records=[]
    element = ""
    for row in contents:
        for element in row:
            if name in element.lower():
                title = row[0]
                description = row[1]
                date = row[2]
                date_format = "%m/%d/%Y"
                a = datetime.strptime(date, date_format)
                b = datetime.strptime(today, date_format)
                delta = abs(b - a)
                numdays = delta.days
                years = numdays/365
                months = (numdays-365*years)/30
                weeks = ((numdays-365*years)-(months*30))/7
                days = (numdays-365*years)-(months*30)-(weeks*7)
                summary = str(description) + " on " + str(date) +". Which is " + str(numdays) + " days from today. Or about " + str(years) + " years " + str(months) + " months " + str(weeks) + " weeks " + str(days) + " days."
                records.append(summary)
    temp1 = '. '.join(records)

    speech_output = str(temp1) + " What else do you want to remember?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def signoff():
    session_attributes = {}
    card_title = "Signing off"
    speech_output = "This is your Memory signing off"
    should_end_session = True
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    should_end_session = True
    speech_output = "Thank you for using My Memory."
    return build_response({}, build_speechlet_response_without_card(
        card_title, speech_output, None, should_end_session))


    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_without_card(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
       'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
def build_response_without_card(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
