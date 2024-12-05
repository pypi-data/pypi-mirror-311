import json
import pika
import logging
from typing import Callable, Dict, Any
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

logger = logging.getLogger(__name__)

class RabbitMQHandler:
    def __init__(self, host: str, port: int, user: str, password: str, vhost: str, heartbeat: int, retry_limit: int, ttl: int):
        self.credentials = pika.PlainCredentials(user, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=self.credentials,
            heartbeat=heartbeat
        )

        self.retry_limit = retry_limit
        self.ttl = ttl

    def setup_queues(self, queue_mappings: Dict[str, str], dlx_exchange: str = 'dlx_exchange'):
        # Declare DLX
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=dlx_exchange, exchange_type='direct', durable=True)

        # Declare DLQs with TTL
        for primary_queue, dlq in queue_mappings.items():
            try:
                channel.queue_declare(queue=dlq, durable=True, arguments={
                    'x-message-ttl': self.ttl,
                    'x-dead-letter-exchange': '',
                    'x-dead-letter-routing-key': primary_queue
                })
            except pika.exceptions.ChannelClosedByBroker as e:
                if e.reply_code == 406:
                    logger.warning(f"Queue {dlq} already exists with different arguments. Skipping re-declaration.")
                    channel = connection.channel()  # Reopen the channel after it was closed
                else:
                    raise e
            channel.queue_bind(exchange=dlx_exchange, queue=dlq, routing_key=dlq)

        # Declare primary queues with DLX
        for primary_queue, dlq in queue_mappings.items():
            try:
                channel.queue_declare(queue=primary_queue, durable=True, arguments={
                    'x-dead-letter-exchange': dlx_exchange,
                    'x-dead-letter-routing-key': dlq
                })
            except pika.exceptions.ChannelClosedByBroker as e:
                if e.reply_code == 406:
                    logger.warning(f"Queue {primary_queue} already exists with different arguments. Skipping re-declaration.")
                    channel = connection.channel()  # Reopen the channel after it was closed
                else:
                    raise e

    def publish_message(self, queue_name: str, message: Dict[str, Any], headers: Dict[str, Any] = {}):
        try:
            connection = pika.BlockingConnection(self.parameters)
            channel = connection.channel()
            json_message = json.dumps(message)
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json_message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    headers=headers
                )
            )
            logger.info(f"Sent message to '{queue_name}' queue: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to '{queue_name}' queue: {e}")

    def is_malformed_message(self, body: bytes):
        try:
            message = json.loads(body)
            return False, message
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return True, None

    def handle_retry(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, message: bytes, callback: Callable, queue_name: str) -> None:
        headers = properties.headers or {}
        logger.info(headers)
        x_death = headers.get('x-death', [])
        retry_count = x_death[0]['count'] if x_death else 0
        logger.info(f"Received message: {message}. Retry count: {retry_count}")

        if retry_count >= self.retry_limit:
            logger.error(f"Retry limit exceeded for message: {message}. Acknowledging and discarding.")
            if channel.is_open:
                channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            try:
                is_malformed, parsed_message = self.is_malformed_message(message)
                print(parsed_message)
                if is_malformed:
                    if channel.is_open:
                        logger.error(f"Malformed message detected: {message}. Sending to DLQ.")
                        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return
                callback(channel, method, properties, json.dumps(parsed_message))
                if channel.is_open:
                    channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}. Retrying {retry_count + 1}/{self.retry_limit}.")
                if channel.is_open:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)