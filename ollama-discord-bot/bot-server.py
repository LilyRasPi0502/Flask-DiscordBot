# 你電腦放客廳家人問你在看什麼欸所以你現在家人聽得到我說話是不是呃這個我的臺我現在在播放的節目是我教大家怎麼吃ㄐㄐ欸咿耶左邊一個ㄐㄐ右邊一個ㄐㄐ噯ㄐㄐ好吃每天吃身體健康

from flask_cors import CORS
from os import system, name
from flask import *
from dc.bot import *
from datetime import *
import json, asyncio, threading

app = Flask(__name__)
CORS(app)

BotStatus = []
BotThread = []

def clear():
	# for windows
	if name == 'nt':
		_ = system('cls')
	# for mac and linux(here, os.name is 'posix')
	else:
		_ = system('clear')

def readJson(Path="config.json"):
	with open("json/"+Path+".json", "r", encoding="utf-8") as f:
		return json.load(f)

def writeJson(data, Path="config.json"):
	with open("json/"+Path+".json", 'w', encoding="utf-8") as f:
		json.dump(data, f)
		
def RemoveSimple(data):
	return data.replace("<@", "").replace(">", "")
	
def Get_Time():
	dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
	dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
	return dt2.strftime("%Y-%m-%d %H:%M:%S")
	
def download_image(image_url, file_dir):
	response = requests.get(image_url)
	if response.status_code == 200:
		directory = os.path.dirname(file_dir)
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open(file_dir, "wb") as fp:
			fp.write(response.content)
		print("Image downloaded successfully.")
	else:
		print(f"Failed to download the image. Status code: {response.status_code}")
	
def run_bot(ID):
	jsonFile = readJson("index")
	for i in range(len(jsonFile["Bot_List"])):
		if RemoveSimple(jsonFile["Bot_List"][i]["ID"]) == ID:
			BotStatus.append({"Bot_ID":ID, "Status": True})
			new_loop = asyncio.new_event_loop()
			asyncio.set_event_loop(new_loop)
			loop = asyncio.get_event_loop()
			task = asyncio.ensure_future(bot1(jsonFile["Bot_List"][i]["Token"]))

			#loop.run_until_complete(asyncio.wait([task]))
			#print(task.result())

@app.route('/bot/<ID>')
def bot(ID):
	if len(BotStatus) > 0:
		for i in range(len(BotStatus)):
			if BotStatus[i]["Bot_ID"] == ID and BotStatus[i]["Status"] :
				return '{"Status":200,"content":"'+str(ID)+' is repeat run!!!"}'
	#bot1(jsonFile["Bot_List"][i]["Token"])
	try:
		thread1 = threading.Thread(target=run_bot, args=(ID, ))
		thread1.start()
		thread1.args = (ID, )
		BotThread.append(thread1)
		return '{"Status":200,"content":"'+str(ID)+' bot is run."}'
	except:
		return '{"Status":200,"content":"cannot run bot."}'

@app.route('/aliveReport', methods=['GET', 'POST'])
def aliveReport():
	if len(BotStatus) > 0:
		#return request.json
		for i in range(len(BotStatus)):
			if BotStatus[i]["Bot_ID"] == request.json["ID"]:
				if request.json["Action"] == "Report":
					BotStatus[i]["Status"] = request.json["Status"]
					return '{"Status":"200"}'
				else:
					if BotStatus[i]["Status"] :
						return '{"Status":"online", "Count": '+request.json["Status"]+'}'
					else:
						return '{"Status":"offline", "Count": '+request.json["Status"]+'}'
				for o in range(len(BotThread)):
					if BotThread[o].args[0] == BotStatus[i]["Bot_ID"]:
						#print(f"Thread is {BotThread[o].is_alive()}")
						if not BotStatus[i]["Status"] :
							del BotThread[o]
			#else:
				#return '{"Status":"offline"}'
		
	
	return '{"Status":"offline", "Count": '+str(request.json["Status"])+'}'
	#return '{"Status":"offline", "Count": "0"}'
	
@app.route('/save', methods=['GET', 'POST'])
def save():
	if request.values["Action"] == "Add_Bot":
		if request.values["botname"] == "Add_Bot":
			botname = f"Add_Bot[{Get_Time()}]"
		else:
			botname = request.values["botname"]
		jsonFile = readJson("index")
		download_image(f"https://www.minabep.uk/momotalk/Avatar/%E5%8D%97%E9%83%A8P.png", f"./static/avatar/{RemoveSimple(request.values['botid'])}.png")
		jsonFile["Bot_List"].append({"name":botname,"ID":request.values["botid"],"Token":request.values["bottoken"]})
		writeJson(data=jsonFile, Path="index")
		writeJson(data={"Setting":request.values["setting"]}, Path=RemoveSimple(request.values["botid"]))
	else:
		jsonFile = readJson("index")
		for i in range(len(jsonFile["Bot_List"])):
			if jsonFile["Bot_List"][i]["name"] == request.values["Action"]:
				jsonFile["Bot_List"][i]["name"] = request.values["botname"]
				jsonFile["Bot_List"][i]["ID"] = request.values["botid"]
				jsonFile["Bot_List"][i]["Token"] = request.values["bottoken"]
				SettingFile = readJson(RemoveSimple(request.values["botid"]))
				SettingFile["Setting"] = request.values["setting"].replace("\n", "")
				writeJson(data=jsonFile, Path="index")
				writeJson(data=SettingFile, Path=RemoveSimple(request.values["botid"]))
	return redirect(url_for('home'))

@app.route('/config/<Select>')
def config(Select):
	Arg = readJson("index")
	data = Arg["Bot_List"][int(Select)]
	Setting = readJson(RemoveSimple(data["ID"]))["Setting"]
	data.update({"Setting": Setting})
	return render_template('abc.html', arg=Arg, title="Bot Configure", slt=data)
	
@app.route('/addBot')
def addBot():
	Arg = readJson("index")
	return render_template('abc.html', arg=Arg, title="Add Bot", slt={"name":"Add_Bot"})
	
@app.route('/home')
def home():
	Arg = readJson("index")
	for i in range(len(Arg["Bot_List"])):
		SettingFile = readJson(RemoveSimple(Arg["Bot_List"][i]["ID"]))
		Arg["Bot_List"][i].update({"Setting": SettingFile["Setting"]})
	return render_template('home.html', title="Bot Home", Bot_List=Arg["Bot_List"], bot_List_Legth=len(Arg["Bot_List"]))
	
"""
@app.route('/login', methods=['GET', 'POST']) 
def login():
	if request.method == 'POST': 
		return 'Hello ' + request.values['username'] 

	return "<form method='post' action='/login'><input type='text' name='username' />" \
	"</br>" \
	"<button type='submit'>Submit</button></form>"
"""

if __name__ == '__main__':
	clear()
	app.run(debug = True, host="0.0.0.0", port=8964)
	

	
