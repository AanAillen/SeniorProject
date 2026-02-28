import cv2

from ultralytics import solutions

cap = cv2.VideoCapture('processed_videos/barrel_fixed_shortClip_20260217_205047.mp4')
assert cap.isOpened(), "Error reading video file"

# Get output filename from user
output_filename = input("Enter output video filename (without extension): ").strip()
if not output_filename:
    output_filename = "object_counting_output"
# Ensure .mp4 extension
if not output_filename.endswith(('.mp4', '.avi')):
    output_filename += ".mp4"

# Video writer
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Calculate vertical box in center of video
box_width = 10  # width of the vertical box in pixels
box_top = 0  # start 10% from top
box_bottom = int(h)  # end 10% from bottom
center_x = w // 2
left_x = center_x - box_width // 2 - 100

# Vertical rectangular region (clockwise: top-left, top-right, bottom-right, bottom-left)
region_points = [
    (left_x, box_top),      # top-left
    (left_x, box_bottom)    # bottom-left
]

# region_points = [(20, 400), (1080, 400)]                                      # line counting
# region_points = [(20, 400), (1080, 400), (1080, 360), (20, 360)]  # rectangular region
# region_points = [(20, 400), (1080, 400), (1080, 360), (20, 360), (20, 400)]   # polygon region
video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize object counter object
counter = solutions.ObjectCounter(
    show=True,  # display the output
    region=region_points,  # pass region points
    model='current_fish_model.pt',  # model="yolo11n-obb.pt" for object counting with OBB model.
    # classes=[0, 2],  # count specific classes, i.e., person and car with the COCO pretrained model.
    tracker="botsort.yaml",  # choose trackers i.e "bytetrack.yaml"
)

# Process video
while cap.isOpened():
    success, im0 = cap.read()

    if not success:
        print("Video frame is empty or processing is complete.")
        break

    results = counter(im0)

    # print(results)  # access the output

    video_writer.write(results.plot_im)  # write the processed frame.

cap.release()
video_writer.release()
cv2.destroyAllWindows()  # destroy all opened windows