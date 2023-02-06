# bot.py
import os
import discord
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox

intents = discord.Intents().all()
client = discord.Client(intents=intents)

# Getting the token and the guild id from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ChannelID = os.getenv('CHANNEL_ID')

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}.')
    channel = client.get_channel(int(ChannelID))
    #await channel.send('OasisChecker est en ligne !') 

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
    def __init__(self, client):
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILD = os.getenv('DISCORD_GUILD')
        self.client = client
        self.ChannelID = os.getenv('CHANNEL_ID')
        self.OASIS_URL = "https://polytech-sorbonne.oasis.aouka.org/?#codepage=MYMARKS"
        self.username = os.getenv('OASIS_USERNAME')
        self.password = os.getenv('OASIS_PASSWORD')
        self.browser = Firefox()

    def Login(self):
        try:
            self.response = self.browser.get(self.OASIS_URL)
            username_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[1]/input')
            password_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[2]/input')
            login_button = self.browser.find_element("xpath", '//*[@id="SubmitLoginBtn"]')
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            print("Connecté à Oasis !")
        except:
            print("Erreur lors de la connexion à Oasis !")

    def run(self):
       self.client.run(self.TOKEN)

if __name__ == "__main__":
    OasisChecker = main(client)
    OasisChecker.Login()
    OasisChecker.run()
    