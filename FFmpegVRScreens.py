
import os
import ffmpeg

createdFiles = []

debug = 0

def main():
    getframes("epcot.webm", isVR=True) # just a random vr video i found on youtube. originally i was using an mp4 file, but now im trying to understand why
                                       # ffmpeg isnt working on a .webm file.

def getframes(videoFile, isVR):
    
    probe = ffmpeg.probe(videoFile)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    parts = 7 #How many spots you want to extract a video from. 
    intervals = time // parts
    intervals = int(intervals)
    interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
    i = 0
    if debug == 0:
        for item in interval_list:
            (
                ffmpeg
                .input(videoFile, ss=item[1])
                .filter('scale', width, -1)
                .output(str(i) + '.png', vframes=1)
                .run()
            )
            createdFiles.append(str(i) + ".png")
        #os.system("ffmpeg-unwarpvr -i " + str(i) + ".jpg -vf unwarpvr=1920:1080:eye_relief_dial=0:left_eye_only=1 -ss 0 -vframes 1 -pix_fmt yuv420p " + str(i) + ".png")
            if isVR:
                os.system("ffmpeg-unwarpvr -i " + str(i) + ".png -vf unwarpvr=1920:1080:left_eye_only=1:scale_width=1.2:scale_height=1.2:eye_relief_dial=10:left_eye_only=1 -sws_flags lanczos+accurate_rnd+full_chroma_int " + str(i) + "unwrap" + ".png")
                createdFiles.append(str(i) + "unwrap" + ".png")
                if i == parts:
                    os.system ("ffmpeg -i %dunwrap.png -vf zoompan=d=(2.5+1)/1:fps=1/1,framerate=25:interp_start=0:interp_end=255:scene=100  -c:v mpeg4 -q:v 2 out.mp4")
            #unwraps vr video frames defined as PARTS as monoscopic(left eye) .png files(im switching from .jpg to .png just to show what state of the process they are in, then deleting the jpgs after)
            else: 
                if i == parts:
                    os.system ("ffmpeg -i %d.png -vf zoompan=d=(2.5+1)/1:fps=1/1,framerate=25:interp_start=0:interp_end=255:scene=100  -c:v mpeg4 -q:v 2 out.mp4")
            i += 1
    
    createdFiles.append("out.mp4") #Makes an mp4 with all the screens, with crossfade between them
    os.system("ffmpeg -i out.mp4 -filter:v \"crop=500:580\" -c:a copy output.mp4")
    for file in createdFiles:
        os.remove(file)

main()
