# Instagram Archive Download prepper for Mac photos import
scrappy python script that adds the IPTC metadata and file dates back to your images for import into Mac Photos.

Go to Instagram and request your data. After a day or so they send you a link to multiple archive files.
Download and unzip them. 

## Set up the python script
Make sure you have the packages available, including the 3rd party 'iptcinfo3' [https://pypi.org/project/IPTCInfo3/]

Add the paths to the parts of the archive to the script (make sure to include the final / ) :
```
23 | pathtoarchive='' #filepath to where your unzipped Instagram archive download is

26 | destFolder = '' #filepath to where you want to save renamed ALL items to

28 | igArchiveparts=['', '', ''] #array of each of the folders in the archive - DO NOT INCLUDE part 1 as no images eg 'murraygm_20190316_part_2/'
```

Also you can add yourself as the 'creator' of the images here:
```
74 | nCreator='' #name of creator
```

## added 22 March
I added the ability to set an earliest date so that you can run it again on subsequent downloads of the archive and just import the new stuff - as long as IG doesn't change the structure ;) 
Just set a string for the date in this variable. 
```
32 | igStartDate = '' #add a starting date string formatted like so '2019-03-19 13:45:59' so that only items after this will be prepped
```

## What the script does
It loops through each part of the archive (as defined in the 'igArchiveparts' array.
It reads the 'media.JSON' file for each archive folder. 
First it loops through the photos and
* creates a new name for the file (prepends the igname with date)
* adds the caption (your initial post comment) to the image IPTC data as 'caption/description' - this becomes a description when imported to Mac Photos
* takes the first 30 characters from the caption and adds them to the image IPTC data as 'object name' - this becomes the Title when imported to Mac Photos
* Splits out any hashtags from the caption and adds them to the image IPTC data as the 'keywords' array - these become Mac Photos keywords
* Adds the text string you specified for 'nCreator' to the image IPTC data as 'by-line'
* Adds the location (named string not GEO) to the image IPTC data as 'content location name'
* Adds the date taken to the image IPTC data as 'reference date'
* then it COPIES the files to the 'destFolder' with the new names
* then applies a new file Modified Date of the date the photo was taken - note this means Mac Photos orders them correctly (hack as can not find way to change creation date too)

Then it loops through the videos and
* creates a new name for the file (prepends the igname with date)
* MOVES the file to the 'destFolder' with the new names
* then applies a new file Modified Date of the date the photo was taken - note this means Mac Photos orders them correctly (hack as can not find way to change creation date too)


When you import them to Mac Photos you can search the keywords, caption, title data and view it from the 'inspector'

## Known issues
* if a photo is part of a multipart post (more than 1 image) no caption is assigned - this is an Instagram issue and no caption is prescent for the JSON items
* emojis are not supported and seem to get turned into fairly useless strings




