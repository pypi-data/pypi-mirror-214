from .deps import BadRequest


class NoSendTextRights(BadRequest):
    match = "Not enough rights to send text messages to the chat"


class NoSendPhotoRights(BadRequest):
    match = "Not enough rights to send photos to the chat"
