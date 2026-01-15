# -*- coding: utf-8 -*-
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
# flashメッセージやセッション管理に必要
app.secret_key = 'super_secret_key_for_inventory_app'

# DB接続設定
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:pass@db/itemsdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# モデル定義
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)

# DB初期化
with app.app_context():
    for i in range(10):
        try:
            db.create_all()
            break
        except Exception as e:
            time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_name = request.form.get('item_name').strip()
        item_qty_str = request.form.get('item_qty')
        action = request.form.get('action') # 'in' or 'out'
        
        if item_name:
            # 入力された数量を数値に変換（デフォルト1）
            qty = int(item_qty_str) if item_qty_str and item_qty_str.isdigit() else 1
            
            # --- 在庫チェック（バリデーション） ---
            # 現在の対象備品の合計在庫を取得
            current_stock = db.session.query(func.sum(Item.quantity)).filter(Item.name == item_name).scalar() or 0
            
            if action == 'out':
                if current_stock < qty:
                    flash(f'エラー：{item_name}の在庫が足りません（現在：{current_stock}）', 'danger')
                    return redirect(url_for('index'))
                qty = -qty # 出庫の場合はマイナスにする
            
            # データの保存
            new_item = Item(name=item_name, quantity=qty, created_at=datetime.now())
            db.session.add(new_item)
            db.session.commit()
            
            status_msg = "出庫" if action == "out" else "入庫"
            flash(f'{item_name}を{abs(qty)}個、{status_msg}登録しました。', 'success')
            
        return redirect(url_for('index'))

    # 在庫合計の取得
    summary_items = db.session.query(
        Item.name,
        func.sum(Item.quantity).label('total_qty'),
        func.max(Item.created_at).label('last_updated')
    ).group_by(Item.name).having(func.sum(Item.quantity) > 0).all()

    # 全履歴の取得
    all_logs = Item.query.order_by(Item.created_at.desc()).all()

    return render_template('index.html', items=summary_items, logs=all_logs)

# 履歴削除
@app.route('/delete_log/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    log_to_delete = Item.query.get(log_id)
    if log_to_delete:
        db.session.delete(log_to_delete)
        db.session.commit()
        flash('履歴を削除しました。在庫数に反映されます。', 'info')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
