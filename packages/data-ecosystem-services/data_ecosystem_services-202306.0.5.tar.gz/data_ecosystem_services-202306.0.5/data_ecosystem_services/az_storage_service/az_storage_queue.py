from azure.storage.queue import QueueService

class AzureStorageQueue:
    def __init__(self, connection_string, queue_name):
        self.queue_service = QueueService(connection_string=connection_string)
        self.queue_name = queue_name
        self.queue_service.create_queue(queue_name)

    def enqueue_task(self, message):
        self.queue_service.put_message(self.queue_name, message)

    def dequeue_task(self):
        messages = self.queue_service.get_messages(self.queue_name, num_messages=1)
        if messages:
            message = messages[0]
            return message.content, message.id, message.pop_receipt
        return None

    def delete_task(self, message_id, pop_receipt):
        self.queue_service.delete_message(self.queue_name, message_id, pop_receipt)
