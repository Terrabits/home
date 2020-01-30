from   aiohttp  import web
import argparse
from   home.app import create_notifications_handler, create_publish_handler, redirect_to_index


def main():
    parser = argparse.ArgumentParser(description='Start home server')
    parser.add_argument('mqtt_broker_address')
    args   = parser.parse_args()

    app = web.Application()
    app.add_routes([web.get('/',              redirect_to_index),
                    web.get('/notifications', create_notifications_handler(args.mqtt_broker_address)),
                    web.get('/publish',       create_publish_handler(args.mqtt_broker_address)),
                    web.static('/',           'site/')])
    web.run_app(app)


if __name__ == '__main__':
    main()
