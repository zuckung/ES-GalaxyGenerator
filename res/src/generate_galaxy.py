import os
import sys
import math
import random
import requests
import zipfile
import shutil
from PIL import Image, ImageDraw, ImageFont


# 2do
# hang up @ > 624 landable planets, omg why?!
# find out why backlinks get added twice (fixed in rearrange_systemtext), fix it earlier!
# moons
# planet sprites & landing images should fit
# planet texts


# 1 race > lasti referenced before assign


def check_local():
	def download():
		# downloading zip
		print('downloading ES')
		request = requests.get('https://github.com/endless-sky/endless-sky/archive/refs/heads/master.zip', allow_redirects=True, timeout=30)
		if not os.path.isdir('tmp/'):
			os.mkdir('tmp/')
		with open('tmp/continuous.zip', 'wb') as zipped: # creating zip file
			zipped.write(request.content)
		print('    DONE')
		archive = zipfile.ZipFile('tmp/continuous.zip')
		for file in archive.namelist():
			archive.extract(file, 'tmp/')
	# setting variables
	global startPos, systemAmount, starRadius, startWormhole, landPlanets, density, tries, dataFolder
	global imageFolder, galaxyImage, starNames, planetNames, landImages, starTypes, planetTypes
	global usedStarnames, name, newname, writetopath, iFont, sunmax, planetmax, minablemax, races
	usedStarnames = []
	print('checking if local test or github')
	if os.getcwd() == '/storage/emulated/0/Download/mgit/ES-GalaxyGenerator/res/src':
		# for local
		print('	local test detected')
		os.chdir('../../')
		starRadius = 100 # distance from system to system (max 200)
		density = 5 # (default 5) after how many system creations the script tries to restart at the prior systems(max 20, higher means more dead system arm ends)
		tries = 15 # (default 15) how many pos generations tried on every system, before skipping (max 20, also control density, higher means denser)
		iFont = '/system/fonts/Roboto-Regular.ttf'
		imageFolder = '/storage/9C33-6BBD/endless sky/images/' # folder to the ES images (for reading planet sprites)
		dataFolder = '/storage/9C33-6BBD/endless sky/data/' # folder to the ES data (for reading star types)
		name = 'zuckung'
		startPos = 10000, 10000 # position of the first system
		systemAmount = 50 # star systems amount
		landPlanets = 10 # number of landable planets
		races = 6 # max 12, auto-lowers if they cant be placed
		startWormhole = 'Sol' # empty for deactivated | vanilla system name for link: firstsystem-vanillasystem
		galaxyImage = 'sculptor' # copy to plugin/images/ui/sculptor.jpg
		sunmax = 3 # max number ob suns 1-3 max
		planetmax = 5 # max number of non-landable planets 1-
		minablemax = 3 # max number of minables 0-
	else:
		# for github
		print('	github run detected')
		iFont = 'DejaVuSans.ttf'
		imageFolder = 'tmp/endless-sky-master/images/'
		dataFolder = 'tmp/endless-sky-master/data/'
		content = os.environ['ISSUE_INPUT']
		splitted = content.split('\n')
		print('	checking if issue is the right template')
		if splitted[0] == '### Name':
			print('		SUCCESS: Newly created issue is a galaxy generation request.')
			name = splitted[2].strip()
			pos = splitted[6].strip()
			possplit = pos.split(' ')
			startPos = int(possplit[0]), int(possplit[1])
			systemAmount = int(splitted[10].strip())
			landPlanets = int(splitted[14].strip())
			races = int(splitted[18].strip())
			startWormhole = splitted[22].strip()
			sunmax = int(splitted[26].strip())
			planetmax = int(splitted[30].strip())
			minablemax = int(splitted[34].strip())
			galaxyImage = splitted[38].strip()
			starRadius = int(splitted[42].strip())
			density = int(splitted[46].strip())
			tries = int(splitted[50].strip())
			download() # download ES for images & data
		else:
			print("		ABORTING: Newly created issue isn't a galaxy generation request.")
			exit()
	# for both
	print('	setting up more variables, folders, files')
	# create folder for generated files
	if not os.path.isdir('generated'):
		os.mkdir('generated')
	# create writetopath variable
	i = 0
	while os.path.isdir('generated' + os.sep + name + str(i)):
		i +=1
	newname = name + str(i)
	writetopath = 'generated' + os.sep + name + str(i) + os.sep
	# check variables
	check_var()
	# write text file
	os.mkdir(writetopath)
	with open(writetopath + name + str(i) + '.txt', 'w') as file1:
		file1.writelines(name + '\n')
		file1.writelines(str(startPos) + '\n')
		file1.writelines(str(systemAmount) + '\n')
		file1.writelines(str(landPlanets) + '\n')
		file1.writelines(str(races) + '\n')
		file1.writelines(startWormhole + '\n')
		file1.writelines(str(sunmax) + '\n')
		file1.writelines(str(planetmax) + '\n')
		file1.writelines(str(minablemax) + '\n')
		file1.writelines(galaxyImage + '\n')
		file1.writelines(str(starRadius) + '\n')
		file1.writelines(str(density) + '\n')
		file1.writelines(str(tries) + '\n')
	# get wordlists
	with open('res/wordlists' + os.sep + 'nameStars.txt', 'r') as source:
		starNames = source.readlines()
	with open('res/wordlists' + os.sep + 'namePlanets.txt', 'r') as source:
		planetNames = source.readlines()
	with open('res/wordlists' + os.sep + 'starTypes.txt', 'r') as source:
		lines = source.readlines()
		starTypes = [line.strip() for line in lines if not line.startswith('#')]
	with open('res/wordlists' + os.sep + 'planetTypes.txt', 'r') as source:
		lines = source.readlines()
		planetTypes = [line.strip() for line in lines if not line.startswith('#')]
	with open('res/wordlists' + os.sep + 'landingImages.txt', 'r') as source:
		lines = source.readlines()
		landImages = [line.strip() for line in lines if not line.startswith('#')]


