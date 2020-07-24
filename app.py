#서버와 교류하는 방법은 get 방식과 post 방식이 있다
#get 방식은 URL에 데이터를 포함시켜서 교류함 (보안 취약, 빠름)
#post 방식은 html문서 body에 데이터를 포함시켜서 교류함(보안 강하고 get보다 느림)


from flask import Flask, render_template,flash,redirect,url_for,session,request,logging      # render_template : 요청한 클라이언트에 HTML형식으로 문서화 시켜서 보내는 Class
from passlib.hash import pbkdf2_sha256
from data import Articles
import pymysql
from functools import wraps


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

def is_logged_out(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'is_logged' in session:
            return redirect(url_for('articles'))
        else:
            return f(*args , **kwargs)
    return wrap


@app.route("/register",methods=['GET','Post'])
@is_logged_out
def register():
    if request.method == 'POST':
        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        sql = 'SELECT username FROM users WHERE username = %s'
        cursor.execute(sql,[username])
        username_1 = cursor.fetchone()
        if  username_1:
            return redirect(url_for('register'))
        else :
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
                return redirect(url_for('login'))
    else :
        return render_template('register.html')
    db.close()


@app.route("/login",methods = ['GET','POST'])
@is_logged_out
def login():
    if request.method == 'POST':
        id = request.form.get('username')
        pw = request.form.get('password')
        
        sql = 'SELECT * FROM users WHERE username = %s'
        cursor.execute(sql,[id])
        users = cursor.fetchone()


        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                session['is_logged'] = True
                session['username'] = users[3]
                return redirect('/')
            else:
                return redirect(url_for('login'))
        
        return "Success"
    else:
        return render_template('login.html')
    db.close()

def is_logged_in(f):
    @wraps(f)
    def _wraper(*args, **kwargs):
        if 'is_logged' in session:
        # if session['is_logged']:
            return f(*args,**kwargs)
        else :
            flash('UnAuthorized,Please login','danger')
            return redirect(url_for('login'))

    return _wraper

def is_admin(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session['username']=="ADMIN":
            return redirect('/admin')
        else :
            return f(*args,**kwargs)
    return wrap


@app.route("/")      # decoration : 메소드를 연계하게 해준다. (app.route 경로지정)
@is_logged_in
@is_admin
def index():
    print("World success")
    # session['test'] = "gary kim"
    # sesson_data = session                                  # cmd에 World success 출력
    # print(sesson_data)
    # return "TEST"
    return render_template("home.html")      # 만들어둔 home.html의 문서 데이터를 페이지로 불러 시각화함
                                                            # render_template class 및 method는 파일 내 templates 파일에 플러그인 함(내부 class 자체가 이렇게 코딩되어있음 즉, templates 파일을 만들 것)
                                                            # hello 변수에 "koy" 저장 후 home.html에 사용가능 {{}}로 호출

@app.route("/about")
@is_logged_in
def about():
    return render_template("about.html")



@app.route("/articles")      
@is_logged_in
def articles():
    # articles = Articles()
    # print(len(articles))
    sql = 'SELECT * FROM topic;'
    cursor.execute(sql)
    articles = cursor.fetchall()
    # return "get success"
    return render_template("articles.html", articles = articles)


@app.route('/article/<int:id>')
@is_logged_in

def article(id):
   
    cursor = db.cursor()
    sql = 'SELECT * FROM topic WHERE id = %s'
    cursor.execute(sql,[id])
    # articles = Articles()[id-1]
    topic = cursor.fetchone()
    print(topic)
    return render_template("article.html",data = topic)
    # return 'success'

@app.route('/article/<string:id>/edit_article',methods=['GET', 'POST'])
@is_logged_in

def edit_article(id):
    if request.method =="POST":
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        cur = db.cursor()
        sql = '''
            UPDATE `topic` SET `title`=%s,`body`=%s, `author`=%s  WHERE  `id`= %s;
        '''
        cur.execute(sql , (title,body,author, id ))
        db.commit()
        return redirect(url_for('articles'))
    else:
        print(id)
        cur = db.cursor()
        sql = 'SELECT * FROM topic WHERE id=%s'
        cur.execute(sql , [id])
        topic = cur.fetchone()
        return render_template('edit_article.html', data= topic)
    db.close()

@app.route('/add_articles',methods=['GET','POST'])  # GET 형식과 POST 형식 둘 다 적용되게 함
@is_logged_in
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

@app.route('/delete/<string:id>',methods = ['POST'])
@is_logged_in
def delete(id):
    cursor = db.cursor()
    sql = 'DELETE FROM topic WHERE id=%s'
    cursor.execute(sql,[id])
    db.commit()
    return redirect(url_for('articles'))

@app.route('/logout',methods = ['GET'])
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

def is_admined(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session['username'] != "ADMIN":
            return redirect('/')
        else :
            return f(*args,**kwargs)
    return wrap

@app.route('/admin',methods = ['GET','POST'])
@is_logged_in
@is_admined
def admin():
    sql = 'SELECT * FROM users;'
    cursor.execute(sql)
    admin_user = cursor.fetchall()
    return render_template('admin.html',data=admin_user)


@app.route('/user/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admined
def change_level(id):
    if request.method =='POST':
        cursor=db.cursor()
        sql = 'UPDATE `users` SET `auth`=%s WHERE  `id`=%s;'
        # 
        auth = request.form['auth']
        cursor.execute(sql ,[auth,id])
        return redirect('/')
    else:
        cursor=db.cursor()
        sql = "SELECT * FROM users WHERE id=%s"
        cursor.execute(sql,[id])
        user = cursor.fetchone()
        return render_template('change_level.html', users=user)



if __name__ == "__main__":      # 여길 제일 먼저 실행 (가장 초입에 작성)
    app.secret_key = 'secretkey123456789'  # app.run(host = "0.0.0.0", port = "8080")
    app.run()                   # defalut 값 port = "5000"

