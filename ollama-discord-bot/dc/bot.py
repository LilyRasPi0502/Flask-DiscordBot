import discord, requests, os, json

from discord.ext import commands
from discord.ext import tasks
from datetime import *

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

def ollama(model="gemma2", message=[{"role":"user","content":"Hi!"}]):
	from ollama import chat
	from ollama import ChatResponse
	response: ChatResponse = chat(model=model, messages=message)
	return response['message']['content']

def readJson(Path="config.json"):
	with open("json/"+Path+".json", "r", encoding="utf-8") as f:
		return json.load(f)

def RemoveSimple(data):
	return str(data).replace("<@", "").replace(">", "")

class MyBot(commands.Bot):
	
	def __init__(self, command_prefix, intent):
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intent)
		self.Reflash_CharacterAI.start()
	
	async def on_ready(self):
		self.message1 = f"[{self.Get_Time()}] 正在使用身分: {self.user}({self.user.id})"
		self.message2 = f"正在使用身分: {self.user}({self.user.id})"
		print(self.message1)
		download_image(f"{self.user.avatar}", f"./static/avatar/{self.user.id}.png") 
		#os.system(f"curl {self.user.avatar} -o ./static/avatar/{self.user.id}.png")
		await self.change_presence(activity=discord.Activity(name="", type=0))
		
	async def on_message(self, message):
		#排除自己的訊息，避免陷入無限循環
		if str(message.author).find(str(self.user)) != -1:
			return
		Send = True
		print(f"[{self.Get_Time()}] Get Message from {str(message.guild)}.{str(message.channel)}.{str(message.author.display_name)}: {str(message.content)}")
		
		#聊天程序
		if message.reference is not None:
			ctx = await message.channel.fetch_message(message.reference.message_id)
			if str(ctx.author).find(str(self.user)) != -1:
				await self.chat(message)
				Send = False
		if (message.content.find(str(self.user.id)) != -1) and Send:
			await self.chat(message)
			Send = False
	
	async def chat(self, message):
		if str(message.content).find("&fuckoff;") != -1:
			await self.CloseSelf()
		async with message.channel.typing():
			file = readJson(f"{RemoveSimple(self.user.id)}")["Setting"]
			prompt = [
				{
					"content": f"Time:[{self.Get_Time()}] {file}, **請直接回覆** **你的使用者ID是{self.user.id}**",
					"role": "system"
				}
			]
			UserMSG = []
	
			if message.reference is not None:
				ctx = await message.channel.fetch_message(message.reference.message_id)
				
				MSG_Serial = [message, ctx]
				MSG_Count = 0
				while MSG_Serial[MSG_Count].reference is not None:
					MSG_Serial.append(await MSG_Serial[MSG_Count].channel.fetch_message(MSG_Serial[MSG_Count].reference.message_id))
					MSG_Count = MSG_Count + 1
				for MSG in MSG_Serial:
					if str(MSG.author).find(str(self.user)) != -1:
						UserMSG.append({"content": MSG.content, "role": "assistant"})
					else:
						UserMSG.append({"content": f"{str(MSG.guild)}.{str(MSG.channel)}{str(MSG.author.display_name)}： {MSG.content}", "role": "user"})	
	
			else:
				UserMSG.append({"content": f"{str(message.guild)}.{str(message.channel)}{str(message.author.display_name)}： {message.content}", "role": "user"})	
	
			UserMSG.reverse()
			prompt = prompt + UserMSG
			#print(prompt)
			Str = ollama(message=prompt)
			await message.reply(Str)
			print(f"[{self.Get_Time()}] Reply message to {str(message.guild)}.{str(message.channel)}.{message.author.display_name}: {str(Str)}")
	
		

	utc = timezone.utc
	times = [
		time(hour=0, tzinfo=utc),
		time(hour=8, tzinfo=utc),
		time(hour=16, tzinfo=utc)
	]
	#Reflash CharacterAI
	@tasks.loop(time=times)
	async def Reflash_CharacterAI(self):
		await self.CloseSelf()

	async def CloseSelf(self):
		try:
			await self.close()
		except:
			pass
		finally:
			exit()

	#獲取時間
	def Get_Time(self):
		dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
		dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
		return dt2.strftime("%Y-%m-%d %H:%M:%S")
			
def bot1(Token):
	intents		= discord.Intents.default()
	intents.message_content = True
	intents.members = True
	bot = MyBot(command_prefix="/", intent=intents)
	bot.run(Token)
	
if __name__ == '__main__':
	bot1("FuckOff")
	
