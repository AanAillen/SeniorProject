"""
Video processing utilities.
"""

import cv2
import csv
from pathlib import Path
from datetime import datetime


class VideoProcessor:
    """
    Process video files for fish detection and counting.
    """
    
    def __init__(self, input_path, output_path, config, display=False):
        """
        Initialize the video processor.
        
        Args:
            input_path: Path to input video file
            output_path: Path to output directory
            config: Configuration dictionary
            display: Whether to display video during processing
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.config = config
        self.display = display
        
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Video settings
        self.video_config = config.get('video', {})
        self.output_config = config.get('output', {})
    
    def process(self, detector, tracker, counter):
        """
        Process video file for fish detection, tracking, and counting.
        
        Args:
            detector: FishDetector instance
            tracker: FishTracker instance
            counter: FishCounter instance
            
        Returns:
            Dictionary with processing results
        """
        # Open input video
        cap = cv2.VideoCapture(str(self.input_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {self.input_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Video properties: {width}x{height} @ {fps} FPS, {total_frames} frames")
        
        # Setup output video writer if needed
        video_writer = None
        if self.output_config.get('save_video', True):
            output_video_path = self.output_path / f"output_{self.input_path.stem}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                str(output_video_path), fourcc, fps, (width, height)
            )
        
        # Process frames
        frame_count = 0
        frame_skip = self.video_config.get('frame_rate', 1)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames based on frame_rate setting
                if frame_count % frame_skip != 0:
                    continue
                
                # Detect fish in frame
                detections = detector.detect(frame)
                
                # Update tracker with detections
                tracked_objects = tracker.update(detections)
                
                # Update counter
                counter.update(tracked_objects, tracker)
                
                # Visualize if needed
                if self.output_config.get('visualization', True):
                    # Draw detections
                    frame = detector.visualize_detections(frame, detections)
                    
                    # Draw counting line and counts
                    frame = counter.draw_counting_line(frame)
                    
                    # Draw tracked objects
                    for object_id, centroid in tracked_objects.items():
                        cv2.circle(frame, tuple(centroid), 4, (0, 255, 255), -1)
                        cv2.putText(
                            frame, str(object_id), 
                            (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2
                        )
                
                # Write frame to output video
                if video_writer is not None:
                    video_writer.write(frame)
                
                # Display frame
                if self.display:
                    cv2.imshow('Fish Counting', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Print progress
                if frame_count % 100 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames} frames)")
        
        finally:
            # Clean up
            cap.release()
            if video_writer is not None:
                video_writer.release()
            if self.display:
                cv2.destroyAllWindows()
        
        # Get final results
        results = counter.get_counts()
        
        # Save statistics
        if self.output_config.get('save_statistics', True):
            self._save_statistics(results)
        
        return results
    
    def _save_statistics(self, results):
        """
        Save counting statistics to file.
        
        Args:
            results: Dictionary with counting results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as CSV
        if self.output_config.get('statistics_format', 'csv') == 'csv':
            csv_path = self.output_path / f"statistics_{timestamp}.csv"
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Metric', 'Count'])
                writer.writerow(['Total Fish', results['total_fish']])
                writer.writerow([results['upstream_label'].title(), results['upstream_count']])
                writer.writerow([results['downstream_label'].title(), results['downstream_count']])
            print(f"Statistics saved to: {csv_path}")
