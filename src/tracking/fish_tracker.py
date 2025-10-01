"""
Fish tracking module for maintaining consistent IDs across frames.
"""

import numpy as np
from collections import OrderedDict
from scipy.spatial import distance


class FishTracker:
    """
    Track fish across multiple frames using centroid tracking.
    """
    
    def __init__(self, config):
        """
        Initialize the fish tracker.
        
        Args:
            config: Configuration dictionary with tracking settings
        """
        self.config = config
        self.tracking_config = config.get('tracking', {})
        self.max_disappeared = self.tracking_config.get('max_disappeared', 50)
        self.max_distance = self.tracking_config.get('max_distance', 100)
        
        # Dictionary to store tracked objects
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.centroids = OrderedDict()
        
        # Next available object ID
        self.next_object_id = 0
    
    def register(self, centroid):
        """
        Register a new object with the next available ID.
        
        Args:
            centroid: (x, y) coordinates of object center
        """
        self.objects[self.next_object_id] = centroid
        self.centroids[self.next_object_id] = [centroid]
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
    
    def deregister(self, object_id):
        """
        Remove an object from tracking.
        
        Args:
            object_id: ID of object to remove
        """
        del self.objects[object_id]
        del self.disappeared[object_id]
        del self.centroids[object_id]
    
    def update(self, detections):
        """
        Update tracked objects based on new detections.
        
        Args:
            detections: List of detection dictionaries with 'bbox' key
            
        Returns:
            Dictionary mapping object IDs to current centroids
        """
        # If no detections, mark all objects as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                
                # Deregister if disappeared too long
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            return self.objects
        
        # Calculate centroids of new detections
        input_centroids = np.zeros((len(detections), 2), dtype="int")
        for i, detection in enumerate(detections):
            bbox = detection['bbox']
            x1, y1, x2, y2 = bbox
            cx = int((x1 + x2) / 2.0)
            cy = int((y1 + y2) / 2.0)
            input_centroids[i] = (cx, cy)
        
        # If no tracked objects, register all detections
        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            # Get existing object IDs and centroids
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            # Calculate distances between existing and new centroids
            D = distance.cdist(np.array(object_centroids), input_centroids)
            
            # Find minimum distances
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            # Match existing objects to new detections
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                if D[row, col] > self.max_distance:
                    continue
                
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.centroids[object_id].append(tuple(input_centroids[col]))
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Handle unmatched existing objects
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            # Register unmatched new detections
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            for col in unused_cols:
                self.register(input_centroids[col])
        
        return self.objects
    
    def get_track_history(self, object_id, length=None):
        """
        Get movement history for a tracked object.
        
        Args:
            object_id: ID of tracked object
            length: Number of recent positions to return (None for all)
            
        Returns:
            List of (x, y) positions
        """
        if object_id not in self.centroids:
            return []
        
        history = self.centroids[object_id]
        if length is not None:
            return history[-length:]
        return history
