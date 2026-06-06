from PIL import Image, ImageChops, JpegImagePlugin
import pillow_jxl

# Set up intial JPEG for demo
img_webp = Image.open('images/NY.webp')
img_webp.save("images/NY.png", quality=70)

# Set up intial JPEG for demo
img_png = Image.open('images/NY.png')
img_png.save("images/NY_to_jxl.jxl", quality=70)
img_png.save("images/NY.jpg", quality=70)

# Save an image as JXL
img_jpg = Image.open("images/NY.jpg")
img_jpg.save("images/NY_jpeg_to_jxl.jxl", quality=70)

# Convert JXL back to JPG to see if any chnages occured
img_jxl = Image.open("images/NY.jxl")
img_jxl.save("images/NY.jpg", quality=70)

# Take the difference from orginal JPEG and JPEG after conversion to JPEG XL.
# A completely black box shows that there is 0 difference introduced by our JPEG 
# XL conversion and thus it is truly lossless compression.
#img_jpg_new = Image.open("images/river.jpg")
#diff = ImageChops.difference(img_jpg_new, img_jpg)
#diff.show()

