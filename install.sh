#! /bin/sh
cd /root
git clone https://github.com/shamhi/HamsterKombatBot.git
cd HamsterKombatBot
python3 -m venv venv
source venv/bin/activate
copy .env-example .env
rm .env-example
pip3 install -r requirements.txt
clear
