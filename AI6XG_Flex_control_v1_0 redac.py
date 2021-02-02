
###This script uses telegram bot to control the Flex radio at AI6XG
#The remote on feature is used to turn on and off the Flex radio
#usb port of the flex is monitored to determine status, 5V when Flex turns on
#Both the remote on and usb ports are connected through opto isolators for
#isolation and for voltage translation between Rpi and the Flex

#Dan Koellen AI6XG  March 2019



token = 'bot token'

import telepot
from telepot.loop import MessageLoop

import datetime
from time import sleep
import RPi.GPIO as gpio

##start with my chat id so program does not throw an error when starting up
dan = 999999999
chat_id = dan

##Other authorized users
di = 123456789

#list of authorized users
users = [dan, di]                   

turn_on_pin = 21                #pin turns on flex thru opto isolator
flex_usb = 16                   #pin that monitors the Flex USB port thru opto isolator

Flex_is_on = 7                 #pin is high when flex is on
Flex_is_off = 12                #pin is high when Flex is off

SDA_1 = 14                      #SDA Control pin
SDA_2 = 15                      #SDA Control pin

startup = datetime.datetime.utcnow()           #time at power up
turn_on_time = startup        #time that flex turns on, initiate at startup
turn_off_time = startup       #time that flex turns off, initiate at startup

loop = 0                        #counts sleep loops
red_led = 0                     #red LED status
green_led = 0                   #green LED status

bot_status = 0                  #status sent by bot, 1 is on 0 is off

##set up outputs
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(turn_on_pin, gpio.OUT)
gpio.output(turn_on_pin, False)         #at start up there will be an open at the Flex(remote on)
                                        #if the radio was turned on by Flex(remote on) it will turn off
                                        #if the radio was turned on with the front switch a 'flex on' command
                                        #will have to been sent to enable remote turn off

gpio.setup(Flex_is_on, gpio.OUT)
gpio.output(Flex_is_on, False)

gpio.setup(Flex_is_off, gpio.OUT)
gpio.output(Flex_is_off, False)

gpio.setup(SDA_1, gpio.OUT)
gpio.output(SDA_1, False)

gpio.setup(SDA_2, gpio.OUT)
gpio.output(SDA_2, False)

