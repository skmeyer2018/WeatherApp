from meta_ai_api import MetaAI
import tkinter as Tk
import re
import pandas as pd
import csv

from tkinter import *
from tkinter import scrolledtext
from tkinter import PhotoImage
from PIL import ImageTk, Image
from datetime import datetime
import time
from GetInfoClass import getInfo
presentdatetime=datetime.now()
weather_headers=['YEAR','MONTH','DATE','HOUR', 'MINUTE', 'DEGREES','DESCRIPTION']

lst_weather=[]

def get_weather():
	infoBox.config(state="normal")
	infoBox.delete("1.0","end")
	location_request=request_box.get()
	city_name=''.join(list(location_request.split(' ')))
	weather_filename=city_name + "WeatherData.csv"
	###
	with open(weather_filename, mode='w') as csv_file:
		writer=csv.DictWriter(csv_file, fieldnames=weather_headers)
		writer.writeheader()
	##
	request_prompt=weather_phrase + location_request + ". "
	request_prompt += "For each day create a set of key value pairs for the items: date, high, low, description.  Include all key names."
	response = ai.prompt(message=request_prompt)
	mssg=""
	resp = getInfo(request_prompt,mssg)
	mssg=response["message"]
	#resp.get_response(request_prompt)
	today_pos=mssg.find("Today")
	mssg=mssg[today_pos:]
	#print(mssg)
	future_cast=[]
	report_lines=mssg.split("\n")
	weather_day={}
	for l in report_lines:
		if ':' not in l:
			future_cast.append(weather_day)
			weather_day={}
			continue
		weather_pair=l.split(':')
		weather_day[weather_pair[0]]=weather_pair[1]
	future_cast.pop(0)
	print("YOUR FUTURE CAST IN THE DICTIONARY:")	
	print(future_cast)
	weather_events=["cloud","rain","snow","sun","thunder","wind"]
	for i in range(len(future_cast)):
		try:
		 desc=future_cast[i]["Description"].lower()
		 print(desc)
		 for evt in weather_events:
		  print(f"is {evt} in {desc}? ")
		  print(evt in desc)
		  if evt in desc:
		   print(f"{evt}.jpg")
		   if evt == "sun":
		    weather_pic1["image"]=sunpic
		   elif evt == "cloud":
		    weather_pic1["image"]=cloudpic
		   elif evt == "rain":
		    weather_pic1["image"]=rainpic
		   elif evt == "wind":
		    weather_pic1["image"]=windpic
		   else:
		    weather_pic1["image"]=snowpic
		   break
		except:
		 pass
	presenttime=str(time.ctime())
	presentdate=presentdatetime.strftime('%m-%d-%Y')
	weather_record=[]
	present_year=presentdatetime.strftime('%Y')
	present_month=presentdatetime.strftime('%m')
	present_date=presentdatetime.strftime('%d')
	present_hour=presentdatetime.strftime('%H')
	present_minute=presentdatetime.strftime('%M')
	#print(mssg)
	#mssg=  mssg + "\n\r" + presenttime
	#print(report)
	infoBox.insert(END,mssg + "\n\r" + presenttime)
	city_label['text']=location_request
	#weather_pic1['image']=sunpic
	weather_keys=list(future_cast[0].keys())
	print(weather_keys[0])
	weather_day1_label['text']=future_cast[0]['Date']
	weather_day2_label['text']=future_cast[1]['Date']
	weather_day3_label['text']=future_cast[2]['Date']
	weather_day4_label['text']=future_cast[3]['Date']
	high_day1_label['text']=future_cast[0]['High']
	high_day2_label['text']=future_cast[1]['High']
	high_day3_label['text']=future_cast[2]['High']
	high_day4_label['text']=future_cast[3]['High']
	low_day1_label['text']=future_cast[0]['Low']
	low_day2_label['text']=future_cast[1]['Low']
	low_day3_label['text']=future_cast[2]['Low']
	low_day4_label['text']=future_cast[3]['Low']


	try:
		#temp_display.delete("1.0","end")
		#temp_display.insert(END, get_temp(resp.response))
		#weather_record.extend([present_year, present_month, present_date, present_hour,present_minute,get_temp(resp.response),resp.response])
		dict_weather_record={"YEAR": present_year , "MONTH": present_month , "DATE": present_date , "HOUR": present_hour , "MINUTE": present_minute ,"DEGREES": get_temp(resp.response) ,"DESCRIPTION": resp.response }
		print(dict_weather_record)
		print ("JUST TRIED TO PRINT LST_WEATHER")
		lst_weather.append(dict_weather_record)
		print(pd.DataFrame.from_dict(lst_weather))
		#self.weather_pic1['image']=sunpic
		#if monitor_button.cget('state') == tk.DISABLED:
			
		#master.after(30000,get_weather)

	except:
		print("INDECIPHERABLE INFORMATION -- CANNOT PROCESS WEATHER RECORD")

	

