import os
from dotenv import load_dotenv

import telebot
from telebot import types

# Bot V 2.4

# Token aquired over Telegram, see API for more info
BotToken  = os.getenv('TELEGRAM_BOT_TOKEN')

class question:
    def __init__(self, key, question, answers, correctAnswer, textHint, photoHint, long, lat):
        self.key = key

        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer

        self.textHint = textHint
        self.photoHint = photoHint

        self.long = long
        self.lat = lat
    # 0 unanswered; 1 correct; 2 incorrect
    correct = 0

class quiz:
    sadFaces = []

    questions = []

    questions.append(question(
        # Key
        "abc",
        # Question
        "What is the name of this bot?",
        # Answers
        ["volundrbot",
        "22",
        "23",
        "24"],
        # Correct Answer
        # a = 0     b = 1   c = 2   d = 3
        "0",
        # Text hint
        "Don't eat the yellow snow\!",
        # Photo hint
        "",
        # GPS hint
        # Long
        33.5973,
        # Lat
        73.0479
    ))

    questions.append(question(
        # Key
        "def",
        # Question
        "What is 1 \+ 1?",
        # Answers
        ["0",
        "1",
        "2",
        "3"],
        # Correct Answer
        # a = 0     b = 1   c = 2   d = 3
        "2",
        # Text hint
        "Don't eat the yellow snow\!",
        # Photo hint
        "",
        # GPS hint
        # Long
        0,
        # Lat
        0
    ))

    questions.append(question(
        # Key
        "ghi",
        # Question
        "What is 0 \+ 1?",
        # Answers
        ["0",
        "1",
        "2",
        "3"],
        # Correct Answer
        # a = 0     b = 1   c = 2   d = 3
        "1",
        # Text hint
        "Don't eat the yellow snow\!",
        # Photo hint
        "",
        # GPS hint
        # Long
        33.5973,
        # Lat
        73.0479
    ))

    @classmethod
    def nrQuestions(cls):
        return len(cls.questions)

    @classmethod
    def correctQuestions(cls):
        numberCorrect = 0
        for i in range(quiz.nrQuestions()):
            if cls.questions[i].correct == 1:
                numberCorrect = numberCorrect + 1
        return numberCorrect

    @classmethod
    def answeredQuestions(cls):
        numberAnswered = 0
        for i in range(quiz.nrQuestions()):
            if cls.questions[i].correct > 0:
                numberAnswered = numberAnswered + 1
        return numberAnswered

    @classmethod
    # Finding the index of the item in the list to pass it into question array
    def getQuestionIndex(cls, submittedKey):
        index = None
        for i in range(cls.nrQuestions()):
            if(cls.questions[i].key == submittedKey.lower()):
                index = i
                break
        return index

quiz = quiz()

# Create instance of telebot - using Markdown for passing tekst format
VolundrBot = telebot.TeleBot(BotToken, parse_mode="MarkdownV2")

welcomeMessage = "*Welcome to the FoxHunt Quiz by Volundr* \U0001F98A \U0001F44B \n\
If you have found a key \U0001F511, submit it for a question using /key _key_\. \
You can then answer this question using /answer _key_ _answer_\. \
Sometimes we do care about you\U00002757 We _might_ give you a hint after a correct answer\. \
Check your _stats_\U0001F4C8 with the /stats command\. \n\n\
There is a total of *" + str(quiz.nrQuestions()) + "* questions but get you started, we will provide you the first key\: *" + quiz.questions[0].key + "*\n\n\
Good Luck \U0001F340\, may the best team win \.\.\.\."

# Command w/o args
# See how to use the bot when typing /help
@VolundrBot.message_handler(commands=['help','start'])
def startMessage(message):
    VolundrBot.send_chat_action(message.chat.id, 'typing')
    VolundrBot.reply_to(message, welcomeMessage)
    foxPhoto = open('./pics/FoxHunt.png', 'rb')
    VolundrBot.send_photo(message.chat.id, foxPhoto)

    uFirstName, uLastName, uID = str(message.from_user.first_name), str(message.from_user.last_name), str(message.from_user.id)
    print("Action by " + uFirstName + " " + uLastName + " ID " + uID + ": Started the Quiz \n")

# Command with args
# So that you can get the question that belongs to a key. Usage /key <key>
@VolundrBot.message_handler(commands=['key'])
def submitKey(message):
    subKey = "NOKEY"
    VolundrBot.send_chat_action(message.chat.id, 'typing')
    args = message.text.split(' ')[1:]
    if len(args) == 1:
        subKey = args[0]
        questionNr = quiz.getQuestionIndex(subKey)
        if(questionNr != None) and (quiz.questions[questionNr].correct == 0):
            sendQuestion(questionNr, message)
            debug = None
        elif(questionNr == None):
            response = "Sorry\, " + subKey + " is not a valid \U0001F511\.\.\."
            debug = "invalid key"
            VolundrBot.send_message(message.chat.id, response)
        else:
            response = "Sorry\, you have already answered \U0001F511 " + subKey + " \.\.\."
            debug = "already answered"
            VolundrBot.send_message(message.chat.id, response)

    elif len(args) < 1:
        response = "Invallid call\! Was expecting *more* args \U0001F972"
        debug = "invalid call, too little args"
        VolundrBot.send_message(message.chat.id, response)
    else:
        response = "Invallid call\! Was expecting *less* args \U0001FAE3"
        debug = "invalid key, too many args"
        VolundrBot.send_message(message.chat.id, response)

    if debug != None:
        uFirstName, uLastName, uID = str(message.from_user.first_name), str(message.from_user.last_name), str(message.from_user.id)
        print("Action by " + uFirstName + " " + uLastName + " ID " + uID + ": Submitted key " + str(subKey) + " and yielded " + debug)
        print("STATS :: Total Questions: " + str(quiz.nrQuestions()) + " - Answered questions: " + str(quiz.answeredQuestions()) + " - Correct Questions: " + str(quiz.correctQuestions()) + "\n")


