# -*- coding: cp860 -*-
import os, glob, copy
from libraries import *

RoomsPath = './rooms/'
RoomValidExt = '.txt'

if os.path.isdir(RoomsPath) is False:
 os.mkdir(RoomsPath)

def GetDicOfRooms():
 roomfiles = glob.glob(RoomsPath + '*' + RoomValidExt)
 roomfilesB = copy.copy(roomfiles)

 for n, i in enumerate(roomfilesB):
  a = i.replace(RoomsPath,'')
  b = a.replace(RoomValidExt,'')
  roomfilesB[n] = b

 for n, i in enumerate(roomfilesB):
  try:
   int(i)
  except ValueError:
   roomfilesB.pop(n)
   roomfiles.pop(n)

 RoomsDic = {}

 for i in roomfiles:
  roomread = open(i,"r")
  thisroom = roomread.readlines()
  roomread.close()
  for i in thisroom:
   thisroom[0] = thisroom[0].replace('\n','')
   thisroom[1] = thisroom[1].replace('\n','')
   thisroom[2] = thisroom[2].replace('\n','')
  RoomsDic[thisroom[0]] = thisroom[1:]

 return RoomsDic

def ShowRoom(RoomsList, RoomNumber):
 print prcolor(6, RoomsList[RoomNumber][1])
 print '[ Exits: ' + prcolor(7,' '.join(list(RoomsList[RoomNumber][0]))) + ' ]'
 print ' '.join(RoomsList[RoomNumber][2:])

ShowRoom(GetDicOfRooms(),'1')
