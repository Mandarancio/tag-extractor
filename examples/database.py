#! /usr/bin/python3
# @Djavan Sergent
# Exemples d'utilisation du sql manager
import sqlmanager as sql
import random

if __name__ == "__main__":

    # Création de la base de données (Tables)
    sql.Base.metadata.create_all(sql.engine)

    # Création de l'instance de l'ORM
    session = sql.Session()

    # Création d'instances de Pictures
    for i in range(10):
        pict = sql.Pictures(pict=str(i), tags="test"+str(i), location=str(random.random()))

        # Persistance de l'instance dans l'ORM
        session.add(pict)

    # Commit des modifications dans la base de données
    session.commit()

    # Query des objets + utilisation fonction __repr__ pour éléments 4 à 8
    for instance in session.query(sql.Pictures).order_by(sql.Pictures.id)[4:8]:
        print(instance)

    # Récupération d'une entrée de la base
    pict = session.query(sql.Pictures).filter_by(id="3").first()
    picts = session.query(sql.Pictures).filter(sql.Pictures.tags.in_(['test1', 'test4', 'test8']))

    # Modification de l'objet
    pict.location = "65.093434 ; 98.0293984"
    print("\n*** modified picture : ***")
    print(pict)
    print("\n*** list of filtered pictures : ***")
    print(picts.all())
