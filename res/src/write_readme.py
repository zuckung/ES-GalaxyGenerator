import os


def check_local():
	# for local testing
	print('checking if local test or github')
	if os.getcwd() == '/storage/emulated/0/Download/mgit/test/res/src': # check for local testing
		os.chdir('../../')
		print('	local test detected')
	else:
		print('	github run detected')


def write_readme():
	print('\nwriting readme.md')
	print('	reading log and template')
	with open('res/log.txt', 'r') as source:
		folder = source.readlines()
	with open('res/template.txt', 'r') as source:
		template = source.read()
	templatesplit = template.split('#### tables\n')			
	headtemplate = templatesplit[0]
	tabletemplate = templatesplit[1]
	# write readme
	print('	writing readme')
	with open('README.md', 'w') as target:
		target.write(headtemplate)
		for each in folder:
			each = each.strip()
			with open('generated' + os.sep + each + os.sep + each + '.txt', 'r') as source:
				lines = source.readlines()
			linkfolder = each
			name = lines[0].strip()
			pos = lines[1].strip()
			systems = lines[2].strip()
			planets = lines[3].strip()
			wormhole = lines[4].strip()
			sunmax = lines[5].strip()
			planetmax = lines[6].strip()
			minablemax = lines[7].strip()
			galaxyImage = lines[8].strip()
			starRadius = lines[9].strip()
			density = lines[10].strip()
			tries = lines[11].strip()
			newtable = tabletemplate\
				.replace('<name>', name)\
				.replace('<pos>', pos)\
				.replace('<systems>', systems)\
				.replace('<planets>', planets)\
				.replace('<wormhole>', wormhole)\
				.replace('<sunmax>', sunmax)\
				.replace('<planetmax>', planetmax)\
				.replace('<minablemax>', minablemax)\
				.replace('<linkfolder>', linkfolder)\
				.replace('<galaxyimage>', galaxyImage)\
				.replace('<starradius>', starRadius)\
				.replace('<density>', density)\
				.replace('<tries>', tries)
			target.write(newtable + '\n')
	print('	DONE')

# 2do



def run():
	check_local()
	write_readme()



if __name__ == '__main__':
	run()
