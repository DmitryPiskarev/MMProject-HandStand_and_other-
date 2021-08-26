import cv2

KPS = 1  # Target Keyframes Per Second
VIDEO_PATH = "media/video/cuted_video.mp4"  # "path/to/video/folder" # Change this
IMAGE_PATH = "media/img_from_video/user1/img"  # "path/to/image/folder" # ...and this
EXTENSION = ".png"
cap = cv2.VideoCapture(VIDEO_PATH)
fps = round(cap.get(cv2.CAP_PROP_FPS))
# exit()
hop = round(fps / KPS)
curr_frame = 0
cycle_num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if curr_frame % hop == 0:
        name = IMAGE_PATH + "_" + str(cycle_num) + EXTENSION
        cv2.imwrite(name, frame)
        cycle_num += 1
    curr_frame += 1
cap.release()
