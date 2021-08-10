from binascii import hexlify, unhexlify
from bitstring import BitArray as ba

class MK7GhostException(Exception):
	pass
class MK7Ghost:
	def parseFinish(self, data):
		data = bytearray(data)
		data.reverse()
		data = ba(data)
		Minutes = data[17:24].uint
		Seconds = data[10:17].uint
		Milliseconds = data[0:10].uint 
		return f'{str(Minutes).zfill(2)}:{str(Seconds).zfill(2)}.{str(Milliseconds).zfill(3)}'
	def parseLaps(self, Minutes, Seconds, Milliseconds):
		return f'{str(Minutes).zfill(2)}:{str(Seconds).zfill(2)}.{str(Milliseconds).zfill(3)}'
	def parseGlider(self, data):
		gliderDict = {0:'Super Glider', 1:'Paraglider', 2:'Peach Parasol', 3:'Flower Glider', 4:'Swooper', 5:'Beast Glider', 6:'Gold Glider'}
		return gliderDict.get(data, None)
	def parseTires(self, data):
		tireDict = {0:'Standard', 1:'Monster', 2:'Roller', 3:'Slick', 4:'Slim', 5:'Sponge', 6:'Gold Tires', 7:'Wood', 8:'Red Monster', 9:'Mushroom'}
		return tireDict.get(data, None)
	def parseCharacter(self, data):
		characterDict = {0:'Bowser', 1:'Daisy', 2:'Donkey Kong', 3:'Honey Queen', 4:'Koopa Troopa', 5:'Lakitu', 6:'Luigi', 7:'Mario', 8:'Metal Mario', 9:'Male Mii', 10:'Female Mii', 11:'Peach', 12:'Rosalina', 13:'Shy Guy', 14:'Toad', 15:'Wario', 16:'Wiggler', 17:'Yoshi'}
		return characterDict.get(data, None)
	def parseKart(self, data):
		kartDict = {0:'Standard', 1:'Bolt Buggy', 2:'Birthday Girl', 3:'Egg 1', 4:'B Dasher', 5:'Zucchini', 6:'Koopa Clown', 7:'Tiny Tug', 8:'Bumble V', 9:'Cact-X', 10:'Bruiser', 11:'Pipe Frame', 12:'Barrel Train', 13:'Cloud 9', 14:'Blue Seven', 15:'Soda Jet', 16:'Gold Standard'}
		return kartDict.get(data, None)
	def __init__(self, data):
		headerle = bytearray(data)
		timele = headerle[0x8:0x12]
		timele.reverse()
		timele = ba(timele)
		headerle = headerle[0x7:0x17]
		headerle.reverse()
		headerle = ba(headerle)
		self.header = data[0x0:0x4].decode('ascii') #always DGDC
		self.miiName = data[0x18:0x2c].decode('utf-16le') #10 characters long
		self.finishTime = self.parseFinish(data[0x4:0x7])
		self.laps = [self.parseLaps(timele[24:31].uint, timele[17:24].uint, timele[6:16].uint), self.parseLaps(timele[48:56].uint, timele[41:48].uint, timele[31:41].uint), self.parseLaps(timele[73:80].uint, timele[66:73].uint, timele[56:66].uint)]
		self.gliderID = headerle[0:4].uint
		self.glider = self.parseGlider(self.gliderID)
		self.tireID = headerle[4:8].uint
		self.tires = self.parseTires(self.tireID)
		self.kartID = headerle[8:12].uint
		self.kart = self.parseKart(self.kartID)
		self.characterID = headerle[12:18].uint
		self.character = self.parseCharacter(self.characterID)
		#self.mii = data[0x30:0x8c]
		self.country = data[0x90]
		self.crc32 = data[0x2898:0x289C]




f = open('replay05.dat', 'rb')
ghost = MK7Ghost(f.read())

print(f'Mii Name: {ghost.miiName}')
print(f'Finish Time: {ghost.finishTime}')
print(f'Lap splits: {ghost.laps[2]} ~ {ghost.laps[1]} ~ {ghost.laps[0]}')
print(f'Character: {ghost.character}')
print(f'Kart: {ghost.kart}')
print(f'Tires: {ghost.tires}')
print(f'Glider: {ghost.glider}')
print(f'Country ID: {ghost.country}')

