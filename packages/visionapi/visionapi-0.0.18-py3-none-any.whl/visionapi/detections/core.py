import numpy as np

def ultralytics_detections(results, format='xyxy'):
    """
    Process YOLO results and extract useful information from boxes.
    
    Args:
    results (ultralytics.engine.results.Results): YOLO detection results
    format (str): Desired bounding box format ('xyxy', 'xywh', 'xyxyn', or 'xywhn'). Default is 'xyxy'.
    
    Returns:
    list: List of dictionaries containing processed information for each detected object
    """
    processed_results = []
    
    for result in results:
        boxes = result.boxes
        
        for i in range(len(boxes)):
            obj = {
                'class': int(boxes.cls[i].item()),
                'class_name': result.names[int(boxes.cls[i].item())],
                'confidence': boxes.conf[i].item(),
                'bbox': getattr(boxes, format)[i].tolist(),
            }
            processed_results.append(obj)
    
    return processed_results

def quick_display(results, ultralytics_results=False, notebook=False, fps=30, width=640, height=480, multicam=False):
    """
    Quickly display detection results in a Jupyter notebook or OpenCV window.

    Args:
        results (list or dict): Detection results from YOLO or other models. Can be:
            - List of ultralytics Results objects for single camera
            - Dict of lists of Results objects for multiple cameras
            - List of frames with detections drawn
        ultralytics_results (bool): If True, assumes results are from Ultralytics YOLO. Default is False.
        notebook (bool): If True, displays in Jupyter notebook. If False, uses OpenCV window. Default is False.
        fps (int): Frames per second for video playback. Default is 30.
        width (int): Width of the display frame. Default is 640.
        height (int): Height of the display frame. Default is 480.
        multicam (bool): If True, assumes results are from multiple cameras. Default is False.

    Returns:
        None: Displays the results either inline in Jupyter notebook or in OpenCV window.

    Note:
        This function requires OpenCV (cv2), base64, IPython.display, and time modules.
        For notebook display, results will be shown inline.
        For OpenCV window display, press 'q' to exit.
    """
    import cv2
    import base64
    from IPython.display import display, HTML, clear_output
    import time

    if notebook:
        if ultralytics_results and len(results) <= 1:
            try:
                _, buffer = cv2.imencode('.jpg', results[0].plot()) 
                img_str = base64.b64encode(buffer).decode('ascii')
                # Display the frame
                clear_output(wait=True)
                display(HTML(f'<img src="data:image/jpeg;base64,{img_str}" width="640" height="480"/>'))
                
            except IndexError:
                print("No detections found")
                pass
        elif multicam:
            frame_count = 0
            while True:
                try:
                    frames = [results[cam][frame_count].plot() for cam in sorted(results.keys())]
                    frame_count += 1
                except IndexError:
                    break
                
                # Resize frames to have the same height
                max_height = max(frame.shape[0] for frame in frames)
                resized_frames = [cv2.resize(frame, (int(frame.shape[1] * max_height / frame.shape[0]), max_height)) for frame in frames]
                
                # Calculate total width
                total_width = sum(frame.shape[1] for frame in resized_frames)
                
                # Create a blank canvas
                canvas = np.zeros((max_height, total_width, 3), dtype=np.uint8)
                
                # Paste frames onto the canvas
                x_offset = 0
                for i, frame in enumerate(resized_frames):
                    canvas[:, x_offset:x_offset+frame.shape[1]] = frame
                    
                    # Add camera label
                    cv2.putText(canvas, f'cam{i}', (x_offset + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                    x_offset += frame.shape[1]
                
                _, buffer = cv2.imencode('.jpg', canvas) 
                img_str = base64.b64encode(buffer).decode('ascii')
                
                # Display the frame
                clear_output(wait=True)
                display(HTML(f'<img src="data:image/jpeg;base64,{img_str}" style="max-width: 100%; height: auto;"/>'))
                time.sleep(1/fps)
                
        else:
            frame_count = 0
            for result in results:
                try:
                    _, buffer = cv2.imencode('.jpg', result.plot()) 
                    img_str = base64.b64encode(buffer).decode('ascii')
                    # Display the frame
                    clear_output(wait=True)
                    display(HTML(f'<img src="data:image/jpeg;base64,{img_str}" width="640"/>'))
                    
                    time.sleep(1/fps)
                    frame_count += 1
                except IndexError:
                    print("No detections found")
                    pass
    else:
        # Display using cv2 window
        frame_count = 0
        while True:
            if isinstance(results, dict):
                try:
                    frames = [results[cam][frame_count].plot() for cam in sorted(results.keys())]
                    frame_count += 1
                except IndexError:
                    break

                # Resize frames to have the same height
                max_height = max(frame.shape[0] for frame in frames)
                resized_frames = [cv2.resize(frame, (int(frame.shape[1] * max_height / frame.shape[0]), max_height)) for frame in frames]
                
                # Calculate total width
                total_width = sum(frame.shape[1] for frame in resized_frames)
                
                # Create a blank canvas
                canvas = np.zeros((max_height, total_width, 3), dtype=np.uint8)
                
                # Paste frames onto the canvas
                x_offset = 0
                for i, frame in enumerate(resized_frames):
                    canvas[:, x_offset:x_offset+frame.shape[1]] = frame
                    cv2.putText(canvas, f'cam{i}', (x_offset + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    x_offset += frame.shape[1]

                cv2.imshow('Detections', canvas)

            else:
                try:
                    frame = results[frame_count].plot()
                    cv2.imshow('Detections', frame)
                    frame_count += 1
                except IndexError:
                    pass

            # Wait for key press
            key = cv2.waitKey(int(1000/fps)) & 0xFF
            
            # Press 'q' to quit
            if key == ord('q'):
                break

        cv2.destroyAllWindows()
        
