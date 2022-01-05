from PIL import Image
import os
dir = '/Users/lukecoburn/Pictures/ria_photos/'
save_dir = dir + 'edited/'
count = 0
for img in os.listdir(dir):

    if count <= 20 and '.jpeg' in img:

        image = Image.open(dir + img)
        width, height = image.size
        border = int(0.5*(13/7.5*width - width))
        new_width = width + 2*border
        new_height = height + 2*border

        result = Image.new(image.mode, (new_width, new_height), (0, 0, 0))
        result.paste(image, (border, border))
        im_str = save_dir + img
        result.save(im_str)
        print(im_str)
