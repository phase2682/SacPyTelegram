

import telepot
token = 'Bot access token'						#insert your access token

print("Obtaining bot information")
print()

ham_bot=telepot.Bot(token)						#setting up the bot
get = ham_bot.getMe()							#get information about ham_bot

print('bot id is: ' + str(get['id']))
print('The name of the bot is: ' + str(get['first_name']))
print('user name is: ' + str(get['username']))
print()

print('73')

