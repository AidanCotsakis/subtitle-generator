import pygame
import os

pygame.init()

characterString = """!"# $%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~Çüéâ\n"""

def pointBoxCollision(point, box):
	if point[0] >= box[0] and point[0] <= box[0] + box[2] and point[1] >= box[1] and point[1] <= box[1] + box[3]:
		return True
	else:
		return False

class textbox():
	def __init__(self, text, fontPath, fontSize, fontColour, position, boundingBox = None, boundingPlacement = "topLeft", fontPlacement = "topLeft", verticalMargin = 0, horizontalMargin = 0, baseColour = None, boundingRadius = None, editable = False, selectedColour = None):
		self.text = text # string of displayed text
		self.fontPath = fontPath # string of fontPath
		self.fontSize = fontSize # int/float of font size in pixels
		self.fontColour = fontColour # rgb value of font colour stored in array (255,255,255)
		self.position = position # 2 coordinates in pixels of the font Orgin (0,0)
		self.boundingPlacement = boundingPlacement #string containing "top/mid/bottom" + "Left/Mid/Right"
		self.fontPlacement = fontPlacement
		self.boundingBox = boundingBox # a box containing the following information (width, height) that the boundingBox is restricted to
		self.verticalMargin = verticalMargin # a single number indicating how far off the center the text is from the bounding box
		self.horizontalMargin = horizontalMargin
		self.boundingColour = baseColour # rgb value of bounding colour stored in array (255,255,255)
		self.boundingRadius = boundingRadius # a single value of the radius of the edges of the bounding box
		self.editable = editable # true or false if the user can click and type in the box
		self.selectedColour = selectedColour # rgb value of font colour stored in array (255,255,255)

		self.showHitbox = False

		self.typeLineFrames = 30 #number of frames per cycle of the type bar 

		self.font = pygame.font.Font(self.fontPath, self.fontSize) # make pygame font object
		self.renderedFont = self.font.render(self.text, True, self.fontColour)
		
		self.dynamicBox = False
		if self.boundingBox == None:
			self.boundingBox = [self.renderedFont.get_size()[0] + self.horizontalMargin*2, self.renderedFont.get_size()[1] + self.verticalMargin*2]
			self.dynamicBox = True

		if self.boundingPlacement == "topLeft": self.boundingOffest = [0,0]
		elif self.boundingPlacement == "topMid": self.boundingOffest = [-self.boundingBox[0]/2,0]
		elif self.boundingPlacement == "topRight": self.boundingOffest = [-self.boundingBox[0],0]
		elif self.boundingPlacement == "midLeft": self.boundingOffest = [0,-self.boundingBox[1]/2]
		elif self.boundingPlacement == "midMid": self.boundingOffest = [-self.boundingBox[0]/2,-self.boundingBox[1]/2]
		elif self.boundingPlacement == "midRight": self.boundingOffest = [-self.boundingBox[0],-self.boundingBox[1]/2]
		elif self.boundingPlacement == "bottomLeft": self.boundingOffest = [0,-self.boundingBox[1]]
		elif self.boundingPlacement == "bottomMid": self.boundingOffest = [-self.boundingBox[0]/2,-self.boundingBox[1]]
		elif self.boundingPlacement == "bottomRight": self.boundingOffest = [-self.boundingBox[0],-self.boundingBox[1]]

		if self.fontPlacement[:3] == "top":
			self.verticalAlign = "top"
		elif self.fontPlacement[:3] == "mid":
			self.verticalAlign = "mid"
		elif self.fontPlacement[:3] == "bot":
			self.verticalAlign = "bottom"

		if self.fontPlacement == "topLeft" or self.fontPlacement == "midLeft" or self.fontPlacement == "bottomLeft":
			self.horizontalAlign = "left"
		if self.fontPlacement == "topMid" or self.fontPlacement == "midMid" or self.fontPlacement == "bottomMid":
			self.horizontalAlign = "mid"
		if self.fontPlacement == "topRight" or self.fontPlacement == "midRight" or self.fontPlacement == "bottomRight":
			self.horizontalAlign = "right"

		self.selected = False
		self.baseColour = baseColour
		self.box = (self.position[0] + self.boundingOffest[0], self.position[1] + self.boundingOffest[1], self.boundingBox[0], self.boundingBox[1])
		self.ticker = 0

		self.heldKey = None # [key, unicode/letter, tickerTime]
		self.heldKeyDelay = 15 #ticks for the key to be held and repeatedly entered

		self.renderOffset = [0,0]

		self.renderSurface()

	def renderSurface(self, ignoreDynamic = False):
		if self.dynamicBox and not ignoreDynamic:
			self.surface = pygame.Surface([self.boundingBox[0]+self.fontSize,self.boundingBox[1]+self.fontSize], pygame.SRCALPHA, 32)
		else:
			self.surface = pygame.Surface([self.boundingBox[0]-self.horizontalMargin*2,self.boundingBox[1]-self.verticalMargin*2], pygame.SRCALPHA, 32)

		self.surface = self.surface.convert_alpha()

		# update boundingOffset if need be
		if self.boundingPlacement == "topLeft": self.boundingOffest = [0,0]
		elif self.boundingPlacement == "topMid": self.boundingOffest = [-self.boundingBox[0]/2,0]
		elif self.boundingPlacement == "topRight": self.boundingOffest = [-self.boundingBox[0],0]
		elif self.boundingPlacement == "midLeft": self.boundingOffest = [0,-self.boundingBox[1]/2]
		elif self.boundingPlacement == "midMid": self.boundingOffest = [-self.boundingBox[0]/2,-self.boundingBox[1]/2]
		elif self.boundingPlacement == "midRight": self.boundingOffest = [-self.boundingBox[0],-self.boundingBox[1]/2]
		elif self.boundingPlacement == "bottomLeft": self.boundingOffest = [0,-self.boundingBox[1]]
		elif self.boundingPlacement == "bottomMid": self.boundingOffest = [-self.boundingBox[0]/2,-self.boundingBox[1]]
		elif self.boundingPlacement == "bottomRight": self.boundingOffest = [-self.boundingBox[0],-self.boundingBox[1]]

		# FIND WHERE EACH LINE SHPOULD BE
		textBreaks = self.text.split("\n")

		textLines = []
		# break each newline and wrap text if it is greater than the surface size
		for textBreak in textBreaks:
			words = textBreak.split(" ")

			textLine = [words[0]]
			for word in words[1:]:
				textLine.append(word)
				if self.font.render(" ".join(textLine), True, self.fontColour).get_size()[0] > self.surface.get_size()[0]:
					textLines.append(" ".join(textLine[:-1]))
					textLine = [word]
			
			textLines.append(" ".join(textLine))

		renderedLines = []
		# render all the final text lines
		for textLine in textLines:
			renderedLines.append(self.font.render(textLine, True, self.fontColour))

		# find the height each line should be
		lineHeight = 0
		maxWidth = 0
		for renderedLine in renderedLines:
			if renderedLine.get_size()[1] > lineHeight:
				lineHeight = renderedLine.get_size()[1]
			if self.dynamicBox and renderedLine.get_size()[0] > maxWidth:
				maxWidth = renderedLine.get_size()[0]


		totalHeight = lineHeight*len(renderedLines)

		lastLineOffset = [0,0]

		# paste the rendered text lines onto the surface depending on the chosen alignment
		for renderedLine in enumerate(renderedLines):
			offset = [0,0]

			if self.horizontalAlign == "mid":
				offset[0] = int(self.surface.get_size()[0]/2 - renderedLine[1].get_size()[0]/2)
			elif self.horizontalAlign == "right":
				offset[0] = int(self.surface.get_size()[0] - renderedLine[1].get_size()[0])

			if self.verticalAlign == "top":
				offset[1] = lineHeight*renderedLine[0]
			elif self.verticalAlign == "mid":
				offset[1] = lineHeight*renderedLine[0] + int(self.surface.get_size()[1]/2 - totalHeight/2)
			elif self.verticalAlign == "bottom":
				offset[1] = lineHeight*renderedLine[0] + int(self.surface.get_size()[1] - totalHeight)

			self.surface.blit(renderedLine[1], offset)

			self.lastLineOffset = [offset[0] + renderedLine[1].get_size()[0], offset[1]]

		self.lineHeight = lineHeight

		if self.dynamicBox and not ignoreDynamic:
			self.boundingBox = [maxWidth + self.horizontalMargin*2, totalHeight + self.verticalMargin*2]
			self.renderSurface(ignoreDynamic = True)
		
		self.box = (self.position[0] + self.boundingOffest[0], self.position[1] + self.boundingOffest[1], self.boundingBox[0], self.boundingBox[1])

	# handles weather or not the text box is selected via click position [0,0]
	def handleClicks(self, pos):
		if self.editable and not self.selected and pointBoxCollision(pos, self.box):
			self.selected = True
			if self.boundingColour:
				self.boundingColour = self.selectedColour

		elif self.editable and self.selected and not pointBoxCollision(pos, self.box):
			self.selected = False
			if self.boundingColour:
				self.boundingColour = self.baseColour
				self.ticker = 0

	def handleKeys(self, key, letter):
		if self.selected:
			if key == pygame.K_BACKSPACE and len(self.text) >= 1:
				self.text = self.text[:-1]
			elif letter in characterString:
				self.text += letter

			self.renderSurface()

	# event.key, event.unicode
	def handleKeyPress(self, key, letter):
		if self.selected:
			self.handleKeys(key, letter)
			self.heldKey = [key, letter, self.ticker]

	# event.key, event.unicode
	def handleKeyRelease(self, key, letter):
		if self.heldKey != None and self.heldKey[:-1] == [key, letter]:
			self.heldKey = None

	def handleSelected(self):
		self.ticker += 1

		if self.heldKey != None and self.ticker - self.heldKey[2] >= self.heldKeyDelay:
			self.handleKeys(self.heldKey[0], self.heldKey[1])

	def draw(self, win):
		if self.boundingColour:
			pygame.draw.rect(win, self.boundingColour, (self.position[0] + self.boundingOffest[0] + self.renderOffset[0], self.position[1] + self.boundingOffest[1] + self.renderOffset[1], self.boundingBox[0], self.boundingBox[1]), 0, self.boundingRadius)

		win.blit(self.surface, (self.position[0] + self.boundingOffest[0] + self.horizontalMargin + self.renderOffset[0], self.position[1] + self.boundingOffest[1] + self.verticalMargin + self.renderOffset[1]))

		if self.showHitbox:
			pygame.draw.rect(win, (0,0,255), self.box, 2)

		if self.selected:
			self.handleSelected()

		if self.selected and self.ticker % self.typeLineFrames < self.typeLineFrames/2:
			pygame.draw.rect(win, self.fontColour, (self.position[0] + self.boundingOffest[0] + self.horizontalMargin + self.lastLineOffset[0] + self.renderOffset[0], self.position[1] + self.boundingOffest[1] + self.verticalMargin + self.lastLineOffset[1] + self.renderOffset[1], 2, self.lineHeight))

