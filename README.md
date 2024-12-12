# Flask-DiscordBot
- 基於python-flask庫 ollama的discord AI機器人
- Based python-flask and ollama discord AI bot

# 如何使用(How to used)
1. 環境建置(environment Build)
   - 安裝[python](https://www.python.org)(install python)
   - 安裝[ollama](https://github.com/ollama/ollama)(install ollama)

2. 安裝依賴庫(Install dependent libraries)
   - `pip install Flask`
   - `pip install ollama`
   - `pip install asyncio`
   - `pip install requests`
   - `pip install threaded`
   - `pip install Flask-Cors`
   - `python3 -m pip install -U py-cord`

3. 啟動Bot-Server(Startup Bot-Server)
   - `git clone https://github.com/LilyRasPi0502/Flask-DiscordBot.git`
   - `cd Flask-DiscordBot/ollama-discord-bot`
   - `python3 bot-server.py`

4. 設定Bot(Setting Bot)
   - [Bots Home](http://127.0.0.1:8964/home)
   - [Add Bot](http://127.0.0.1:8964/addBot)

5. 機器人遙控指令(Bot remote control commands)
   - `<@Your_bot_ID>`: 呼叫機器人(Call bot)
   - `<@Your_bot_ID> &fuckoff;`: 使機器人關閉(bot shut down)
   - `<@Your_bot_ID> Hi!......`: 跟AI機器人講話(Talk with AI bot)

6. 注意事項(Note)
   - 為了節省資源，機器人會在 UCT+8 [00:00, 08:00, 16:00] 自動關閉(To save resources, Bot auto close on UCT+8 [00:00, 08:00, 16:00])

# 更新日誌(Update logging)
- [20241202] Create this project
- [20241203] Create this repository
- [20241204] Fixed repeated startup and UI issues
- [20241205] Added online status indicator to Home page
- [20241206] Fixed the port issue where Bot could not report online status normally
- [20241212] Added subsequent self-holding switch

