from fbchat import  Client, log
from fbchat.models import *
import apiai, codecs, json
import credentials as cred
import pyowm

class Jarvis(Client):

    #apiai method for setting up connection and getting the reply.
    def apiai(self):
        self.ClientAccessToken = 'apiAiClientAccessToken'
        self.ai = apiai.ApiAI(self.ClientAccessToken)
        self.request = self.ai.text_request()
        self.request.lang = 'es'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    
    #modifying pre defined method onMessage, where author_id is the sender id, thread_id is the id of the chatbox or the
    #  thread and thread_type is weather its personal chat or group chat.
    def onMessage(self, author_id=None, message=None,thread_id=None, thread_type=ThreadType.USER, **kwargs):
        #Weather and forecast api
        owm = pyowm.OWM('pyWomKey')
        #marking the message as read
        self.markAsRead(author_id)
        #printing to terminal as a message is received.
        log.info("Message {} from {} in {}".format(message,thread_id,thread_type.name))
        #printing message text
        print("The received message - ",message)
        try:
            #setting up connection with apiai
            self.apiai()
            #sending the query (message received)
            self.request.query = message
            #getting the json response
            api_response = self.request.getresponse()
            json_reply = api_response.read()
            #decoding to utf-8 (converting byte object to json format)
            decoded_data = json_reply.decode("utf-8")
            #loading it into json
            response = json.loads(decoded_data)
            print("El result es: ")
            print(response['result']['parameters'])
            #taking out the reply from json
            if(response['result']['parameters']):
                if(response['result']['parameters']['ciudad'] and response['result']['parameters']['dia'] and response['result']['parameters']['peticion']):
                    observationDestiny = response['result']['parameters']['ciudad'] + ',CO'
                    observation = owm.weather_at_place(observationDestiny)
                    w = observation.get_weather()
                    temp = w.get_temperature('celsius')
                    if(temp['temp']):
                        reply = "La temperatura es "+ str(temp['temp'])
                    else:
                        reply = "Error obteniendo la temperatura"
                else:
                    reply = response['result']['fulfillment']['speech']
            else:
                reply = response['result']['fulfillment']['speech']

        except Exception as e:
            print(e)
            reply = "Intencion no reconocida"

        #if we are not the sender of the message
        if author_id!=self.uid:
            #sending the message.
            self.sendMessage(reply, thread_id = thread_id, thread_type = thread_type)

        self.markAsDelivered(author_id,thread_id)

# Create an object of our class, enter your email and password for facebook.
client = Jarvis(cred.email,cred.password)

# Listen for new message
client.listen()