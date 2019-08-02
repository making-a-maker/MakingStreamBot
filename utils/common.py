
# from datetime import datetime
import logging

logger = logging.getLogger()
logger.debug("Hey oh, down here - {}".format(logger.name))


class Message:
    def __init__(self):
        self.channel = ""
        self.command = ""
        self.user = ""
        self.message = ""
        self.badges = ""


def read_message(response):

    msg = parse_message(response)

    if msg.user == "Twitch" and msg.message == "":
        pass
    else:
        logger.info("> @{}: {}".format(msg.user, msg.message))
        logger.debug("Channel: {}  Command: {}  User: {}  Message: {}\nBadges: {}".format(
            msg.channel, msg.command, msg.user, msg.message, msg.badges))

    return msg


def parse_message(response):

    msg = Message()

    # Strip trailer (CR-LF) from response
    response = response.strip("\r\n")

    # Split tags, commands, message
    lines = response.split(":")

    # Badges
    msg.badges = lines[0]
    # parsed_badges = parse_badges(badges)

    # User / host, Command, and Channel
    payload = lines[1].split()

    user_string = payload[0].split("tmi.twitch.tv")
    if user_string[0] == "":
        msg.user = "Twitch"
    else:
        msg.user = user_string[0].split("!")[0]

    msg.command = payload[1]
    msg.channel = payload[2]

    # If there is a message, it's after another ":" character
    msg.message = ""
    if len(lines) > 2:
        msg.message = lines[2]

    return msg


def parse_badges(badges):
    # ToDo: Parse the badge information
    # @badge-info=subscriber/2;badges=moderator/1,subscriber/0;color=;display-name=MakingBot;emote-sets=0,300103696;mod=1;subscriber=1;user-type=mod
    # @badge-info=subscriber/4;badges=broadcaster/1,subscriber/3,premium/1;color=#2297B2;display-name=Making_A_Maker;emotes=;flags=;id=a09e0b47-5660-4e7b-9e9d-201182c7f82c;mod=0;room-id=259533454;subscriber=1;tmi-sent-ts=1564103901474;turbo=0;user-id=259533454;user-type=
    return badges
