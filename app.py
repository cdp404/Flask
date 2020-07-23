#서버와 교류하는 방법은 get 방식과 post 방식이 있다
#get 방식은 URL에 데이터를 포함시켜서 교류함 (보안 취약, 빠름)
#post 방식은 html문서 body에 데이터를 포함시켜서 교류함(보안 강하고 get보다 느림)


from flask import Flask, render_template,flash,redirect,url_for,session,request,logging      # render_template : 요청한 클라이언트에 HTML형식으로 문서화 시켜서 보내는 Class
from passlib.hash import pbkdf2_sha256
from data import Articles
import pymysql


app = Flask(__name__)
app.debug = True


db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd='1234',db = 'myflaskapp')
cursor = db.cursor()

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

@app.route("/home")
def home():
    return render_template("home.html")    

@app.route("/register",methods=['GET','Post'])
def register():
    if request.method == 'POST':
        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        if not(pbkdf2_sha256.verify(re_password,password)):
            print((pbkdf2_sha256.verify(re_password,password)))
            return "Invalid Password"
        else:
        # name = form.name.data
            print([name,email,password,re_password,username])
            
           
            sql = ''' INSERT INTO users(name, email, username, password) 
                   VALUES(%s,%s,%s,%s);
                  '''
            cursor.execute(sql,(name,email,username,password))
            db.commit()
            # cursor.execute('SELECT * FROM users;')
            # users = cursor.fetchall()
            return redirect(url_for('home'))
    else :
        return render_template('register.html')
    db.close()
@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('email')
        pw = request.form.get('password')
        
        sql = 'SELECT * FROM users WHERE email =%s'
        cursor.execute(sql,[id])
        users = cursor.fetchone()


        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                return redirect(url_for('articles'))
            else:
                return redirect(url_for('login'))
        
        return "Success"
    else:
        return render_template('login.html')
    db.close()





@app.route("/articles")      
def articles():
    # articles = Articles()
    # print(len(articles))
    sql = 'SELECT * FROM topic;'
    cursor.execute(sql)
    articles = cursor.fetchall()
    print(articles)
    # return "get success"
    return render_template("articles.html", articles = articles)


@app.route('/article/<int:id>')
def article(id):
    sql = 'SELECT * FROM topic WHERE id = %s'
    print(id)
    articles = Articles()[id-1]
    print(articles)
    return render_template("article.html",data = articles)
    # return 'success'

@app.route('/add_articles',methods=['GET','POST'])  # GET 형식과 POST 형식 둘 다 적용되게 함
def add_articles():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        sql = ''' INSERT INTO topic(title,body,author) 
                   VALUES(%s,%s,%s);
                  '''
        cursor.execute(sql,(title,body,author))
        db.commit()
        return redirect('/articles')
    else :
        return render_template('add_articles.html')
    db.close()

if __name__ == "__main__":      # 여길 제일 먼저 실행 (가장 초입에 작성)
    # app.run(host = "0.0.0.0", port = "8080")
    app.run()                   # defalut 값 port = "5000"

