from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib2
import sys
import time

os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"

def main():
	searchtext = sys.argv[1]
	num_requested = int(sys.argv[2])
	number_of_scrolls = num_requested / 400 + 1 

	if not os.path.exists(download_path + searchtext.replace(" ", "_")):
		os.makedirs(download_path + searchtext.replace(" ", "_"))

	url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
	driver = webdriver.Firefox()
	driver.get(url)

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	extensions = {"jpg", "jpeg", "png", "gif"}
	img_count = 0
	downloaded_img_count = 0
	
	for _ in xrange(number_of_scrolls):
		for __ in xrange(10):
			
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		
		time.sleep(0.5)
		try:
			driver.find_element_by_xpath("//input[@value='Show more results']").click()
		except Exception as e:
			print ("Less images found:"), e
			break

	imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
	print ("Total images:"), len(imges), "\n"
	for img in imges:
		img_count += 1
		img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
		img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
		print ("Downloading image"), img_count, ": ", img_url
		try:
			if img_type not in extensions:
				img_type = "jpg"
			req = urllib2.Request(img_url, headers=headers)
			raw_img = urllib2.urlopen(req).read()
			f = open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, "wb")
			f.write(raw_img)
			f.close
			downloaded_img_count += 1
		except Exception as e:
			print ("Download failed:"), e
		finally:
			print
		if downloaded_img_count >= num_requested:
			break

	print ("Total downloaded: "), downloaded_img_count, "/", img_count
	driver.quit()

if __name__ == "__main__":
	main()
