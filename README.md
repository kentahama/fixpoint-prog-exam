# サーバログ監視

## 使い方
```
python3 src/main.py N m t
```

## テスト
```
python3 src\main.py 3 3 50 < test\input1.txt
```

input1:

```
20201020123410,192.168.11.1/24,8
20201020123411,192.168.11.1/24,121
20201020123412,192.168.11.1/24,113
# ここで 3回の平均が 50 を超える
20201020123413,192.168.11.1/24,108
20201020123414,192.168.11.1/24,-
# ここからタイムアウト
20201020123415,192.168.11.1/24,-
20201020123416,192.168.11.1/24,-
# ここでネットワーク内のサーバが3回タイムアウト
20201020123417,192.168.11.1/24,-
20201020123418,192.168.11.1/24,9
# タイムアウトここまで (ネットワークも同じ)
20201020123419,192.168.11.1/24,11
# ここで 3回の平均が 50 以下になる
20201020123420,192.168.11.1/24,8
```

## 結果
```
192.168.11.1/24 has been timeout;
         from 2020-10-20 12:34:14
         to   2020-10-20 12:34:18
Network 192.168.11.0/24 has been down
         from 2020-10-20 12:34:16
         to   2020-10-20 12:34:18
192.168.11.1/24 has been overloaded;
         from 2020-10-20 12:34:12
         to   2020-10-20 12:34:19
```
