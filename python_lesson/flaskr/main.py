from flaskr import app
from flask import render_template, request
import openai

import pandas as pd

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        user_text = request.form.get('user')
        # ここで必要な処理を実行する
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"この文章から5W1Hを抜き出してください。「{user_text}」" },
            ]
        )
        res_content = res["choices"][0]["message"]["content"]

        if res_content:
        # 5W1Hの表を作成
            data = {
                "5W1H": ["いつ", "誰と", "何を", "どこで", "何が必要"],
                "回答": [""] * 5  # 空のセルを持つリストを作成
            }
        
            res_content_split = res_content.split()
            num_values = min(len(res_content_split), len(data["5W1H"]))  # 要素数を5W1Hの数に制限

            # 回答に値を設定
            for i in range(num_values):
                data["回答"][i] = res_content_split[i]

            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(columns=["5W1H", "回答"])  # 空のデータフレームを作成

        table = df.to_html(index=False)
        return render_template('result.html', table=table, res_content=res_content)


    return "無効なリクエストです。"
