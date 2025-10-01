"""
Utility module for loading configuration files.
"""

import yaml
from pathlib import Path


def load_config(config_path):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary with configuration settings
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Warning: Configuration file not found at {config_path}")
        print("Using default configuration")
        return get_default_config()
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def get_default_config():
    """
    Get default configuration settings.
    
    Returns:
        Dictionary with default configuration
    """
    return {
        'video': {
            'frame_rate': 30,
            'resize_width': 1280,
            'resize_height': 720
        },
        'detection': {
            'model_type': 'yolov8',
            'confidence_threshold': 0.5,
            'nms_threshold': 0.4
        },
        'tracking': {
            'max_disappeared': 50,
            'max_distance': 100,
            'track_history': 30
        },
        'counting': {
            'counting_line': {
                'enabled': True,
                'x1': 640,
                'y1': 0,
                'x2': 640,
                'y2': 720
            },
            'direction_left': 'downstream',
            'direction_right': 'upstream'
        },
        'output': {
            'save_video': True,
            'save_statistics': True,
            'visualization': True,
            'statistics_format': 'csv'
        },
        'performance': {
            'use_gpu': True,
            'batch_size': 1,
            'num_workers': 2
        }
    }
