# Oasis Checker Discord Bot

## Overview
The Oasis Checker Discord Bot is an automated solution designed to notify students at Sorbonne University through Discord whenever new grades are posted on the university's Oasis platform. The bot connects to the Oasis platform, fetches grade information, compares it with previous data, and sends notifications on a designated Discord channel.

## Features
- **Grade Extraction:** Uses Selenium for web navigation and BeautifulSoup for HTML parsing to extract user grades from the Oasis platform.
- **Grade Comparison:** Compares current average grade with the previously recorded average, stored in `last_average_grade.txt`.
- **GitHub Integration:** Updates the `last_average_grade.txt` on a public GitHub repository using the GitHub API and an authentication token stored in `.env`.
- **Discord Notifications:** Sends alerts on a specified Discord channel when a new grade is detected.
- **Continuous Monitoring:** Hosted on an Azure Linux VM and containerized with Docker for consistent performance and stability.

## Technology Stack
- **Python:** Core programming language.
- **Selenium & BeautifulSoup:** Web scraping and HTML data extraction.
- **Discord API:** For interaction with Discord.
- **GitHub API:** For updating files on GitHub.
- **Docker:** Containerization of the bot.
- **Azure VM:** Hosting platform.
- **Cron:** Task scheduling for regular bot execution.

## Setup and Installation

1. **Environment Configuration:**
   Store your Discord bot TOKEN, channel ID, and Oasis login credentials in a `.env` file.

2. **Docker Image:**
   The bot is packaged as a Docker image, with all dependencies handled in the Dockerfile. Pull the image from Docker Hub:
   ```bash
   docker pull gregoiremahon1/oasis-discord-bot
   ```

3. **Cron Job Setup:**
   The bot is executed periodically via a cron job on the Azure VM. The cron command is as follows:
   ```bash
   */30 * * * * docker run --rm -v /home/gregoiremahon/.env:/app/.env gregoiremahon1/oasis-discord-bot:latest >> /home/gregoiremahon/logs_bot_oasis/logs_bot.log 2>&1
   ```
   This command ensures that the bot runs every 30 minutes, and logs are recorded for monitoring and troubleshooting. It also mounts your .env file containing your credentials.

## Usage
- **Starting the Bot:** 
  Once the setup is complete, the bot will automatically start according to the schedule set by the cron job.
- **Monitoring:** 
  Check the logs at `/home/gregoiremahon/logs_bot_oasis/logs_bot.log` for activity and potential issues.
