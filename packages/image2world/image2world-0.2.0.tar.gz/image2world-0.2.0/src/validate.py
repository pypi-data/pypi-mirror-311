from interface import *
import numpy as np
from sensor_msgs.msg import CameraInfo

class Validate:
    def __init__(self):
        pass

    def _validateCenter(self, center2D: Pose2D):
        if not isinstance(center2D.x, (int, float)) or not isinstance(center2D.y, (int, float)):
            raise Exception("Center values must be numbers")
        
    def _validateCenter3D(self, center3D: Pose):
        if not isinstance(center3D.position.x, (int, float)) or not isinstance(center3D.position.y, (int, float)) or not isinstance(center3D.position.z, (int, float)):
            raise Exception("Center values must be numbers")

    def _validateSize2D(self, size_x: float, size_y: float):
        if not isinstance(size_x, (int, float)) or not isinstance(size_y, (int, float)):
            raise Exception("Size values must be numbers")
        
    def _validateSize3D(self, size: Vector3):
        if not isinstance(size.x, (int, float)) or not isinstance(size.y, (int, float)) or not isinstance(size.z, (int, float)):
            raise Exception("Size values must be numbers")
    
    def _validateCenterDepth(self, centerDepth):
        if centerDepth <= 0:
            raise Exception("Center depth is not valid")
        
    def _validateCompareCameraInfo(self, currentCameraInfo: CameraInfo, cameraInfo: CameraInfo):
        equal = True
        equal = equal and (cameraInfo.width == currentCameraInfo.width)
        equal = equal and (cameraInfo.height == currentCameraInfo.height)
        equal = equal and np.all(np.isclose(np.asarray(cameraInfo.k),
                                            np.asarray(currentCameraInfo.k)))
        return equal
    
    def _validateBoundingBox3D(self, bbox: BoundingBox3D): 
        self._validateCenter3D(bbox.center)
        self._validateSize3D(bbox.size)
        # TODO: FINISH THIS VALIDATE METHOD
    
    def _validatePolygonVertices(self, vertices):
        if not isinstance(vertices, list):
            raise Exception("Vertices must be a list")
        for vertex in vertices:
            if not isinstance(vertex, Pose):
                raise Exception("Vertices must be Pose objects")