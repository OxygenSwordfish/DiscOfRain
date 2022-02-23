import discord
import os
import csv
import random
import game
import enemy

client = discord.Client()

curEnemy = enemy.Enemy("",0,0,0,0)
runGame = game.GameLoop()

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('-chest'):
    if(runGame.gameReady == False):
      checkID = str(message.author.id)
      if(inGame(checkID)):
        itemget = chestroll()

        invCheck(checkID, itemget)

   # if(os.getenv(checkID)):
   #   await message.channel.send(chestroll())
      await message.channel.send(message.author.name + ' picked up '+(os.getenv(itemget)).split(',')[0])
      runGame.tickUp()
    await message.delete()
   # else:
    #  os.environ[checkID] = "User inventory Initialised"
    #  await message.channel.send(os.getenv(checkID))
  if message.content.startswith('-inventory'):
    checkID = str(message.author.id)
    if(inGame(checkID)):
      userInv = invpull(checkID)

      await message.channel.send(message.author.name + ' is carrying: ' + userInv)
    await message.delete()
  if message.content.startswith('-lockbox'):
    checkID = str(message.author.id)
    if(inGame(checkID)):
      if(rustyKey(checkID)):
        itemget = bigroll()

        invCheck(checkID, itemget)

        await message.channel.send(message.author.name + ' picked up ' +(os.getenv(itemget)))
    
      else:
       await message.channel.send(message.author.name + 'has no rusted keys in their inventory')
    await message.delete()   

    

  if message.content.startswith('-newgame'):
    if(startGame()):
      await message.channel.purge()
      await message.channel.send("New game is ready! type '-join' to take part")
      
  if message.content.startswith('-cancelgame'):
    cancelGame()
    await message.channel.purge()
    await message.channel.send("Game cancelled")
  
  if message.content.startswith('-join'):
    if(runGame.playerCount < 4):
      checkID = str(message.author.id)
      if(joinGame(checkID)):
        await message.channel.send(message.author.name + ' joined!')
        runGame.playerCount += 1
    else:
      await message.channel.send("Game Full!")
    await message.delete()
    
  if message.content.startswith('-leave'):
    if(runGame.playerCount>0):
      checkID = str(message.author.id)
      if(leaveGame(checkID)):
        await message.channel.send(message.author.name + ' left!')
        runGame.playerCount -= 1
    await message.delete()

  if message.content.startswith('-gamestart'):
    with open("playerList.csv") as pList:
      if(sum(1 for row in pList)>0):
        await message.channel.send("Game starting...")
        curEnv = 1
       
      else:
        await message.channel.send("Someone tried to start with no players in the lobby")
    await message.delete()

  if message.content.startswith('-fight'):
    if(runGame.inFight==False):
      curEnemy = enemy.enemies[(random.randint(0,len(enemy.enemies)-1))]
      runGame.inFight = True
      await message.channel.send(message.author.name + ' encountered a ' + curEnemy.n)
    await message.delete()
    await fight(curEnemy, message)
      
  if message.content.startswith('-boss'):
    if(runGame.inFight==False):
      if(runGame.inBoss==False):
        curEnemy = enemy.bosses[(random.randint(0,len(enemy.bosses)))]
        runGame.inFight = True
        runGame.inBoss = True
      await message.channel.send(curEnemy.n + ' came forth from the teleporter!')
    await message.delete()   


async def fight(cE: enemy.Enemy, message):
  runGame.startFight(cE)
  party = startFight()
  
  while runGame.inFight == True:
    d = 0
    for i in party:
      d += int(i[3])
      
    cE.hp -= d
    await message.channel.send("Dealt " + str(d) + " damage to " + cE.n)
    if(cE.hp <= 0):
      await message.channel.send(cE.n + " defeated!")
      break

    v = random.randint(0, len(party)-1)
   
    vD = int(party[v][4])
    eD = int(cE.at * (1-(vD/(100 + vD))))

    x = int(party[v][2])
    x -= eD
    party[v][2] = str(x)

    vN = await client.fetch_user(int(party[v][0]))
    vN = vN.name
    await message.channel.send(cE.n + " dealt " + str(eD) + " damage to " + vN)
    if(x <= 0):
      await message.channel.send(vN + " died!")
      break
  
################################################################################################################################################################################

#Inventory Management

