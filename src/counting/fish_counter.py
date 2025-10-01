"""
Fish counting module for tracking fish crossing counting lines.
"""

import cv2
import numpy as np
from collections import defaultdict


class FishCounter:
    """
    Count fish crossing a virtual counting line in the video.
    """
    
    def __init__(self, config):
        """
        Initialize the fish counter.
        
        Args:
            config: Configuration dictionary with counting settings
        """
        self.config = config
        self.counting_config = config.get('counting', {})
        
        # Get counting line coordinates
        line_config = self.counting_config.get('counting_line', {})
        self.counting_line = (
            line_config.get('x1', 640),
            line_config.get('y1', 0),
            line_config.get('x2', 640),
            line_config.get('y2', 720)
        )
        
        # Direction labels
        self.direction_left = self.counting_config.get('direction_left', 'downstream')
        self.direction_right = self.counting_config.get('direction_right', 'upstream')
        
        # Tracking which fish have crossed
        self.counted = defaultdict(lambda: False)
        self.directions = {}  # Track direction of each fish
        
        # Counts
        self.left_count = 0   # downstream
        self.right_count = 0  # upstream
        self.total_count = 0
    
    def _is_crossing_line(self, prev_pos, curr_pos):
        """
        Check if movement crosses the counting line.
        
        Args:
            prev_pos: Previous (x, y) position
            curr_pos: Current (x, y) position
            
        Returns:
            Tuple (crossed, direction) where:
                - crossed: Boolean indicating if line was crossed
                - direction: 'left' or 'right' if crossed, None otherwise
        """
        if prev_pos is None or curr_pos is None:
            return False, None
        
        x1, y1, x2, y2 = self.counting_line
        px, py = prev_pos
        cx, cy = curr_pos
        
        # For vertical line (most common case)
        if x1 == x2:
            line_x = x1
            # Check if crossed the vertical line
            if (px < line_x and cx >= line_x):
                return True, 'right'  # Moving right (upstream)
            elif (px > line_x and cx <= line_x):
                return True, 'left'   # Moving left (downstream)
        
        # For horizontal line
        elif y1 == y2:
            line_y = y1
            # Check if crossed the horizontal line
            if (py < line_y and cy >= line_y):
                return True, 'down'
            elif (py > line_y and cy <= line_y):
                return True, 'up'
        
        return False, None
    
    def update(self, tracked_objects, tracker):
        """
        Update counts based on tracked object positions.
        
        Args:
            tracked_objects: Dictionary mapping object IDs to centroids
            tracker: FishTracker instance for accessing history
            
        Returns:
            Dictionary with current counts
        """
        for object_id, current_pos in tracked_objects.items():
            # Get movement history
            history = tracker.get_track_history(object_id, length=2)
            
            if len(history) >= 2:
                prev_pos = history[-2]
                curr_pos = history[-1]
                
                # Check if crossed counting line
                crossed, direction = self._is_crossing_line(prev_pos, curr_pos)
                
                if crossed and not self.counted[object_id]:
                    # Mark as counted
                    self.counted[object_id] = True
                    self.directions[object_id] = direction
                    self.total_count += 1
                    
                    # Update direction counts
                    if direction == 'right':
                        self.right_count += 1
                    elif direction == 'left':
                        self.left_count += 1
        
        return self.get_counts()
    
    def get_counts(self):
        """
        Get current counting statistics.
        
        Returns:
            Dictionary with counting statistics
        """
        return {
            'total_fish': self.total_count,
            'upstream_count': self.right_count,
            'downstream_count': self.left_count,
            'upstream_label': self.direction_right,
            'downstream_label': self.direction_left
        }
    
    def draw_counting_line(self, frame):
        """
        Draw the counting line on the frame.
        
        Args:
            frame: Input video frame
            
        Returns:
            Frame with counting line drawn
        """
        output_frame = frame.copy()
        x1, y1, x2, y2 = self.counting_line
        
        # Draw line
        cv2.line(output_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
        
        # Draw counts
        counts = self.get_counts()
        y_offset = 30
        cv2.putText(
            output_frame,
            f"Total: {counts['total_fish']}",
            (10, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        cv2.putText(
            output_frame,
            f"{counts['upstream_label']}: {counts['upstream_count']}",
            (10, y_offset + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        cv2.putText(
            output_frame,
            f"{counts['downstream_label']}: {counts['downstream_count']}",
            (10, y_offset + 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )
        
        return output_frame
