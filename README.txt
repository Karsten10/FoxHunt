Hello fellow FoxHunt enjoyer!

To compile the bot, I have used Python version 3.7.8rc1 and pyTelegramBotAPI 4.9.0. Make sure both are installed!

Install Telegram Bot API via CMD with:
	python -m pip install pyTelegramBotAPI

To run the bot, open CMD and just run the .py file (python compiler obv)

There should be pleny comments in the code to have a rough understanding of how everything works

Art is generated using Dall E 2

Project file indexing is relative
File structure should be the following:
	main.py
	|_____
	|	| hints
	|
	|_____
		| pics

Notification of anybody finishing the FoxHunt will be sent to the HOST ID defined in the first couple of lines.
These messages look something like:

Someone has completed the FoxHunt!
ID: 34634412
User: Karsten

and can be used to see who finished everything first. The first question key is given, hence everybody will start at the same point.

To-Do:
o Audio hint implementation
o Location hint implementation
o Random start key and start location


If there's anything you need help with, don't hesitate contacting me
~ Karsten
