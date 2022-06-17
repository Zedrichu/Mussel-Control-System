from umqtt.robust import MQTTClient
import os
AIO_USERNAME = b'Zedrichu'

# Create the feedName for the client
def makeFeedname(feed):
    return bytes('{:s}/feeds/{:s}'.format(AIO_USERNAME, feed), 'utf-8')
    

class Client (MQTTClient):
    def __init__(self, server, 
                user, password):
        # create a random MQTT clientID 
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
        super(MQTTClient, self).__init__(mqtt_client_id,server = server, user = user, password = password)
        
    # Publish Temperature to Adafruit IO using MQTT
    def publishTemp(self, props):
        temp = props['temperature']
        if not temp == None:
            self.publish(makeFeedname('temperature'),bytes(str(temp),'utf-8'),qos=0)

    # Publish Concentration to Adafruit IO using MQTT
    def publishCon(self, props):
        con = props['concentration']
        if not con == None:
            self.publish(makeFeedname('algae.algae-concentration'),bytes(str(con),'utf-8'),qos=0)
            
    def publishStream(self, status):
        self.publish(makeFeedname('stream'),bytes(status,'utf-8'),qos=0)
    