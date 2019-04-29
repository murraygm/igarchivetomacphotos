'''
prep_igdownload_files_for_macphotos.py

v.2

Description: a little python script that takes the JSON
from your Instagram Data Download and uses it as IPTC data. 
It then adds this back to the image so that you can import 
the metadata into Mac Photos.

This update supports Emoji and UTF-8 char set

Created by: Murray Grigo-McMahon
Github ref: https://github.com/murraygm
Date created: 2019-04-29

OS - MAC

license: Public domain, free to use (packages may have additional licenses)


DEPENDANCIES: exiftool must be installed - download and install before running: http://owl.phy.queensu.ca/~phil/exiftool/

Based on Instagram JSON structure in 'media.json' file like so:
{
  "photos": [
    {
      "caption": "",
      "taken_at": "",
      "path": ""
    },
    {
      "caption": "",
      "taken_at": "",
      "path": ""
    }
  ],
  "videos": [
    {
      "caption": "",
      "taken_at": "",
      "path": ""
    },
    {
      "caption": "",
      "taken_at": "",
      "path": ""
    }
  ],
  "direct": [
    {
      "taken_at": "",
      "path": ""
    }
  ]
}


'''

import json
import os
import sys
from datetime import datetime, time
import exiftool

#filepath to where your unzipped Instagram archive download is
pathtoarchive='/Users/murray/Desktop/instagram/'

#filepath to where you want to save renamed ALL items to
destFolder = '/Users/murray/Desktop/instagram/OUT/'


#array of each of the folders in the archive - ignorring part 1 as no images (eg: murraygm_20190318_part_2/)
#ensure end slash added to the foldername
igArchiveparts=['','']

#set the photographers name for all items
photographer = ''


#after date limit - so if you've already imported your library and just want to add the new stuff from the full download 
igStartDate = '' #date string formatted like so '2019-03-19 13:45:59'

try:
	datetime.strptime(igStartDate, '%Y-%m-%d %H:%M:%S')
except:
	igStartDateFlag = 0
	igStartDateStamp = datetime.timestamp(datetime.strptime('2010-07-15 00:00:00', '%Y-%m-%d %H:%M:%S'))
	igStartDate = '2010-07-15 00:00:00'
else:	
	igStartDateFlag = 1
	igStartDateStamp = datetime.timestamp(datetime.strptime(igStartDate, '%Y-%m-%d %H:%M:%S'))

print('started proccessing images after date: ' + igStartDate)


for a in range(len(igArchiveparts)):

	targJson = pathtoarchive+igArchiveparts[a]+"media.json"

	with open(targJson, encoding="utf-8") as data_file:
		data = json.load(data_file)

		targFolder = pathtoarchive+igArchiveparts[a]
		
		#Photos
		#loop through items
		for photos in data['photos']:


			origPath = pathtoarchive+igArchiveparts[a]+photos['path']
			

			aFileDate = str.split( photos['taken_at'], 'T')

			newDate = aFileDate[0] + ' ' + aFileDate[1]
			newStamp = datetime.strptime(newDate, '%Y-%m-%d %H:%M:%S')
			newCreateDate = datetime.timestamp(newStamp)


			if igStartDateStamp < newCreateDate:

				nFileDate = "-IPTC:ReferenceDate=" + aFileDate[0]

				nTitle="-IPTC:ObjectName=" + photos['caption'][:30]
				nByLine="-IPTC:By-line=" + photographer 
				nLocal="-IPTC:ContentLocationName="

				aCaption = photos['caption']
				nCaption="-IPTC:Caption-Abstract="+ photos['caption']
				aKeywords= []
				nKeywords= "-IPTC:Keywords="

				

				if "#" in aCaption:  
					nKeywordsA=aCaption.split(' ')
					nKeywordsB=[]

					for i in range(len(nKeywordsA)):
						nKeywordsB=nKeywordsA[i].split('#')
						if len(nKeywordsB)>1:
							aKeywords.append(nKeywordsB[1])

				if 'location' in photos:
						nLocal="IPTC:ContentLocationName=" + photos['location']
						nCaption = nCaption + ' - tagged location: ' + photos['location']
						aKeywords.append(photos['location'])


				nKeywords= "-IPTC:Keywords=" + ", ".join(str(x) for x in aKeywords)

#				print(nCaption)
				with exiftool.ExifTool() as et:

					pic = bytes(origPath, 'utf-8')
					#
					et.execute(bytes("-overwrite_original", "utf-8"),
						bytes("-codedCharacterSet=utf8", "utf-8"),
						bytes(nTitle,'utf-8'),
						bytes(nCaption,'utf-8'),
						bytes(nByLine,'utf-8'),
						bytes(nLocal,'utf-8'),
						bytes(nFileDate,'utf-8'),
						bytes(nKeywords,'utf-8'),
						pic)

				fileNameBit = str.split( photos['path'], '/')
				newFname = aFileDate[0]+'_'+fileNameBit[2]
				newPath = destFolder+newFname

				if os.path.exists(origPath):
					os.rename(origPath, newPath)
				else:
					print(origPath + ' - PHOTO NOT FOUND')

				if os.path.exists(newPath):	
					#set the new creation date
					os.utime(newPath, (newCreateDate, newCreateDate))
				else:
					print(newPath + ' - MOVED PHOTO NOT FOUND')

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

				if os.path.exists(vorigPath):
					#rename file
					os.rename(vorigPath, vnewPath)
				else:
					print(vorigPath + ' - VIDEO NOT FOUND')

				if os.path.exists(vnewPath):
					#set the new creation date
					os.utime(vnewPath, (vnewCreateDate, vnewCreateDate))
				else:
					print(vnewPath + ' - MOVED VIDEO NOT FOUND')

		#Direct
		#loop through items
		if 'direct' in data:
			for direct in data['direct']:

				dfileDate = str.split( direct['taken_at'], 'T')
				#set the date on the file (last modified)
				dfileDateTrim = dfileDate[1]
				dnewDate = dfileDate[0] + ' ' + dfileDateTrim[:7]
				dnewStamp = datetime.strptime(dnewDate, '%Y-%m-%d %H:%M:%S')
				dnewCreateDate = datetime.timestamp(dnewStamp)

				if igStartDateStamp < dnewCreateDate:

					dfileNameBit = str.split( direct['path'], '/')
					dnewFname = dfileDate[0]+'_'+dfileNameBit[2]

					dorigPath = targFolder+direct['path']
					dnewPath = destFolder+dnewFname

					if os.path.exists(dorigPath):
						#rename file
						os.rename(dorigPath, dnewPath)
					else:
						print(dorigPath + ' - DIRECT NOT FOUND')
					if os.path.exists(dnewPath):	
						#set the new creation date
						os.utime(dnewPath, (dnewCreateDate, dnewCreateDate))
					else:
						print(dnewPath + ' - MOVED DIRECT NOT FOUND')