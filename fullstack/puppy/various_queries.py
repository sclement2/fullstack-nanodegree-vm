from sqlalchemy import create_engine
from sqlalchemy.sql import select
from datetime import date, datetime, timedelta
from sqlalchemy.orm import sessionmaker

from puppies import Base, Puppy, Shelter

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#conn = engine.connect()
#rs = session.query(Puppy.name, Shelter.name)\
#	.join(Shelter, Shelter.id == Puppy.shelter_id)\
#	.group_by(Shelter.name, Puppy.name).all()
rs = session.query(Shelter.name, Puppy.name)\
	.join(Puppy, Shelter.id == Puppy.shelter_id)\
	.group_by(Shelter.name, Puppy.name).all()
print rs
prev = ''
for row in rs:
	if prev != row[0]:
		print('\n' + row[0])
		prev = row[0]
	else:
		print(row[1])

#print rs


def run_query(s):
	rs = conn.execute(s)
	for row in rs:
		print row


def run_orm_query(s):
	for name in s.query(Puppy.name).order_by(Puppy.name):
		print name


#sel = select([Puppy])
#sel = select([Puppy.name, Puppy.dateOfBirth]).where(Puppy.dateOfBirth > (date.today() - timedelta(days=180))).order_by(Puppy.dateOfBirth)
#sel = select([Puppy.name, Puppy.weight]).order_by(Puppy.weight)
#sel = select([Puppy.name, Shelter.name]).select_from(join(Shelter, Shelter.id == Puppy.shelter_id)
#run_query(sel)
#run_orm_query(session)


#print(lowest)



