#Python
# -*- coding: utf-8 -*-
"""
Inherited Client from MQTTClient.

Description: Inherited class defined for abstraction of client controls.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 14/06/2022
@__Version --> 1.0
@__Status --> Prod
"""

from umqtt.robust import MQTTClient
import os
# Definition of the Adafruit IO username used
AIO_USERNAME = b'Zedrichu'

# Create the feedName for the client
def makeFeedname(feed):
    return bytes('{:s}/feeds/{:s}'.format(AIO_USERNAME, feed), 'utf-8')
    

class Client(MQTTClient):
    def __init__(self, server, 
                user, password):
        """
            Client constructor with the server, user and password to be connected to.

            Params:
                server - Adafruit IO hostname 
                user - Adafruit IO username
                password - Adafruit IO password
        """
        # create a random MQTT clientID 
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
        super(MQTTClient, self).__init__(mqtt_client_id,server= server, user= user, password= password)
    
    def publishTemp(self, props):
        """
            Method to publish the temperature measured to the respective Adafruit feed.
        
            Params:
                props - dictionary of system properties
        """
        temp = props['temperature']
        if not temp == None:
            self.publish(makeFeedname('temperature'),bytes(str(temp),'utf-8'),qos=0)

    def publishCon(self, props):
        """
            Method to publish the concentration measured to the respective Adafruit feed.
        
            Params:
                props - dictionary of system properties
        """
        con = props['concentration']
        if not con == None:
            self.publish(makeFeedname('algae.algae-concentration'),bytes(str(con),'utf-8'),qos=0)
  
    def publishStream(self, status):
        """
            Method to publish a text stream message to the respective Adafruit feed.
        
            Params:
                status - message to be sent as stream
        """
        self.publish(makeFeedname('stream'),bytes(status,'utf-8'),qos=0)

    def publishSpeed(self,props):
        """
            Method to publish the speed of the cooling pump to the respective Adafruit feed.
        
            Params:
                props - dictionary of system properties
        """
        speed = props['pumpSpeed']
        self.publish(makeFeedname('cooling-pump'),bytes(str(speed),'utf-8'),qos=0)

    
    