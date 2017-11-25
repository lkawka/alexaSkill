from __future__ import print_function

def getListOfNeeds():
    listOfNeeds = ["Toilet Paper", "Old Spice Shower Gel", "Gillete razer"]
    return listOfNeeds

def getUpcomingNeeds():
    upcomingNeeds = ["Pampers"]
    return upcoming

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Welcome"
    
    listOfNeeds = getListOfNeeds()
    
    speech_output = "Hello, it's P and G Assistant"
    
    if not listOfNeeds:
        speech_output = speech_output + ", you are all good"
    else:
        speech_output = speech_output + ", I thing that right about now you should be running out of : " + ", ".join(listOfNeeds)+". Do you want me to order anything?"
    
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
                                                                       card_title, speech_output, reprompt_text, should_end_session))

def repeatList(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    reprompt_text = None
    
    speech_output = "Sure, "
    
    listOfNeeds = getListOfNeeds()
    
    if not listOfNeeds:
        speech_output = speech_output + "I don't think you are in need of anything"
    else:
        speech_output = speech_output + "here is what I think you should get: " + ", ".join(listOfNeeds)
    
    return build_response(session_attributes, build_speechlet_response(
                                                                       card_title, speech_output, reprompt_text, should_end_session))

def orderAll(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    reprompt_text = None
    
    speech_output = "Okey, I'm ordering everything"
    
    return build_response(session_attributes, build_speechlet_response(
                                                                       card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying P and G Assistant. " \
        "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
                                                                       card_title, speech_output, reprompt_text, should_end_session))

def selectedOrder(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    reprompt_text = None
    
    speech_output = "I am sorry but we don't have this product"
    if 'product' in intent['slots']:
        session_attributes = {"product": intent['slots']['product']['value']}
        speech_output = "No problem, I'm ordering " + intent['slots']['product']['value']
    
    return build_response(session_attributes, build_speechlet_response(
                                                                       card_title, speech_output, reprompt_text, should_end_session))

def orderExcept(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    reprompt_text = None
    
    speech_output = "Sorry, I don't know of which product you are talking about"
    if 'product' in intent['slots']:
        session_attributes = {"product": intent['slots']['product']['value']}
        speech_output = "Okey, I am ordering all except for " + intent['slots']['product']['value']


# --------------- Events ------------------

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
          if intent_name == "repeatList":
              return repeatList(intent, session)
          elif intent_name == "orderAll":
              return orderAll(intent, session)
                  elif intent_name == "selectedOrder":
                      return selectedOrder(intent, session)
                          elif intent_name == "orderExcept":
                              return orderExcept(intent, session)
                                  elif intent_name == "AMAZON.HelpIntent":
                                      return get_welcome_response()
                                          elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
                                              return handle_session_end_request()
                                                  else:
                                                      raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
        
        Is not called when the skill returns should_end_session=true
        """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
# add cleanup logic here


# --------------- Main handler ------------------

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

