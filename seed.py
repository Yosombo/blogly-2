from models import User, db, Post
from app import app

db.drop_all()
db.create_all()

User.query.delete()

puje = User(first_name='Puje', last_name='Gana')
soyo = User(first_name='Soyo', last_name='Enk')
amar = User(first_name='Amar', last_name='Tsog')
anny = User(first_name='Anny', last_name='Amar')
db.session.add_all([puje, soyo, amar, anny])

pj_post1 = Post(title="puje 1st", content='qwerty111', user_id=1)
pj_post2 = Post(title="puje 2nd", content='qwerty222', user_id=1)
soyo_post1 = Post(title="soyombo 1st", content='qwerty111', user_id=2)
soyo_post2 = Post(title="soyombo 2nd", content='qwerty222', user_id=2)
anny_post1 = Post(title="anny 1st", content='qwerty111', user_id=4)
anny_post2 = Post(title="anny 2nd", content='qwerty222', user_id=4)
amar_post1 = Post(title="amar 1st", content='qwerty111', user_id=3)
amar_post2 = Post(title="amr 2nd", content='qwerty222', user_id=3)
db.session.add_all([
    pj_post2, pj_post1, soyo_post1, soyo_post2, anny_post1, anny_post2,
    amar_post1, amar_post2
])
db.session.commit()
