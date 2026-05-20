import sys

import numpy as np

from annotation import FootballVideoProcessor
from ball_to_player_assignment import BallToPlayerAssigner
from club_assignment import ClubAssigner, Club
from config import club1_name, club1_player_color, club1_gk_color, club2_name, club2_player_color, club2_gk_color
from tracking import ObjectTracker, KeypointsTracker
from utils import process_video


OBJ_MODEL_PATH = 'models/weights/object-detection.pt'
KP_MODEL_PATH = 'models/weights/keypoints-detection.pt'
OBJ_CONF_THRESHOLD = .5
BALL_CONF_THRESHOLD = 0.05
FIELD_CONF_THRESHOLD = 0.3
KP_CONF_THRESHOLD = 0.7
FIELD_IMG_PATH = 'input_videos/field_2d_v2.png'
BATCH_SIZE = 10
SAVE_TRACKS_DIR = 'output_videos'
DRAW_FRAME_NUM = True


def main():
    """
    Main function to demonstrate how to use the football analysis project.
    This script will walk you through loading models, assigning clubs, tracking objects and players, and processing the video.
    """

    if len(sys.argv) != 2:
        print("Usage: python main.py <video_source>")
        sys.exit(1)

    print("Team information will be based on config.py. Make sure the file was updated based on the input video.")
    input("Press Enter to continue, or Ctrl+C to exit...")

    video_source = sys.argv[1]
    run_processing(video_source)

def run_processing(video_source, club1_name=club1_name, club1_player_color=club1_player_color, club1_gk_color=club1_gk_color, 
                   club2_name=club2_name, club2_player_color=club2_player_color, club2_gk_color=club2_gk_color):
    
    video_file_name = video_source.split('/')[-1].split('.')[0]
    output_video = f'output_videos/{video_file_name}_annotated.mp4'

    print(f"Processing video: {video_source}")
    print(f"Output will be saved as: {output_video}")

    # 1. Load the object detection model
    # Adjust the 'conf' value as per your requirements.
    print("Loading object detection model...")
    obj_tracker = ObjectTracker(
        model_path=OBJ_MODEL_PATH,      # Object Detection Model Weights Path
        conf=OBJ_CONF_THRESHOLD,        # Object Detection confidence threshold
        ball_conf=BALL_CONF_THRESHOLD,  # Ball Detection confidence threshold
    )
    print("Object detection model loaded.")

    # 2. Load the keypoints detection model
    # Adjust the 'conf' and 'kp_conf' values as per your requirements.
    print("Loading keypoints detection model...")
    kp_tracker = KeypointsTracker(
        model_path=KP_MODEL_PATH,   # Keypoints Model Weights Path
        conf=FIELD_CONF_THRESHOLD,  # Field Detection confidence threshold
        kp_conf=KP_CONF_THRESHOLD,  # Keypoint confidence threshold
    )
    print("Keypoints detection model loaded.")
    
    # 3. Assign clubs to players based on their uniforms' colors
    # Create 'Club' objects - Needed for Player Club Assignment
    # Replace the RGB values with the actual colors of the clubs.
    print("Creating teams...")
    
    club1 = Club(
        club1_name,         # club name 
        club1_player_color, # player jersey color
        club1_gk_color      # goalkeeper jersey color
    )
    club2 = Club(
        club2_name,         # club name 
        club2_player_color, # player jersey color
        club2_gk_color      # goalkeeper jersey color
    )
    print("Teams created.")

    # Create a ClubAssigner Object to automatically assign players and goalkeepers 
    # to their respective clubs based on jersey colors.
    print("Initializing Club Assigner...")
    club_assigner = ClubAssigner(club1, club2)
    print("Club Assigner initialized.")

    # 4. Initialize the BallToPlayerAssigner object
    print("Initializing BallToPlayerAssigner...")
    ball_player_assigner = BallToPlayerAssigner(club1, club2)
    print("BallToPlayerAssigner initialized.")

    # 5. Define the keypoints for a top-down view of the football field (from left to right and top to bottom)
    # These are used to transform the perspective of the field.
    top_down_keypoints = np.array([
        [0, 0], [0, 57], [0, 122], [0, 229], [0, 293], [0, 351],             # 0-5 (left goal line)
        [32, 122], [32, 229],                                                # 6-7 (left goal box corners)
        [64, 176],                                                           # 8 (left penalty dot)
        [96, 57], [96, 122], [96, 229], [96, 293],                           # 9-12 (left penalty box)
        [263, 0], [263, 122], [263, 229], [263, 351],                        # 13-16 (halfway line)
        [431, 57], [431, 122], [431, 229], [431, 293],                       # 17-20 (right penalty box)
        [463, 176],                                                          # 21 (right penalty dot)
        [495, 122], [495, 229],                                              # 22-23 (right goal box corners)
        [527, 0], [527, 57], [527, 122], [527, 229], [527, 293], [527, 351], # 24-29 (right goal line)
        [210, 176], [317, 176]                                               # 30-31 (center circle leftmost and rightmost points)
    ])

    # 6. Initialize the video processor
    # This processor will handle every task needed for analysis.
    print("Initializing video processor...")
    processor = FootballVideoProcessor(
        obj_tracker,                        # Created ObjectTracker object
        kp_tracker,                         # Created KeypointsTracker object
        club_assigner,                      # Created ClubAssigner object
        ball_player_assigner,               # Created BallToPlayerAssigner object
        top_down_keypoints,                 # Created Top-Down keypoints numpy array
        field_img_path=FIELD_IMG_PATH,      # Top-Down field image path
        save_tracks_dir=SAVE_TRACKS_DIR,    # Directory to save tracking information.
        draw_frame_num=DRAW_FRAME_NUM,      # Whether or not to draw current frame number on the output video.
    )
    print("Video processor initialized.")
    
    # 7. Process the video
    # Specify the input video path and the output video path. 
    # The batch_size determines how many frames are processed in one go.
    print("Processing video...")
    process_video(
        processor,                  # Created FootballVideoProcessor object
        video_source=video_source,  # Video source (in this case video file path)
        output_video=output_video,  # Output video path (Optional)
        batch_size=BATCH_SIZE,      # Number of frames to process at once
    )
    print(f"Video processed. Result saved as {output_video}")


if __name__ == '__main__':
    main()