def check_var():
	# check for correct parameter, else exit script
	if not os.path.isdir(dataFolder):
		print('error: ES data folder not found!')
		exit()
	if not os.path.isdir(imageFolder):
		print('error: ES images folder not found!')
		exit()
	if not os.path.isfile('res' + os.sep + 'galaxyimages' + os.sep + galaxyImage + '.jpg'):
		print('error: galaxyImage not found!')
		exit()
	if systemAmount > 500:
		print('error: systemAmount is higher than 500!')
		exit()
	elif systemAmount < 2:
		print('error: systemAmount is lower than 2!')
		exit()
	if landPlanets > 500:
		print('error: landPlanets is higher than 500!')
		exit()
	if races > 12:
		print('error: Races is higher than 12!')
		exit()
	if sunmax > 3:
		print('error: SunMax is higher than 3!')
		exit()
	elif sunmax < 1:
		print('error: SunMax is lower than 1!')
		exit()
	if planetmax < 1:
		print('error: PlanetMax is lower than 1!')
		exit()
	if starRadius > 200:
		print('error: star radius is higher thab 200!')
		exit()
	if density > 20:
		print('error: density is higher than 20!')
		exit()
	if tries > 20:
		print('error: tries are higher than 20!')
		exit()
	
		

def write_other_stuff():
	with open(writetopath + 'MapGenStuff.txt', 'w') as target:
		# writing startWormhole script
		if startWormhole != '':
			target.writelines('system "' + startWormhole + '"\n\tadd object "Mysterious Wormhole"\n\t\tsprite planet/wormhole-red\n\t\tdistance 1000\n\t\tperiod 1\n\n')
			target.writelines('wormhole "Mysterious Wormhole"\n\tlink "' + startWormhole + '" "Alcor"\n\tlink "Alcor" "' + startWormhole + '"\n\n')
			target.writelines('planet "Mysterious Wormhole"\n\tspaceport ``\n\tgovernment "Republic"\n\twormhole "Mysterious Wormhole"\n\n')
		# writing galaxy image script
		target.writelines('galaxy "' + galaxyImage + '"\n\tpos ' + str(startPos[0]) + ' ' + str(startPos[1]) + '\n\tsprite "ui/' + galaxyImage + '"\n')


