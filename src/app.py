import os
import sys
import traceback
import json
import paho.mqtt.client as mqtt

class App():
    '''
    This sample application subscribes to data on an MQTT data topic,
    scales that data by 1000, and publishes the data to back to the broker under a new tag.

    Attributes:
        predix_edge_broker - the name of the predix edge broker as defined
                            in our docker-compose file
        topic - either a string or a list of strings indicating which topic(s) to subsrcibe to
        tag_name - string indicating the tag of the data we want to modify
        client - manages relationship with MQTT data broker
    '''

    def __init__(self, predix_edge_broker, sub_topic, pub_topic,
                 tag_name):
        '''
        Initializes App class with default names for predix_edge_broker,
        a single topic called 'app_data', and a sample tag to look for
        '''
        self.predix_edge_broker = predix_edge_broker
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic
        self.tag_name = tag_name
        self.client = mqtt.Client()

        #add MQTT callbacks and enable logging for easier debugging
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.message_callback_add(self.sub_topic, self.scalar_on_message)
        self.client.enable_logger()

    def on_connect(self, client, userdata, flags, rc):
        '''
        The callback for when the client receives a CONNACK response from the server.
        The variables it takes are part of the underlying MQTT library
        '''
        print("Connected with result code "+str(rc))
        client.subscribe(self.sub_topic)

    def on_message(self, client, userdata, msg):
        '''
        The callback for when a PUBLISH message is received from the server.
        '''
        print(msg.pub_topic+" "+str(msg.payload))

    def on_publish(self, client, userdata, is_published):
        '''
        the callback for when we send something to be published
        '''
        print("Is published " + str(is_published))


    def scalar_on_message(self, client, userdata, msg):
        '''
        Specific callback for our topic
        '''
        #Convert message from bytearray to json object
        payload_as_string = bytes.decode(msg.payload)
        payload = json.loads(payload_as_string)

        scaled_payload = scale_data(payload, self.tag_name)

        payload_as_string = json.dumps(scaled_payload)
        client.publish(self.pub_topic, payload_as_string.encode())

def scale_data(message, tag_to_match):
    '''
    This function takes in a JSON message and goes through the body of it
    If an item in the body has the tag we are looking to scale, it scales it and updates the tag name
    '''
    item = message['body']
    length = len(item)
    for i in range(length):
        #if item[i]['name'] == tag_to_match:
        value = item[i]['datapoints'][0][1]
        value = value * 1000
        # item[0]['datapoints'][0][1] = value
        # item[0]['name'] = self.tag_name + '.scaled_x_1000' #publish with a new tagname
        #
        # #convert message back to bytearray for publishing
        # payload_as_string = json.dumps(payload)
        # client.publish(self.topic, payload_as_string.encode())
        item[i]['datapoints'][0][1] = value
        item[i]['name'] =  item[i]['name'] + '.scaled_x_1000' #publish with a new tagname


    return message

if __name__ == '__main__':
    #Set broker values if we are running locally
    if len(sys.argv) > 1:
        if sys.argv[1] == "local":
            BROKER = "127.0.0.1"
            SUB_TOPIC = "app_data"
            PUB_TOPIC = "timeseries_data"
            TAG_NAME = "My.App.DOUBLE1"
    #Otherwise, read from environment variables
    else:
        try:
            BROKER = os.environ['BROKER']
            SUB_TOPIC = os.environ['SUB_TOPIC']
            PUB_TOPIC = os.environ['PUB_TOPIC']
            TAG_NAME = os.environ['TAG_NAME']
        except KeyError:
            print(traceback.print_tb(sys.exc_info()[2]))
            sys.exit("Not all of your environment variables are set")
    APP = App(BROKER, SUB_TOPIC, PUB_TOPIC, TAG_NAME)
    APP.client.connect(APP.predix_edge_broker)
    APP.client.loop_forever()
