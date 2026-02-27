# My Tech Blog 🚀

FastAPI (Python) で構築した個人ブログシステムです。
さくらVPS上に構築し、独自ドメインとSSL（HTTPS）に対応した本番環境で運用しています。

**[https://gorankudasai.com/](https://gorankudasai.com/)**

**常時稼働しています👆**


## 🛠 技術スタック
- **言語**: Python 3.12.10
- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL (本番) / SQLite (開発)
- **サーバー**: さくらVPS (Ubuntu)
- **Webサーバー**: Nginx
- **デプロイ**: Git / GitHub

## 📂 ディレクトリ構造
```text
.
├── main.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
├── posts/               # 各記事のHTMLファイル
└── .gitignore
```
## 🚀 ローカルでの起動方法

### 1. リポジトリをクローン
```bash
git clone [https://github.com/daiki-program/BlogApp.git](https://github.com/daiki-program/BlogApp.git)
```
```bash
cd BlogApp
```

### 2. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```

### 3. アプリケーションの起動
```bash
python main.py
```

http://127.0.0.1:8000 にアクセスして確認できます。

## 🌐 デプロイについて
本プロジェクトは GitHub Actions 等は使用せず、VPS側で git fetch および git reset --hard を行うことで最新コードを反映させています。
---

Developed by D. S.
