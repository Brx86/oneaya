python -m venv .env --upgrade-deps
source .env/bin/activate
pip install nb-cli
nb driver install HTTPX
nb driver install websockets
nb adapter install OneBot
nb plugin install nonebot-plugin-rauthman
nb plugin install nonebot_plugin_apscheduler