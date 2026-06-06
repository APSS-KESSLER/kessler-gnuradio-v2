from PIL import Image

# This is a standard JPEG to compare to, it uses  %quality factor like Software team
img_webp = Image.open('images/NY.webp')
img_webp.save('images/NY.png')

img_png = Image.open('images/NY.png')
img_png.save('images/standard_modified_NY.jpg', quality=70)

img_jpg = Image.open('images/standard_modified_NY.jpg')

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



img_my = Image.open('images/NY.png')



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

# These are the custom quantization tables from the (3) 'simulated
# annealing for JPEG' paper.
third_custom_luma_table_35 = [11, 35, 35, 53, 61, 63, 47, 69,
                              35, 41, 39, 54, 54, 57, 44, 47, 
                              44, 51, 61, 65, 48, 62, 79, 63, 
                              38, 53, 60, 57, 58, 96, 102, 76, 
                              44, 58, 68, 57, 81, 100, 96, 76, 
                              74, 60, 62, 72, 98, 121, 94, 110, 
                              55, 47, 91, 89, 81, 130, 102, 105, 
                              96, 106, 107, 100, 79, 87, 97, 103]
third_custom_luma_table_50 = [8, 30, 64, 86, 105, 97, 95, 70, 
                              31, 58, 78, 99, 88, 79, 73, 65, 
                              52, 66, 93, 103, 81, 83, 86, 70, 
                              70, 87, 94, 79, 80, 79, 104, 71, 
                              75, 98, 71, 91, 74, 111, 111, 83, 
                              92, 81, 71, 71, 69, 101, 142, 93, 
                              84, 82, 79, 64, 83, 120, 113, 103, 
                              100, 93, 127, 115, 128, 116, 69, 108]
third_custom_luma_table_75 = [8, 22, 39, 43, 74, 67, 63, 65,
                              34, 55, 48, 51, 76, 65, 77, 55,
                              33, 42, 50, 57, 77, 75, 68, 47, 
                              58, 44, 60, 82, 78, 123, 76, 68, 
                              50, 74, 71, 91, 84, 103, 91, 66, 
                              50, 52, 53, 71, 73, 72, 137, 97, 
                              48, 66, 82, 66, 102, 154, 119, 96, 
                              100, 72, 92, 86, 94, 82, 124, 90]
third_custom_luma_table_95 = [8, 13, 16, 25, 39, 68, 95, 74, 
                              13, 19, 47, 17, 49, 65, 79, 69, 
                              19, 15, 36, 23, 67, 95, 79, 58, 
                              15, 39, 30, 85, 79, 127, 128, 77, 
                              27, 47, 55, 75, 122, 174, 116, 76,
                              45, 87, 75, 86, 102, 167, 178, 105, 
                              71, 96, 113, 115, 139, 156, 151, 122, 
                              137, 131, 161, 140, 176, 115, 132, 125]

# This is from libvips library (Table tuned for PSNR-HVS-M on Kodak image set),
# on the doc this should be (4)
foruth_custom_luma_table_HVS = [9, 10, 12, 14, 19, 26, 38, 57,
                                10, 12, 14, 19, 26, 38, 57, 86,
                                12, 14, 19, 26, 38, 57, 86, 129,
                                14, 19, 26, 38, 57, 86, 129, 193,
                                19, 26, 38, 57, 86, 129, 193, 289,
                                26, 38, 57, 86, 129, 193, 289, 433,
                                38, 57, 86, 129, 193, 289, 433, 650,
                                57, 86, 129, 193, 289, 433, 650, 975]
foruth_custom_luma_table_MSSIM = [9, 9, 10, 12, 13, 17, 23, 31,
                                  9, 11, 11, 12, 15, 19, 25, 33,
                                  10, 11, 13, 15, 18, 23, 29, 39,
                                  12, 12, 15, 18, 22, 27, 34, 46,
                                  13, 15, 18, 22, 28, 34, 43, 58,
                                  17, 19, 23, 27, 34, 44, 55, 74,
                                  23, 25, 29, 34, 43, 55, 73, 100,
                                  31, 33, 39, 46, 58, 74, 100, 139]


# Currently set JPEG Q-table for 
custom_q_tables = [foruth_custom_luma_table_MSSIM, standard_chroma_table]

img_my.save('images/custom_modified_NY.jpg', qtables=custom_q_tables)