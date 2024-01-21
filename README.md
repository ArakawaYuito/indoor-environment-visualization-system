![ヘッダー画像](docs/img/header/header.png)
<br />
## システムURL
https://arakawabase.com/

## システム背景
近年、BEMS(ビル･エネルギー管理システム)をはじめとする、建物管理のための室内熱環境計測センサーが建物に設置され、建築設備の最適運転が図られている。しかし、センサー設置位置は、壁面等の施工段階で取付可能な位置が選択されることが多いため，居住空間<sup>※</sup>の熱環境とセンサー値に乖離が生じるという課題が挙げられている。したがって、建築設備の最適運転が図るためには、センサー値を居住空間の値に補正する必要がある。
<br>
本システムはその課題を解決することを目的としており、機械学習により居住空間の値を予測・補正し、その結果をリアルタイムに可視化するシステムである。本システムにおいて可視化の対象とするセンサーは、**温度センサー**、**湿度センサー**、**CO2濃度センサー**の3つである。
<br>
（※ 居住空間：部屋の中央や中央に近い領域で、生活活動を行うための主要なスペース。）

## システム動作イメージ
![システム動作イメージ](docs/img/system-view/system-view.gif)

## ユーザ側機能一覧
| ホーム画面 |　温度分布可視化画面 |
| ---- | ---- |
| ![Home画面](docs/img/system-view/home.png) | ![予測画面](docs/img/system-view/RoomInfo_temp.png) |
| 予測結果を確認したい部屋を選択する画面。それぞれの部屋のセンサー値を一目で確認することもできる。 | AIによって予測された温度分布をリアルタイムで可視化する画面。ヒートマップのセルをクリックするとその場所の温度・湿度・CO2濃度を確認できる。 |

| 湿度分布可視化画面 |　CO2濃度分布可視化画面 |
| ---- | ---- |
| ![湿度分布画面](docs/img/system-view/RoomInfo_humid.png) | ![CO2濃度分布画面](docs/img/system-view/RoomInfo_co2.png) |
| 上部のタブボタンで表示する情報を変更できる。こちらはAIによって予測された湿度分布をリアルタイムで可視化する画面 | AIによって予測されたCO2濃度分布をリアルタイムで可視化する画面。|

| センサー値の推移可視化画面 | 過去の分布の選択画面 |
| ---- | ---- |
| ![センサー値の推移](docs/img/system-view/RoomInfo_plot.png) | ![CO2濃度分布画面](docs/img/system-view/RoomInfo_db.png) |
| 各分布可視化画面の下部では、その部屋におけるセンサー値の推移を確認できる。 | 過去の予測結果の分布をDBから取得し表示する画面|

## AIモデル開発者側機能一覧
本システムではAIモデルのライフサイクル管理ツールとしてオープンソースフレームワークの**MLflow**を使用している。
| 実験管理画面 | モデル選択画面 |
| ---- | ---- |
| ![実験管理画面](docs/img/modelDev-view/experiment-view.png) | ![モデル選択画面](docs/img/modelDev-view/select_model-view.png) |
| 実験時の環境を一元管理している。 | データの傾向変化に応じて迅速にモデルを更新できるよう、Aliasesに`@champion`を付与するだけで本番環境のモデルを更新できるようにしてある。 |

## 使用技術一覧
### Frontend
<div>
    <img src="https://img.shields.io/badge/-HTML-E34F26.svg?logo=html5&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/-css-1572B6.svg?logo=css3&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/Vue.js | 3.3.4-4FC08D.svg?logo=vuedotjs&logoColor=white&style=for-the-badge">
</div>

### Backend
<div>
    <img src="https://img.shields.io/badge/Python | 3.11-FEE571.svg?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/Flask | 3.0.0-000000.svg?logo=flask&logoColor=white&style=for-the-badge">
</div>

### Database
<div>
    <img src="https://img.shields.io/badge/SQlite-003B57.svg?logo=sqlite&logoColor=white&style=for-the-badge">
</div>

### Model development
<div>
    <img src="https://img.shields.io/badge/Python | 3.11-FEE571.svg?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/tensorflow | 2.15-FF6F00.svg?logo=tensorflow&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/scikitlearn | 1.3.2-F7931E.svg?logo=scikitlearn&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/mlflow | 2.9.2-0194E2.svg?logo=mlflow&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/numpy | 1.26.1-013243.svg?logo=numpy&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/pandas | 2.1.3-150458.svg?logo=pandas&logoColor=white&style=for-the-badge">
</div>

### Environment setup
<div>
    <img src="https://img.shields.io/badge/docker-1D63ED.svg?logo=docker&logoColor=white&style=for-the-badge">
</div>

### etc.
<div>
    <img src="https://img.shields.io/badge/linux-FCC624.svg?logo=linux&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/ubuntu-E95420.svg?logo=ubuntu&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/nginx-009639.svg?logo=nginx&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/letsencrypt-003A70.svg?logo=letsencrypt&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/npm-C53635.svg?logo=npm&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/vite-646CFF.svg?logo=vite&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/git-F05032.svg?logo=git&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/github-181717.svg?logo=github&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/githubactions-2088FF.svg?logo=githubactions&logoColor=white&style=for-the-badge">
</div>

## インフラ構成図
![インフラ構成図](docs/img/system-architecture/system_architecture.png)

## 今後の課題
現状、データの収集および予測モデルの構築が完了しているのが"House"のみとなっている。したがって、"House"以外の部屋については"House"の予測結果をそのまま表示している。今後は"House"以外の部屋についてもデータの収集および予測モデルの構築を行い、予測結果を表示できるようにする。