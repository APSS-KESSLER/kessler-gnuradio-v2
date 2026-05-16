from PIL import Image, ImageChops, JpegImagePlugin
import pillow_jxl

# Set up intial JPEG for demo
img_png = Image.open('NY.png')
img_png.save("NY.jpg", quality=70)

# Save an image as JXL
img_jpg = Image.open("NY.jpg")
img_jpg.save("NY.jxl", quality=70)

sampling = JpegImagePlugin.get_sampling(img_jpg)
print("sampling is: ", sampling)

# Convert JXL back to JPG to see if any chnages occured
img_jxl = Image.open("NY.jxl")
img_jxl.save("NY.jpg", quality=70)

# Take the difference from orginal JPEG and JPEG after conversion to JPEG XL.
# A completely black box shows that there is 0 difference introduced by our JPEG 
# XL conversion and thus it is truly lossless compression.
img_jpg_new = Image.open("NY.jpg")
diff = ImageChops.difference(img_jpg_new, img_jpg)
diff.show()

