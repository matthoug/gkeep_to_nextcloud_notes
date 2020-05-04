import gkeepapi
import os
import glob
import time

keep = gkeepapi.Keep()
#Once you have a password account from google you can indicate you email + password below
success = keep.login('...', '...')

Directory = '/home/BobDylan/Documents/gkeep_to_nextcloud_notes/'

gnotes = keep.all()
count=0
for x in gnotes:
	try:
		# If the note does not contains title and content
		if not x.title and not x.text:
			continue
		
		time_modified = time.mktime(x.timestamps.created.timetuple())

		#Create directory for labels
		if [y.name for y in x.labels.all()]:
			label = [y.name for y in x.labels.all()][0]
			if os.path.isdir(Directory + label):
				pass
			else:
				os.mkdir(Directory + label)
		else:
			label = ''
		
		#If the note has no title, take the first line of the text
		if not x.title:
			title = x.text.splitlines()[0].replace('/',' ')

		else:
			title = x.title
		
		#Raise error if file already exists (note with the same title.txt)
		if len((glob.glob("{}**/{}.txt".format(Directory,title), recursive = True))) == 1:
			print('file already exists !', title)

		if label != '' :
			with open ("{}{}/{}.txt".format(Directory,label,title), "w") as efile:
				efile.write('{}'.format(x.text))
			os.utime("{}{}/{}.txt".format(Directory,label,title), (time_modified, time_modified))
			count+=1
		else:
			with open ("{}{}.txt".format(Directory,title), "w") as efile:
				efile.write('{}'.format(x.text))
			os.utime("{}{}.txt".format(Directory,title), (time_modified, time_modified))
			count+=1

	except Exception as e:
		print('Timestamp:{}\nLabel : {}\nTitle : {}\nContent :\n{}Error :{}'.format(x.timestamps.edited, [y.name for y in x.labels.all()],x.title,x.text, e))

print('{} notes were imported from Google Keep'.format(count))
