from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import os

# 使用static文件夹
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


@app.route('/')
def index():
    """返回首页"""
    return app.send_static_file('index.html')


@app.route('/api/launches')
def get_launches():
    """获取发射数据"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'mission_launches.csv')

        if not os.path.exists(csv_path):
            return jsonify({'success': False, 'error': 'CSV文件不存在'}), 404

        df = pd.read_csv(csv_path)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)

        df = df.replace({np.nan: 0})  # 用 0 替代 NaN
        print(f" 成功读取 {len(df)} 条数据")

        return jsonify({
            'success': True,
            'count': len(df),
            'data': df.to_dict('records')
        })
    except Exception as e:
        print(f" 错误: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



if __name__ == '__main__':
    print("=" * 60)
    print("✅ 访问: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
