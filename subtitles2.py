import pygame
from pydub import AudioSegment
import sys
import os
import time
import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
from subtitlesHelper import *
import copy

pygame.init()

fps = 30
audioFile = "output/audio.wav"
windowSize = [1920, 1080]
audio = AudioSegment.from_file(audioFile)
audioDuration = len(audio)/1000
audioFrames = math.ceil(audioDuration*fps)
pixelsPerFrame = 10
totalPixels = audioFrames*pixelsPerFrame
clipThinkness = 40
clipCurve = 3
clipMarginLeft = 200
fontPath = "temp/calibri.ttf"
fontColour = (255,255,255)
bigFontSize = 200
smallFontSize = 20
wordMarginLeft = 20
playing = False
saveOffset = (20,20)

currentFrame = 0

clipColour = (200,255,255)
backgroundColour = (30,30,30)

prevWordIndex = -1

clock = pygame.time.Clock()
pygame.display.set_caption("Subtile Bot")
os.environ['SDL_VIDEO_CENTERED'] = '1'
win = pygame.display.set_mode(windowSize, pygame.NOFRAME)

mainTextBox = textbox("", fontPath, bigFontSize, fontColour, (int(windowSize[0]/3*2), int(windowSize[1]/3)), boundingBox = (int(windowSize[0]), int(bigFontSize*1.5)), boundingPlacement = "midMid", fontPlacement = "midMid", verticalMargin = 0, horizontalMargin = 0, baseColour = None, boundingRadius = None, editable = False, selectedColour = None)
saveTextBox = textbox("Save and Exit", fontPath, 50, (100,100,100), (int(windowSize[0]-saveOffset[0]), int(windowSize[1]-saveOffset[1])), boundingBox = None, boundingPlacement = "bottomRight", fontPlacement = "bottomRight", verticalMargin = 0, horizontalMargin = 0, baseColour = None, boundingRadius = None, editable = False, selectedColour = None)


words = []
wordBoxes = []
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
		words.append([textbox(word, fontPath, smallFontSize, fontColour, (0, 0), boundingBox = (int(windowSize[0]/4), smallFontSize), boundingPlacement = "midLeft", fontPlacement = "midLeft", verticalMargin = 0, horizontalMargin = 0, baseColour = None, boundingRadius = None, editable = True, selectedColour = None), start, end, colour, False])

def playAudioFrames(file, frame, frames):
	pygame.mixer.quit()
	pygame.mixer.init()
	audio = AudioSegment.from_file(file)

	# Convert frame number to milliseconds
	start_time = frame * (1000/fps)
	end_time = (frame+frames) * (1000/fps)
	
	if start_time < len(audio)-1:
		if end_time >= len(audio):
			end_time = len(audio-1)

		# Extract the segment to play
		segment = audio[start_time:end_time]
		temp_file = "temp/temp_segment.wav"
		segment.export(temp_file, format="wav")

		# Load the temporary file for playback
		pygame.mixer.music.load(temp_file)
		pygame.mixer.music.play()

def getSelectedWordIndex():
	for i, word in enumerate(words):
		if word[0].selected:
			return i
	return -1

def getCurrentWordIndex(frame):
	for i, word in enumerate(words):
		if word[1] == frame:
			return i
		if word[1] <= frame and word[2] > frame:
			return i
		if word[1] > frame:
			return -1
	return -1

def getNearestWordIndex(frame):
	returnValue = 0 
	for i, word in enumerate(words):
		if word[1] <= frame:
			returnValue = i
	return returnValue

def renderWordBoxes():
	offset = int(windowSize[1]/2-currentFrame*pixelsPerFrame)
	pygame.draw.rect(win, (100,100,100), (clipMarginLeft-clipThinkness, offset, 300, 1))
	pygame.draw.rect(win, (100,100,100), (clipMarginLeft-clipThinkness, offset+audioFrames*pixelsPerFrame, 300, 1))
	for word in words:
		pygame.draw.rect(win, clipColour, (clipMarginLeft, offset+word[1]*pixelsPerFrame, clipThinkness, (word[2]-word[1])*pixelsPerFrame-1), 0, clipCurve)

		x = clipMarginLeft + clipThinkness + wordMarginLeft
		y = offset+int(word[1]+(word[2]-word[1])/2)*pixelsPerFrame

		word[0].position = [x,y]
		word[0].box = (word[0].position[0] + word[0].boundingOffest[0], word[0].position[1] + word[0].boundingOffest[1], word[0].boundingBox[0], word[0].boundingBox[1])

		word[0].draw(win)

def pause():
	global playing
	if playing:
		playing = False
		pygame.mixer.quit()

def play():
	global playing
	if not playing:
		playing = True
		playAudioFrames(audioFile, currentFrame, 1000000)

def drawMainTextBox():
	global prevWordIndex
	i = getCurrentWordIndex(currentFrame)
	word = ""
	if i != -1:
		word = words[i][0].text
		
	if prevWordIndex != i:
		prevWordIndex = i
		mainTextBox.text = word
		mainTextBox.renderSurface()

	mainTextBox.draw(win)

def writeToFile():
	fileString = ""
	for word in words:
		fileString += f"{word[1]} {word[2]} {word[0].text}\n"

	with open("temp/words.txt", "w") as f:
		f.write(fileString)

def draw():
	win.fill(backgroundColour)
	renderWordBoxes()
	pygame.draw.rect(win, (255,0,0), (clipMarginLeft-clipThinkness, int(windowSize[1]/2), 300, 1))
	drawMainTextBox()
	saveTextBox.draw(win)
	pygame.display.update()