def on_off(pin):                    #thread that runs on an interupt on flex_usb
    global turn_off_time
    global turn_on_time
    global startup
    if gpio.input(pin):
        turn_off_time = datetime.datetime.utcnow()
        diff = turn_off_time - startup
        if diff.seconds < 10:
            return
        bot.sendMessage(dan, str("AI6XG Flex just turned off") + turn_off_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"))
        if bot_status:
            bot.sendMessage(chat_id, str("The bot did not turn off AI6XG Flex"))
                           
    if not gpio.input(pin):
        turn_on_time = datetime.datetime.utcnow()
        diff = turn_on_time - startup
        if diff.seconds < 10:
            return
        bot.sendMessage(dan, str("AI6XG Flex just turned on") + turn_on_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"))
        if not bot_status:
            bot.sendMessage(chat_id, str("The bot did not turn on AI6XG Flex"))

#setup inputs
gpio.setup(flex_usb, gpio.IN, pull_up_down = gpio.PUD_UP)       #pullup is active



#setup bot
bot = telepot.Bot(token)
print(bot.getMe())

bot_status = not gpio.input(flex_usb)                  #inital bot_status is set by flex_usb at start up
print("The initial flex_usb status is " + str(bot_status))
if bot_status:
    bot.sendMessage(dan, str("AI6XG Flex was on when the controller powered up on " + startup.strftime("%B %d, %Y at %H:%M:%S UTC")))
else:
    bot.sendMessage(dan, str("AI6XG Flex was off when the controller powered up on " + startup.strftime("%B %d, %Y at %H:%M:%S UTC")))

#add interrupt on flex_usb
gpio.add_event_detect(flex_usb, gpio.BOTH, on_off, 100)         #interupt on both rise and fall, initiate on_off thread, 100 mS debounce
                                                                #add interrupt now so power up does not cause interrupt


def handle2(msg):                   #handler that runs when a message is received
    global chat_id
    global bot_status
    global startup
    now=datetime.datetime.utcnow()
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Received ' + command + " command from " + str(chat_id) + " on " + now.strftime("%B %d, %Y at %H:%M:%S UTC") )

    if (chat_id in users):                                  #check if user is authorized
        print (str(chat_id) + " is an authorized user")
    else:
        print (str(chat_id) + " is not an authorized user") #unathorized user
        bot.sendMessage(dan, str("Unauthorized user " +str(chat_id) + " attempted access on "\
                                 + now.strftime("%B %d, %Y at %H:%M:%S UTC")))      #notify dan
        bot.sendMessage(chat_id, str("You are not allowed access. Don't go away mad, just go away!"))
        return          #get out of function with no actions
    
    if chat_id != dan:              #dan rcvs message if another user sends a message
        bot.sendMessage(dan, str("Received " + command + " command from " + str(chat_id) + " on " + \
                                 now.strftime("%B %d, %Y at %H:%M:%S UTC") ))
        

    if 'cq' in command or 'CQ' in command:
        bot.sendMessage(chat_id, str("CQ " + str(chat_id) + " de AI6XG"))
        
    if 'time' in command or 'Time' in command:
        bot.sendMessage(chat_id, str('Time: ') + now.strftime("%H:%M:%S UTC"))
        
    if 'date' in command or 'Date' in command:
        bot.sendMessage(chat_id, str('Date: ') + now.strftime ("%B %d, %Y UTC"))
        
    if 'Flex' in command or 'flex' in command:                  #start of commands that affect the Flex radio
        
        if 'on' in command or 'On' in command:                  #turns on Flex by driving Flex(remote on) low thru opto isolator
            bot.sendMessage(chat_id, str("AI6XG Flex is turning on"))
            gpio.output(turn_on_pin, True)
            if gpio.input(flex_usb):
                bot_status = 1
            
        elif 'off' in command or 'Off' in command:              #turns off Flex by clearing Flex(remote on) thru opto isolator
            bot.sendMessage(chat_id, str("AI6XG Flex is turning off"))
            gpio.output(turn_on_pin, False)
            if not gpio.input(flex_usb):
                bot_status = 0
                                
        if 'status' in command or 'Status' in command:          #commands to check the status of Flex by monitoring flex_usb
            
            if gpio.input(flex_usb):                            #flex is off when opto isolator output is off/open, GPIO pulled up
                if startup == turn_off_time:
                    bot.sendMessage(chat_id, str("AI6XG Flex was off when the controller powered up ") + turn_off_time.strftime("at %H:%M:%S on %B %d, %Y UTC"))
                else:
                    bot.sendMessage(chat_id, str("AI6XG Flex turned off ") + turn_off_time.strftime("at %H:%M:%S on %B %d, %Y UTC"))
                diff = now - turn_off_time
                hrs = diff.seconds//3600
                mins = (diff.seconds - hrs * 3600)//60
                secs = (diff.seconds - hrs * 3600)%60
                if startup == turn_off_time:
                    bot.sendMessage(chat_id, str("AI6XG Flex has been off for at least {0} days, {1} hours, {2} minutes and {3} seconds".format(diff.days, hrs, mins, secs)))
                    return
                else:
                    bot.sendMessage(chat_id, str("AI6XG Flex has been off for {0} days, {1} hours, {2} minutes and {3} seconds".format(diff.days, hrs, mins, secs)))
                if bot_status:
                    bot.sendMessage(chat_id, str("The bot did not turn off AI6XG Flex"))
                else:
                    bot.sendMessage(chat_id, str("AI6XG Flex was turned off by the bot"))
                
            if gpio.input(flex_usb) == False:                   #flex is on when opto isolator output is on, GPIO pulled low
                if startup == turn_on_time:
                    bot.sendMessage(chat_id, str("AI6XG Flex was on when the controller powered up ") + turn_on_time.strftime("at %H:%M:%S on %B %d, %Y UTC"))
                else:
                    bot.sendMessage(chat_id, str("AI6XG Flex turned on ")+ turn_on_time.strftime("at %H:%M:%S on %B %d, %Y"))
                diff = now - turn_on_time
                hrs = diff.seconds//3600
                mins = (diff.seconds - hrs * 3600)//60
                secs = (diff.seconds - hrs * 3600)%60
                if startup == turn_on_time:
                    bot.sendMessage(chat_id, str("AI6XG Flex has been on for at least {0} days, {1} hours, {2} minutes and {3} seconds".format(diff.days, hrs, mins, secs)))
                    return
                else:
                    bot.sendMessage(chat_id, str("AI6XG Flex has been on for {0} days, {1} hours, {2} minutes and {3} seconds".format(diff.days, hrs, mins, secs)))
                if bot_status:
                    bot.sendMessage(chat_id, str("AI6XG Flex was turned on by the bot"))
                else:
                    bot.sendMessage(chat_id, str("The bot did not turn on AI6XG Flex"))

    if command == '/help':
        bot.sendMessage(chat_id, str('Send the following to interact with AI6XG Flex ==>\nCQ or cq for a welcome message\n\
Time or time for current time\nDate or date for current date\nFlex or flex plus the following:\nStatus or status for current status\n\
On or on to turn AI6XG Flex on\nOff or off to turn AI6XG Flex off'))

MessageLoop(bot, handle2).run_as_thread()                       #monitors for incoming messages

try:

    while 1:

        sleep(1) 
        if loop == 0:                           #check status every tenth 1 second loop
            loop = 10
            if (gpio.input(flex_usb) and (not bot_status)):            #flex_usb is off
                gpio.output(Flex_is_on,False)
                gpio.output(Flex_is_off,True)   #Red LED
                red_led = 1; green_led = 0

            elif ((not gpio.input(flex_usb)) and (bot_status)):         #flex_usb is on
                gpio.output(Flex_is_off,False)
                gpio.output(Flex_is_on,True)    #Green LED
                green_led= 1;red_led = 0

        if (not gpio.input(flex_usb) and (not bot_status)):     #flex_usb is on but bot_status is off, flash green LED
            if green_led == 0:
                gpio.output(Flex_is_off,False)
                gpio.output(Flex_is_on,True)                        #Green LED
                green_led = 1; red_led = 0;
            else:
                gpio.output(Flex_is_off,False)
                gpio.output(Flex_is_on,False)                        #Green LED
                green_led = 0; red_led = 0;

        if (gpio.input(flex_usb) and (bot_status)):            #flex_usb is off but bot_status is on, flash red LED
            if red_led == 0:
                gpio.output(Flex_is_off,True)                       #Red LED
                gpio.output(Flex_is_on,False)                       #Green LED
                green_led = 0; red_led = 1;
            else:
                gpio.output(Flex_is_off,False)                      #Red LED
                gpio.output(Flex_is_on,False)                       #Green LED
                green_led = 0; red_led = 0;
        
        loop -= 1



except:
    print()
    print("Program terminated")
    gpio.cleanup(Flex_is_on)
    gpio.cleanup(Flex_is_off)
    

