import cv2
from pyzbar.pyzbar import decode
import requests
import time
from datetime import datetime
import pygame  # 音声ファイルを再生するためのライブラリ


# SlackのWebhook URL
webhook_url = 


# Webカメラの設定
cap = cv2.VideoCapture(4)
if not cap.isOpened():
    raise RuntimeError('カメラが開けませんでした。カメラが接続されていることを確認してください。')


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラの解像度を上げる
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラの解像度を上げる


# QRコードに埋め込む情報
names = ["小堀さん", "花川さん", "保科さん", "伊藤さん", "遠藤さん", "久馬さん", "関取さん", "若海さん", "森さん", "櫻井さん", "三谷さん", "大賀さん", "藤江さん"]


# 最後に認証された時間とステータスを記録する辞書
last_auth = {name: {'time': 0, 'status': 'Exited'} for name in names}


# pygameを初期化
pygame.mixer.init()


while True:
    # 現在の時間を取得
    now = datetime.now()


    # 22時になったら全員のステータスをリセット
    if now.hour == 22 and now.minute == 0:
        last_auth = {name: {'time': 0, 'status': 'Exited'} for name in names}


    # Webカメラから画像を取得
    ret, frame = cap.read()
    if not ret:
        print('フレームが読み取れませんでした。')
        continue


    # カラー画像であることを確認
    if len(frame.shape) != 3 or frame.shape[2] != 3:
        print('カラー画像を取得できませんでした。')
        continue


    # QRコードの読み取り
    decoded_objects = decode(frame)


    # QRコードが読み取れた場合
    if decoded_objects:
        # QRコードのデータが一致するか確認
        data = decoded_objects[0].data.decode()
        if data.isdigit():
            index = int(data) - 1
            if 0 <= index < len(names):
                name = names[index]
                # 最後に認証されてから1分以上経過しているか確認
                if time.time() - last_auth[name]['time'] > 60:
                    # ステータスに応じてメッセージを変更
                    if last_auth[name]['status'] == 'Exited':
                        message = f'{name}が入室しました！'
                        last_auth[name]['status'] = 'Entered'
                    else:
                        message = f'{name}が退出しました！'
                        last_auth[name]['status'] = 'Exited'
                    # Slackに通知を送る
                    requests.post(webhook_url, json={'text': message})
                    # 最後に認証された時間を更新
                    last_auth[name]['time'] = time.time()
                    print(message)  # 認証されたことをコンソールに表示


                    # 音声ファイルを再生
                    pygame.mixer.music.load('zun.wav')
                    pygame.mixer.music.play()


    # 画像を表示
    cv2.imshow('frame', frame)


    # 'q'キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# キャプチャをリリースしてウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
