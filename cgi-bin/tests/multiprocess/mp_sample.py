import multiprocessing as mp
import time
import sys
import tty
import termios
import os

def get_ch():
	fd=sys.stdin.fileno()
	old_settings=termios.tcgetattr(fd)
	
	try:
		tty.setraw(sys.stdin.fileno())
		ch=sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return ch


def getKey():
	fd=sys.stdin.fileno()
	old=termios.tcgetattr(fd)
	new=termios.tcgetattr(fd)
	new[3]=new[3] & ~termios.ICANON & ~termios.ECHO
	new[6][termios.VMIN]=1
	new[6][termios.VTIME]=0
	termios.tcsetattr(fd,termios.TCSANOW,new)
	key=new

	try:
		key=os.read(fd,3)
	finally:
		termios.tcsetattr(fd,termios.TCSAFLUSH,old)

	print "key was captured="+str(key)
	return key

def getKey2():
	key=sys.stdin.read(1)
	print "key="+str(key)		

def worker():
	
	while True:
		print "Idle state"
		time.sleep(2)

p=mp.Process(target=worker)
p.start()
getKey()
#p.terminate()	