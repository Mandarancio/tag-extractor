#! /usr/bin/python3
# @Djavan Sergent
import sqlmanager as sql

if __name__ == "__main__":

    # Création de la base de données (Tables)
    sql.Base.metadata.create_all(sql.engine)

    # Création de l'instance de l'ORM
    session = sql.Session()

    # Création d'une instance de Pictures
    pict = sql.Pictures(pict="4563-56667-324", tags="test", location="65.034 ; 0.847439")

    # Persistance de l'instance dans l'ORM
    session.add(pict)

    # Modification de l'objet
    pict.location = "65.093434 ; 98.0293984"

    # Commit des modifications dans la base de données
    session.commit()

    # Appel de la fonction __repr__ de l'objet
    print(pict)
