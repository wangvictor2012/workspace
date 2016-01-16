from app import db_user, models, db

db_user.create_all()
cursor = db.cursor()
sqlx = "SELECT * FROM user_table"
cursor.execute(sqlx)
table = cursor.fetchall()
for i in range(len(table)):
    u = models.User(id = table[i][0],
                    name = table[i][1],
                    password = table[i][2],
                    rights = table[i][3],
                    date = table[i][4])
    db_user.session.add(u)
    
db_user.session.commit()
