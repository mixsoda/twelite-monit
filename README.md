# twelite-monit
Wireless data collection and notification system using TWELITE

## Description
MONOSTICKが接続されたRaspberryPI等のサーバにインストールして、自宅内にある複数のTWELITEからセンサーデータを収集し記録、Pushbulletを使ったスマートフォンへのプッシュ通知を行うPythonスクリプトです。
現在のところ、以下のシステムに対応しています。

* TWELITE PALを使った窓の開閉検知と通知
* タグアプリをインストールしたTWEILTEからのアナログ出力データの収集＋通知

<img src="https://github.com/mixsoda/twelite-monit/blob/master/images/analog_sensor.JPG?raw=true" width="30%" /><img src="https://github.com/mixsoda/twelite-monit/blob/master/images/window.JPG?raw=true" width="30%" />

## File List
| File name                      | Description                                                       |
|--------------------------------|-------------------------------------------------------------------|
| lib/pushbullet.py              | Pushbulletを使ったプッシュ通知                                    |
| lib/twelite_PAL_parent.py      | 子機のTWELITEから送られてきたデータのデコード                     |
| twelite_monitor_interactive.py | MONOSTICKで受信したデータをデコードし標準出力に表示（デバック用） |
| twelite_monitor_logging.py     | MONOSTICKで受信したデータをデコードしロギング＋プッシュ通知       |
| run_twelite_monit.sh           | 起動用スクリプト                                                  |


## How to Use

### 想定環境
Raspberry Pi + Berryconda3上で実行する場合を例にセットアップ方法を説明します。

berryconda3のインストールディレクトリは「/home/pi/berryconda3/」と仮定しています。

Python3が動作するLinux環境なら動作すると思いますので、適宜読み替えてください。

### 下準備
まず、このリポジトリのファイルをダウンロードしてLinux上に展開してください。（ここでは展開先を「/home/pi/twelite/monitor/」と仮定しています。）

展開したら起動用スクリプト「run_twelite_monit.sh」に実行属性を付与し、スクリプトの３行目にPythonのインストールされているディレクトリを設定します。

以下、/home/pi/berryconda3/binにインストールされている場合の例：
```bash
export PATH="/home/pi/berryconda3/bin:$PATH"
```

プッシュ通知を送るためにPushbulletの設定を行います。

プッシュ通知送信先のアクセストークンを「lib/pushbullet.py」のtoken変数に設定します。

```python
def push_message(title, body):
	token = "YOUR PRIVATE TOKEN IS HERE"
```

twelite-monitは複数のTWELITEデバイスからのデータ受信とロギングに対応しています。
そこで、TWELITEの各デバイスIDがどのセンサータイプ（窓の開閉検知 or アナログデータの収集）、設置場所に対応しているか設定します。設定は、twelite_monitor_logging.pyの以下の位置で設定します。

```python
## global conf ##
#monitoring type of each end device {EndDevice_Logical_ID:"TYPE"}
#TYPE :: WINDOW or MOISTURE
monitor_type = {1:"WINDOW", 2:"MOISTURE"}
#LOCATION
monitor_location = {1:"2Fベランダ窓", 2:"1F観葉植物"}
```

この設定では、TWELITEのデバイスID=1が窓の開閉監視（設置場所は2Fのベランダ窓）、ID-2がアナログ出力データ監視（1Fの観葉植物の水分センサー）する場合の例です。locationの名前は、プッシュ通知する場合に使われますので、場所が特定できるなら何でもよいです。

Raspberry Piに接続しているMONOSTICKのシリアルポートのパスを設定します。他にシリアルポートを使用するデバイスを接続していない場合は、おそらく変更しなくても問題ないはず。
```python
	#serial port
	port_name = "/dev/ttyUSB0" #for linux
	#port_name = "COM4"        #for win
```

最後に、「lib/twelite_PAL_parent.py」に、TWELITEにインストールされているアプリをデバイスIDごとに指定します。TAGアプリとPALアプリに対応しています。
```python
	#installed applist of each end device
	installed_app = {1:"PAL", 2:"TAG"}
```

ここまでで、準備完了です。

### ロギングと監視の開始
twelite_monitor_logging.pyはMONOSTICKからデータが送られてくるのを待ち受けていて、送られてきたらロギング＋通知を行います。起動は、以下のコマンドで行います。

```bash
./run_twelite_monit.sh
```

twelite_monitor_logging.pyは常時起動したままにしておく必要があります。不意に停止してしまうと、ロギングも通知もされなくなるので、run_twelite_monit.shには、cronと併用することで死活監視する機能がついています。
死活監視するには、crontabに以下の行を追加しrun_twelite_monit.shを定期的に実行します。

```bash
2 */3 * * * /home/pi/twelite/monitor/run_twelite_monit.sh
```

この例では、３時間おきに死活監視します。
これで、logディレクトリ内にcsvファイルが作成されてデータが記録されていきます。

## 参考
[TWELITE PALを使って窓の施錠確認システムを電子工作なしで作る](https://zlog.hateblo.jp/entry/2019/08/18/Twelite-pal-window-monitor)

[TWELITEでリモート土壌水分センサーを作る](https://zlog.hateblo.jp/entry/2019/10/19/twelite-soil-moisture-sensor)

## License

These codes are licensed under CC0.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)
