'''
╔═╗╔═╗╔═╗╦╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
║ ║╠═╣╚═╗║╚═╗  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
╚═╝╩ ╩╚═╝╩╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═      
Version 1.0.1                                                                          
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
import sys
import requests
import base64

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
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}.')
    channel = client.get_channel(int(ChannelID))
    if NewGrade == True:
        await channel.send(dt_string + " @everyone : Nouvelle note disponible sur Oasis !")
        sys.exit()

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
        self.client = client
        self.GITHUB_REPO = "gregoiremahon/oasis-checker-discord-bot"
        self.OASIS_URL = "https://polytech-sorbonne.oasis.aouka.org/?#codepage=MYMARKS"
        self.username = os.getenv('OASIS_USERNAME')
        self.password = os.getenv('OASIS_PASSWORD')
        self.Firefox_options = Options()
        self.Firefox_options.add_argument("--headless")
        self.browser = Firefox(options=self.Firefox_options)
        self.time_sleeper = 2
        self.ErrorCouter = 0
        self.average_grade = None

    def oasis_login(self):
        try:
            self.response = self.browser.get(url=self.OASIS_URL)
            username_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[1]/input')
            password_field = self.browser.find_element("xpath", '//*[@id="LoginForm"]/div[2]/input')
            login_button = self.browser.find_element("xpath", '//*[@id="SubmitLoginBtn"]')
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            print("Connecté à Oasis !")
        except Exception as e:
            print("Exception lors de la connexion à OASIS : " + str(e))
            print("Erreur lors de la connexion à Oasis !")

    def read_last_average_grade(self):
        github_url = f"https://api.github.com/repos/{self.GITHUB_REPO}/contents/last_average_grade.txt"
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

        response = requests.get(github_url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            last_average_grade_encoded = content['content']
            last_average_grade_decoded = base64.b64decode(last_average_grade_encoded).decode("utf-8")
            self.last_average_grade = float(last_average_grade_decoded)
        else:
            self.last_average_grade = 0

    def write_last_average_grade(self, new_average_grade):
        github_url = f"https://api.github.com/repos/{self.GITHUB_REPO}/contents/last_average_grade.txt"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        new_average_grade = str(new_average_grade)
        new_average_grade_encoded = base64.b64encode(new_average_grade.encode("utf-8")).decode("utf-8")
        data = {
            "message": "Mise à jour de la dernière note",
            "content": new_average_grade_encoded,
            "sha": self.get_file_sha(github_url),
        }
        response = requests.put(github_url, headers=headers, json=data)
        if response.status_code == 200:
            print("Dernière note mise à jour avec succès sur GitHub !")
        else:
            print("Erreur lors de la tentative de mise à jour de la note sur GitHub : " + response.text)
            sys.exit()

    def get_file_sha(self, url):
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            return content["sha"]
        return None

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
        span = self.average_grade_soup.find("span", class_="semesterAverage")
        self.average_grade = span.text.strip()
        self.average_grade = float(self.average_grade.replace(",", "."))
        print("AVERAGE : ", self.average_grade)
        if self.average_grade is not None:
            if float(self.average_grade) != float(self.last_average_grade):
                return True
            else:
                return False

    def run_bot(self):
        self.client.run(TOKEN)

if __name__ == "__main__":
    OasisChecker = main(client)
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
        OasisChecker.write_last_average_grade(Average_grade)
        OasisChecker.run_bot()
    OasisChecker.browser.close()
    OasisChecker.browser.quit()
    sys.exit()