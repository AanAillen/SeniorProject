# System Architecture

## Overview

The Fish Migration Monitoring System is composed of four main components that work together to process video data and count fish:

1. **Fish Detector**: Detects fish in video frames
2. **Fish Tracker**: Maintains consistent IDs for fish across frames
3. **Fish Counter**: Counts fish crossing a virtual counting line
4. **Video Processor**: Orchestrates the pipeline and manages I/O

## Component Details

### 1. Fish Detector (`src/detection/fish_detector.py`)

**Purpose**: Identify fish in individual video frames

**Key Features**:
- Supports multiple detection models (YOLO, Faster R-CNN, etc.)
- Configurable confidence thresholds
- Bounding box visualization

**How it works**:
- Takes a video frame as input
- Runs the frame through a deep learning model
- Returns detected fish with bounding boxes and confidence scores

**Current State**: 
- Placeholder implementation (returns empty detections)
- Ready for integration with trained models

### 2. Fish Tracker (`src/tracking/fish_tracker.py`)

**Purpose**: Maintain consistent IDs for fish across multiple frames

**Key Features**:
- Centroid-based tracking algorithm
- Handles temporary occlusions
- Maintains movement history for each fish

**How it works**:
1. Receives detections from the detector
2. Calculates centroid (center point) for each detection
3. Matches new detections to existing tracked objects
4. Assigns unique IDs that persist across frames
5. Stores movement history for direction analysis

**Algorithm**: 
- Uses Euclidean distance to match detections
- Deregisters objects that disappear for too long
- Registers new objects as they appear

### 3. Fish Counter (`src/counting/fish_counter.py`)

**Purpose**: Count fish crossing a virtual line

**Key Features**:
- Configurable counting line
- Bi-directional counting (upstream/downstream)
- Real-time count display

**How it works**:
1. Monitors tracked fish positions
2. Checks if fish crossed the counting line
3. Determines direction of crossing
4. Increments appropriate counter
5. Ensures each fish is only counted once

**Counting Logic**:
- Uses previous and current positions to detect line crossings
- Supports vertical and horizontal counting lines
- Prevents duplicate counts per fish

### 4. Video Processor (`src/utils/video_processor.py`)

**Purpose**: Orchestrate the entire pipeline

**Key Features**:
- Video I/O management
- Frame-by-frame processing
- Results export (video and statistics)
- Progress tracking

**Pipeline Flow**:
```
1. Open video file
2. For each frame:
   a. Run detector → get detections
   b. Update tracker → get tracked objects
   c. Update counter → get counts
   d. Visualize results
   e. Write to output video
3. Save final statistics
4. Clean up resources
```

## Data Flow

```
Input Video
    ↓
[Video Processor]
    ↓
Frame-by-frame
    ↓
[Fish Detector] → Detections (bounding boxes)
    ↓
[Fish Tracker] → Tracked Objects (IDs + positions)
    ↓
[Fish Counter] → Counts (upstream/downstream)
    ↓
Output: Annotated Video + Statistics
```

## Configuration System

The system uses a YAML-based configuration (`config/config.yaml`) that controls:

- **Video Settings**: Resolution, frame rate
- **Detection Parameters**: Model selection, thresholds
- **Tracking Parameters**: Distance metrics, history length
- **Counting Setup**: Line position, direction labels
- **Output Options**: Video/statistics export settings

Configuration is loaded by `src/utils/config_loader.py` and shared across all components.

## Extensibility

The modular design allows for easy customization:

### Adding New Detection Models
1. Modify `FishDetector.__init__()` to load your model
2. Update `FishDetector.detect()` to run inference
3. Configure model path in `config.yaml`

### Custom Tracking Algorithms
1. Create a new tracker class with `update()` method
2. Replace `FishTracker` in `main.py`
3. Ensure it returns the same data structure

### Alternative Counting Methods
1. Subclass `FishCounter` or create new counter
2. Implement custom counting logic
3. Update `main.py` to use new counter

## Performance Considerations

### Optimization Strategies
- **Frame Skipping**: Process every Nth frame to speed up processing
- **GPU Acceleration**: Use CUDA for model inference
- **Batch Processing**: Process multiple frames simultaneously
- **Resolution Scaling**: Reduce frame size for faster processing

### Bottlenecks
- **Detection**: Usually the slowest component (model inference)
- **Video I/O**: Reading/writing video can be slow for large files
- **Visualization**: Drawing annotations takes time

### Recommendations
- Use GPU for detection models
- Skip frames when real-time processing isn't needed
- Disable visualization for faster processing
- Process videos in batches offline

## Future Enhancements

Potential improvements:
1. Multi-species detection and classification
2. Size estimation for individual fish
3. Behavior analysis (schooling, feeding)
4. Real-time processing with video streams
5. Web-based dashboard for monitoring
6. Database integration for long-term data storage
