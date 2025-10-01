"""
Basic tests for the fish counting system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import load_config, get_default_config
from detection.fish_detector import FishDetector
from tracking.fish_tracker import FishTracker
from counting.fish_counter import FishCounter
import numpy as np


def test_config_loader():
    """Test configuration loading."""
    # Test default config
    config = get_default_config()
    assert 'video' in config
    assert 'detection' in config
    assert 'tracking' in config
    assert 'counting' in config
    print("✓ Configuration loader test passed")


def test_fish_detector_initialization():
    """Test fish detector initialization."""
    config = get_default_config()
    detector = FishDetector(config)
    assert detector is not None
    assert detector.model_type == 'yolov8'
    print("✓ Fish detector initialization test passed")


def test_fish_detector_detect():
    """Test fish detection on dummy frame."""
    config = get_default_config()
    detector = FishDetector(config)
    
    # Create dummy frame
    dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    # Run detection (should return empty list with placeholder implementation)
    detections = detector.detect(dummy_frame)
    assert isinstance(detections, list)
    print("✓ Fish detector detect test passed")


def test_fish_tracker_initialization():
    """Test fish tracker initialization."""
    config = get_default_config()
    tracker = FishTracker(config)
    assert tracker is not None
    assert tracker.next_object_id == 0
    print("✓ Fish tracker initialization test passed")


def test_fish_tracker_update():
    """Test fish tracker update with detections."""
    config = get_default_config()
    tracker = FishTracker(config)
    
    # Create dummy detections
    detections = [
        {'bbox': [100, 100, 150, 150], 'confidence': 0.9, 'class': 'fish'},
        {'bbox': [300, 300, 350, 350], 'confidence': 0.85, 'class': 'fish'}
    ]
    
    # Update tracker
    tracked = tracker.update(detections)
    assert len(tracked) == 2
    assert tracker.next_object_id == 2
    print("✓ Fish tracker update test passed")


def test_fish_counter_initialization():
    """Test fish counter initialization."""
    config = get_default_config()
    counter = FishCounter(config)
    assert counter is not None
    assert counter.total_count == 0
    assert counter.left_count == 0
    assert counter.right_count == 0
    print("✓ Fish counter initialization test passed")


def test_fish_counter_get_counts():
    """Test getting counts from counter."""
    config = get_default_config()
    counter = FishCounter(config)
    
    counts = counter.get_counts()
    assert 'total_fish' in counts
    assert 'upstream_count' in counts
    assert 'downstream_count' in counts
    assert counts['total_fish'] == 0
    print("✓ Fish counter get_counts test passed")


def test_counting_line_crossing():
    """Test line crossing detection."""
    config = get_default_config()
    counter = FishCounter(config)
    
    # Test crossing from left to right
    prev_pos = (600, 360)  # Left of line
    curr_pos = (680, 360)  # Right of line
    crossed, direction = counter._is_crossing_line(prev_pos, curr_pos)
    assert crossed == True
    assert direction == 'right'
    
    # Test crossing from right to left
    prev_pos = (680, 360)  # Right of line
    curr_pos = (600, 360)  # Left of line
    crossed, direction = counter._is_crossing_line(prev_pos, curr_pos)
    assert crossed == True
    assert direction == 'left'
    
    # Test no crossing
    prev_pos = (600, 360)  # Left of line
    curr_pos = (620, 360)  # Still left of line
    crossed, direction = counter._is_crossing_line(prev_pos, curr_pos)
    assert crossed == False
    
    print("✓ Counting line crossing test passed")


def run_all_tests():
    """Run all tests."""
    print("\nRunning Fish Counting System Tests")
    print("=" * 50)
    
    try:
        test_config_loader()
        test_fish_detector_initialization()
        test_fish_detector_detect()
        test_fish_tracker_initialization()
        test_fish_tracker_update()
        test_fish_counter_initialization()
        test_fish_counter_get_counts()
        test_counting_line_crossing()
        
        print("=" * 50)
        print("All tests passed! ✓")
        return 0
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