heldArrows = [0,0]
ctrl = False
shift = False

loop = True
while loop:
	clock.tick(30)
	for event in pygame.event.get():
		# Exit program
		if event.type == pygame.QUIT:
			loop = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			# LEFT CLICK
			if event.button == 1:
				mousePos = pygame.mouse.get_pos()

				if pointBoxCollision(mousePos, saveTextBox.box):
					writeToFile()
					loop = False

				# mainTextBox.handleClicks(mousePos)
				for word in words:
					word[0].handleClicks(mousePos)

		if event.type == pygame.KEYDOWN:
			# mainTextBox.handleKeyPress(event.key, event.unicode)
			if event.key == pygame.K_LCTRL:
				ctrl = True
			if event.key == pygame.K_LSHIFT:
				shift = True

			if event.key == pygame.K_RETURN:
				index = getCurrentWordIndex(currentFrame)
		
				newWords = []
				for i in range(len(words)):
					newWords.append(words[i])
					if i == index:
						newWords.append([textbox(words[i][0].text, fontPath, smallFontSize, fontColour, (0, 0), boundingBox = (int(windowSize[0]/4), smallFontSize), boundingPlacement = "midLeft", fontPlacement = "midLeft", verticalMargin = 0, horizontalMargin = 0, baseColour = None, boundingRadius = None, editable = True, selectedColour = None), words[i][1], words[i][2], words[i][3], False])

						newWords[i][2] = currentFrame
						newWords[i+1][1] = currentFrame

				words = newWords

			if event.key == pygame.K_DELETE:
				i = getCurrentWordIndex(currentFrame)
				if i != -1:
					words[i][4] = True
					words = [word for word in words if not word[4]]
			
			if event.key == pygame.K_UP:
				if ctrl:
					i = getNearestWordIndex(currentFrame-1)
					currentFrame = words[i][1]
					playAudioFrames(audioFile, currentFrame, 1)

					heldArrows[0] += 1

				elif shift:
					i = getSelectedWordIndex()
					if i != -1 and currentFrame <= words[i][2]:
						oldStart = words[i][1]
						words[i][1] = currentFrame
						for wi, word in enumerate(words):
							if wi != i:
								if word[2] == oldStart:
									word[2] = currentFrame
								if word[1] >= currentFrame and word[2] <= words[i][2]:
									word[4] = True
								if word[1] < currentFrame and word[2] > currentFrame:
									word[2] = currentFrame

						words = [word for word in words if not word[4]]
				else:
					currentFrame -= 1
					if currentFrame < 0:
						currentFrame = 0
					playAudioFrames(audioFile, currentFrame, 1)
				
					heldArrows[0] += 1
			
			if event.key == pygame.K_DOWN:
				if ctrl:
					i = getNearestWordIndex(currentFrame)
					if i + 1 < len(words):
						currentFrame = words[i+1][1]
						playAudioFrames(audioFile, currentFrame, 1)
					
					heldArrows[1] += 1

				elif shift:
					i = getSelectedWordIndex()
					if i != -1 and currentFrame >= words[i][1]:
						oldEnd = words[i][2]
						words[i][2] = currentFrame
						for wi, word in enumerate(words):
							if wi != i:
								if word[1] == oldEnd:
									word[1] = currentFrame
								if word[1] >= words[i][1] and word[2] <= currentFrame:
									word[4] = True
								if word[1] < currentFrame and word[2] > currentFrame:
									word[1] = currentFrame

						words = [word for word in words if not word[4]]
				else:
					currentFrame += 1
					if currentFrame > audioFrames:
						currentFrame = audioFrames
					playAudioFrames(audioFile, currentFrame, 1)
				
					heldArrows[1] += 1

			if event.key == pygame.K_LALT:
				i = getCurrentWordIndex(currentFrame)
				if i != -1:
					for word in words:
						word[0].handleClicks((words[i][0].position[0]+1,words[i][0].position[1]))

			if event.key == pygame.K_SPACE:
				if not ctrl and not shift:
					if playing:
						pause()
					else:
						play()
				else:
					for word in words:
						word[0].handleKeyPress(event.key, event.unicode)

			elif not ctrl:
				for word in words:
					word[0].handleKeyPress(event.key, event.unicode)

		if event.type == pygame.KEYUP:
			# mainTextBox.handleKeyRelease(event.key, event.unicode)
			if event.key == pygame.K_LCTRL:
				ctrl = False
			if event.key == pygame.K_LSHIFT:
				shift = False
			if event.key == pygame.K_UP:
				heldArrows[0] = 0
			if event.key == pygame.K_DOWN:
				heldArrows[1] = 0
			
			for word in words:
				word[0].handleKeyRelease(event.key, event.unicode)
	
	if heldArrows[0] != 0:
		heldArrows[0] += 1
	if heldArrows[1] != 0:
		heldArrows[1] += 1

	if heldArrows[0] > 10:
		if ctrl:
			i = getNearestWordIndex(currentFrame-1)
			currentFrame = words[i][1]
		else:
			currentFrame -= 1
			if currentFrame < 0:
				currentFrame = 0
	if heldArrows[1] > 10:
		if ctrl:
			i = getNearestWordIndex(currentFrame)
			if i + 1 < len(words):
				currentFrame = words[i+1][1]
		else:
			currentFrame += 1
			if currentFrame > audioFrames:
				currentFrame = audioFrames

	if playing:
		currentFrame += 1
		if currentFrame > audioFrames:
			currentFrame = audioFrames

	draw()