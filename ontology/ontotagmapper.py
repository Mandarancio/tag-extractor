from owlready import *
import tagextractor.storage.dbmanager as dbm

# Data sources
onto_path.append('..\\resources')
onto = get_ontology('kr-owlxml.owl')
onto.load()
manager = dbm.DBManager('sqlite:///../database/instagram.db')

# Database tags
session = manager.session()
tags = session.query(dbm.Tag)

# all classes in ontology
classes = ONTOLOGIES['http://tagis.kr.com'].classes
tagis = []
for c in classes:
    tagis.append(c.name.lower())

# Comparison
matchs = []
for t in tags:
    if t.tag.lower() in tagis:
        matchs.append(t.tag.lower())

pictures = session.query(dbm.PictureTagLink).filter(dbm.PictureTagLink.tag_id.in_(matchs))

for m in matchs:
    print(m)

for p in pictures:
    print(p)


print(matchs)
