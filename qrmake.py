import qrcode

# QRコードに埋め込む情報
names = ["小堀さん", "花川さん", "保科さん", "伊藤さん", "遠藤さん", "久馬さん", "関取さん", "若海さん", "森さん", "櫻井さん", "三谷さん", "大賀さん", "藤江さん"]

for i, name in enumerate(names):
    # QRコードの生成
    qr = qrcode.QRCode(
        version=2,  # QRコードの複雑さを増やす
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # エラー訂正レベルを上げる
        box_size=10,
        border=4,
    )
    qr.add_data(str(i+1), optimize=0)  # 数字を文字列として埋め込む
    qr.make(fit=True)

    # QRコードの描画と保存
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'qrcode_{name}.png')
