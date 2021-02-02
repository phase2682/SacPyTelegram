
import time
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def action(update, context):
	global message
	global chat_id
	message = update.message.text
	chat_id = update.effective_chat.id
	now = datetime.datetime.utcnow()
	
	print('sender id is: ' + str(chat_id))
	print('The message is: '+ str(message))


token = 'bot token'

print()

updater_sacpy = Updater(token)				#gets updates from the bot
dispatcher_sacpy = updater_sacpy.dispatcher				#dispatches the updates
updater_sacpy.start_polling()						#starts the bot

#handler for messages	
msg_handler = MessageHandler(Filters.text & (~Filters.command), action)
dispatcher_sacpy.add_handler(msg_handler)			#adds msg handler 


while 1:
		print('listening')
		time.sleep(30)

