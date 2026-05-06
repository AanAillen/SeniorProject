# AI Tools for Fish Migration and Counting

This project utilizes the YOLOv12 computer vision models to detect, track and count fish in videos. 
Additionally, there is a pre-processing component that corrects the footage from the State of Maine's 
archive of underwater footage to optimize the videos for model detection. This project offers a user
interface to easily upload videos and run the counting process.

## Running the application

### Prerequisites
- Python 3.10 or higher
- pip

All `.pt` models file must be placed in the project root directory.

### Installation
1. Clone the repository
2. Install dependencies:
```
pip install ultralytics
pip install opencv-python
pip install numpy
pip install Pillow
```
3. Add one or multiple `.pt` YOLO model files to the project root
4. Run the application:
```
python3 codeFiles/gui_app.py
```

### Using the application
- 
Once running the program a user can upload a '.mp4' video file to run the fish counting. The user will first
run the pre-processing correction on the video and then run the fish detection and counting on the corrected
video. The user can then adjust their model settings choosing the model of their choice and adjust the
confidence threshold for the detection. The user can then run the detection and counting. The video will be processed locally on the user's device and the live detection will be displayed in the UI and the finished anotated video will be saved locally in the user's 'GUI_processed_videos' directory. The anotated video will be displayed in the UI once finished and the user can adjust the playback speed for analysis. The number of fish counted will also be displayed in the bottom right of the UI once the detection is complete.

Note: In the anotated video there will display an "In" and "Out" count. The "In" count is the number of fish swimming left to right and the "Out" count is the number of fish swimming right to left. For this project the "Out" count is the direction of interest and is the number displayed in the fish count on the UI.