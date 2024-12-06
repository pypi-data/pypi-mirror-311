# File: visiontools/pipeline.py
from typing import Any

class ModelRegistry:
    """Registry for model types and their handlers"""
    _handlers = {}
    
    @classmethod
    def register(cls, model_type: type, handler: callable):
        """Register a handler for a model type"""
        cls._handlers[model_type] = handler
    
    @classmethod
    def get_handler(cls, model):
        """Get handler for a model instance"""
        for model_type, handler in cls._handlers.items():
            if isinstance(model, model_type):
                return handler
        return None

class PipelineInput:
    """Wrapper for pipeline inputs (e.g., image paths)"""
    def __init__(self, data: Any):
        self.data = data
    
    def __or__(self, model):
        """Support for the | operator"""
        handler = ModelRegistry.get_handler(model)
        if handler:
            return Pipeline(model, handler).__ror__(self.data)
        return NotImplemented

class Pipeline:
    """Core pipeline class"""
    def __init__(self, model, handler):
        self.model = model
        self.handler = handler
    
    def __ror__(self, input_data):
        return self.handler(self.model, input_data)

def setup_ultralytics():
    """Setup pipeline for ultralytics models"""
    try:
        from ultralytics import YOLO, SAM
        from ultralytics.engine.results import Results
    except ImportError:
        print("Error: ultralytics package not found. Please install it using 'pip install ultralytics'.")
        raise
    
    def handle_yolo(model, input_data):
        print(f"Running YOLO detection")
        results = model(input_data)
        return results[0]
    
    def handle_sam(model, input_data):
        print(f"Running SAM segmentation")
        if hasattr(input_data, 'boxes'):
            boxes = input_data.boxes.xyxy.cpu().numpy().tolist()
            return model(input_data.path, bboxes=boxes)
        return model(input_data)
    
    # Register handlers
    ModelRegistry.register(YOLO, handle_yolo)
    ModelRegistry.register(SAM, handle_sam)
    
    # Add pipe operator support
    def model_or(self, other):
        return Pipeline(self, ModelRegistry.get_handler(self)).__ror__(other)
    
    def results_or(self, model):
        handler = ModelRegistry.get_handler(model)
        if handler:
            return Pipeline(model, handler).__ror__(self)
        return NotImplemented
    
    YOLO.__or__ = model_or
    SAM.__or__ = model_or
    Results.__or__ = results_or
    
def setup_depth_estimation():
    """Setup pipeline for depth estimation models"""
    try:
        from transformers import pipeline
        from PIL import Image
    except ImportError:
        print("Error: transformers or Pillow package not found. Please install them using 'pip install transformers Pillow'.")
        raise

    def handle_depth(model, input_data):
        print(f"Running depth estimation")
        if isinstance(input_data, str):
            # If input_data is a string (file path), open the image
            input_data = Image.open(input_data)
        elif not isinstance(input_data, Image.Image):
            raise ValueError("Input must be either a file path or a PIL Image object")
        
        result = model(input_data)
        return result

    # Create a dummy pipeline to get its type
    dummy_pipeline = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")
    
    # Register handler
    ModelRegistry.register(type(dummy_pipeline), handle_depth)

    # Add pipe operator support
    def model_or(self, other):
        return Pipeline(self, ModelRegistry.get_handler(self)).__ror__(other)

    type(dummy_pipeline).__or__ = model_or

def init():
    """Initialize the pipeline system"""
    setup_ultralytics()
    setup_depth_estimation()
    return lambda x: PipelineInput(x)

