import os
import cv2

os.environ['OPENCV_FFMPEG_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'


class Video:
    @staticmethod
    def fill_images(video_file, frames):
        cam = cv2.VideoCapture(video_file)
        frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        for i in range(int(frame_count)):
            ret, frame = cam.read()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    @staticmethod
    def get_video_duration(video_path):
        video = cv2.VideoCapture(video_path)
        frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        duration_in_seconds = frame / fps
        return duration_in_seconds

    @staticmethod
    def get_image(path):
        print(id)
        dir_contents = os.listdir(path)
        files = [f for f in dir_contents if os.path.isfile(path + '/' + f)]
        cam = cv2.VideoCapture(os.path.join(path, files[0]))
        print(cam.isOpened())
        cam.read()
        for _ in (0, 5):
            ret, frame = cam.read()
        print(frame)
        print(os.path.join(path, files[0]))
        print(ret)
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
