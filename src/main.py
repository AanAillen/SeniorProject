"""
Main entry point for the fish counting system.

This script processes video files to detect, track, and count fish
swimming in different directions.
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from utils.video_processor import VideoProcessor
from utils.config_loader import load_config
from detection.fish_detector import FishDetector
from tracking.fish_tracker import FishTracker
from counting.fish_counter import FishCounter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fish Migration Counting System"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to input video file"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="results/",
        help="Path to output directory"
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--display",
        "-d",
        action="store_true",
        help="Display video during processing"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()
    
    # Load configuration
    print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    
    # Initialize components
    print("Initializing fish detection system...")
    detector = FishDetector(config)
    tracker = FishTracker(config)
    counter = FishCounter(config)
    
    # Process video
    print(f"Processing video: {args.input}")
    processor = VideoProcessor(
        input_path=args.input,
        output_path=args.output,
        config=config,
        display=args.display
    )
    
    results = processor.process(detector, tracker, counter)
    
    # Display results
    print("\n" + "="*50)
    print("FISH COUNTING RESULTS")
    print("="*50)
    print(f"Total fish detected: {results['total_fish']}")
    print(f"Fish swimming upstream: {results['upstream_count']}")
    print(f"Fish swimming downstream: {results['downstream_count']}")
    print(f"Results saved to: {args.output}")
    print("="*50)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