#Add item to inventory
def invCheck(userID,itemID):
  items=[]
  counts=[]
  
  
  with open ('playerInventories.csv', 'r') as PI:
    reader = csv.reader(PI)
   
    for row in reader:
      print('reading')
      if(row[0]==userID):
        
        print('found ID')
        PI.close()
       
        for i in range(len(row)):
          
          print('reading row index' + str(i))
          if(i>0):
            if(i%2==1):
              items.append(row[i])
              print('item added')
            else:
              counts.append(row[i])
              print('count added')

        print(items)
        print(counts)

        for x in range(len(items)):
          print(items[x])
          print(str(len(items)))
          if(items[x]==itemID):
            print('found item')
                    
            with open('playerInventories.csv', 'r') as PI:
              reader = csv.reader(PI)
              with open('temp.csv', 'w') as temp:
                writer = csv.writer(temp)
                found = False
                for row in reader:
                  if(row[0]==userID):

                    line = []
                    for ind in range(len(row)):
                      if(row[ind]==itemID):
                        found = True
                        current = row[ind]
                      elif(found):
                        found = False
                        current = str(int(row[ind])+1)
                      else:
                        current = row[ind]
                      
                      line.append(current)
                    writer.writerow(line)
                  else:
                    writer.writerow(row)
              temp.close()
            PI.close()

            with open('tempI.csv', 'r') as temp:
              reader = csv.reader(temp)
              with open('playerInventories.csv', 'w') as PI:
                writer = csv.writer(PI)
                for row in reader:
                  writer.writerow(row)
                PI.close()
              temp.close()    
            statMod(userID, itemID)       
            return

          

          elif(x==len(items)-1):
            print('not got item')
            with open('playerInventories.csv', 'r') as PI:
              reader = csv.reader(PI)
              with open('temp.csv', 'w') as temp:
                writer = csv.writer(temp)
                for row in reader:
                  if(row[0]==userID):
                    line = row
                    line.append(itemID)
                    line.append("1")
                    writer.writerow(line)
                  else:
                    writer.writerow(row)
                temp.close()
                PI.close()
            with open('tempI.csv', 'r') as temp:
              reader = csv.reader(temp)
              with open('playerInventories.csv', 'w') as PI:
                writer = csv.writer(PI)
                for row in reader:
                  writer.writerow(row)
                PI.close()
              temp.close()
            statMod(userID, itemID)  
            return
         
          else:
            print('searching')

              


    print('user not listed')
    newline = [userID, itemID, 1]
    with open('playerInventories.csv', 'a') as PI:
      writer = csv.writer(PI)
      writer.writerow(newline)
      PI.close()

    statMod(userID, itemID)
    return

#Get chest items
def chestroll():
  #w23/g49/r68/y79  
  chance = random.randint(0,999)
  if(chance<792):
    itempool=23
    itemoffset=0
  elif(chance<900):
    itempool=26
    itemoffset=23
  else:
    itempool=19
    itemoffset=49

  pooldrop = str(hex(random.randint(0,itempool)+itemoffset))
 
  
  
  return pooldrop

#for getting big chest items
def bigroll():
  #w23/g49/r68/y79  
  chance = random.randint(1,5)
 
  if(chance<5):
    itempool=26
    itemoffset=23
  else:
    itempool=19
    itemoffset=49

  pooldrop = str(hex(random.randint(0,itempool)+itemoffset))
 
  
  
  return pooldrop

#List inventory
def invpull(userID):
  inventory=""
  items=[]
  counts=[]
  
 
  with open ('playerInventories.csv', 'r') as PI:
    reader = csv.reader(PI)
    
    for row in reader:
      if(row[0]==userID):
        print('found ID')
        
       
        for i in range(len(row)):
          
          print('reading row index' + str(i))
          if(i>0):
            if(i%2==1):
              items.append(row[i])
              print('item added')
            else:
              counts.append(row[i])
              print('count added')
        for x in range(len(items)):
          inventory+=(os.getenv(items[x]).split(",")[0] + ' (')
          inventory+=(counts[x]+'), ')
    PI.close()
  return inventory

