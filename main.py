# bot.py
import os
import discord
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from time import sleep

intents = discord.Intents().all()
client = discord.Client(intents=intents)


last_average_grade = None

# Getting the token and the guild id from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ChannelID = os.getenv('CHANNEL_ID')

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}.')
    channel = client.get_channel(int(ChannelID))

    # Get last bot message in the current channel
    try:
        messages = await channel.history(limit=1).flatten()

        # Parse the last message to get the last average grade
        for message in messages:
            if message.author == client.user:
                last_average = message.content.split(":")[1].strip()    
        global last_average_grade
        last_average_grade = last_average
    except:
        await channel.send('OasisChecker est en ligne !') 

@client.event
async def on_message(message):
    channel = client.get_channel(int(ChannelID))
    if message.content == "Ping":
        await message.channel.send("Pong")
    if message.content == "OasisChecker --version":
        await message.channel.send("OasisChecker v1.0.0 / Credits : @mouityx#4533 & @Ranxort#5961")
    if message.content == "OasisChecker --help":
        await message.channel.send("OasisChecker v1.0.0\nCe bot vous préviendra si une nouvelle note a été entrée sur Oasis !")    


class main:
    def __init__(self, client, last_average_grade):
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILD = os.getenv('DISCORD_GUILD')
        self.client = client
        self.ChannelID = os.getenv('CHANNEL_ID')
        self.OASIS_URL = "https://polytech-sorbonne.oasis.aouka.org/?#codepage=MYMARKS"
        self.username = os.getenv('OASIS_USERNAME')
        self.password = os.getenv('OASIS_PASSWORD')
        self.browser = Firefox()
        self.response = None
        self.time_sleeper = 2
        self.ErrorCouter = 0
        self.average_grade = last_average_grade

    def oasis_login(self):
        try:
            self.response = self.browser.get(url = self.OASIS_URL)
            username_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[1]/input')
            password_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[2]/input')
            login_button = self.browser.find_element("xpath", '//*[@id="SubmitLoginBtn"]')
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            print("Connecté à Oasis !")
            
        except:
            print("Erreur lors de la connexion à Oasis !")
    
    def check_grades(self):
        sleep(self.time_sleeper)
        oasis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        oasis_page_content = oasis_soup.get_text()
        try:
            if "Mes notes" in oasis_page_content:
                print("Connexion réussie !")
                print("Vérification des notes...")
            else:
                print(oasis_page_content)
        except:
            self.ErrorCouter += 1
            self.time_sleeper += 1
            self.checkGrades()
            if self.ErrorCouter == 5:
                print("Erreur lors de la vérification des notes !")
                self.browser.quit()
                exit()
    def check_new_grade(self):
        sleep(self.time_sleeper)
        oasis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        oasis_page_content = oasis_soup.get_text()
        self.average_grade = self.browser.find_element("xpath", '//*[@id="Semester21214249_2022_1"]/h2/span[2]')
        print('MOYENNE', self.average_grade)
        try:
            if self.average_grade is not None:
                return float(self.average_grade) != float(self.last_average_grade)
            else:
                print(oasis_page_content)
        except:
                print("Erreur pas d'ancienne moyenne générale trouvée...!")
                self.browser.quit()

    def run_bot(self):
       self.client.run(self.TOKEN)

if __name__ == "__main__":
    OasisChecker = main(client, last_average_grade)
    OasisChecker.oasis_login()
    OasisChecker.check_grades()
    OasisChecker.check_new_grade()
    OasisChecker.run_bot()