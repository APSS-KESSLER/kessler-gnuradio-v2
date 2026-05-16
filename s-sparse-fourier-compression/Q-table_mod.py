from PIL import Image

# This is a standard JPEG to compare to, it uses 70% quality factor like Software team
img_webp = Image.open('NY.webp')
img_webp.save('NY.png')

img_png = Image.open('NY.png')
img_png.save('standard_modified_NY.jpg', quality=70)

img_jpg = Image.open('standard_modified_NY.jpg')
print("---------------------BELOW ARE 70% IMG Q-TABLES-------------------------")
q_tables = img_jpg.quantization
print(q_tables)

# This standard set up allows us to replicate Pillow's default JPEG 70% quality set up.
# Mainly was used for debugging purposes to ensure no extra bytes were added to our cusotmised
# JPEG due to our manipulations here.
standard_luma_table = [10, 7, 6, 10, 14, 24, 31, 37, 
                       7, 7, 8, 11, 16, 35, 36, 33, 
                       8, 8, 10, 14, 24, 34, 41, 34, 
                       8, 10, 13, 17, 31, 52, 48, 37, 
                       11, 13, 22, 34, 41, 65, 62, 46, 
                       14, 21, 33, 38, 49, 62, 68, 55, 
                       29, 38, 47, 52, 62, 73, 72, 61, 
                       43, 55, 57, 59, 67, 60, 62, 59]

standard_chroma_table = [10, 11, 14, 28, 59, 59, 59, 59, 
                         11, 13, 16, 40, 59, 59, 59, 59, 
                         14, 16, 34, 59, 59, 59, 59, 59, 
                         28, 40, 59, 59, 59, 59, 59, 59, 
                         59, 59, 59, 59, 59, 59, 59, 59, 
                         59, 59, 59, 59, 59, 59, 59, 59, 
                         59, 59, 59, 59, 59, 59, 59, 59, 
                         59, 59, 59, 59, 59, 59, 59, 59]

standard_q_tables = [standard_luma_table, standard_chroma_table]



img_my = Image.open('NY.png')



# This is a custom quantization table taken from the (1) 'Optimal quantization table 
# generation for efficient satellite image compression using teaching learning 
# based optimization technique' paper.
first_custom_luma_table = [53, 39, 38, 36, 224, 37, 139, 128,
                    46, 40, 37, 34, 38, 142, 224, 170,
                    38, 30, 41, 41, 77, 204, 239, 58,
                    36, 37, 31, 58, 95, 86, 83, 116,
                    31, 51, 53, 89, 106, 249, 75, 81,
                    60, 63, 85, 228, 119, 171, 145, 69,
                    80, 65, 95, 192, 161, 124, 117, 295,
                    194, 80, 72, 78, 121, 81, 82, 152]

# These are the custom quantization tables from the (2) 'Adjusted JPEG Quantization 
# Tables in Support of GPS Maps' paper.
second_custom_luma_table = [6, 6, 6, 6, 8, 8, 9, 9,
                            6, 6, 6, 6, 8, 8, 9, 9,
                            6, 6, 6, 6, 8, 8, 9, 9,
                            6, 6, 6, 8, 8, 9, 9, 9,
                            8, 8, 8, 8, 9, 9, 9, 9,
                            8, 8, 8, 9, 9, 9, 9, 9,
                            9, 9, 9, 9, 9, 9, 9, 9,
                            9, 9, 9, 9, 9, 9, 9, 9]
second_custom_chroma_table = [6, 6, 6, 6, 8, 8, 9, 10,
                              6, 6, 6, 6, 8, 8, 9, 10,
                              6, 6, 6, 6, 8, 8, 9, 10,
                              6, 6, 6, 8, 8, 9, 9, 10,
                              8, 8, 8, 8, 9, 9, 10, 10,
                              8, 8, 8, 9, 9, 10, 10, 10,
                              9, 9, 9, 9, 10, 10, 10, 10,
                              10, 10, 10, 10, 10, 10, 10, 10]

third_custom_luma_table = [13, 17, 21, 39, 45, 81, 65, 75,
                           24, 32, 0, 19, 45, 113, 110, 54,
                           19, 29, 50, 57, 75, 105, 115, 70,
                           18, 40, 27, 45, 89, 109, 119, 61,
                           28, 47, 56, 115, 131, 127, 128,  69,
                           56, 35, 77, 118, 161, 171, 87, 109,
                           87, 125, 105, 138, 163, 167, 182, 137,
                           117, 146, 156, 180, 138, 136, 147, 118]


# Currently set JPEG Q-table for 

custom_q_tables = [third_custom_luma_table, third_custom_luma_table]

img_my.save('custom_modified_NY.jpg', qtables=custom_q_tables)