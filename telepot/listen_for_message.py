
import time
import telepot
from telepot.loop import MessageLoop

def action(msg):												#code to be executed when a message is received
	print('sender id is: ' + str(msg['chat']['id']))			#the message sender's id
	print('The message is: '+ str(msg['text']))


token = 'Bot access token'										#insert your access token

print()

ham_bot=telepot.Bot(token)										#set up bot
MessageLoop(ham_bot, action).run_as_thread()             		#monitors for incoming messages


while 1:
		print('listening')
		time.sleep(10)



