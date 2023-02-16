# oasis-checker-discord-bot
Discord bot to check if new grades have been uploaded on Sorbonne University Oasis page. Sends notifications to users on the discord channel.

# How to use ? 
Install these dependencies using pip (in a venv) : 

pip install selenium

pip install bs4

pip install python-dotenv

pip install schedule

# How it works ? 
Store your Discord bot TOKEN and your channel ID, with your Oasis login informations in a .env file to begin. 
Then, just launch 'Refresher.py' to run the main program in automatic mode. This will run main.py every minute, and send a message on the discord channel you configured
to notify @everyone that a new grade is available. Every time main.py is launched, it compares the last average grade stored in last_average_grade.txt and if the readed average grade on the website is different, it sends a message on the discord server.
