# -*- coding: utf-8 -*-
import time
from pythonosc import udp_client

# OSCクライアントの設定
OSC_IP = "127.0.0.1"
OSC_PORT = 9000
client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

print("Testing OSC connection...")
print(f"Sending to {OSC_IP}:{OSC_PORT}")

try:
    for i in range(10):
        # テストデータを送信
        test_x = 0.5 + 0.1 * (i % 3)  # 0.5, 0.6, 0.7 を繰り返し
        test_y = 0.5 + 0.1 * (i % 2)  # 0.5, 0.6 を繰り返し
        
        client.send_message("/tobii/gaze", [test_x, test_y])
        print(f"Sent test data {i+1}/10: /tobii/gaze {test_x:.1f}, {test_y:.1f}")
        time.sleep(1)
        
    print("Test completed!")
    
except Exception as e:
    print(f"OSC Error: {e}")
