# import pymysql
# import re 
# f = open('dict.txt')
# db = pymysql.connect(host='localhost',
#                             user='root',
#                             password='123456',
#                             database='dict',
#                             charset='utf8',
#                             port=3306)
# cur =  db.cursor()
# s=f.read()
# l1=[]
# for i in re.findall("\n\w+",s):
#     l1.append(i[1:])
# l2=[]
# for i in re.findall("  .+",s):
#     l2.append(i.strip())

# for line in range(len(l2)):
#     # l = re.split('[ ]+',line)

#     sql_insert = """insert into aaa values ("%s","%s");"""%(l1[line],l2[line])
#     print(sql_insert)
#     cur.execute(sql_insert)
#     db.commit()
#     # try:
#     # except Exception as e:
#     #     db.rollback()
#     #     print(e)
# cur.close()
# db.close()
# f.close()

import pymysql
import re
f = open('dict.txt')
db = pymysql.connect('localhost','root','123456','dict')
cursor = db.cursor()


for line in f:
    l = re.split(r'\s+',line)
    name = l[0]
    hanyi = ' '.join(l[1:])
    sql = "insert into aaa(name,hanyi) values('%s','%s')"%(name,hanyi)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()