def create_systemtexts():
	def get_system_text(x, y, firstWorm):
		# create the script text for a system
		def get_starsprite():
			starsprite = random.choice(starTypes)
			if os.path.isfile(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'.png'):
				im = Image.open(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'.png')
			elif os.path.isfile(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'+.png'):
				im = Image.open(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'+.png')
			elif os.path.isfile(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'.jpg'):
				im = Image.open(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'.jpg')
			elif os.path.isfile(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'+.jpg'):
				im = Image.open(imageFolder + starsprite.replace('"', '').replace('/', os.sep) +'+.jpg')
			width, height = im.size
			return starsprite, width
		# check for name, prevent multiple use
		if firstWorm != '':
			name = 'Alcor'
		else:
			name = str(random.choice(starNames)).replace('\n', '')
		while name in usedStarnames:
			name = str(random.choice(starNames)).replace('\n', '')
		usedStarnames.append(name)
		# get minables
		minables = ['aluminum', 'copper', 'gold', 'iron', 'lead', 'neodymium', 'platinum', 'silicon', 'silver', 'titanium', 'tungsten', 'uranium']
		minablesstring = ''
		minablemin = 1
		if minablemax == 0:
			minablemin = 0
		for i in range(0, random.randint(minablemin, minablemax)):
			minablesstring = minablesstring + '\tminables ' + random.choice(minables) + ' ' + str(random.randint(6,25)) + ' ' +\
				str(random.randint(3,12)) + '\n' #: minables lead 24 9
		# get objects
		objectsstring = ''
		# stars
		staramount = random.randint(1,sunmax) #add amount stars
		minablesyottrite = ''
		for i in range(1, staramount+1):
			if staramount == 1:
				starsprite = random.choice(starTypes)
				if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
					minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
				objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tperiod ' + str(random.randint(10,15)) + '\n'
			elif staramount == 2:
				if i ==1:
					starsprite, width = get_starsprite()
					if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
						minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
					objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tdistance ' + str(random.randint(width,width + 100))\
					+ '\n\t\tperiod ' + str(random.randint(10,15)) +  '\n'
				else:
					starsprite, width = get_starsprite()
					if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
						minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
					objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tdistance ' + str(random.randint(width,width + 100))\
					+ '\n\t\tperiod ' + str(random.randint(10,15)) + '\n\t\toffset 180\n'
			elif staramount == 3:
				if i ==1:
					starsprite, width = get_starsprite()
					if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
						minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
					objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tdistance ' + str(random.randint(width,width + 100))\
					+ '\n\t\tperiod ' + str(random.randint(10,15)) +  '\n'
				elif i ==2:
					starsprite, width = get_starsprite()
					if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
						minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
					objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tdistance ' + str(random.randint(width,width + 100))\
					+ '\n\t\tperiod ' + str(random.randint(10,15)) + '\n\t\toffset 120\n'
				elif i ==3:
					starsprite, width = get_starsprite()
					if starsprite.startswith('"star/nova') or starsprite.startswith('"star/wr'):
						minablesyottrite += '\tminables yottrite ' + str(random.randint(6,15)) + ' ' + str(random.randint(3,12)) + '\n'
					objectsstring = objectsstring + '\tobject\n\t\tsprite ' + starsprite + '\n' + '\t\tdistance ' + str(random.randint(width,width + 100))\
					+ '\n\t\tperiod ' + str(random.randint(10,15)) + '\n\t\toffset 240\n'
		# planets
		planetmin = 1
		if planetmax == 0:
			planetmin = 0
		planetamount = random.randint(planetmin,planetmax) # add 2 to 5 planets
		objectsstring = objectsstring + firstWorm # add wormhole, only first system gives content, else firstWorm is empty
		for i in range(0, planetamount):
			objectsstring = objectsstring + '\tobject\n\t\tsprite planet/' + random.choice(planetTypes)\
			+ '\n\t\tdistance ' + str(random.randint(600,4000)) + '\n\t\tperiod ' + str(random.randint(500,1500)) + '\n'
		# create the script now
		systemtext = 'system "' + name + '"\n'\
			+ '\tpos ' + str(x) + ' ' + str(y) + '\n'\
			+ '\tgovernment "Uninhabited"\n'\
			+ '\tarrival ' + str(random.randint(500,1200)) + '\n'\
			+ '\thabitable ' + str(random.randint(500,1200)) + '\n'\
			+ '\tbelt ' + str(random.randint(800,1800)) + '\n'\
			+ minablesstring\
			+ minablesyottrite\
			+ objectsstring
		# links get added at the bottom
		return systemtext, name
	def new_pos(center_x, center_y):
		# generates a new system pos, somewhere on the border of the circle
		theta = math.radians(random.randint(1,360))
		x = center_x + starRadius * math.cos(theta)
		y = center_y + starRadius * math.sin(theta)
		return int(x), int(y)
	systemtexts, positions = [], []
	print('\ncreating systems [', systemAmount, ']')
	count = 0 # for counting systems
	densitycounter = 0
	counter2 = 0 # for changing system
	for i in range(0, systemAmount):
		if i == 0: # only for the first system
			# start system
			if startWormhole != '':
				firstWorm = '\tobject "Mysterious Wormhole"\n\t\tsprite planet/wormhole-red\n\t\tdistance 1000\n\t\tperiod 1\n'
			else:
				firstWorm = ''
			x, y = 0, 0
			systemtext, name = get_system_text(x, y, firstWorm)
			systemtexts.append(systemtext)
			positions.append([x,y])
			count +=1
			print('	found new system position (' + str(count) + '): [' + str(x) + ' ' + str(y) + '] ' + name)
			firstWorm = ''
		else: # after starting system got added
			repeat = True
			counter = 0 # for pos generating
			#
			if densitycounter > density:
				densitycounter = 1
				oldx, oldy = 0, 0
			else:
				oldx, oldy = x, y # old system
			# get new system pos
			while repeat == True:
				if counter < tries: # if not {tries} failed pos generations
					x, y = new_pos(oldx, oldy) # generate from previous system
				else: # {tries} times failed, resets counter, and changes oldx,oldy to a previous system pos
					counter = 0
					if counter2 < len(positions)-1:
						counter2 += 1
					else:
						counter2 = 1
					oldx, oldy = positions[counter2-1]
					x, y = new_pos(oldx, oldy)
				for systempos in positions:
					fx, fy = systempos
					result = dot_in_circle(fx, fy, x, y, starRadius-1)
					if result == False:
						repeat = False
					else:
						counter += 1
						repeat = True
						break
			# new system pos found, generating text
			densitycounter +=1
			systemtext, name = get_system_text(x, y, firstWorm)
			systemtexts.append(systemtext)
			positions.append([x,y]) # finally new system added
			count +=1
			print('	found new system position (' + str(count) + '): [' + str(x) + ' ' + str(y) + '] ' + name)
	print('	DONE')
	return systemtexts, positions


