# Fish Counting System - Quick Reference

## Installation
```bash
# Clone the repository
git clone https://github.com/AanAillen/SeniorProject.git
cd SeniorProject

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Process a video
```bash
python src/main.py --input data/raw/video.mp4 --output results/
```

### With real-time display
```bash
python src/main.py --input data/raw/video.mp4 --output results/ --display
```

### With custom configuration
```bash
python src/main.py --input data/raw/video.mp4 --output results/ --config config/custom.yaml
```

## Configuration

Edit `config/config.yaml` to adjust:
- Detection model and thresholds
- Tracking parameters
- Counting line position
- Output settings

### Key Settings

**Counting Line** (vertical line in middle of 1280x720 video):
```yaml
counting_line:
  x1: 640  # x-coordinate
  y1: 0    # top
  x2: 640  # same x (vertical)
  y2: 720  # bottom
```

**Detection**:
```yaml
detection:
  model_path: "models/fish_detector.pt"
  confidence_threshold: 0.5
```

**Tracking**:
```yaml
tracking:
  max_disappeared: 50  # frames before losing track
  max_distance: 100    # pixels for matching
```

## Project Structure

```
SeniorProject/
├── src/                    # Source code
│   ├── main.py            # Entry point
│   ├── detection/         # Fish detection
│   ├── tracking/          # Fish tracking
│   ├── counting/          # Fish counting
│   └── utils/             # Utilities
├── config/                # Configuration files
├── data/                  # Video data
│   ├── raw/              # Input videos
│   ├── processed/        # Processed data
│   └── annotations/      # Training annotations
├── models/               # Trained models
├── results/              # Output results
├── notebooks/            # Jupyter notebooks
├── docs/                 # Documentation
└── tests/                # Test files
```

## Documentation

- **README.md**: Project overview and setup
- **docs/GETTING_STARTED.md**: Detailed setup and usage guide
- **docs/ARCHITECTURE.md**: System architecture and design
- **data/README.md**: Data management guidelines
- **models/README.md**: Model training and usage

## Common Commands

### Run tests
```bash
python -m pytest tests/
# or
python tests/test_basic.py
```

### Check syntax
```bash
python -m py_compile src/**/*.py
```

### View results
Output is saved in `results/` directory:
- `output_*.mp4`: Annotated video
- `statistics_*.csv`: Counting statistics

## Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Clone repository
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Add a video to `data/raw/`
- [ ] Run the system: `python src/main.py --input data/raw/video.mp4 --output results/`
- [ ] Check results in `results/` directory

## Training a Model

1. Collect and annotate fish images/videos
2. Save annotations in `data/annotations/`
3. Train YOLO model (see `models/README.md`)
4. Save trained model to `models/`
5. Update `config/config.yaml` with model path

## Need Help?

- Check **docs/GETTING_STARTED.md** for detailed instructions
- Review example notebook: **notebooks/example_usage.ipynb**
- Open an issue in the repository

## Key Features

✓ Fish detection using computer vision  
✓ Multi-object tracking across frames  
✓ Bi-directional counting (upstream/downstream)  
✓ Configurable counting zones  
✓ Video output with annotations  
✓ Statistical reporting (CSV export)  
✓ Real-time display option  
✓ Modular and extensible design  

## System Requirements

**Minimum**:
- Python 3.8+
- 4GB RAM
- CPU-only operation supported

**Recommended**:
- Python 3.9+
- 8GB+ RAM
- NVIDIA GPU with CUDA support
- 2GB+ GPU memory

## Team Workflow

1. **Data Collection**: Add videos to `data/raw/`
2. **Annotation**: Label fish in frames for training
3. **Model Training**: Train detection model
4. **Processing**: Run videos through system
5. **Validation**: Compare with manual counts
6. **Analysis**: Review statistics and trends

## Important Notes

⚠️ The current implementation uses placeholder detection (returns no detections)  
⚠️ Train or load an actual model for real fish detection  
⚠️ Video files are excluded from git (see `.gitignore`)  
⚠️ Large model files should use Git LFS or external storage  

For more information, see the comprehensive documentation in the `docs/` directory.
