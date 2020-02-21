
# from datetime import datetime
import logging

logger = logging.getLogger()


class Message:
    def __init__(self):
        self.channel = ""
        self.irc_command = ""
        self.user = ""
        self.message = ""
        self.badges = ""


def read_message(response):

    msg = parse_message(response)

    # Don't log the reply messages from Twitch
    if msg.user == "Twitch" and msg.message == "":
        pass
    else:
        logger.info("> @{}: {}".format(msg.user, msg.message))
        logger.debug("Channel: {}  IRC Command: {}  User: {}  Message: {}\nBadges: {}".format(
            msg.channel, msg.irc_command, msg.user, msg.message, msg.badges))

    return msg


def parse_message(response):

    msg = Message()

    # Strip trailer (CR-LF) from response
    response = response.strip("\r\n")

    # Split on whitespace -> badges, user/channel payload, command, channel, and message
    lines = response.split(" ", 4)

    msg.badges = lines[0]
    payload = lines[1]
    msg.irc_command = lines[2]
    msg.channel = lines[3]

    # ToDo: Add some stuff to parse the badges
    # parsed_badges = parse_badges(badges)

    # Sample payload for user messages:
    # :makingtest!makingtest@makingtest.tmi.twitch.tv

    user_string = payload.split("tmi.twitch.tv")
    if user_string[0] == ":":
        msg.user = "Twitch"
    else:
        # The first list item after splitting on twitch.tv, split on "!",
        # take the first item from that, and then remove the first character
        msg.user = user_string[0].split("!")[0][1:]

    # Strip the first character (:)
    if len(lines) > 4:
        msg.message = lines[4][1:]

    return msg


def parse_badges(badges):
    # ToDo: Parse the badge information
    # @badge-info=subscriber/2;badges=moderator/1,subscriber/0;color=;display-name=MakingBot;emote-sets=0,300103696;mod=1;subscriber=1;user-type=mod
    # @badge-info=subscriber/4;badges=broadcaster/1,subscriber/3,premium/1;color=#2297B2;display-name=Making_A_Maker;emotes=;flags=;id=a09e0b47-5660-4e7b-9e9d-201182c7f82c;mod=0;room-id=259533454;subscriber=1;tmi-sent-ts=1564103901474;turbo=0;user-id=259533454;user-type=
    return badges