def dot_in_circle(fx, fy, x, y, rad):
	# checks if the pos is inside the circle
	distance = math.sqrt((fx - x)**2 + (fy - y)**2)
	if distance <= rad:
		result = True
	else:
		result = False
	return result


def create_landable_planets(systemtexts):
	if landPlanets > 0:
		print('\ncreating landable planets [', landPlanets, ']')
		used_planetNames = []
		rare = systemAmount / landPlanets # float, number of planets in each system
		count = 0
		whole = 0
		with open(writetopath + 'MapGenPlanets.txt', 'w') as planettxt:
			for i in range(1, landPlanets+1):
				# generate unique name
				name = str(random.choice(planetNames))
				while name in used_planetNames:
					name = str(random.choice(planetNames))
				used_planetNames.append(name)
				print('	planet:', i +1, '/', landPlanets, 'added to system:', whole+1,'planetname:', name.strip())
				# planet creation planet file
				planettxt.writelines('planet "' + name.strip() + '"\n\tattributes uninhabited ' + galaxyImage + '\n\tgovernment "Uninhabited"\n\tlandscape land/' +\
					random.choice(landImages) +'\n\tdescription ``\n\n')
				# planet creation system object
				addObject = '\tobject "' + name.strip() + '"\n\t\tsprite planet/' + random.choice(planetTypes) + '\n' + '\t\tdistance ' + str(random.randint(600,2000))\
					+ '\n\t\tperiod ' + str(random.randint(300,1500)) + '\n'
				# choose systems
				count += rare
				while count >= whole+1:
					whole +=1
				systemtexts[whole-1] += addObject	
		print('	DONE')
	else:
		with open(writetopath + 'MapGenPlanets.txt', 'w') as planettxt:
			planettxt.writelines('no planets got generated\n')
	return systemtexts, used_planetNames


