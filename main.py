'''
╔═╗╔═╗╔═╗╦╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
║ ║╠═╣╚═╗║╚═╗  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
╚═╝╩ ╩╚═╝╩╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═      
Version 1.0.0                                                                          
'''                                                                                
import os
import discord
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
from datetime import datetime

intents = discord.Intents().all()
client = discord.Client(intents=intents)
NewGrade = False
Average_grade = 0
last_average_grade = None
Curr_date_time = datetime.now()
dt_string = Curr_date_time.strftime("%d/%m/%Y %H:%M:%S")

# Getting the token and the guild id from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ChannelID = os.getenv('CHANNEL_ID')

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}.')
    channel = client.get_channel(int(ChannelID))
    if NewGrade == True:
        await channel.send(dt_string + " @everyone : Nouvelle note disponible sur Oasis !")
        exit()

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
        self.Firefox_options = Options()
        self.Firefox_options.add_argument("--headless")
        self.browser = Firefox(options = self.Firefox_options)
        self.response = None
        self.time_sleeper = 2
        self.ErrorCouter = 0
        self.average_grade = None

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

    #read the last average grade in a txt file
    def read_last_average_grade(self):
        with open("last_average_grade.txt", 'r') as InputFile:
            try:
                lines = InputFile.readlines()
                for Value in lines:
                    self.last_average_grade = Value.replace(',', '.')
            except:
                self.last_average_grade = 0

    def check_grades(self):
        sleep(self.time_sleeper)
        oasis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        oasis_page_content = oasis_soup.get_text()
        try:
            if "Mes notes" in oasis_page_content:
                print("Connexion réussie !")
                print("Vérification des notes...")
            else:
                print("Erreur lors de la connexion à Oasis !")
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
        self.average_grade_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        span = self.average_grade_soup.find("span", class_="yearAverage")
        self.average_grade = span.text.strip()
        self.average_grade = float(self.average_grade.replace(",", "."))
        print("AVERAGE : ",self.average_grade)
        if self.average_grade is not None:
            if float(self.average_grade) != float(self.last_average_grade):
                with open('last_average_grade.txt', 'w') as InputFile:
                    InputFile.write(str(self.average_grade))
                self.average_grade = self.last_average_grade
                return True
            else:
                return False
            
    def run_bot(self):
       self.client.run(self.TOKEN)

if __name__ == "__main__":
    
    OasisChecker = main(client, last_average_grade)
    OasisChecker.oasis_login()
    OasisChecker.check_grades()
    OasisChecker.read_last_average_grade()
    NewGrade = OasisChecker.check_new_grade()
    Average_grade = OasisChecker.average_grade
    if NewGrade == False:
        print(dt_string + " / No new grade available, retrying in 60 seconds...")
        OasisChecker.browser.close()
        OasisChecker.browser.quit()
        exit()
    else:
        OasisChecker.run_bot()
        OasisChecker.browser.close()
        OasisChecker.browser.quit()