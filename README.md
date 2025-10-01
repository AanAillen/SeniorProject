# Fish Migration Monitoring Project

## Overview
This project uses computer vision to monitor and count fish migration patterns in video data. The system analyzes video streams to automatically detect fish, track their movement, and count how many fish swim in each direction.

## Project Description
We are compiling video data of fish and applying computer vision models to:
- Detect and track individual fish in video streams
- Count the number of fish swimming in each direction (upstream/downstream)
- Analyze migration patterns and generate reports

## Features
- Video processing and frame extraction
- Fish detection using computer vision models
- Direction tracking (left/right or upstream/downstream)
- Automated counting and statistics
- Data export and visualization

## Project Structure
```
SeniorProject/
├── data/               # Video files and datasets
│   ├── raw/           # Raw video files
│   ├── processed/     # Processed video clips
│   └── annotations/   # Manual annotations for training
├── models/            # Trained models and weights
├── src/               # Source code
│   ├── detection/     # Fish detection modules
│   ├── tracking/      # Fish tracking algorithms
│   ├── counting/      # Counting logic
│   └── utils/         # Utility functions
├── notebooks/         # Jupyter notebooks for analysis
├── config/            # Configuration files
├── results/           # Output results and reports
└── docs/              # Documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster processing

### Setup
1. Clone the repository:
```bash
git clone https://github.com/AanAillen/SeniorProject.git
cd SeniorProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Processing a Video
```bash
python src/main.py --input data/raw/video.mp4 --output results/
```

### Configuration
Edit `config/config.yaml` to adjust:
- Model parameters
- Detection thresholds
- Video processing settings
- Output formats

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. Format code using:
```bash
black src/
flake8 src/
```

## Contributing
Team members should:
1. Create a new branch for each feature
2. Write tests for new functionality
3. Submit pull requests for review
4. Document code and update README as needed

## Team
Senior Project Team - Fish Migration Monitoring

## License
This project is for educational purposes as part of our senior project.

## Contact
For questions or issues, please open an issue in the repository.
