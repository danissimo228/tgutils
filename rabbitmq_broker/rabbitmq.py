from typing import Callable
import aio_pika


async def send_message(url: str, service: str, service_to: str, method: str, body: str) -> None:
    message = {
        "service": service,
        "method": method,
        "body": body
    }
    connection = await aio_pika.connect_robust(url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(service, auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(message).encode()),
            routing_key=service_to
        )


async def send_error_message(url: str, service: str, service_to: str, error_message: str) -> None:
    message = {
        "service": service,
        "error": error_message
    }
    connection = await aio_pika.connect_robust(url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(service, auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(message).encode()),
            routing_key=service_to
        )


async def listen_queue(url: str, service_name: str, method: Callable) -> None:
    connection = await aio_pika.connect_robust(url)
    channel = await connection.channel()
    queue = await channel.declare_queue(service_name, auto_delete=True)
    await queue.consume(method)