def create_links(systemtexts, positions):
	def get_link(index):
		# get linkname & name from coordinates
		linkindex = positions.index(index)
		linkname = systemtexts[linkindex][systemtexts[linkindex].find(' ')+1:systemtexts[linkindex].find('\n')].replace('"', '')
		link = '\tlink "' + linkname + '"\n'
		return link, linkname
	def other_system(source, linkname):
		# writes back link to the linked system
		for system in systemtexts:
			if system.startswith('system "' + linkname + '"\n'):
				index = systemtexts.index(system)
				break
		if f'\tlink "{source}"\n' not in systemtexts2[index]:
			systemtexts2[index] += f'\tlink "{source}"\n'
	global systemtexts2
	systemtexts2 = systemtexts.copy()
	# create system links
	print('\ncreate system links')
	for system in systemtexts:
		links = ''
		index = systemtexts.index(system)
		x, y = positions[index]
		name = system[system.find(' ')+1:system.find('\n')].replace('"', '')
		# get nearest systems
		nearsys = [] # list of position of systems within the radius circle
		for position in positions:
			if position == positions[index]:
				continue
			fx, fy = position
			if dot_in_circle(fx, fy, x, y, starRadius+50) == True:
				nearsys.append(position)
		# add links
		if len(nearsys) == 1:
			for i in range(0,1):
				link, linkname = get_link(nearsys[i]) # \t link "name"\n | name
				links = links + link
				other_system(name, linkname)
		elif len(nearsys) == 2:
			for i in range(0,2):
				link, linkname = get_link(nearsys[i])
				links = links + link
				other_system(name, linkname)
		else:
			for i in range(0,random.randint(2, 3)):
				link, linkname = get_link(nearsys[i])
				links = links + link
				other_system(name, linkname)
		systemtexts2[index] = systemtexts2[index] + links
	print('	DONE')
	systemtexts = systemtexts2.copy()
	return systemtexts


def rearrange_systemtexts(systemtexts):
	# re-arranging links
	print('\nre-arranging system scripts')
	systemtexts2 = systemtexts.copy()
	# save the first part, the objects and the links into lists
	for system in systemtexts:
		first_part = [] # text till objects start
		objectlines = [] # text till links start
		links = [] # links
		startblock = True
		objectblock = True
		splitted = system.split('\n')
		for line in splitted:
			if startblock == True:
				if not line.startswith('\tobject'):
					first_part.append(line)
				else:
					objectlines.append(line)
					startblock = False
			else:
				if objectblock == True:
					if not line.startswith('\tlink'):
						objectlines.append(line)
					else:
						links.append(line)
						objectblock = False
				else:
					if not line in links: # corrects an error i can't find in create_links(), showing backlinks doubled
						links.append(line)
		# separate objects
		start = True
		objects = []
		for line in objectlines:
			if line.startswith('\tobject'):
				if start == True:
					text = line + '\n'
					start = False
				else:
					objects.append(text)
					text = line + '\n'
			elif line.startswith('\t\t'):
				text += line + '\n'
		objects.append(text)
		# get new list with distances
		distance = []
		for obj in objects:
			if not '\tdistance ' in obj:
				distance.append(0)
			else:
				pos1 = obj.find('\tdistance')
				pos2 = obj.find('\n', pos1)
				distance.append(int(obj[pos1+10:pos2]))
		# sort both lists
		distance, objects = zip(*sorted(zip(distance, objects)))
		objtext = ''
		for obj in objects:
			objtext += obj
		# lists are created
		final_text = '\n'.join(first_part) + '\n' + '\n'.join(links) + objtext
		index = systemtexts2.index(system)
		systemtexts2[index] = final_text
		systemtexts = systemtexts2.copy()
	print('	DONE')
	return systemtexts


