from binascii import hexlify, unhexlify
from bitstring import BitArray as ba
import sys

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
	def parseCourse(self, data):
		courseDict = {0:'Mario Circuit', 1:'Rock Rock Mountain / Alpine Pass', 2:'Cheep Cheep Lagoon / Cheep Cheep Cape', 3:'Daisy Hills', 4:'Toad Circuit', 5:'Shy Guy Bazaar', 6:'Neo Bowser City / Koopa City', 7:'DK Jungle', 8:'Wuhu Loop / Wuhu Island Loop', 9:'Maka Wuhu / Wuhu Mountain Loop', 10:'Rosalinas Ice World', 11:'Bowsers Castle', 12:'Piranha Plant Slide / Piranha Plant Pipeway', 13:'Rainbow Road', 14:'Wario Shipyard / Warios Galleon', 15:'Music Park / Melody Motorway', 16:'Wii Coconut Mall', 17: 'Wii Koopa Cape', 18: 'Wii Maple Treeway', 19: 'Wii Mushroom Gorge', 20: 'DS Luigis Mansion', 21: 'DS Airship Fortress', 22: 'DS DK Pass', 23: 'DS Waluigi Pinball', 24: 'GCN Dino Dino Jungle', 25: 'GCN Daisy Cruiser', 26: 'N64 Luigi Raceway', 27: 'N64 Kalimari Desert', 28: 'N64 Koopa Beach / N64 Koopa Troopa Beach', 29: 'GBA Bowser Castle 1', 30: 'SNES Mario Circuit 2', 31: 'SNES Rainbow Road', 32: 'Wuhu Town', 33: 'Honeybee Hive / Honeybee House', 34: 'Sherbet Rink', 35: 'DS Palm Shore', 36: 'N64 Big Donut', 37: 'GBA Battle Course 1', 38: 'Toad Circuit (Grand Prix winning cutscene)'}
		return courseDict.get(data, None)
	def parseCourseLapType(self, data):
		courseLapTypeDict = {0:'Section-based course (Beta)', 1:'Section-based course', 3:'Lap-based course'}
		return courseLapTypeDict.get(data, None)
	def __init__(self, data):
		ghost_file = bytearray(data)
		timele = ghost_file[0x8:0x12]
		timele.reverse()
		timele = ba(timele)
		headerle = ghost_file[0x7:0x17]
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
		self.kartID = headerle[9:13].uint
		self.kart = self.parseKart(self.kartID)
		self.characterID = headerle[13:18].uint
		self.character = self.parseCharacter(self.characterID)
		self.courseID = headerle[18:24].uint
		self.course = self.parseCourse(self.courseID)
		#self.mii = data[0x30:0x8c]
		self.country = data[0x90]
		self.region_coordinates = ba(data[0x94:0x98])
		#self.region_coordinates.reverse()
		self.crc32 = ba(data[0x2898:0x289C])

		self.first_person = bool((ghost_file[0x07] << 4) >> 7)
		self.courseLapType = self.parseCourseLapType((ghost_file[0x07] << 5) >> 5)
		revision_byte_array = ghost_file[0x9c:0x9f]
		revision_byte_array.reverse()
		self.revision = ba(revision_byte_array)

		self.unk_4 = ghost_file[0x07] >> 4
		self.unk_8 = ghost_file[0x0B] >> 7
		self.unk_C = ghost_file[0x0F] >> 7
		unk_10_byte_array = ghost_file[0x11:0x14]
		unk_10_byte_array.reverse()
		unk_10_byte_array = ba(unk_10_byte_array)
		self.unk_10 = unk_10_byte_array >> 2
		self.unk_14 = ghost_file[0x17]
		self.unk_2C = ba(ghost_file[0x2c:0x30])
		self.unk_98 = ba(ghost_file[0x98:0x9c])
		self.unk_a0 = ba(ghost_file[0xa0:0xc0])




filename = sys.argv[1]
f = open(filename, 'rb')
ghost = MK7Ghost(f.read())

print(f'Mii Name: {ghost.miiName}')
print(f'Finish Time: {ghost.finishTime}')
print(f'Lap splits: {ghost.laps[2]} | {ghost.laps[1]} | {ghost.laps[0]}')
print(f'Course: {ghost.course}')
print(f'Course lap type: {ghost.courseLapType}')
print(f'Character: {ghost.character}')
print(f'Kart: {ghost.kart}')
print(f'Tires: {ghost.tires}')
print(f'Glider: {ghost.glider}')
print(f'Country ID: {ghost.country}')
print(f'Region coordinates (in 32 bit little endian): {ghost.region_coordinates}')
print(f'Raced in 1st person 80% of the time?: {ghost.first_person}')
print(f'Ghost file revision number?: {ghost.revision}')
print(f'CRC32 (in 32 bit little endian): {ghost.crc32}')
print('\n')
print(f'Unknown 0x04 (4 bits): {ghost.unk_4}')
print(f'Unknown 0x08 (1 bit): {ghost.unk_8}')
print(f'Unknown 0x0C (1 bit): {ghost.unk_C}')
print(f'Unknown 0x10 (22 bits): {ghost.unk_10}')
print(f'Unknown 0x14 (8 bits): {ghost.unk_14}')
print(f'Unknown 0x2C (32 bits): {ghost.unk_2C}')
print(f'Unknown 0x98 (32 bits): {ghost.unk_98}')
print(f'Unknown 0xA0 (0x20 bytes): {ghost.unk_a0}')
