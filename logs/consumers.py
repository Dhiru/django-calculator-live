import json
from channels import Group
from .models import Calculator


# The "slug" keyword argument here comes from the regex capture group in
# routing.py.
def connect_log(message, slug):
    """
    When the user opens a WebSocket to a calculator stream, adds them to the
    group for that stream so they receive new log notifications.

    The notifications are actually sent in the Log model on save.
    """
    # Try to fetch the calculator by slug; if that fails, close the socket.
    try:
        calculator = Calculator.objects.get(slug=slug)
    except Calculator.DoesNotExist:
        # You can see what messages back to a WebSocket look like in the spec:
        # http://channels.readthedocs.org/en/latest/asgi.html#send-close
        # Here, we send "close" to make Daphne close off the socket, and some
        # error text for the client.
        message.reply_channel.send({
            # WebSockets send either a text or binary payload each frame.
            # We do JSON over the text portion.
            "text": json.dumps({"error": "bad_slug"}),
            "close": True,
        })
        return
    # Each different client has a different "reply_channel", which is how you
    # send information back to them. We can add all the different reply channels
    # to a single Group, and then when we send to the group, they'll all get the
    # same message.
    Group(calculator.group_name).add(message.reply_channel)


def disconnect_log(message, slug):
    """
    Removes the user from the calculator group when they disconnect.

    Channels will auto-cleanup eventually, but it can take a while, and having old
    entries cluttering up your group will reduce performance.
    """
    try:
        calculator = Calculator.objects.get(slug=slug)
    except Calculator.DoesNotExist:
        # This is the disconnect message, so the socket is already gone; we can't
        # send an error back. Instead, we just return from the consumer.
        return
    # It's called .discard() because if the reply channel is already there it
    # won't fail - just like the set() type.
    Group(calculator.group_name).discard(message.reply_channel)
