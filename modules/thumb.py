from PIL import Image

# Open the image
img = Image.open("input.jpg")

# Resize the image to a smaller size
img_resized = img.resize((img.width // 4, img.height // 4), Image.ANTIALIAS)

# Save with lower quality
img_resized.save("output.jpg", quality=30)
