#!/bin/bash

while true; do
  docker run -it --name oasis-bot-container oasis-discord-bot
  sleep 60  # Pause de 1 minute avant la prochaine exécution
  docker stop oasis-bot-container
  docker rm oasis-bot-container
done
