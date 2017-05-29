"""ontology classifier."""
# TODO add more concepts (boat) and
# NONE concepts (color, geography, lake)  as well
import owlready as owlr
from nltk.corpus import wordnet as wn

NONE_CATEGORY = "NONE"


def __get_synset__(owlclass):
    name = owlclass.name.lower()
    synsets = wn.synsets(name)
    if synsets:
        return synsets
    return None


def __classify__(tag, classes):
    if tag['synset']:
        synset = wn.synset(tag['synset'])
        shortest = 0.1
        category = NONE_CATEGORY
        for name in classes:
            syns = classes[name][1]
            for syn in syns:
                taxonomy_distance = synset.path_similarity(syn)
                if taxonomy_distance and taxonomy_distance > shortest:
                    category = name
                    shortest = taxonomy_distance
        # if shortest > 0.1:
            # print("{}: {}[{}]".format(tag['raw'], category, shortest))
        return category
    return NONE_CATEGORY


def __get_concept_subclasses__(ontology):
    owlclasses = ontology.classes
    metaclasses = []
    subclasses = []

    for concept in owlclasses:
        if 'Concept' in concept.name and concept.name != 'Concept':
            metaclasses.append(concept)
        if concept.name == 'Picture':
            subclasses.append(concept)

    for metaclasse in metaclasses:
        subs = ontology.subclasses_of(metaclasse)
        for sub in subs:
            subclasses.append(sub)
    return subclasses


def load_ontology(base_path, filename, ontoname):
    """Load ontology."""
    owlr.onto_path.append(base_path)
    ontology = owlr.get_ontology(filename)
    ontology.load()
    return owlr.ONTOLOGIES[ontoname]


def write_ontology(onto_in, onto_out):
    """Write the new ontology to file."""
    results = owlr.to_owl(onto_in)
    output = open(onto_out, 'w')
    output.write(results)
    output.close()


def make_distinct(ontology):
    """Meke all instnaces distinct."""
    ontology.add(owlr.AllDistinct(*ontology.instances))


def classifier(pictures, ontology):
    """Simple classifier."""
    # owlclasses = ontology.classes
    owlconcept = __get_concept_subclasses__(ontology)

    classes = {}
    for owlclass in owlconcept:
        # print(owlclass.name)
        syn = __get_synset__(owlclass)
        if syn:
            classes[owlclass.name] = (owlclass, syn)
    for picture in pictures:
        tags = picture['tags']
        instance = classes['Picture'][0]()
        for tag in tags:
            tag['concept'] = __classify__(tag, classes)
            # instance of concept
            concept = classes[tag['concept'].lower().title()][0]()
            # propriety of instance
            instance.hasTags.append(concept)
        yield picture


if __name__ == '__main__':
    from tagextractor.classification.loader import DBLoader
    LOADER = DBLoader("sqlite:///database/url_instagram.db")
    ONTOLOGY = load_ontology('resources', 'kr-owlxml.owl',
                             'http://tagis.kr.com')

    print(LOADER.photo_number())
    for pic in classifier(LOADER.load(20), ONTOLOGY):
        print(pic['name'])
        for ptag in pic['tags']:
            print('  {}: {}'.format(ptag['raw'], ptag['concept']))

    make_distinct(ONTOLOGY)
    ONTOLOGY.sync_reasoner()
    ONTOLOGY.save('result.owl')
