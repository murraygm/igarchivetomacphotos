# Instagram Archive Download prepper for Mac photos import
scrappy python script that adds the IPTC metadata and file dates back to your images for import into Mac Photos.

Go to Instagram and request your data. After a day or so they send you a link to multiple archive files.
Download and unzip them. 
**Note the script moves and renames files, so keep the zips incase you need to rerun it**.

![Screenshot](ig_to_photos_metadata.png?raw=true "Screenshot")

## Set up the python script
Make sure you've got exiftool installed on your system, if not get it here
http://owl.phy.queensu.ca/~phil/exiftool/


Add the paths to the parts of the archive to the script (make sure to include the final / ) :
```
68 | pathtoarchive='' #filepath to where your unzipped Instagram archive download is

71 | destFolder = '' #filepath to where you want to save renamed ALL items to


76 | igArchiveparts=['',''] #array of each of the folders in the archive
```

Also you can add yourself as the 'by-line' or creator of the images here:
```
79 | photographer='' #photographers name
```

I added the ability to set an earliest date so that you can run it again on subsequent downloads of the archive and just import the new stuff - as long as IG doesn't change the structure ;) 
Just set a string for the date in this variable. 
```
83 | igStartDate = '' #add a starting date string formatted like so '2019-03-19 13:45:59' so that only items after this will be prepped
```
Also added the location name data to the description and as a keyword as Photos expects real Geo data for location.

## What the script does
It loops through each part of the archive (as defined in the 'igArchiveparts' array.
It reads the 'media.JSON' file for each archive folder. 
First it loops through the photos and
* creates a new name for the file (prepends the igname with date)
* adds the caption (your initial post comment) to the image IPTC data as 'Caption-Abstract' - this becomes a description when imported to Mac Photos
* takes the first 30 characters from the caption and adds them to the image IPTC data as 'ObjectName' - this becomes the Title when imported to Mac Photos
* Splits out any hashtags from the caption and adds them to the image IPTC data as the 'Keywords' array - these become Mac Photos keywords (if you don't want them comment out line 166 'bytes(nKeywords,'utf-8'),')
* Adds the text string you specified for 'photographer' to the image IPTC data as 'By-line'
* Adds the location (named string not GEO) to the image IPTC data as 'ContentLocationName', also adds it to Mac Photos as a keyword and at the end of the image description
* Adds the date taken to the image IPTC data as 'ReferenceDate'
* then it **MOVES** the files to the 'destFolder' with the new names
* then applies a new file Modified Date of the date the photo was taken - note this means Mac Photos orders them correctly (hack as can not find way to change creation date)

Then it loops through the videos and
* creates a new name for the file (prepends the igname with date)
* **MOVES** the file to the 'destFolder' with the new names
* then applies a new file Modified Date of the date the photo was taken - note this means Mac Photos orders them correctly (hack as can not find way to change creation date )

Then it loops through the direct files (images and video) and
* creates a new name for the file (prepends the igname with date)
* **MOVES** the file to the 'destFolder' with the new names
* then applies a new file Modified Date of the date the photo was taken - note this means Mac Photos orders them correctly (hack as can not find way to change creation date )

When you import them to Mac Photos you can search the keywords, caption, title data and view it from the 'inspector'

## Known issues
* if a photo is part of a multipart post (more than 1 image) no caption is assigned - this is an Instagram issue and no caption is present for the JSON items
* Videos and Direct items don't get the any of the metadata and are only tweaked for name and file date




