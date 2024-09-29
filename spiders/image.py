import scrapy
import shutil
import time
import os
from scrapy.crawler import CrawlerProcess
from PIL import Image
import face_recognition

class ImageSpider(scrapy.Spider):
    name = "image"
    start_urls = ["https://edition.cnn.com/2021/06/11/politics/gallery/g7-summit-history/index.html"]

    # Clear the old filestore and make a new one
    try:
        shutil.rmtree('./filestore')
        print("removing old filestore")
    except OSError:
        pass
    # time.sleep(0.5)

    try:
        os.makedirs('./filestore')
        print("make new filestore")
    except OSError:
        pass

    def parse(self, response):
        # Extract the main image URL
        image_div = response.xpath('//div[@data-name="01 g7 family photos through the years"]/@data-url').get()

        # Download the image from 'image_div' if it exists
        if image_div:
            yield scrapy.Request(url=image_div, callback=self.scrape_image)

    def scrape_image(self, response):
        # Extract the file name from the URL
        file_name = response.url.split("?")[0].split("/")[-1]
        file_path = os.path.join('filestore', file_name)
        
        # Write the image to the 'filestore' directory
        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f"Saved file {file_name}")

        # Call face_detection method
        self.face_detection(file_path)

    def face_detection(self, file_path):
        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(file_path)

        # Find all the faces in the image using the default HOG-based model.
        face_locations = face_recognition.face_locations(image)

        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location

            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()

# Run the Scrapy spider
process = CrawlerProcess()
process.crawl(ImageSpider)
process.start()



