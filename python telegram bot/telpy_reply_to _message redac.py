
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import datetime
from time import sleep
import requests
import re


token = 'bot token'

def action(update, context):
	global message
	global chat_id
	message = update.message.text
	chat_id = update.effective_chat.id
	now = datetime.datetime.utcnow()
	
#	print('sender id is: ' + str(chat_id))
#	print('The message is: '+ str(message))
#	print ('sending a reply')
	if 'cq' in message or 'CQ' in message:
		context.bot.send_message(chat_id, str(chat_id) +' de AI6XG')
	elif 'date' in message or 'Date' in message:
	    context.bot.send_message(chat_id, str('Date: ') + now.strftime ("%B %d, %Y UTC"))
	else:
		# context.bot.sendMessage(chat_id, 'tu fer ur message 73')
		update.message.reply_text('tu fer ur message 73')
		
	
#action to take with a /time command
def time(update, context):	
	now = datetime.datetime.utcnow()		
	context.bot.send_message(update.effective_chat.id, str('Time: ') + now.strftime("%H:%M:%S UTC"))

#action to take with an unknown command
def unknown(update, context):			
	context.bot.send_message(chat_id=update.effective_chat.id, text= 'Command not recognized, no action taken')

def get_url():
	contents = requests.get('https://random.dog/woof.json').json()
	url = contents['url']
	return url
	
def get_image_url():
	allowed_extension = ['jpg', 'jpeg', 'png']
	file_extension = ''
	while file_extension not in allowed_extension:
		url = get_url()
		file_extension = re.search("([^.]*)$", url).group(1).lower()
	return url
	
#action to take with /dog command
def woof(update, context):
	# global message
	# global chat_id
	chat_id = update.effective_chat.id
	url = get_image_url()
	context.bot.send_photo(chat_id, photo = url)
	
	
updater_sacpy = Updater(token)				#gets updates from the bot
dispatcher_sacpy = updater_sacpy.dispatcher				#dispatches the updates
updater_sacpy.start_polling()						#starts the bot

#handler for /time	
time_handler = CommandHandler('time', time)		
dispatcher_sacpy.add_handler(time_handler)			#adds /time handler 

#handler for messages	
msg_handler = MessageHandler(Filters.text & (~Filters.command), action)
dispatcher_sacpy.add_handler(msg_handler)			#adds msg handler 

#handler for /dog	
dog_handler = CommandHandler('dog', woof)		
dispatcher_sacpy.add_handler(dog_handler)			#adds /dog handler

#handler for unknown command
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher_sacpy.add_handler(unknown_handler)			#adds unknown handler 







while 1:
		print('listening')
		sleep(30)

