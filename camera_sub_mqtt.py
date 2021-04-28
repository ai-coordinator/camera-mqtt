#!usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("topic/test", 0)  # subするトピックを設定

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている

  jpg_as_np = np.frombuffer(msg.payload, dtype=np.uint8)
  image_buffer = cv2.imdecode(jpg_as_np, flags=1)
  cv2.imshow("image", image_buffer)

  key = cv2.waitKey(10)
        # Escキーが押されたら
  if key == 27:
      cv2.destroyAllWindows()

# MQTTの接続設定
client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック

client.connect("localhost", 1883, 60)  # 接続先は自分自身

client.loop_forever()                  # 永久ループして待ち続ける