def create_races(positions, races, systemtexts, usedPlanetnames):
	systemtexts2 = systemtexts.copy()
	def distance(x1, y1, x2, y2):
		distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return distance
	racepos = []
	usednames = []
	if races > 0:
		print('\ncreating races')
		#read templates
		with open ('res/template_plugin.txt', 'r') as source:
			all = source.read()
			template_plugin = all.split('####')
			Tgovernment = template_plugin[2]
			Tshipyard = template_plugin[4]
			Tbigfleet = template_plugin[6]
			Tsmallfleet = template_plugin[8]
			Tships = template_plugin[10]
			Toutfitter = template_plugin[12]
		with open(writetopath + 'MapGenStuff.txt', 'a') as target:
				target.writelines(Tshipyard)
				target.writelines(Tships)
		# read race names
		with open ('res/wordlists/races.txt', 'r') as source:
			racenames = source.readlines()
		# get random position for race
		racepos = []
		print('	get system for races')
		lasti = races
		for i in range(0,races):
			name = random.choice(racenames)
			while name in usednames:
				name = random.choice(racenames)
			usednames.append(name)
			# write governments and fleets
			with open(writetopath + 'MapGenStuff.txt', 'a') as target:
				target.writelines(Tgovernment.replace('replace me', name.strip()))
				target.writelines(Tbigfleet.replace('replace me', name.strip()))
				target.writelines(Tsmallfleet.replace('replace me', name.strip()))
			if i == 0:
				print('		placing race: 1')
				racepos.append(random.choice(positions))
			else:
				loop = True
				counter = 0
				while loop == True:
					newpos = random.choice(positions)
					loop = False
					for each in racepos:
						x1,y1 = each
						x2,y2 = newpos
						if distance(x1, y1, x2, y2) < 400:
							loop = True
							counter +=1
							break
					if counter == 50:
						loop = False
						#races = i
				if counter < 50:
					print('		placing race:', i +1)
					lasti = i
					racepos.append(newpos)
		if lasti+1 < races:
			print('		not enough system space:', lasti + 1, '/', races, ' races placed')
		# change systems
		print('	add neighbouring systems for', len(racepos), 'systems')
		for each in racepos:
			index = racepos.index(each)
			neighbouring = []
			x,y = each
			for system in systemtexts:
				# change actual system
				if str(x) + ' ' + str(y) in system:
					sysindex = systemtexts.index(system)
					planetname = random.choice(planetNames)
					while planetname in usedPlanetnames:
						planetname = random.choice(planetNames)
					usedPlanetnames.append(planetname)
					system = system.replace('\tgovernment "Uninhabited"\n', '\tgovernment "' + usednames[index].strip() + '"\n')
					system += '\tobject "' + planetname.strip() + '"\n\t\tsprite planet/earth\n\t\tdistance 2500\n\t\tperiod 400\n'
					system += '\tfleet "' + usednames[index].strip() + ' Small Fleet" ' + str(random.randint(1000,2500)) + '\n'
					system += '\tfleet "' + usednames[index].strip() + ' Big Fleet" ' + str(random.randint(2000,3500)) + '\n\n'
					systemtexts2[sysindex] = system
					# add to planet file
					with open(writetopath + 'MapGenPlanets.txt', 'a') as planettxt:
						planettxt.writelines('planet "' + planetname.strip() + '"\n')
						planettxt.writelines('\tattributes ' + galaxyImage + '\n')
						planettxt.writelines('\tlandscape land/city1\n')
						planettxt.writelines(Toutfitter + '\n')
						planettxt.writelines('\tspaceport ``\n')
						planettxt.writelines('\tdescription `This is the capital of ' + usednames[index].strip() + '.`\n\n')
					sys = system
					# get linked systems
					while '\tlink ' in sys:
						pos1 = sys.find('\tlink ')
						pos2 = sys.find('\n', pos1)
						neighbouring.append(sys[pos1+6:pos2])
						sys = sys[pos2:len(sys)]
					break
			# change linked systems
			for neighbour in neighbouring: # len = linked systems
				for system in systemtexts:
					if system.startswith('system ' + neighbour):
						sysindex = systemtexts.index(system)
						system = system.replace('\tgovernment "Uninhabited"\n', '\tgovernment "' + usednames[index].strip() + '"\n')
						planetname = random.choice(planetNames)
						while planetname in usedPlanetnames:
							planetname = random.choice(planetNames)
						usedPlanetnames.append(planetname)
						with open(writetopath + 'MapGenPlanets.txt', 'a') as planettxt:
							planettxt.writelines('planet "' + planetname.strip() + '"\n')
							planettxt.writelines('\tattributes ' + galaxyImage + '\n')
							planettxt.writelines('\tlandscape land/city1\n')
							planettxt.writelines('\tspaceport ``\n')
							planettxt.writelines('\tdescription `This is a colony of ' + usednames[index].strip() +  '.`\n\n')
						system += '\tobject "' + planetname.strip() + '"\n\t\tsprite planet/earth\n\t\tdistance 2500\n\t\tperiod 400\n'
						system += '\tfleet "' + usednames[index].strip() + ' Small Fleet" ' + str(random.randint(1000,2500)) + '\n'
						system += '\tfleet "' + usednames[index].strip() + ' Big Fleet" ' + str(random.randint(2000,3500)) + '\n\n'
						systemtexts2[sysindex] = system
						break
	return systemtexts2
		


