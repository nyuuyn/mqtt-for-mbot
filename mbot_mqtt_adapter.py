from lib.mBot import *
import paho.mqtt.client as mqtt
import sys

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	print("Received message:")
	print(msg.topic + " " +str(msg.payload))
	if(str(msg.topic).startswith("mbot/command")):
		if(str(msg.payload).startswith("doMove")):
			split = str(msg.payload).split(",")
			leftVal = float(split[1])
			rightVal = float(split[2])
			cmdDoMove(leftVal,rightVal)


def cmdDoMove(leftVal,rightVal):
	bot.doMove(leftVal,rightVal)
	sleep(commandtimeout)

def onLight(value):
	print "light = ",value
	client.publish("mbot/light",value)

def onDistance(value):
	print "distance = ",value
	client.publish("mbot/distance",value)


sensortimeout = 2.0
commandtimeout = 0.5
mqtt_host = "localhost"
mqtt_port = 1883
mqtt_keepalive = 60
usb_serial = "/dev/ttyUSB0"

client = mqtt.Client()
bot = mBot()

def substring_after(s, substring):
	return s.partition(substring)[2].strip()

def parse_arg(argv):
	for arg in argv:
		if str(arg).startswith("mqtt_host="):
			if substring_after(arg,"mqtt_host="):
				mqtt_host = substring_after(arg,"mqtt_host=")
		if str(arg).startswith("mqtt_port="):
			if substring_after(arg,"mqtt_port="):
				mqtt_port = substring_after(arg,"mqtt_port=")
		if str(arg).startswith("usb_serial="):
			if substring_after(arg,"usb_serial="):
				usb_serial = substring_after(arg,"usb_serial=")

def main(argv):
	parse_arg(argv)
	client.on_connect=on_connect
	client.on_message=on_message
	client.connect(mqtt_host,mqtt_port,mqtt_keepalive)
	client.loop_start()
	client.subscribe("mbot/command")

	bot.startWithSerial(usb_serial)
	#bot.startWithHID()
	while(1):
		bot.requestLightOnBoard(1,onLight)
		sleep(sensortimeout)
		bot.requestUltrasonicSensor(1,3,onDistance)
		sleep(sensortimeout)
		#sleep(0.5)
		#bot.doMove(100,100)
		#sleep(5)
		#bot.doMove(0,0)
		#sleep(5)

if __name__ == '__main__':
	main(sys.argv[1:])
