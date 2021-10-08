from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta_plus_week1

from datetime import datetime

# index.html
@app.route('/')
def home():
    return render_template('index.html')


# Diary POST 방식
@app.route('/send', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    # File Area
    file = request.files["file_give"]

    # File에서 . 뒤에 값을 가져오는 명령어( ex> 가.나.다.라.마.바.사 => 가[0]나[1]다[2]라[3]마[-3]바[-2]사[-1]
    # 파일 확장자 확인용
    extension = file.filename.split('.')[-1]

    # 현재시각 Data
    today = datetime.now()

    # year/month/day/hour/minute/second -> 위에서 받아온 현재시각을 규칙에 맞게 수정
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    print(mytime)
    # year/month/day-> 위에서 받아온 현재시각을 규칙에 맞게 수정2
    datatime = today.strftime('%Y.%m.%d')

    # File 이름 지정하는 부분
    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)


    # 몽고 db저장
    doc = {
        'title' : title_receive,
        'content' : content_receive,
        'file' : f'{filename}.{extension}',
        'data' : datatime
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)