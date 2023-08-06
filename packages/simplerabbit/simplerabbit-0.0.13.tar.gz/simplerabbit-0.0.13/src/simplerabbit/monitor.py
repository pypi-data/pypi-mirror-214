import requests
import json

class RabbitMonitor:

    def __init__(self, host, port, username, password, ca_file, client_cert, client_key):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ca_file = ca_file
        self.client_cert = client_cert
        self.client_key = client_key

    def get_queue_publish_rate(self, queue_name, vhost):
        data = self._get_queue_info(queue_name, vhost)
        if 'message_stats' in data:
            return data["message_stats"]["publish_details"]["rate"]
        else:
            return 0

    def get_queue_total_messages(self, queue_name, vhost):
        data = self._get_queue_info(queue_name, vhost)
        ready_message_no = 0
        unack_message_no = 0
        if 'messages_ready' in data:
            ready_message_no = data["messages_ready"]
        if 'messages_unacknowledged' in data:
            unack_message_no = data["messages_unacknowledged"]
        return ready_message_no + unack_message_no

    def _get_queue_info(self, queue_name, vhost):
        url = 'https://{}:{}/api/queues/{}/{}'.format(self.host, self.port, vhost, queue_name)
        auth = (self.username, self.password)
        cert = (self.client_cert, self.client_key)
        ca_file = self.ca_file

        response = requests.get(url, auth=auth, cert=cert, verify=ca_file)
        return json.loads(response.text)