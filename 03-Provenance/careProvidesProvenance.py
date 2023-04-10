from rdflib import Namespace, Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF, PROV, FOAF, XSD


RESOURCE_NS = Namespace("https://DuongXuanAnh.github.io/resources/")
PROV_NS = Namespace("https://DuongXuanAnh.github.io/provenance#")


def generate_provenance() -> None:
    prov_data = get_provenance_data()
    prov_data.serialize(format="trig", destination = "./careProvidersProvenance.trig")


def get_provenance_data() -> Graph:
    prov_graph  = Graph(bind_namespaces="rdflib")
    
    add_entities(prov_graph)

    add_agents(prov_graph)

    add_activities(prov_graph)
    
    return prov_graph 


def add_entities(prov_graph: Graph) -> None:
    data_cube = RESOURCE_NS.CareProviders
    prov_graph.add((data_cube, RDF.type, PROV.Entity))
    prov_graph.add((data_cube, PROV.wasGeneratedBy, PROV_NS.CareProvidersETLScript))
    prov_graph.add((data_cube, PROV.wasDerivedFrom, PROV_NS.CareProvidersDataset))
    prov_graph.add((data_cube, PROV.wasAttributedTo, PROV_NS.CareProvidersETLScript))
    
    dataset = PROV_NS.CareProvidersDataset
    prov_graph.add((dataset, RDF.type, PROV.Entity))
    prov_graph.add((dataset, PROV.wasGeneratedBy, PROV_NS.HealthMinistryCR))
    

def add_agents(prov_graph: Graph) -> None:
    script = PROV_NS.CareProvidersETLScript
    prov_graph.add((script, RDF.type, PROV.SoftwareAgent))
    prov_graph.add((script, PROV.wasAttributedTo, PROV_NS.DuongXuanAnh))
    prov_graph.add((script, PROV.atLocation, URIRef("care_providers_cube.py")))

    health_ministry = PROV_NS.HealthMinistryCR
    prov_graph.add((health_ministry, RDF.type, PROV.Agent))
    prov_graph.add((health_ministry, RDF.type, FOAF.Organization))
    prov_graph.add((health_ministry, FOAF.name, Literal("Ministerstvo zdravotnictví ČR", lang="cs")))
    prov_graph.add((health_ministry, FOAF.homepage, Literal("https://www.mzcr.cz/", datatype=XSD.anyURI)))

    organization = PROV_NS.MFF
    prov_graph.add((organization, RDF.type, PROV.Agent))
    prov_graph.add((organization, RDF.type, FOAF.Organization))
    prov_graph.add((organization, FOAF.name, Literal("Matematicko-fyzikální fakulta", lang="cs")))
    prov_graph.add((organization, FOAF.homepage, Literal("https://www.mff.cuni.cz/", datatype=XSD.anyURI)))
    
    author = PROV_NS.DuongXuanAnh
    prov_graph.add((author, RDF.type, FOAF.Person))
    prov_graph.add((author, RDF.type, PROV.Agent))
    prov_graph.add((author, PROV.wasAttributedTo, PROV_NS.PetrSkoda))
    prov_graph.add((author, FOAF.name, Literal("Duong Xuan Anh", lang="cs")))
    prov_graph.add((author, FOAF.mbox, URIRef("email:david.anh@email.cz")))
    
    instructor = PROV_NS.PetrSkoda
    prov_graph.add((instructor, RDF.type, FOAF.Person))
    prov_graph.add((instructor, RDF.type, PROV.Agent))
    prov_graph.add((instructor, PROV.wasAttributedTo, PROV_NS.MFF_UK))
    prov_graph.add((instructor, FOAF.name, Literal("Mgr. Petr Škoda, Ph.D.", lang="cs")))
    prov_graph.add((instructor, FOAF.mbox, URIRef("email:petr.skoda@matfyz.cuni.cz")))
    
    

def add_activities(prov_graph: Graph) -> None:
    dc_activity = PROV_NS.CareProvidersCubeCreationActivity
    prov_graph.add((dc_activity, RDF.type, PROV.Activity))
    prov_graph.add((dc_activity, PROV.used, PROV_NS.CareProvidersDataset))
    prov_graph.add((dc_activity, PROV.startedAtTime, Literal("2023-04-10T00:00:00", datatype=XSD.dateTime)))
    prov_graph.add((dc_activity, PROV.endedAtTime, Literal("2023-05-10T00:00:00", datatype=XSD.dateTime)))
    
    usage = BNode()
    prov_graph.add((dc_activity, PROV.qualifiedUsage, usage))
    prov_graph.add((usage, RDF.type, PROV.Usage))
    prov_graph.add((usage, PROV.entity, PROV_NS.CareProvidersDataset))
    prov_graph.add((usage, PROV.hadRole, PROV_NS.ETLRole))
    

if __name__ == "__main__":
    generate_provenance()