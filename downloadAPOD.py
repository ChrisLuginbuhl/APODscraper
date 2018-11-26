
#! python3
# downloadAPOD.py - Downloads every single APOD image, excludes non-image files.
# Chris Luginbuhl Nov 2018
# Based on an example by from: Al Sweigart. “Automate the Boring Stuff with Python.” Apple Books. p284

import requests, os, bs4

#Download the archive page and put it in a soup object
archiveUrl = 'https://apod.nasa.gov/apod/archivepix.html'  # starting url
startPoint = 5                                             # skip first few links
counter = 0
os.makedirs('apod', exist_ok=True)                         # store imgs in ./apod
print('Downloading page %s...' % archiveUrl)
res = requests.get(archiveUrl)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

#find the URLs for the images in each of the web pages linked from the archive page
#skipping the first few links which are not images
for tag in soup.find_all('a')[(startPoint + counter):]:
    htmlFilename = tag.get('href')    
    print(startPoint + counter, ".  html filename: ", htmlFilename, "    ", end = '')
    imgPageUrl = os.path.join('https://apod.nasa.gov/apod/', htmlFilename)
    page = requests.get(imgPageUrl)
    page.raise_for_status()
    soupTxt = bs4.BeautifulSoup(page.text, "lxml") #converts webpage unicode to string - hierarchy of tags
    imgElem = soupTxt.img #these pages only have one img tag. Otherwise this would return a list(?)
    if imgElem == None:
        print('Could not find image.')
    else:
        imgUrl = 'https://apod.nasa.gov/apod/' + imgElem.get('src')
        # download the images from each of those URLs
        print('Downloading image %s...' % (imgUrl))
        resp = requests.get(imgUrl)
        resp.raise_for_status()
        #save the file
        imageFile = open(os.path.join('apod', os.path.basename(imgUrl)), 'wb')
        for chunk in resp.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        counter += 1
print('Done.')