def write_map_file(systemtexts):
	print('\nwriting map file')
	addx, addy = startPos
	# correct pos with startpos
	with open(writetopath + 'MapGenSystems.txt', 'w') as mapfile:
		print('	correcting pos with startpos')
		for text in systemtexts:			
			pos1 = text.find('\tpos ')
			pos2 = text.find('\n', pos1)
			splitted = text[pos1+5:pos2].split(' ')
			x = int(splitted[0])
			y = int(splitted[1])
			text = text.replace(text[pos1+5:pos2], str(x + addx) + ' ' + str(y + addy))
			# write to mapfile
			mapfile.writelines(text + '\n')
	print('	DONE')


def create_image(systemtexts, positions):
	# creating overview image, just to see result
	def findpos(text):
		pos1 = text.find('pos')
		pos2 = text.find('\n', pos1)
		x, y = text[pos1+4:pos2].split(' ')
		return int(x), int(y)
	print('\ncreating image')
	# analyzing positions to get right picture size
	print('	getting drawn image size')
	hx = max((x for x, _ in positions if x >= 0), default=0)
	lx = min((x for x, _ in positions if x < 0), default=0)
	hy = max((y for _, y in positions if y >= 0), default=0)
	ly = min((y for _, y in positions if y < 0), default=0)
	x = max(hx, -lx)
	y = max(hy, -ly)
	sizex = x*2 + 300
	sizey = y*2 + 300
	# define image
	print('		drawn size will be:', sizex, sizey)
	#im = Image.open(mode = "RGB", size = (sizex, sizey), color=(10,10,10)) # black background, and cut to relevant parts
	im = Image.open('res' + os.sep + 'galaxyimages' + os.sep + galaxyImage + '.jpg')
	width, height = im.size
	print('		background size will be:', width, height)
	draw = ImageDraw.Draw(im, 'RGBA')
	font = ImageFont.truetype(font=iFont, size=15)
	print('	drawing systems and links')
	for system in systemtexts:
		# get positions
		pos1 = system.find('system ')
		pos2 = system.find('\n')
		name = system[pos1+7:pos2]
		x, y = findpos(system)
		pos = [x +(width/2), y +(height/2)]
		# draw systems
		pos1 = system.find('\tgovernment ')
		pos2 = system.find('\n', pos1)
		gov = system[pos1+12:pos2]
		if gov == '"Uninhabited"':
			draw.ellipse((pos[0]-7, pos[1]-7, pos[0]+7, pos[1]+7), fill=(0,0,0,0), outline=(102,102,102), width=3)
		else:
			draw.ellipse((pos[0]-7, pos[1]-7, pos[0]+7, pos[1]+7), fill=(0,0,0,0), outline=(255,0,0), width=3)
		draw.text((pos[0]+15, pos[1]-14) , name.replace('"', ''), fill=(255,255,255), font=font)
		# draw link lines
		start = x +(width/2), y +(height/2)
		othersystem = []
		splitted = system.split('\n')
		for line in splitted:
			if line.startswith('\tlink '):
				pos1 = line.find('"')
				pos2 = line.find('"', pos1+1)
				linked = line[pos1+1:pos2]
				othersystem.append(linked) # system name
		for linked in othersystem:
			for checksystem in systemtexts:
				if checksystem.startswith('system "' + linked + '"'):
					x,y = findpos(checksystem)
					end = x +(width/2), y +(height/2)
					draw.line((start, end), fill=(128,128,128))
	# save image
	im = im.convert('RGB')
	print('	saving image')
	im.save(writetopath + 'MapGenMap.jpg')
	# generating thumbnail
	base_width = 300
	img = Image.open(writetopath + 'MapGenMap.jpg')
	wpercent = (base_width / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((base_width, hsize), Image.LANCZOS) # Resampling
	img.save(writetopath + 'miniMapGenMap.jpg')
	print('	DONE')


def create_zip():
	print('\nzipping plugin')
	# create plugin structure
	shutil.copytree('res/pluginfiles', newname)
	os.mkdir(newname + os.sep + 'data/')
	shutil.copy(writetopath + os.sep + 'MapGenStuff.txt', newname + os.sep + 'data/' + 'MapGenStuff.txt')
	shutil.copy(writetopath + os.sep + 'MapGenSystems.txt', newname + os.sep + 'data/' + 'MapGenSystems.txt')
	shutil.copy(writetopath + os.sep + 'MapGenPlanets.txt', newname + os.sep + 'data/' + 'MapGenPlanets.txt')
	os.mkdir(newname + os.sep + 'images/')
	shutil.copytree('res/images/ship', newname + os.sep + 'images/ship')
	os.mkdir(newname + os.sep + 'images/ui/')
	shutil.copy('res/galaxyimages/' + galaxyImage + '.jpg', newname + os.sep + 'images/ui/' + galaxyImage + '.jpg')
	# create zip
	file_paths = []
	for root, directories, files in os.walk(newname):
		for filename in files: 
			filepath = os.path.join(root, filename) 
			file_paths.append(filepath) 
	with zipfile.ZipFile(newname + '.zip','w') as zip: 
		for file in file_paths: 
			zip.write(file)
	# modify log.txt
	print('	modifying log.txt')
	lines = []
	if os.path.isfile('res/log.txt'):
		with open('res/log.txt', 'r') as source:
			lines = source.readlines()
	newlines = ''
	delete = ''
	if len(lines) > 4:
		newlines = lines[0:4]
		delete = lines[4].strip()
	else:
		newlines = lines
	with open('res/log.txt', 'w') as target:
		target.writelines(newname +'\n')
		target.writelines(newlines)
	# delete 6th generated folder
	if not delete == '':
		if os.path.isdir('generated/' + delete):
			shutil.rmtree('generated/' + delete)
	print('	DONE')
	
	
			

def run():
	check_local() # set up variables for local test or github run
	write_other_stuff() # write generated/MapGenStuff.txt
	systemtexts, positions = create_systemtexts() # creates system scripts
	systemtexts, usedPlanetnames = create_landable_planets(systemtexts) # updates system scripts with landable planets and writes generated/MapGenPlanets.txt
	systemtexts = create_links(systemtexts, positions) # updates system scripts with links
	systemtexts = rearrange_systemtexts(systemtexts) # puts objects and links of systems in the correct order
	systemtexts = create_races(positions, races, systemtexts, usedPlanetnames) # add races to systems
	write_map_file(systemtexts) # writes generated/MapGenSystems.txt
	create_image(systemtexts, positions) # creates generated/MapGenMap.jpg just for the overview
	create_zip() # create zip for release upload


if __name__ == '__main__':
	run()