#Rare item roll
def rustyKey(userID):
  #0x16
  items=[]
  counts=[]
  newcount=0
  gotKey=False
  remove=False
  reduced=False
  removed=False


  with open ('playerInventories.csv', 'r') as PI:
    reader = csv.reader(PI)
    
    for row in reader:
      if(row[0]==userID):
          
        for i in range(len(row)):
          
          print('reading row index' + str(i))
          if(i>0):
            if(i%2==1):
              items.append(row[i])
              
            else:
              counts.append(row[i])
        
      for j in range(len(items)):
        if(items[j]=='0x16'):
          gotKey=True
          if(int(counts[j])>1):
            newcount = int(counts[j])-1
          else:
            remove=True

    if(gotKey):
      line=[]
      with open('tempI.csv', 'w') as temp:
        writer = csv.writer(temp)
        for row in reader:
          if(row[0]==userID):
            for i in range(len(row)):
              if(row[i]=='0x16'):
                if(remove):
                  removed=True
                  continue

                else:
                  reduced=True

              if(removed):
                removed=False
                continue

              elif(reduced):
                reduced=False
                line.append(str(newcount))
                continue
              line.append(row[i])
            writer.writerow(line)
          else:
            writer.writerow(row)
        temp.close()
        PI.close()

      with open('tempI.csv', 'r') as temp:
          reader = csv.reader(temp)
          with open('playerInventories.csv', 'w') as PI:
            writer = csv.writer(PI)
            for row in reader:
              writer.writerow(row)
            PI.close()
          temp.close()
 
      return(True)
    else:
      return(False)


################################################################################################################################################################################

#Game Running
def startGame():
  
  if(runGame.gameInit==False):
    
    runGame.gInit(True)
    
    with open('playerInventories.csv', 'w') as pInv:
      pInv.truncate()
    pInv.close()
    with open('playerList.csv', 'w') as pList:
      pList.truncate()
    pList.close()
  
  return(runGame.gameInit)


def cancelGame():
  if(runGame.gameInit== True):
    runGame.gameInit = False
    runGame.gameReady = False
    runGame.inFight = False
    with open('playerInventories.csv', 'w') as pInv:
      pInv.truncate()
    pInv.close()
    with open('playerList.csv', 'w') as pList:
      pList.truncate()
    pList.close()
  return

def joinGame(userID):

  with open('playerList.csv', 'r') as pList:
    reader = csv.reader(pList)
    for row in reader:
      if(row[0]==userID):
        return(False)
    pList.close()
    with open('playerList.csv', 'a') as pList:
      pList.write(userID + ", 1, 100, 1, 0, 1") #ID, Level, HP, Atk, Def, Heal, GameReady
      pList.close()
  return(True)
    
def leaveGame(userID):

  wasIn = False
  with open('playerList.csv', 'r') as pList:
    reader = csv.reader(pList)
    with open('tempP.csv', 'w') as temp:
      writer = csv.writer(temp)
      for row in reader:
        if(row[0]==userID):
          wasIn = True
        else:
          writer.writerow(row)
    temp.close()
  pList.close()

  if(wasIn):
    with open('tempP.csv', 'r') as temp:
      reader = csv.reader(temp)
      with open('playerList.csv', 'w') as pList:
        writer = csv.writer(pList)
        for row in reader:
          writer.writerow(row)
      pList.close()
    temp.close()
  
  return(wasIn)

def inGame(userID):
  with open('playerList.csv', 'r') as pList:
    reader = csv.reader(pList)
    for row in reader:
      if(row[0]==userID):
        pList.close()
        return(True)
    pList.close()
  return(False)

def statMod(userID, itemID):
  playerStats = []
  itemStats = os.getenv(itemID).split(',')
  with open('playerList.csv', 'r') as pList:
    reader = csv.reader(pList)
    with open('tempP', 'w') as temp:
      writer = csv.writer(temp)
      for row in reader:
        if(row[0]==userID):
          playerStats = row
          playerStats[3]=int(playerStats[3]+itemStats[1])
          playerStats[4]=int(playerStats[4]+itemStats[2])
          playerStats[5]=int(playerStats[5]+itemStats[3])
          writer.writerow(playerStats)
        else:
          writer.writerow(row)
    temp.close()
  pList.close()

  with open('tempP', 'r') as temp:
    reader = csv.reader(temp)
    with open('playerList.csv', 'w') as pList:
      writer = csv.writer(pList)
      for row in reader:
        writer.writerow(row)
    pList.close
  temp.close()
 
  return
  

def startFight():
  p=[]
  with open ('playerList.csv', 'r') as pList:
    reader = csv.reader(pList)
    for row in reader:
      p.append(row)
      
      
  return(p)
  
client.run(os.getenv('TOKEN'))
