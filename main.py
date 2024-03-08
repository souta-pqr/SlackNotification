import cv2
from pyzbar.pyzbar import decode
import requests
import time

# SlackのWebhook URL
webhook_url = ''

# Webカメラの設定
cap = cv2.VideoCapture(0)

# QRコードに埋め込む情報
names = ["小堀", "花川", "保科", "伊藤", "遠藤", "久馬", "関取", "若海", "森", "櫻井", "三谷", "大賀", "藤江"]

# 最後に認証された時間を記録する辞書
last_auth = {name: 0 for name in names}

while True:
    # Webカメラから画像を取得
    ret, frame = cap.read()

    # QRコードの読み取り
    decoded_objects = decode(frame)

    # QRコードが読み取れた場合
    if decoded_objects:
        # QRコードのデータが一致するか確認
        name = decoded_objects[0].data.decode()
        if name in names:
            # 最後に認証されてから1分以上経過しているか確認
            if time.time() - last_auth[name] > 60:
                # Slackに通知を送る
                requests.post(webhook_url, json={'text': f'{name}さん認証されました！'})
                # 最後に認証された時間を更新
                last_auth[name] = time.time()

    # 画像を表示
    cv2.imshow('frame', frame)

    # 'q'キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャをリリースしてウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
