
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, FOAF, XSD, PROV


POPULATION_NS = Namespace("http://DuongXuanAnh/population#")
PROV_NS = Namespace("http://DuongXuanAnh.org/provenance#")


POPULATION_2021_DATASET = POPULATION_NS['MeanPopulation2021']
CARE_PROVIDERS_DATASET = PROV_NS['CareProvidersDataset']
COUNTY_CODELIST_MAP = PROV_NS['CountyCodelistMap']
POPULATION_2021_ETL_SCRIPT = PROV_NS['Population2021ETLScript']
CZECH_STATISTICAL_OFFICE = PROV_NS['CzechStatisticalOffice']
HEALTH_MINISTRY_CR = PROV_NS['HealthMinistryCR']
POPULATION_2021_CUBE_CREATION_ACTIVITY = PROV_NS['Population2021CubeCreationActivity']


def generate_provenance() -> None:
    prov_data = get_provenance_data()
    prov_data.serialize(format="trig", destination = "./populationProvenance.trig")

def get_provenance_data() -> Graph:
    prov_graph = Graph(bind_namespaces="rdflib")
    
    add_entities(prov_graph)
    add_agents(prov_graph)
    add_activities(prov_graph)
    
    return prov_graph


def add_entities(prov_graph: Graph) -> None:
    data_cube = POPULATION_NS.MeanPopulation2021
    prov_graph.add((data_cube, RDF.type, PROV.Entity))
    prov_graph.add((data_cube, PROV.wasGeneratedBy, PROV_NS.Population2021CubeCreationActivity))
    prov_graph.add((data_cube, PROV.wasDerivedFrom, PROV_NS.Population2021Dataset))
    prov_graph.add((data_cube, PROV.wasAttributedTo, PROV_NS.Population2021ETLScript))

        
    prov_graph.add((CARE_PROVIDERS_DATASET, RDF.type, PROV.Entity))
    prov_graph.add((CARE_PROVIDERS_DATASET, PROV.wasAttributedTo, PROV_NS.HealthMinistryCR))
    
    prov_graph.add((POPULATION_2021_DATASET, RDF.type, PROV.Entity))
    prov_graph.add((POPULATION_2021_DATASET, PROV.wasAttributedTo, PROV_NS.CzechStatisticalOffice))
    
    prov_graph.add((COUNTY_CODELIST_MAP, RDF.type, PROV.Entity))
    prov_graph.add((COUNTY_CODELIST_MAP, PROV.wasAttributedTo, PROV_NS.CzechStatisticalOffice))
    

def add_agents(prov_graph: Graph) -> None:
    script = PROV_NS.Population2021ETLScript
    prov_graph.add((script, RDF.type, PROV.SoftwareAgent))
    prov_graph.add((script, PROV.actedOnBehalfOf, PROV_NS.DuongXuanAnh))
    prov_graph.add((script, PROV.atLocation, URIRef("population_2021_cube.py")))
    
    author = PROV_NS.DuongXuanAnh
    prov_graph.add((author, RDF.type, FOAF.Person))
    prov_graph.add((author, RDF.type, PROV.Agent))
    prov_graph.add((author, PROV.actedOnBehalfOf, PROV_NS.PetrSkoda))
    prov_graph.add((author, FOAF.name, Literal("Duong Xuan Anh", lang="cs")))
    prov_graph.add((author, FOAF.mbox, URIRef("email:david.anh@email.cz")))
    
    instructor = PROV_NS.PetrSkoda
    prov_graph.add((instructor, RDF.type, FOAF.Person))
    prov_graph.add((instructor, RDF.type, PROV.Agent))
    prov_graph.add((instructor, PROV.actedOnBehalfOf, PROV_NS.MFF_UK))
    prov_graph.add((instructor, FOAF.name, Literal("Mgr. Petr Škoda, Ph.D.", lang="cs")))
    prov_graph.add((instructor, FOAF.mbox, URIRef("email:petr.skoda@matfyz.cuni.cz")))
    
    organization = PROV_NS.MFF
    prov_graph.add((organization, RDF.type, PROV.Agent))
    prov_graph.add((organization, RDF.type, FOAF.Organization))
    prov_graph.add((organization, FOAF.name, Literal("Matematicko-fyzikální fakulta", lang="cs")))
    prov_graph.add((organization, FOAF.homepage, Literal("https://www.mff.cuni.cz/", datatype=XSD.anyURI)))

    prov_graph.add((HEALTH_MINISTRY_CR, RDF.type, FOAF.Organization))
    prov_graph.add((HEALTH_MINISTRY_CR, RDF.type, PROV.Agent))
    prov_graph.add((HEALTH_MINISTRY_CR, FOAF.name, Literal("Ministerstvo zdravotnictví ČR", lang="cs")))
    prov_graph.add((HEALTH_MINISTRY_CR, FOAF.homepage, Literal("https://www.mzcr.cz/", datatype=XSD.anyURI)))
    
    prov_graph.add((CZECH_STATISTICAL_OFFICE, RDF.type, FOAF.Organization))
    prov_graph.add((CZECH_STATISTICAL_OFFICE, RDF.type, PROV.Agent))
    prov_graph.add((CZECH_STATISTICAL_OFFICE, FOAF.name, Literal("Český statistický úřad", lang="cs")))
    prov_graph.add((CZECH_STATISTICAL_OFFICE, FOAF.homepage, Literal("https://www.czso.cz/", datatype=XSD.anyURI)))
    

    
def add_activities(prov_graph: Graph) -> None:
    dc_activity = POPULATION_2021_CUBE_CREATION_ACTIVITY
    prov_graph.add((dc_activity, RDF.type, PROV.Activity))
    prov_graph.add((dc_activity, PROV.wasAssociatedWith, POPULATION_2021_ETL_SCRIPT))
    prov_graph.add((dc_activity, PROV.startedAtTime, Literal("2023-04-10T00:00:00", datatype=XSD.dateTime)))
    prov_graph.add((dc_activity, PROV.endedAtTime, Literal("2023-05-10T00:00:00", datatype=XSD.dateTime)))
    
    usages = [
        (POPULATION_2021_DATASET, PROV_NS.ETLRole),
        (CARE_PROVIDERS_DATASET, PROV_NS.ETLRole),
        (COUNTY_CODELIST_MAP, PROV_NS.ETLRole)
    ]
    
    for _, (entity, role) in enumerate(usages, start = 1):
        usage = BNode()
        prov_graph.add((dc_activity, PROV.used, usage))
        prov_graph.add((usage, RDF.type, PROV.Usage))
        prov_graph.add((usage, PROV.entity, entity))
        prov_graph.add((usage, PROV.hadRole, role))
    

if __name__ == "__main__":
    generate_provenance()