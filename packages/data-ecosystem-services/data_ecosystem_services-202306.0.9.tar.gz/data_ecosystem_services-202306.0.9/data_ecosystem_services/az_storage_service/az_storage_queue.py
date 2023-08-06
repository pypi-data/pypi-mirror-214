from azure.storage.queue import QueueClient
from azure.identity import ClientSecretCredential

class AzureStorageQueue:
    def __init__(self, connection_string, queue_name, tenant_id, client_id, client_secret):

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        self.queue_service = QueueClient.from_connection_string(connection_string, queue_name)
        self.queue_name = queue_name
        self.queue_service.create_queue()

    def enqueue_task(self, message):
        self.queue_service.send_message(message)

    def dequeue_task(self):
        messages = self.queue_service.receive_messages(num_messages=1)
        if messages:
            message = messages[0]
            return message.content, message.id, message.pop_receipt
        return None

    def delete_task(self, message_id, pop_receipt):
        self.queue_service.delete_message( message_id, pop_receipt)
