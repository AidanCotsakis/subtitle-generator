from tkinter import *
from tkinter import filedialog

root = Tk()
root.withdraw()

filetypes = (
		("Video files", "*.mp4;*.mkv;*.avi;*.mov;*.flv"),
		("All files", "*.*")
	)
INITIAL_VIDEO_FILE_NAME = filedialog.askopenfilename(initialdir = "", filetypes=filetypes)

if INITIAL_VIDEO_FILE_NAME == "":
	quit()

print("IMPORTING MODULES")
from moviepy.editor import *

# INITIAL_VIDEO_FILE_NAME = "input/input.mov"
OUTPUT_AUDIO_NAME = "output/audio.wav"

def exportAudio(videoFile, audioFile):
	video = VideoFileClip(videoFile)
	video.audio.write_audiofile(audioFile, ffmpeg_params=["-ac", "1"]) 

print("ANALYZING AUDIO")
exportAudio(INITIAL_VIDEO_FILE_NAME, OUTPUT_AUDIO_NAME)
