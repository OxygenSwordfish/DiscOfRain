class Enemy:
  def __init__(self, eName, HP, hpL, ATK, atkL):
    self.n = eName
    self.hp = HP
    self.hl = hpL
    self.at = ATK
    self.al = atkL

  

enemies=[Enemy("Lesser Wisp", 35, 10, 3.5, 0.7), Enemy("Beetle", 80, 24, 12, 2.4), Enemy("Lemurian", 80, 24, 12, 2.4), Enemy("Stone Golem", 480, 144, 20, 4),Enemy("Greater Wisp", 750, 225, 15, 3), Enemy("Beetle Guard", 480, 144, 12, 2.4), Enemy("Alloy Vulture", 140, 42, 15, 3), Enemy("Stone Golem", 480, 144, 20, 4), Enemy("Bighorn Bison", 480, 144, 12, 2.4), Enemy("Brass Contraption ", 300, 90, 10, 2), Enemy("Clay Templar", 700, 210, 16, 3.2), Enemy("Elder Lemurian", 900, 270, 16, 3.2), Enemy("Hermit Crab", 100, 30, 12, 2.4), Enemy("Imp", 140, 42, 10, 2), Enemy("Jellyfish", 60, 18, 5, 1), Enemy("Mini Mushrum", 290, 87, 16, 3.2), Enemy("Parent", 585, 176, 16, 3.2), Enemy("Solus Probe", 220, 66, 15, 3)]

bosses=[Enemy("Beetle Queen", 2100, 630, 25, 5), Enemy("Clay Dunestrider", 2100, 630, 20, 4), Enemy("Stone Titan", 2100, 630, 40, 8), Enemy("Grovetender", 2800, 840, 23, 4.6), Enemy("Mithrix", 1000, 300, 16, 3.2), Enemy("Aurelionite", 2100, 630, 40, 8), Enemy("Wandering Vagrant", 2100, 630, 6.5, 1.3), Enemy("Magma Worm", 2400, 720 , 10, 2), Enemy("Imp Overlord", 2800, 840, 16, 3.2), Enemy("Overloading Worm", 12000, 3600, 50, 10), Enemy("Alloy Worship Unit", 2500, 750, 15, 3)]

def bosscheck():
  #Get stage bosses
  #choose stage boss
  #Run fight loop
  #victory or defeat
  #distribute items or end run  
  return