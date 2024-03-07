from typing import Callable
from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustChannel
import uuid


async def connect_and_get_channel(url: str) -> AbstractRobustChannel:
    connection = await connect_robust(url)
    channel = await connection.channel()
    return channel


async def send_message(url: str, service: str, service_to: str, method: str, body: str) -> str:
    message_id = str(uuid.uuid4())
    message = {
        "service": service,
        "message_id": message_id,
        "method": method,
        "body": body
    }
    channel = await connect_and_get_channel(url)
    await channel.declare_queue(service, auto_delete=True)
    await channel.default_exchange.publish(
        Message(body=str(message).encode()),
        routing_key=service_to
    )
    return message_id


async def send_answer_message(url: str, service: str, service_to: str, body: str) -> str:
    message_id = str(uuid.uuid4())
    message = {
        "service": service,
        "message_id": message_id,
        "body": body
    }
    channel = await connect_and_get_channel(url)
    await channel.declare_queue(service, auto_delete=True)
    await channel.default_exchange.publish(
        Message(body=str(message).encode()),
        routing_key=service_to
    )
    return message_id


async def send_error_message(url: str, service: str, service_to: str, error_message: str) -> str:
    message_id = str(uuid.uuid4())
    message = {
        "service": service,
        "message_id": message_id,
        "error": error_message
    }
    channel = await connect_and_get_channel(url)
    await channel.declare_queue(service, auto_delete=True)
    await channel.default_exchange.publish(
        Message(body=str(message).encode()),
        routing_key=service_to
    )
    return message_id


async def listen_queue(url: str, service_name: str, method: Callable) -> None:
    channel = await connect_and_get_channel(url)
    queue = await channel.declare_queue(service_name, auto_delete=True)
    await queue.consume(method)


async def get_message(url: str, service: str) -> dict:
    channel = await connect_and_get_channel(url)
    queue = await channel.get_queue(service)
    message = await queue.get()
    await queue.delete(if_empty=True)

    return eval(message.body.decode())
