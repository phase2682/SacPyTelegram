
import datetime
import time
import telepot
from telepot.loop import MessageLoop

def action(msg):											#code to be executed when a message is received
	global message
	global chat_id
	message = msg['text']									#the text of the message
	chat_id = msg['chat']['id']								#the message sender's id
	now = datetime.datetime.utcnow()
	
	if 'cq' in message or 'CQ' in message:
		ham_bot.sendMessage(chat_id, str(chat_id) +' de AI6XG')
	else:
		ham_bot.sendMessage(chat_id, 'tu fer ur message 73')
	if message == '/time':
		ham_bot.sendMessage(chat_id, str('Time: ') + now.strftime("%H:%M:%S UTC"))
	if 'date' in message or 'Date' in message:
	    ham_bot.sendMessage(chat_id, str('Date: ') + now.strftime ("%B %d, %Y UTC"))


token = 'Bot access token'									#insert your access token

ham_bot=telepot.Bot(token)									#set up bot
MessageLoop(ham_bot, action).run_as_thread()				#monitors for incoming messages                       


while 1:
		print('listening')
		time.sleep(10)

