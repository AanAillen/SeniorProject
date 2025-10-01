# Models Directory

This directory contains trained machine learning models for fish detection.

## Supported Models

The system supports various detection models:

### YOLO (You Only Look Once)
- **YOLOv8**: Recommended for real-time detection
- **YOLOv5**: Good balance of speed and accuracy
- Fast inference, good for video processing

### Other Models
- Faster R-CNN: Higher accuracy, slower inference
- SSD (Single Shot Detector): Good for mobile deployment
- Custom models: Any PyTorch/TensorFlow model can be integrated

## Model Files

Model files are typically large (50MB - 500MB) and should:
- Use Git LFS if committing to repository
- Be stored in cloud storage for team sharing
- Follow naming conventions

### Naming Convention
```
model_type_version_dataset_date.ext

Examples:
- yolov8n_v1_fish_20240315.pt
- yolov5m_custom_20240301.pt
- faster_rcnn_resnet50_fish.pth
```

## Directory Structure

```
models/
├── yolo/
│   ├── yolov8n.pt          # Nano model (fastest)
│   ├── yolov8s.pt          # Small model
│   ├── yolov8m.pt          # Medium model
│   └── yolov8l.pt          # Large model (most accurate)
├── checkpoints/             # Training checkpoints
│   └── best_weights.pt
└── README.md
```

## Training Your Own Model

### Using YOLOv8 (Recommended)

1. **Prepare your dataset** in YOLO format:
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

2. **Create dataset YAML** (`dataset.yaml`):
```yaml
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

nc: 1  # number of classes
names: ['fish']  # class names
```

3. **Train the model**:
```python
from ultralytics import YOLO

# Load a pretrained model
model = YOLO('yolov8n.pt')

# Train the model
results = model.train(
    data='dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='fish_detector'
)
```

4. **Save and use the trained model**:
```python
# Best weights are automatically saved to:
# runs/detect/fish_detector/weights/best.pt

# Copy to models directory
# Update config.yaml to use your model
```

## Pre-trained Models

### Download Pre-trained YOLO Models

```bash
# YOLOv8 nano (smallest, fastest)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# YOLOv8 small
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt

# YOLOv8 medium
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt
```

**Note**: These are general-purpose COCO models. For best results, fine-tune on your fish dataset.

## Model Selection Guide

| Model | Speed | Accuracy | GPU Memory | Use Case |
|-------|-------|----------|------------|----------|
| YOLOv8n | Fastest | Good | Low | Real-time, CPU |
| YOLOv8s | Fast | Better | Medium | General use |
| YOLOv8m | Medium | Good | High | Accuracy focused |
| YOLOv8l | Slow | Best | Very High | Offline processing |

## Configuration

To use a model, update `config/config.yaml`:

```yaml
detection:
  model_type: "yolov8"
  model_path: "models/yolo/yolov8s.pt"
  confidence_threshold: 0.5
  nms_threshold: 0.4
```

## Model Performance

Track model performance metrics:
- **mAP (mean Average Precision)**: Detection accuracy
- **Inference time**: Speed per frame
- **FPS**: Frames processed per second
- **Precision/Recall**: Detection quality

### Testing Your Model

```python
from ultralytics import YOLO

model = YOLO('models/yolo/fish_detector.pt')

# Validate on test set
metrics = model.val()

print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}")
```

## Model Versioning

Keep track of model versions:
- Training date and dataset
- Hyperparameters used
- Performance metrics
- Known issues or limitations

Consider creating a `model_log.md` file to document each model version.

## GPU Requirements

For training:
- Minimum: 4GB GPU memory
- Recommended: 8GB+ GPU memory
- CPU training is possible but very slow

For inference:
- Models can run on CPU
- GPU recommended for real-time processing
- Smaller models (nano/small) work well on CPU

## Troubleshooting

### Common Issues

**Issue**: Model file not found
- Check the path in `config.yaml`
- Ensure the model file exists
- Use absolute or relative paths correctly

**Issue**: Out of memory during training
- Reduce batch size
- Use smaller model variant
- Reduce image size

**Issue**: Poor detection performance
- Collect more training data
- Increase training epochs
- Try different model architecture
- Adjust confidence thresholds

## Resources

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
- [YOLO Training Tutorial](https://docs.ultralytics.com/modes/train/)
- [Model Export Guide](https://docs.ultralytics.com/modes/export/)
