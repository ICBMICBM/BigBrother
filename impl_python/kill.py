import time
import os

def getFileList(path):
	fileList = []
	for a,b,c in os.walk(path):
		for f in c:
			fileList.append(os.path.join(a,f))
	return fileList


def getFileNameList(path):
	fileNames = []
	for a,b,c in os.walk(path):
		for i in c:
			fileNames.append(i)
	return fileNames

while True:
	time.sleep(3)
	l = getFileList('/var/www/html')
	# print(l)
	white = getFileNameList('/home/patch/ns')
	# print(white)
	for i in l:
		if 'php' in i and os.path.basename(i) not in white:
			try:
				# print("remove"+str(i))
				try:
					os.remove(i)
					os.mkdir(i)
					print('mkdir {} success'.format(i))
				except:
					print('mkdir fail')
			except:
				print(i) 
