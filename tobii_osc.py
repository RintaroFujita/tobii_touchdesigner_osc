# -*- coding: utf-8 -*-
import tobii_research as tr
import time
from pythonosc import udp_client

# OSCクライアントの設定
# 送信先のIPアドレスとポート番号を指定します
# TouchDesignerを同じPCで動かす場合は '127.0.0.1'
OSC_IP = "127.0.0.1"
OSC_PORT = 9000  # TouchDesigner側で待ち受けるポート
client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# Tobii Eye Trackerを探す
found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers:
    print("Eye tracker not found.")
    exit()

my_eyetracker = found_eyetrackers[0]
print(f"Connected: {my_eyetracker.device_name}")
print("Using existing calibration from Tobii Software...")

# 視線データを処理するコールバック関数
def gaze_data_callback(gaze_data):
    print("*** GAZE DATA RECEIVED ***")  # 確実に呼ばれているか確認
    
    # 左目と右目の3D座標と2D座標を取得
    left_gaze_point_2d = gaze_data['left_gaze_point_on_display_area']
    right_gaze_point_2d = gaze_data['right_gaze_point_on_display_area']
    
    print(f"Left valid: {gaze_data['left_gaze_point_validity']}, Right valid: {gaze_data['right_gaze_point_validity']}")
    print(f"Left gaze: {left_gaze_point_2d}, Right gaze: {right_gaze_point_2d}")

    # 座標の有効性チェックを改善（片目だけでも有効な場合は送信）
    if (gaze_data['left_gaze_point_validity'] or 
        gaze_data['right_gaze_point_validity']):
        # 有効な座標のみを使用して平均を計算
        valid_coords = []
        if gaze_data['left_gaze_point_validity']:
            valid_coords.append(left_gaze_point_2d)
        if gaze_data['right_gaze_point_validity']:
            valid_coords.append(right_gaze_point_2d)
        
        if valid_coords:
            avg_x = sum(coord[0] for coord in valid_coords) / len(valid_coords)
            avg_y = sum(coord[1] for coord in valid_coords) / len(valid_coords)
            
            try:
                # OSCメッセージを送信
                client.send_message("/tobii/gaze", [avg_x, avg_y])
                print(f"Sent: /tobii/gaze {avg_x:.3f}, {avg_y:.3f}")
            except Exception as e:
                print(f"OSC Error: {e}")
    else:
        print("No valid gaze data - both eyes invalid")

# 視線データの購読を開始
print("Starting gaze data subscription...")
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
print("Gaze data subscription started. Looking for gaze data...")

# 購読状態を確認
print(f"Subscription active: {my_eyetracker.get_gaze_output_frequency()}")
print("Please look at the screen and move your eyes around...")
print("You should see '*** GAZE DATA RECEIVED ***' messages if gaze data is being received.")

# デバイス情報を表示
print(f"Device info: {my_eyetracker}")
print(f"Device capabilities: {my_eyetracker.device_capabilities}")
print(f"Device frequency: {my_eyetracker.get_gaze_output_frequency()}")

# 5秒待ってから強制的にテストデータを送信
print("Waiting 5 seconds for gaze data...")
time.sleep(5)
print("Sending test data to verify OSC connection...")
try:
    client.send_message("/tobii/gaze", [0.5, 0.5])
    print("Test OSC message sent successfully!")
except Exception as e:
    print(f"Test OSC failed: {e}")

# 追加のデバッグ情報
print("\n=== DEBUG INFO ===")
print(f"Subscription status: {my_eyetracker.get_gaze_output_frequency()}")
print("If you don't see '*** GAZE DATA RECEIVED ***' messages above,")
print("it means the gaze data callback is not being called.")
print("This usually means:")
print("1. Tobii Software calibration is not completed")
print("2. Eye tracking is not started in Tobii Software")
print("3. You need to look at the screen and move your eyes")
print("==================\n")

# スクリプトを終了させないための待機処理
print("Script is running. Press Ctrl+C to stop.")
print("Make sure to look at the screen and move your eyes around.")
print("If no gaze data appears, check Tobii Software calibration.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # 購読を停止
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    print("Connection closed.")