import pymysql

db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd='1234',db = 'myflaskapp')

cursor = db.cursor()
# sql = ''' 
#         CREATE TABLE users(
#             id INT(11) AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100),
#             email VARCHAR(100),
#             username VARCHAR(30),
#             password VARCHAR(100),
#             register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
#             ENGINE=InnoDB DEFAULT CHARSET=utf8;
#     '''
# sql=''' 
#     CREATE TABLE `topic` (
# 	`id` int(11) NOT NULL AUTO_INCREMENT,
# 	`title` varchar(100) NOT NULL,
# 	`body` text NOT NULL,
# 	`author` varchar(30) NOT NULL,
#     `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# 	PRIMARY KEY (id)
# 	) ENGINE=innoDB DEFAULT CHARSET=utf8;
# '''

sql_1 = 'SELECT name ,email FROM users;'
# sql_1 = ''' INSERT INTO users(name, email, username, password) 
#         VALUES('LEE','3@naver.com','LEE','1234');
# 		'''


# sql_2 = ''' INSERT INTO users(name, email, username, password) 
#         VALUES('Park','4@naver.com','Park','1234');
#         '''

# result = cursor.execute(sql_2)
# db.commit
# db.close
# cursor.execute(sql_1)
# users = cursor.fetchall()
# print(users)

# print('******************',users[0][1],'*******************')
# print(result)

# cursor.execute(sql_1)
# users = cursor.fetchall()
# print(users)
# db.commit()
# db.close

# name = 'Song'
# email = '5@naver.com'
# username = 'Song'
# password = '1234'
# sql_3 = ''' INSERT INTO users(name, email, username, password) 
#          VALUES(%s,%s,%s,%s);
#         '''

# cursor.execute(sql_3,(name,email,username,password))
# db.commit()
# db.close



# name = 'Gang'
# email = '6@naver.com'
# username = 'Gang'
# password = '1234'

# sql_4 = ''' INSERT INTO users(name, email, username, password) 
#           VALUES(%s,%s,%s,%s);
#         '''

# cursor.execute(sql_4,(name,email,username,password))
# db.commit()
# db.close


# sql_4 = 'DELETE FROM users WHERE  `name`="hong";'


# sql_6 = 'UPDATE users SET `name`="Kong" WHERE  `name`="Song";'
# cursor.execute(sql_6)
# db.commit()
# db.close
#------------------------------------------------------------------------
title = 'javascript'
body = '프로토타입기반의 객체지향 프로그래밍 언어로, 스크립트 언어에 해당된다. 특수한 목적이 아닌 이상 모든 웹 브라우저에 인터프리터가 내장되어 있다. 오늘날 HTML, CSS와 함께 웹을 구성하는 요소 중 하나다. HTML이 웹 페이지의 기본 구조를 담당하고, CSS가 디자인을 담당한다면 JavaScript는 클라이언트 단에서 웹 페이지가 동작하는 것을 담당한다.'
author = 'Gary'
sql_7 = ''' INSERT INTO topic(title, body, author) 
         VALUES(%s,%s,%s);
        '''
# cursor.execute(sql_7,(title,body,author))
# db.commit()
# db.close
# sql_8 = 'SELECT * FROM topic'
# cursor.execute(sql_8)
# topics = cursor.fetchall()
# print(topics)

#--------------------------------------------------------------------------
title = 'Arduino'
body = '영어로 "아두이노", 이탈리아어로 "아르두이노"라고 읽는다. 영어권의 영향이 강한 국내에서 많이 사용되는 명칭은 아두이노. 이탈리아어로 "강력한 친구"라는 뜻이라는 듯. 2005년 이탈리아의 Massimo Banzi와 David Cuartielles가 처음 개발하였다. 개발자 Massimo Banzi가 직접 저술한 <Getting Started with Arduino>(번역명 <손에 잡히는 아두이노>)를 필두로 많은 입문서들이 나와 있다.'
author = 'Gary'
sql_9 = ''' INSERT INTO topic(title, body, author) 
         VALUES(%s,%s,%s);
        '''
sql_10 = 'DELETE FROM topic WHERE  id=3;'
# cursor.execute(sql_9,(title,body,author))
cursor.execute(sql_10)
db.commit()
db.close
