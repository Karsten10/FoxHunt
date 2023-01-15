import telebot

# Bot V 0.3

# Token aquired over Telegram, see API for more info
BotToken  = "xxxxxxxxxxxxxxxxx"

# Chat ID to send logs to, in this case it's user Karsten
hostChatID = "xxxxxxxxxxxxxxxxx"

# Defining the keys with the questions, format: key, question, answer, 0, hint
# Don't forget to add comma's after each entry!
questions = [
	["L32saD", "What is the name of the association?", "Thor", 0, "Look to your left\.", "No"], 
	["346da", "What is the name of the event?", "Foxhunt", 0, "No", './hints/hintExample.png'],
]
nrQuestions = len(questions)

# Create instance of telebot - using Markdown for passing tekst format
VolundrBot = telebot.TeleBot(BotToken, parse_mode="MarkdownV2")

welcomeMessage = "*Welcome to the FoxHunt Quiz by Volundr* \U0001F98A \U0001F44B \n\
If you have found a key \U0001F511, submit it for a question using /key _key_\. \
You can then answer this question using /answer _key_ _answer_\. \
Sometimes we do care about you\U00002757 We _might_ give you a hint after a correct answer\. \
Check your _stats_\U0001F4C8 with the /stats command\. \n\n\
There is a total of *" + str(nrQuestions) + "* questions but get you started, we will provide you the first key\: *" + questions[0][0] + "*\n\n\
Good Luck \U0001F340\, may the best team win \.\.\.\."

# Command w/o args
# See how to use the bot when typing /help
@VolundrBot.message_handler(commands=['help','start'])
def startMessage(message):
	VolundrBot.reply_to(message, welcomeMessage)
	foxPhoto = open('./pics/FoxHunt.png', 'rb')
	VolundrBot.send_photo(message.chat.id, foxPhoto)


# Command with args
# So that you can get the question that belongs to a key. Usage /key <key>
@VolundrBot.message_handler(commands=['key'])
def submitKey(message):
	args = message.text.split(' ')[1:]
	if(len(args) == 1):
		subKey = args[0]
		response = "Sorry\, " + subKey + " is not a valid \U0001F511\.\.\."
		keyIndex = getIndex(0, questions, subKey)
		if(keyIndex != None):
			response = "Valid \U0001F511 submitted\n *Question\:* " + questions[keyIndex][1]
	elif(len(args) < 1):
		response = "Invallid call\! Was expecting *more* args \U0001F972"
	else:
		response = "Invallid call\! Was expecting *less* args \U0001FAE3"
	VolundrBot.reply_to(message, response)

# Command w/o args
# See the stats of the player
@VolundrBot.message_handler(commands=['stats'])
def sendStats(message):
	nrCorrect = correctQuestions(questions)
	VolundrBot.reply_to(message, "\U00002192*STATS* \U0001F4C8  \nCorretly answered questions\: "
	+ str(nrCorrect) + " \/ *" + str(nrQuestions) + "*\n  " + progressBar(nrCorrect))

# Command with args
# So that you can answer a question. Usage /answer <key> <answer>
@VolundrBot.message_handler(commands=['answer'])
def submitAnswer(message):
	args = message.text.split(' ')[1:]
	hint = 0
	if(len(args) == 2):
		subKey, givenAnswer = args[0], args[1]
		questionNr = getIndex(0, questions, subKey)
		if(questionNr != None):
			answer = questions[questionNr][2]
			if(questions[questionNr][3] == 1):
				response = "*What are you doing\?\!* This question has already been answered correctly\! \U0001FAE5"
			elif(givenAnswer.lower() == answer.lower()):
				response = "That's the right answer\! Question flagged as *correct* \U00002611"
				questions[questionNr][3] = 1
				hint = 1
			else:
				response = "That's *not* right answer\! Question flagged as *incorrect* \U000025FB\, please try again\."
		else:
			response = "Sorry\, " + subKey + " is not a valid key\.\.\."
	elif(len(args) < 2):
		response = "Invallid call\! Was expecting more args \:\("
	else:
		response = "Invallid call\! Was expecting less args \:\("
	VolundrBot.reply_to(message, response)
	# If a hint is set to No, it will not be used
	# Printing tekst hint if defined
	if(hint == 1 and (questions[questionNr][4] != "No" or questions[questionNr][5] != "No")):
		response = "We're also giving you a *hint*\: \n\n"
		if(questions[questionNr][4] != "No"):
			response = response + questions[questionNr][4]
		VolundrBot.send_message(message.chat.id, response)
	# Sending image hint if defined
	if(hint == 1 and questions[questionNr][5] != "No"):
		hintPhoto = open(questions[questionNr][5], 'rb')
		VolundrBot.send_photo(message.chat.id, hintPhoto)
	# Win the game
	if(correctQuestions(questions) == nrQuestions):
		VolundrBot.send_message(message.chat.id, "*You've completed the FoxHunt*\U0001F38A\U0001F38A\U0001F38A")
		foxPhoto = open('./pics/WinningImageFox.png', 'rb')
		VolundrBot.send_message(hostChatID, "*Someone has completed the FoxHunt\!*\nID\: " + str(message.chat.id) + "\nUser\: " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) )
		VolundrBot.send_photo(message.chat.id, foxPhoto)

# Command that's useful for developing the bot
# Resets the correctness parameter of all the questions to 0 so I don't have to reboot the bot everytime I test it.
@VolundrBot.message_handler(commands=['reset'])
def resetCorrectness(message):
	for i in range(nrQuestions):
		questions[i][3] = 0
	response = "Bot has been reset, nrQuestions\: " + str(nrQuestions) + " \nHave fun\!"
	VolundrBot.reply_to(message, response)

# Finding the index of the item in the list to pass it into question array
def getIndex(itemType, searchIn, value):
	#itemType	||	0 key	||	1 question	||	2 answer	||	3 correctness	||	4 txt hint	||	5 IMG hint
	index = None
	for i in range(nrQuestions):
		if(searchIn[i][itemType].lower() == value.lower()):
			index = i
			break
	return index

# Return the amount of correctly answered questions in int value
def correctQuestions(questions):
	correctQuestions = 0
	for i in range(nrQuestions):
		if(questions[i][3] == 1):
			correctQuestions = correctQuestions + 1
	return correctQuestions

# Make the progress bar with emoji's
def progressBar(nrCorrect):
	progress = []
	for i in range(nrQuestions):
		if(i < nrCorrect):
			progress.append("\U00002611")
		else:
			progress.append("\U000025FB")
	if(nrQuestions == nrCorrect):
		progress.append("\U0001F60E\U0001F60E\U0001F60E")
	return ''.join(progress)

# Restart entire bot and go over 
VolundrBot.infinity_polling()