def get_temp(phrase):
	try:

		degrees=re.findall(r'\d+',phrase)
		print("DEGREES: " + str(degrees[0]))
		return str(degrees[0])
	except:
		pass

def monitor_for_updates():
	monitor_button.config(state=DISABLED)
	stop_monitor.config(state=NORMAL)
	get_weather()
	master.after(1800000,monitor_for_updates)
	if monitor_button.cget('state') == NORMAL:
		return 


def stop_monitoring():
	monitor_button.config(state=NORMAL)
	stop_monitor.config(state=DISABLED)			
		

ai = MetaAI()

weather_phrase="List for today and the next three days of weather forecast in " 


master=Tk()
master.geometry("1000x700")
master.config(bg="#ccddee")
master.title("Your quick weather information app")
request_label=Label(master, text="Where would you like your weather information?", font=("Arial",14,"bold"), bg="#ccddee")
request_label.pack()
request_box=Entry(master, width=80)
request_box.pack()
get_button=Button(master, text="GET YOUR WEATHER", command=get_weather)
get_button.pack()

infoBox=scrolledtext.ScrolledText(master,height=15,width=50, fg="darkgreen")
infoBox.configure(font=("Arial",12,"bold"))
infoBox.place(x=350, y=70)
city_label=Label(master, text=request_box.get(), font=("Arial",20,"bold"),fg="#0000ff", bg="#ccddee")
city_label.place(x=90,y=370)
#temp_display=Text(master,height=0.5,width=3,font=("Arial",40,"bold"),bg="black",fg="#00ffaa")
#temp_display.place(x=350,y=370)
sunpic=ImageTk.PhotoImage(Image.open("sun.jpg").resize((50,50)))
cloudpic=ImageTk.PhotoImage(Image.open("cloud.jpg").resize((50,50)))
snowpic=ImageTk.PhotoImage(Image.open("snow.jpg").resize((50,50)))
windpic=ImageTk.PhotoImage(Image.open("wind.jpg").resize((50,50)))
rainpic=ImageTk.PhotoImage(Image.open("rain.jpg").resize((50,50)))
weather_pic1=Label(master,height=80, width=80)
weather_pic2=Label(master,height=80, width=80)
weather_pic3=Label(master,height=80, width=80)
weather_pic4=Label(master,height=80, width=80)

#weather_pic1['image']=sunpic
weather_pic1.place(x=80,y=510)
weather_pic1.config(bg="#ccddee")
temp_high_label=Label(master, font=("Arial",13,"bold"))
temp_high_label.place(x=50,y=460)
temp_high_label["text"]="HIGH"
temp_low_label=Label(master, font=("Arial",13,"bold"))
temp_low_label.place(x=50,y=500)
temp_low_label["text"]="LOW"
weather_day1_label=Label(master, font=("Arial",12,"bold"))
weather_day2_label=Label(master, font=("Arial",12,"bold"))
weather_day3_label=Label(master, font=("Arial",12,"bold"))
weather_day4_label=Label(master, font=("Arial",12,"bold"))
weather_day1_label.place(x=100, y=420)
weather_day2_label.place(x=250, y=420)
weather_day3_label.place(x=400, y=420)
weather_day4_label.place(x=550, y=420)
high_day1_label=Label(master, font=("Arial",12))
high_day2_label=Label(master, font=("Arial",12))
high_day3_label=Label(master, font=("Arial",12))
high_day4_label=Label(master, font=("Arial",12))
high_day1_label.place(x=100, y=460)
high_day2_label.place(x=250, y=460)
high_day3_label.place(x=400, y=460)
high_day4_label.place(x=550, y=460)

low_day1_label=Label(master, font=("Arial",12))
low_day2_label=Label(master, font=("Arial",12))
low_day3_label=Label(master, font=("Arial",12))
low_day4_label=Label(master, font=("Arial",12))
low_day1_label.place(x=100, y=500)
low_day2_label.place(x=250, y=500)
low_day3_label.place(x=400, y=500)
low_day4_label.place(x=550, y=500)


description_day1=scrolledtext.ScrolledText(master,height=3,width=5, fg="black")
description_day2=scrolledtext.ScrolledText(master,height=3,width=5, fg="black")
description_day3=scrolledtext.ScrolledText(master,height=3,width=5, fg="black")
description_day4=scrolledtext.ScrolledText(master,height=3,width=5, fg="black")

monitor_button=Button(master, text="MONITOR", command=monitor_for_updates)
monitor_button.place(x=350, y=600)
stop_monitor=Button(master, text="STOP MONITOR", command=stop_monitoring, state=DISABLED)
stop_monitor.place(x=350, y=650)
mainloop()
