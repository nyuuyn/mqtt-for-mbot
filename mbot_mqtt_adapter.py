from lib.mBot import *
import paho.mqtt.client as mqtt

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

client = mqtt.Client()
bot = mBot()

if __name__ == '__main__':
	client.on_connect=on_connect
	client.on_message=on_message
	client.connect("localhost",1883,60)
	client.loop_start()
	client.subscribe("mbot/command")

	bot.startWithSerial("/dev/tty.Makeblock-ELETSPP")
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
