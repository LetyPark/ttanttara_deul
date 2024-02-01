# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)

# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()
    

emotions1 = {
    "슬픔": ["우울", "미련", "좌절"],
    "행복": ["설레임", "즐거움", "성취감"],
    "분노": ["배신감", "불쾌감", "원망"]
}

@app.route("/")
def home():
    return render_template('intro.html')

@app.route("/survey1/")
def survey1():
    return render_template('survey1.html')

@app.route("/survey2/<emotion>")
def survey2(emotion):
    feelings = emotions1.get(emotion, [])
    return render_template('survey2.html', feelings=feelings, emotion=emotion)

@app.route("/survey3/<emotion>/<feeling>")
def survey3(emotion, feeling):
    options = reason(emotion, feeling)
    return render_template('survey3.html', emotion=emotion, feeling=feeling, options=options)
    
def reason(emotion, feeling):
    reason_options = {    
        "슬픔": {
            "우울": ["결별", "실패", "비도 오고 그래서....", "무기력", "지인 또는 반려견의 죽음", "몸무계 상승", "파산", "권고사직"],
            "미련": ["X애인", "그리움", "아쉬움", "주식 하락", "눈 앞에서 놓친 대중교통", "한 끗 차이"],  
            "좌절": ["실패", "열등감", "패배", "몸무계 상승", "시험 탈락", "자존감 하락"],  
        },
        "행복": {
            "설레임": ["연애", "새로운 시작", "썸", "여헹 가는 길", "입사일", "소개팅"],  
            "즐거움": ["여행", "날씨 좋음", "재미", "연휴", "용돈 or 월급날", "취미 활동"],  
            "성취감": ["성공", "합격", "주식 상승", "인센티브", "다이어트 성공", "팀플 성공", "상장 수여", "자랑"],  
        },
        "분노": {
            "배신감": ["환승이별", "친구에게 사기", "팀플잠수(무임승차)", "믿는 도끼에 발등 찍힘", "잘 본줄 알았던 시험에 낙방", "채무관계"],  
            "불쾌감": ["출퇴근 혼잡시간", "냄새", "같이 사는 룸메이트의 위생이슈", "팀플 잠수", "예의 없을때"],  
            "원망": ["다툼", "여행 준비물 놓고 오는 상황(여권 등 필수템)", "팀플 잠수", "도용", "사기"],  

        },
    }
    # Use get method to handle cases where emotion or feeling is not in options_mapping
    return reason_options.get(emotion, {}).get(feeling, [])


@app.route("/music/<emotion>")
def music(emotion):
    emotion = request.args.get("emotion")
    print("Emotion:" , emotion)
    song_list = Song.query.all()
    return render_template('music.html', data=song_list, emotion=emotion)


@app.route("/music_detail/")
def music_detail():
    song_list = Song.query.all()
    return render_template('music_detail.html', data=song_list)


# @app.route("/music/<username>/")
# def render_music_filter(username):
#     filter_list = Song.query.filter_by(username=username).all()
#     return render_template('music.html', data=filter_list)
    

@app.route("/music/create/")
def music_create():
    # form에서 보낸 데이터 받아오기
    username_receive = request.args.get("username")
    title_receive = request.args.get("title")
    artist_receive = request.args.get("artist")
    image_receive = request.args.get("image_url")
    
    # 데이터를 DB에 저장하기
    song = Song(username=username_receive, title=title_receive, artist=artist_receive, image_url=image_receive)
    db.session.add(song)
    db.session.commit()
    return redirect(url_for('render_music_filter', username=username_receive))


if __name__ == "__main__":
    app.run(debug=True)