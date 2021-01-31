
import datetime
import time
import RPi.GPIO as gpio
import telepot
from telepot.loop import MessageLoop

token = 'Bot access token'				#insert your access token

##start with my chat id so program does not throw an error when starting up
you = 'your id'
chat_id = you

##Other authorized users
ham2 = 'ham2 id'

#list of authorized users
users = [you, ham2]  

LED = 21							#output pin for driving LED
LED_mon = 20						#input pin for monitoring LED

##set up outputs
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(LED, gpio.OUT)			#output pin for driving LED
gpio.output(LED, False) 			#initial state

def on_off(pin):                    #thread that runs on an interupt
    
    if gpio.input(pin):				#if pin is high
	    turn_on_time = datetime.datetime.utcnow()
	    ham_bot.sendMessage(chat_id, str("LED just turned on") + turn_on_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"))
                           
    if not gpio.input(pin):			#if pin is not high
	    turn_off_time = datetime.datetime.utcnow()
	    ham_bot.sendMessage(chat_id, str("LED just turned off") + turn_off_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"))

#setup inputs
gpio.setup(LED_mon, gpio.IN)		#input pin for monitoring LED      


def action(msg):														#code to be executed when a message is received
	global message
	global chat_id
	message = msg['text']												#the text of the message
	chat_id = msg['chat']['id']											#the message sender's id
	now = datetime.datetime.utcnow()
	
	if (chat_id in users):                                  			#check if user is authorized
		print (str(chat_id) + " is an authorized user")
	else:
		print (str(chat_id) + " is not an authorized user") 			#unathorized user
		bot.sendMessage(you, str("Unauthorized user " +str(chat_id) + " attempted access on "\
					 + now.strftime("%B %d, %Y at %H:%M:%S UTC")))      #notify owner
		bot.sendMessage(chat_id, str("You are not allowed access"))
		return          												#boot unathorized user out of function with no actions
	
	if 'on' in message or 'On' in message:								#asked to turn on LED
		ham_bot.sendMessage(chat_id, 'Ham_Bot is turning on LED')
		gpio.output(LED, True)											#turn on LED 
		
	elif 'off' in message or 'Off' in message:							#asked to turn off LED
		ham_bot.sendMessage(chat_id, 'Ham_Bot is turning off LED')
		gpio.output(LED, False)											#turn off LED
		
	elif 'LED' in message and ('Status' in message or 'status' in message):				#asked for LED status
		if gpio.input(LED_mon):											#LED monitor pin is high
			ham_bot.sendMessage(chat_id, 'The LED is on')
		else:															#LED monitor pin is not high
			ham_bot.sendMessage(chat_id, 'The LED is off')
			 
	else:
		ham_bot.sendMessage(chat_id, 'Message not recognized, no action taken')			#command not recognized 
		



ham_bot=telepot.Bot(token)										#set up bot
MessageLoop(ham_bot, action).run_as_thread()                    #monitors for incoming messages

#add interrupt on LED_mon
gpio.add_event_detect(LED_mon, gpio.BOTH, on_off, 100)         	#interupt on both rise and fall, initiate on_off thread, 100 mS debounce
                                                                #add interrupt now so power up does not cause interrupt


while 1:
		print('listening')
		time.sleep(10)

