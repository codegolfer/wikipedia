"""
bot implementation.
"""
import os
import wikipedia
import ciscospark


# Sets config values from the config file
ACCESS_TOKEN_SPARK = "Bearer " + os.environ['access_token_spark']
MYSELF = os.environ['my_person_id']
BOT_NAME = os.environ['bot_name']


def handler(event, context):
    """
    wikipedia
    """
    print "Event is {0}".format(event)

    try:
        room_id = event['data']['roomId']
        message_id = event['data']['id']
        person_id = event['data']['personId']
        person_email = event['data']['personEmail']
        print "Consumer: {}".format(person_email)
    except KeyError as error:
        print "Duh - key error %r" % error
        return False

    if person_id == MYSELF:
        return False

    message = ciscospark.get_message(ACCESS_TOKEN_SPARK, message_id)
    user_query = message.get('text', "None")
    print "Query: {}".format(user_query)

    if user_query is None:
        return False

    if user_query.lower().startswith(BOT_NAME):
        user_query = user_query[len(BOT_NAME):]

    if user_query.lower().startswith('@{}'.format(BOT_NAME)):
        user_query = user_query[len('@{}'.format(BOT_NAME)):]

    print "Query (final): {}".format(user_query)

    if "help" in user_query.lower():
        print "No trigger word. Returning ..."
        ciscospark.post_message_rich(
            ACCESS_TOKEN_SPARK, room_id, "<blockquote><i>Supported commands: help, or search for any factual information</i></blockquote>")
        return True

    result = wikipedia.summary(user_query)
    ciscospark.post_message_rich(
        ACCESS_TOKEN_SPARK, room_id, "<blockquote><i>{}</i></blockquote>".format(result))
    return True
