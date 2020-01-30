from aiohttp          import web, WSMsgType
from paho.mqtt.client import Client


def parse(data):
    first_space = data.find(' ')
    if first_space == -1:
        return data, ''
    topic       = data[:first_space]
    message     = data[first_space + 1:]
    return topic, message


def publish(broker, topic, message):
    print(f"publishing {topic}: '{message}'")
    client = Client()
    client.connect(broker)
    client.publish(topic, message)
    client.disconnect()


def create_publish_handler(broker):
    async def publish_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                publish(broker, *parse(msg.data))
            elif msg.type == WSMsgType.ERROR:
                print(f'publish websocket closed with exception {ws.exception()}')
            else:
                raise web.HTTPForbidden()
    return publish_handler
