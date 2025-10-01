# Getting Started with Fish Migration Monitoring

## Quick Start Guide

### 1. Installation
Follow the installation steps in the main README.md

### 2. Prepare Your Data
- Place your video files in the `data/raw/` directory
- Supported formats: MP4, AVI, MOV

### 3. Configure the System
Edit `config/config.yaml` to customize:

#### Detection Settings
- Choose your detection model
- Adjust confidence thresholds
- Set detection parameters

#### Counting Line Setup
The counting line is a virtual line in the video. Fish crossing this line are counted.

To configure the counting line:
1. Open your video in a viewer
2. Identify where you want to count fish
3. Note the pixel coordinates
4. Update `config/config.yaml` with these coordinates

Example for a vertical line in the middle of a 1280x720 video:
```yaml
counting_line:
  x1: 640  # Middle of frame
  y1: 0    # Top of frame
  x2: 640  # Same x (vertical line)
  y2: 720  # Bottom of frame
```

### 4. Run the System

Basic usage:
```bash
python src/main.py --input data/raw/your_video.mp4 --output results/
```

With display (shows processing in real-time):
```bash
python src/main.py --input data/raw/your_video.mp4 --output results/ --display
```

With custom configuration:
```bash
python src/main.py --input data/raw/your_video.mp4 --output results/ --config config/custom_config.yaml
```

### 5. Review Results

After processing, check the `results/` directory for:
- `output_*.mp4`: Annotated video with detections and counts
- `statistics_*.csv`: CSV file with counting results

## Training a Custom Model

The system comes with placeholder detection. To use actual fish detection:

### Option 1: Use Pre-trained YOLO
If you have a pre-trained YOLO model:
1. Place the model file in `models/` directory
2. Update `config/config.yaml` to point to your model:
   ```yaml
   detection:
     model_path: "models/your_model.pt"
   ```

### Option 2: Train Your Own Model
1. Collect and annotate training data
2. Train a YOLO model using the Ultralytics library
3. Save the trained model to `models/`
4. Update the configuration file

## Tips and Best Practices

### Video Quality
- Use high-resolution videos for better detection
- Ensure good lighting conditions
- Minimize water turbulence and reflections

### Counting Line Placement
- Place the line perpendicular to fish movement
- Avoid areas with heavy vegetation or obstacles
- Test different positions to find optimal placement

### Performance Optimization
- Process videos in batches during off-hours
- Use GPU acceleration if available
- Skip frames if processing is too slow

## Troubleshooting

### Common Issues

**Issue**: Video won't open
- Check that the file path is correct
- Verify the video format is supported
- Try converting to MP4 format

**Issue**: No detections
- The placeholder detector returns empty results by default
- Train or load an actual detection model
- Adjust confidence threshold if too high

**Issue**: Incorrect counts
- Adjust the counting line position
- Fine-tune tracking parameters (max_distance, max_disappeared)
- Review the annotated output video to debug

**Issue**: Slow processing
- Enable GPU acceleration in config
- Increase frame_rate to skip more frames
- Reduce video resolution

## Next Steps

1. **Collect Training Data**: Gather and annotate video frames with fish
2. **Train Model**: Use the annotations to train a detection model
3. **Validate Results**: Compare automated counts with manual counts
4. **Optimize**: Fine-tune parameters for your specific use case

## Support

For questions or issues:
- Check the main README.md
- Review example notebooks in `notebooks/`
- Open an issue in the repository
