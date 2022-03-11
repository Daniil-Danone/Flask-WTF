from PIL import Image

width = 750
img = Image.open('image.jpg')
ratio = (basewidth / float(img.size[0]))
height = int((float(img.size[1]) * float(ratio)))
img = img.resize((basewidth, height), PIL.Image.ANTIALIAS)
img.save('resized_image.jpg')