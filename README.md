# twelite-monit
Wireless data collection and notification system using TWELITE

## Description
MONOSTICKが接続されたRaspberryPI等のサーバにインストールして、自宅内にある複数のTWELITEからセンサーデータを収集し記録、必要に応じてスマートフォンへのプッシュ通知を行うPythonスクリプトです。
現在のところ、以下のシステムに対応しています。

* TWELITE PALを使った窓の開閉検知と通知
* タグアプリをインストールしたTWEILTEからのアナログ出力データの収集＋通知

## File List
| File name                      | Description                                                       |
|--------------------------------|-------------------------------------------------------------------|
| lib/pushbullet.py              | Pushbulletを使ったプッシュ通知                                    |
| lib/twelite_PAL_parent.py      | 子機のTWELITEから送られてきたデータのデコード                     |
| twelite_monitor_interactive.py | MONOSTICKで受信したデータをデコードし標準出力に表示（デバック用） |
| twelite_monitor_logging.py     | MONOSTICKで受信したデータをデコードしロギング＋プッシュ通知       |
| start_twelite_monitor.sh       | 起動用スクリプト                                                  |


## How to Use
(作成中)

## License

These codes are licensed under CC0.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)
