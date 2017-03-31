#! /usr/bin/python3
# @Djavan Sergent
# Exemples d'utilisation du sql manager
import sqlmanager as sql
import random
import models.pictures as pic

if __name__ == "__main__":

    # Création de la base de données (Tables)
    sql.Dbconfig().Base.metadata.create_all(sql.Dbconfig().engine)

    # Création de l'instance de l'ORM
    session = sql.Dbconfig().Session()

    # Création d'instances de Pictures
    for i in range(11,100):
        pict = pic.Pictures(pict=str('{0:010d}'.format(random.randint(1, 9999999999))),
                            tags="test"+str(i), ntags=1, lat=random.random(), lon=random.random())

        # Persistance de l'instance dans l'ORM
        session.add(pict)

    # Commit des modifications dans la base de données
    session.commit()

    # Query des objets + utilisation fonction __repr__ pour éléments 4 à 8
    for instance in session.query(pic.Pictures).order_by(pic.Pictures.id)[4:8]:
        print(instance)

    # Récupération d'une entrée de la base
    pict = session.query(pic.Pictures).filter_by(id="3").first()
    picts = session.query(pic.Pictures).filter(pic.Pictures.tags.in_(['test1', 'test4', 'test8']))

    # Modification de l'objet
    pict.location = "65.093434 ; 98.0293984"
    print("\n*** modified picture : ***")
    print(pict)
    print("\n*** list of filtered pictures : ***")
    print(picts.all())
