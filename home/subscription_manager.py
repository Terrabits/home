from paho.mqtt.client import Client


class SubscriptionManager:
    def __init__(self, broker_address, broker_port=1883):
        self.broker_address      = broker_address
        self.broker_port         = broker_port
        self.callbacks_for_topic = {}

    def __del__(self):
        self.stop()

    @property
    def connected(self):
        if not getattr(self, 'broker'):
            return False
        return self.broker.is_connected()

    # callback(message=b'')
    def register_notification(self, topic, callback):
        if topic not in self.callbacks_for_topic:
            self.callbacks_for_topic[topic] = [callback]
            self._subscribe_to_topic(topic)
        else:
            self.callbacks_for_topic[topic].append(callback)

    def stop_notifications_for(self, callback):
        for topic, callbacks in self.callbacks_for_topic.items():
            while callback in callbacks:
                callbacks.remove(callback)
            if callbacks:
                self.callbacks_for_topic[topic] = callbacks
            else:
                self._unsubscribe_from_topic(topic)
                del(self.callbacks_for_topic[topic])

    def notify(self, topic, message=b''):
        if topic not in self.callbacks_for_topic:
            return
        for callback in self.callbacks_for_topic[topic]:
            callback(message)

    # broker thread
    def start(self):
        self.return_code          = None
        self.broker               = Client()
        self.broker.on_disconnect = self._on_disconnect
        self.broker.connect(self.broker_address, self.broker_port)
        return self.broker.loop_start()

    def stop(self):
        if not self.broker:
            return
        self.broker.disconnect()
        return_value = self.broker.loop_stop()
        self.broker  = None
        return return_value

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    # mqtt broker connect/disconnect
    def _on_disconnect(self, client, userdata, rc):
        self.return_code = rc

    # mqtt broker subscriptions
    def _subscribe_to_topic(self, topic):
        callback = self._generate_callback_for(topic)
        self.broker.message_callback_add(topic, callback)
        self.broker.subscribe(topic)

    def _unsubscribe_from_topic(self, topic):
        self.broker.unsubscribe(topic)
        self.broker.message_callback_remove(topic)

    def _generate_callback_for(self, topic):
        def callback(client, userdata, message):
            self.notify(topic, message.payload)
        return callback
