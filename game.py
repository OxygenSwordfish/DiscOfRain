import enemy

inFight = False
inBoss = False

class GameLoop:
  def __init__(self):
    self.curEnv = 0
    self.curLev = 0
    self.curTic = 0

    self.gameInit = False
    self.gameReady = False
    self.playerCount = 0  

    self.inFight = False
    self.inBoss = False

    
  def tickUp(self):
    if(self.curTic < 5):
     self.curTic += 1
    else:
      self.difUp(self)
      self.curTic = 0
    return

  def difUp(self):
    if(self.curLev < 99):
      self.curLev += 1
    return

  def gInit(self,r):
    self.gameInit = r
    return
  
  def startFight(self, cE: enemy.Enemy):
    cE.hp += (cE.hl * self.curLev)
    cE.at += (cE.al * self.curLev)
    return
