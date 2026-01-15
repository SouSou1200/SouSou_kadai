# 1. Python 3.11が入った状態からスタート
FROM python:3.14

# 2. フォルダ「/app」の中で作業するよ、と決める
WORKDIR /app

# 3. 買い物リストをコピーして、部品をインストールする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 今あるすべてのファイル（app.pyなど）をコピーする
COPY . .

# 5. 「python app.py」というコマンドでアプリを起動してね！
CMD ["python", "app.py"]