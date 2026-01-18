import requests

class SlackUtil:

    @staticmethod
    def send_message(webhook_url, message):
        payload = {"text": message}
        requests.post(webhook_url, json=payload)
