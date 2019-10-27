import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
import CooperData
import pyowm
from googletrans import Translator
from CooperData import *


opts = {
    "alias": ('купер','куп','купердяй','купертяй','ку','куппи',
              'купик','куб','копер','кипр','cooper', 'супер', 'кучер'),
    "tbr": ('назови', 'скажи','расскажи','покажи','сколько','произнеси', 'раскажи про'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "music": ('включи музыку','воспроизведи аудио','включи что-то'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты', 'расскажи еще'),
        "statecity": ('погоду', 'температуру'),
        "random": ('рандомное число', 'случайное число', 'любое число'),
        "trnslt": ('переведи фразу', 'переведи слово', 'перевод')
    }
}


def speak(what):
	print(what)
	speak_engine.say(what)
	speak_engine.runAndWait()
	speak_engine.stop()

def callback(recognizer, audio):
	try:
		global voice
		voice = recognizer.recognize_google(audio, language = 'ru-RU').lower()
		print('[log] Распознано: ' + voice)
			
		if voice.startswith(opts['alias']):
			cmd = voice
				
			for x in opts['alias']:
				cmd = cmd.replace(x, '').strip()
					
			for x in opts['tbr']:
				cmd = cmd.replace(x, '').strip()
				
			cmd = recognize_cmd(cmd)
			execute_cmd(cmd['cmd'])
				
	except sr.UnknownValueError:
		print('[log] Голос не распознан!')
	except sr.RequestError as e:
		print("[log] Неизвестная ошибка, проверьте подключение к интернету!")
			
def recognize_cmd(cmd):
	RC = {'cmd':'', 'percent':0}
	for c,v in opts['cmds'].items():
			
		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt
					
	return RC

def execute_cmd(cmd):
	vc = voice.split(' ')
	translator = Translator()
	
	if cmd == 'ctime':
		now = datetime.datetime.now()
		speak('Сейчас ' + str(now.hour) + ":" + str(now.minute))
		
			
	elif cmd == 'stupid1':
		speak(random.choice(anecdots))

			
	elif cmd == 'music':
		os.system("C:\\Users\\User\\Music\\%s" % random.choice(Music))
		
	elif cmd == 'statecity':
		if 'городе' in vc:
			txt = vc[voice.split(' ').index('городе')+1]
			tr_txt = translator.translate(txt, src='ru', dest='en')

		owm = pyowm.OWM('d248c802000831e43e1598b670a1bcba')
		observation = owm.weather_at_place(str(tr_txt.text))
		w = observation.get_weather()
		temperature = w.get_temperature('celsius')['temp']
		tr_stat = translator.translate(str(w.get_detailed_status()), src='en', dest='ru') 
		speak('В городе ' + str(txt.capitalize()) + ' сейчас температура ' + str(temperature) + ' по Цельсию.\nТакже, в указаном городе ' +  str(tr_stat.text))
		
	elif cmd == 'random':
		if 'от' in vc and 'до' in vc:
			ot = vc[voice.split(' ').index('от')+1]
			do = vc[voice.split(' ').index('до')+1]
			speak('Ваше число ' + str(int(random.randint(int(ot), int(do)))))
		speak('Это число ' + str(random.randint(0, 100)))
			
# не уверен будет ли работать, пока не тестил!
	elif cmd == 'trnslt':
		if 'слова' in vc and 'фразы' in vc:
			phrase = int(vc.index('фразу'))
			word = int(vc.index('слова'))
			if phrase < word:
				speak(str(vc[word].title()) + ' это не фраза а слово!')
				
			speak('Перевод вашего слова это "%s"' % str(translator.translate('фразы').text))
		
		if 'слова' in vc:
			word = vc[voice.split(' ').index('слова')+1]
			speak('Перевод вашего слова это "%s" ' % str(translator.translate(word).text))
			
		if 'фразы' in vc:
			phrase = vc[voice.split(' ').index('фразы')]
			ph = vc[phrase:]
			speak('Перевод вашей фразы это "%s" ' % str(translator.translate(ph).text))
# ---------	
	else:
		print('Команда не распознана, повторите!')
			
			
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
	 
with m as source:
	r.adjust_for_ambient_noise(source)
	 
speak_engine = pyttsx3.init()
	 
# голоса для синтеза речи!
# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[4].id)
	 

	 
speak("Добрый день, повелитель")
speak("Купер слушает")
	 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop
