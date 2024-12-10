from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Load Images
image1 = Image.open('images/current.png') # update this path
image2 = Image.open('images/current.png')
image3 = Image.open('images/energy.png')
image4 = Image.open('images/voltage_2.png')


# Define the size of the blank template (e.g., 4000 x 2250 pixels)
template_width = 4000
template_height = 2250

template_image = Image.new('RGB', (template_width, template_height), color='lightgray')

positions = [(50,1300),(2450, 1300),(2450, 250),(0,0),(2450,1200),(2450,150)]

image1_resized = image1.resize((2350, 900))
image2_resized = image2.resize((1500, 900))
image3_resized = image3.resize((1500, 900))
header = Image.new('RGB', (4000, 100), color=(176, 196, 222))
title_header = Image.new('RGB', (1500,100), color=(176, 196, 222))

# Paste the resized images onto the template at the specified positions
template_image.paste(image1_resized, positions[0])
template_image.paste(image2_resized, positions[1])
template_image.paste(image3_resized, positions[2])
template_image.paste(header, positions[3])
template_image.paste(title_header, positions[4])
template_image.paste(title_header, positions[5])


# ----------------------------------------------


# Initialize ImageDraw
draw = ImageDraw.Draw(template_image)

# Define the text and position
title = "Energy Consumption Report: SmartFit Monterrico"
title_pos = (50, 0)

subtitle_1 = "Consumed Energy (KW): Last 3 Hours"
subtitle_2 = "Current: Last 2 Hours"
subtitle_pos_1 = (2950,1220)
subtitle_pos_2 = (2700,170)

# Define the font and size (you can use a truetype font file if available)
title_font = ImageFont.truetype("arial.ttf", 80)
subtitle_font = ImageFont.truetype("arial.ttf", 60)
# Define the text color
text_color = (0, 0, 0)  # white

# Add text to the image
draw.text(title_pos, title, fill=text_color, font=title_font, bold=True)
draw.text(subtitle_pos_1, subtitle_2, fill=text_color, font=subtitle_font, bold=True)
draw.text(subtitle_pos_2, subtitle_1, fill=text_color, font=subtitle_font, bold=True)

# Display the final image to verify the text is placed correctly
template_image.show()