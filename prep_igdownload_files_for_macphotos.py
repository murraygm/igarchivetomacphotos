import json
import os, sys
from datetime import datetime, time
#3rd party packages
from iptcinfo3 import IPTCInfo

'''
Description: a little python 3 script that takes the JSON
from your Instagram Data Download and uses it as IPTC data. 
It then adds this back to the image so that you can import 
the metadata into Mac Photos.

Created by: Murray Grigo-McMahon
Github ref: https://github.com/murraygm
Date created: 2019-03-18

OS - MAC

license: Public domain, free to use (packages may have additional licenses)
'''


pathtoarchive='' #filepath to where your unzipped Instagram archive download is


destFolder = '' #filepath to where you want to save renamed ALL items to

igArchiveparts=['', '', ''] #array of each of the folders in the archive - DO NOT INCLUDE part 1 as no images


#already imported your library and just want to add the new stuff from the full down load? 
igStartDate = '' #add a starting date string formatted like so '2019-03-19 13:45:59' so that only items after this will be prepped

try:
	datetime.strptime(igStartDate, '%Y-%m-%d %H:%M:%S')
except:
	igStartDateFlag = 0
	igStartDateStamp = datetime.timestamp(datetime.strptime('2010-07-15 00:00:00', '%Y-%m-%d %H:%M:%S'))
else:	
	igStartDateFlag = 1
	igStartDateStamp = datetime.timestamp(datetime.strptime(igStartDate, '%Y-%m-%d %H:%M:%S'))


for a in range(len(igArchiveparts)):

	targJson = pathtoarchive+igArchiveparts[a]+"media.json"

	with open(targJson, encoding="utf-8") as data_file:
		data = json.load(data_file)

		targFolder = pathtoarchive+igArchiveparts[a]
		

		#Photo
		#loop through items
		for photos in data['photos']:
			#pull creation date and make new string
			fileDate = str.split( photos['taken_at'], 'T')

			#set the date on the file (last modified)
			newDate = fileDate[0] + ' ' + fileDate[1]
			newStamp = datetime.strptime(newDate, '%Y-%m-%d %H:%M:%S')
			newCreateDate = datetime.timestamp(newStamp)

			if igStartDateStamp < newCreateDate:

				fileNameBit = str.split( photos['path'], '/')
				newFname = fileDate[0]+'_'+fileNameBit[2]

				origPath = targFolder+photos['path']
				newPath = destFolder+newFname

				nTitle=photos['caption']
				nCreator='' #added a creator name
				nLocal=''

				nCaption=photos['caption']
				nKeywords= []

				if 'location' in photos:
					nLocal=photos['location']
					nCaption = nCaption + ' - tagged location: ' + nLocal
					nKeywords.append(nLocal)
				
				if "#" in nCaption:  
					nKeywordsA=nCaption.split(' ')
					nKeywordsB=[]

					for i in range(len(nKeywordsA)):
						nKeywordsB=nKeywordsA[i].split('#')
						if len(nKeywordsB)>1:
							nKeywords.append(nKeywordsB[1])

				info = IPTCInfo(origPath)

				info['object name'] = nTitle[:30]
				info['content location name'] = nLocal
				info['reference date'] = fileDate[0]
				info['keywords'] = nKeywords
				info['by-line'] = nCreator
				info['caption/abstract'] = nCaption

	#			print(nTitle[:30], newFname)
				info.save()
				info.save_as(newPath)

				#set the new creation date
				os.utime(newPath, (newCreateDate, newCreateDate))

		#Video
		#loop through items
		for videos in data['videos']:

			vfileDate = str.split( videos['taken_at'], 'T')
			#set the date on the file (last modified)
			vnewDate = vfileDate[0] + ' ' + vfileDate[1]
			vnewStamp = datetime.strptime(vnewDate, '%Y-%m-%d %H:%M:%S')
			vnewCreateDate = datetime.timestamp(vnewStamp)

			if igStartDateStamp < vnewCreateDate:

				vfileNameBit = str.split( videos['path'], '/')
				vnewFname = vfileDate[0]+'_'+vfileNameBit[2]

				vorigPath = targFolder+videos['path']
				vnewPath = destFolder+vnewFname

	#			print (vorigPath)
	#			print (vnewPath)

				#rename file
				os.rename(vorigPath, vnewPath)

				#set the new creation date
				os.utime(vnewPath, (vnewCreateDate, vnewCreateDate))
