import os

import modal

stub = modal.Stub(image=modal.Image.debian_slim().pip_install("slack-sdk"))


@stub.function(secret=modal.Secret.from_name("my-slack-secret"))
def bot_token_msg(channel, message):
    import slack_sdk

    client = slack_sdk.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    # client.chat_postMessage(channel=channel, text=message)
    # client.chat_delete(channel=channel, )
    client.search_messages(query="everyone!")


@stub.local_entrypoint()
def main():
    # This writes "hello" to the #integration-app-test channel
    # If your bot is not in this channel (or the channel does not exist),
    # it will get an error such as {'ok': False, 'error': 'not_in_channel'}
    bot_token_msg.remote("#team-formation", "hi everyone!")
