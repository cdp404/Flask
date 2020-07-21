#서버와 교류하는 방법은 get 방식과 post 방식이 있다
#get 방식은 URL에 데이터를 포함시켜서 교류함 (보안 취약, 빠름)
#post 방식은 html문서 body에 데이터를 포함시켜서 교류함(보안 강하고 get보다 느림)


from flask import Flask, render_template,flash,redirect,url_for,session,request,logging      # render_template : 요청한 클라이언트에 HTML형식으로 문서화 시켜서 보내는 Class
from flask_mysqldb import MySQL
from data import Articles
import pymysql


app = Flask(__name__)
app.debug = True

#config MySQL
app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORd'] = '1234'
app.config ['MYSQL_DB'] = 'myflaskapp'
app.config ['MYSQL_CURSORCLASS']='DictCursor'

db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd='1234',db = 'myflaskapp')




sql_1 = 'SELECT * FROM users;'
sql_2 = ''' INSERT INTO users(name, email, username, password') 
        VALUES('Lee','3@naver.com','Lee','1234');
        '''
cursor = db.cursor()
# result = cursor.execute(sql_2)
# db.commit
# db.close
# # users = cursor.fetchall()
# cursor.execute(sql_1)
# print(users)

# print('******************',users[0][1],'*******************')
# print(result)




#init mysql
# mysql = MySQL(app)

# cur = mysql.connecetion.cursor()
# cur.execute("SELECT * FROM users;")
# users = cur.fetchall()
# print(users)

@app.route("/")      # decoration : 메소드를 연계하게 해준다. (app.route 경로지정)
def index():
    print("World success")                                  # cmd에 World success 출력
    # return "TEST"
    return render_template("home.html", hello = "Koy")      # 만들어둔 home.html의 문서 데이터를 페이지로 불러 시각화함
                                                            # render_template class 및 method는 파일 내 templates 파일에 플러그인 함(내부 class 자체가 이렇게 코딩되어있음 즉, templates 파일을 만들 것)
                                                            # hello 변수에 "koy" 저장 후 home.html에 사용가능 {{}}로 호출

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articles", methods = ['GET', 'POST'])      # GET 형식과 POST 형식 둘 다 적용되게 함
def articles():
    articles = Articles()
    print(len(articles))
    return render_template("articles.html", articles = articles)

@app.route('/test')
def show_image():
    return render_template('image.html')

@app.route('/article/<int:id>')
def article(id):
    print(id)
    articles = Articles()[id-1]
    print(articles)
    return render_template("article.html",data = articles)
    # return 'success'


if __name__ == "__main__":      # 여길 제일 먼저 실행 (가장 초입에 작성)
    # app.run(host = "0.0.0.0", port = "8080")
    app.run()                   # defalut 값 port = "5000"