def sendQuestion(questionNr, message):
    response = "Valid \U0001F511 submitted\n *Question\:* " + quiz.questions[questionNr].question
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(quiz.questions[questionNr].answers)):
        button = types.InlineKeyboardButton(quiz.questions[questionNr].answers[i], callback_data = str(i))
        keyboard.add(button)

    VolundrBot.arbitrary_callback_data = questionNr
    VolundrBot.send_message(message.chat.id, text=response, reply_markup=keyboard)

@VolundrBot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    questionNr = VolundrBot.arbitrary_callback_data
    VolundrBot.answer_callback_query(callback_query_id=call.id, text='Answer submitted!')

    if call.data == str(quiz.questions[questionNr].correctAnswer):
        response = "This was the correct answer"
        quiz.questions[questionNr].correct = 1
        VolundrBot.send_message(call.message.chat.id, response)
        VolundrBot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    else:
        response = "This answer was incorrect"
        quiz.questions[questionNr].correct = 2
        VolundrBot.send_message(call.message.chat.id, response)
        VolundrBot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    if quiz.answeredQuestions() == quiz.nrQuestions():
        finalizeQuizClient(call.message.chat.id)
    elif quiz.questions[questionNr].textHint != "" or quiz.questions[questionNr].textHint != "" or quiz.questions[questionNr].long != 0 or quiz.questions[questionNr].lat != 0:
            giveHint(call.message.chat.id, questionNr)

    uFirstName, uLastName, uID = str(call.from_user.first_name), str(call.from_user.last_name), str(call.from_user.id)
    print("Action by " + uFirstName + " " + uLastName + " ID " + uID + ": Answered Question " + str(questionNr) + " and yielded " + str(quiz.questions[questionNr].correct) + " points added")

    print("NEW STATS :: Total Questions: " + str(quiz.nrQuestions()) + " - Answered Questions: " + str(quiz.answeredQuestions()) + " - Correct Questions: " + str(quiz.correctQuestions()) + "\n")

# Command w/o args
# See the stats of the player
@VolundrBot.message_handler(commands=['stats'])
def sendStats(message):
	VolundrBot.send_message(message.chat.id,
    "\U00002192*STATS* \U0001F4C8  \nCorretly answered questions\: "
	+ str(quiz.correctQuestions()) + " \/ *" + str(quiz.nrQuestions()) + "*\n  " + progressBar())

# Command that's useful for developing the bot
# Resets the correctness parameter of all the questions to 0 so I don't have to reboot the bot everytime I test it.
@VolundrBot.message_handler(commands=['reset'])
def resetCorrectness(message):
	for i in range(quiz.nrQuestions()):
		quiz.questions[i].correct = 0
	response = "Bot has been reset, nrQuestions\: " + str(quiz.nrQuestions()) + " \nHave fun\!"
	VolundrBot.reply_to(message, response)

# Make the progress bar with emoji's
def progressBar():
	progress = []
	for i in range(quiz.nrQuestions()):
        # Not answered
		if quiz.questions[i].correct == 0:
			progress.append("\U00002B1C")
        # Correct
		elif quiz.questions[i].correct == 1:
			progress.append("\U0001F7E9")
        # Incorrect
		elif quiz.questions[i].correct == 2:
			progress.append("\U0001F7E5")
	return ''.join(progress)

def giveHint(chatID, questionNr):
    response = "We're also giving you a *hint*\: \n\n"
    if quiz.questions[questionNr].textHint != "":
        response = response + quiz.questions[questionNr].textHint

    VolundrBot.send_message(chatID, response)

    if quiz.questions[questionNr].photoHint != "":
        hintPhoto = open(quiz.questions[questionNr].photoHint, 'rb')
        VolundrBot.send_photo(chatID, hintPhoto)

    if quiz.questions[questionNr].long != 0 or quiz.questions[questionNr].lat != 0:
        VolundrBot.send_location(chatID, quiz.questions[questionNr].lat, quiz.questions[questionNr].long)


def finalizeQuizClient(chatID):
    VolundrBot.send_message(chatID, "*You've completed the FoxHunt*\U0001F38A\U0001F38A\U0001F38A \n\n Final stats: \n" + progressBar())
    foxPhoto = open('./pics/WinningImageFox.png', 'rb')
    VolundrBot.send_photo(chatID, foxPhoto)

# Restart entire bot and go over
VolundrBot.infinity_polling()
