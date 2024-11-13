print("Importing Modules...")

from PIL import Image, ImageDraw, ImageFont, ImageColor
import math
# import moviepy.video.io.ImageSequenceClip
from moviepy.editor import ImageClip, concatenate_videoclips

fps = 30
videoSize = [1080,200]
textHeight = 165
textSize = 150
sizes = [1,1.1,1.2]
heights = [135, 145, 155]

words = []
with open("temp/words.txt", "r") as f:
	content = f.read()

content = content.split("\n")

c = ImageColor.colormap

for word in content:
	split = word.split(" ")
	if len(split) >= 3:
		colour = "white"
		start = int(split[0])
		end = int(split[1])
		word = " ".join(split[2:])
		if (len(split) >= 4):
			if (split[-1] in c):
				colour = split[-1]
				word = " ".join(split[2:-1])
		words.append([word, start, end, colour])

def drawText(text, colour, filename):
	for i in range(3):
		im = Image.new('RGB', videoSize, (0, 255, 0))
		x = int(videoSize[0]/2)
		y = textHeight
		size = int(textSize*sizes[i])

		stroke_width = math.floor(size/15)+1

		draw = ImageDraw.Draw(im)
		font = ImageFont.truetype('temp/calibri.ttf', size=size)
		_, _, w, h = draw.textbbox((0,0), text, font=font)
		draw.text((x-int(w/2), y-heights[i]), text, fill=colour, font=font, stroke_width=stroke_width, stroke_fill='black')

		im.save(f'{filename}{i}.png')

def produceImages(words):
	im = Image.new('RGB', videoSize, (0, 255, 0))
	im.save(f'temp/images/blank.png')
	numWords = len(words)
	for word in enumerate(words):
		print(f"{word[0]}/{numWords}")
		drawText(word[1][0], word[1][3], f"temp/images/{word[0]}_")

def render_video_without_imagesequenceclip(image_files, fps):
    # List to store all the image clips
    image_clips = []

    # Set duration per frame (1 frame per second divided by FPS)
    frame_duration = 1 / fps

    # Create ImageClip for each image and set its duration
    for img_path in image_files:
        img_clip = ImageClip(img_path).set_duration(frame_duration)
        image_clips.append(img_clip)

    # Concatenate all the image clips into one video
    video = concatenate_videoclips(image_clips, method="compose")

    # Set the final video FPS
    video = video.set_fps(fps)

    # Write the video file
    output_filename = 'output/subtitles.mp4'
    print("Writing Video...")
    video.write_videofile(output_filename)

def renderVideo(words):
	totalFrames = words[-1][2]
	currentWord = 0
	animationIndex = 0

	image_files = []

	for i in range(totalFrames):
		if words[currentWord][2] == i:
			currentWord += 1
			animationIndex = 0

		if words[currentWord][1] <= i:
			image_files.append(f"temp/images/{currentWord}_{animationIndex}.png")
		else:
			image_files.append(f"temp/images/blank.png")
			animationIndex = 0

		if animationIndex < 2:
			animationIndex += 1

		while words[currentWord][2] == i:
			currentWord += 1
			animationIndex = 0

			if words[currentWord][1] <= i:
				image_files.append(f"temp/images/{currentWord}_{animationIndex}.png")
			else:
				image_files.append(f"temp/images/blank.png")

	print("Combining Frames...")
	render_video_without_imagesequenceclip(image_files, fps=fps)

print("Rendering Frames...")
produceImages(words)
print("Rendering Videos...")
renderVideo(words)

# input()