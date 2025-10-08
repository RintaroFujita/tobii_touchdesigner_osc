# -*- coding: utf-8 -*-
import tobii_research as tr
import time

print("=== Tobii Eye Tracker Simple Test ===")

# Step 1: Browsing
print("Step 1: Browsing for eye trackers...")
found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers:
    print("No eye trackers found.")
    exit()

print(f"Found {len(found_eyetrackers)} eye tracker(s)")

# Step 2: Connecting
print("Step 2: Connecting to eye tracker...")
my_eyetracker = found_eyetrackers[0]
print(f"Connected to: {my_eyetracker.device_name}")

# Step 4: Subscribing to data
print("Step 4: Subscribing to gaze data...")

def simple_gaze_callback(gaze_data):
    print("*** GAZE DATA RECEIVED ***")
    print(f"Left eye valid: {gaze_data['left_gaze_point_validity']}")
    print(f"Right eye valid: {gaze_data['right_gaze_point_validity']}")
    if gaze_data['left_gaze_point_validity']:
        print(f"Left gaze: {gaze_data['left_gaze_point_on_display_area']}")
    if gaze_data['right_gaze_point_validity']:
        print(f"Right gaze: {gaze_data['right_gaze_point_on_display_area']}")

# Subscribe to gaze data
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, simple_gaze_callback, as_dictionary=True)
print("Subscription started. Looking for gaze data...")
print("Please look at the screen and move your eyes around.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...")
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, simple_gaze_callback)
    print("Disconnected.")

