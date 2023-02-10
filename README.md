# oasis-checker-discord-bot
Discord bot to check if new grades have been uploaded on Sorbonne University Oasis page. Sends notifications to users on the discord channel.

How it works ? 
Store your Discord bot TOKEN and your channel ID, with your Oasis login informations in a .env file to begin. 
Then, just launch 'Refresher.py' to run the main program in automatic mode. This will run main.py every minute, and send a message on the discord channel you configured
to notify @everyone that a new grade is available.
