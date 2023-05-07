import os
import pandas as pd
import datetime

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import QB, RDF, XSD, SKOS, DCTERMS
from rdflib.namespace import DCAT, FOAF

NS = Namespace("https://DuongXuanAnh.github.io/ontology#")
NSR = Namespace("https://DuongXuanAnh.github.io/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

EUROVOC = Namespace("http://eurovoc.europa.eu/")
AT = Namespace("http://publications.europa.eu/resource/authority/")

def create_dcat_dataset():
    dcat_graph = Graph()

    dataset = NSR.CareProviders
    dcat_graph.add((dataset, RDF.type, DCAT.Dataset))
    dcat_graph.add((dataset, RDFS.label, Literal("Poskytovatelé zdravotních služeb", lang="cs")))
    dcat_graph.add((dataset, RDFS.label, Literal("Care Providers", lang="en")))
    dcat_graph.add((dataset, DCTERMS.description, Literal("A dataset containing care providers information.")))
    dcat_graph.add((dataset, DCTERMS.accrualPeriodicity, AT.FREQ_A))
    dcat_graph.add((dataset, DCTERMS.spatial, AT.CNTR_CZ))
    dcat_graph.add((dataset, DCAT.keyword, Literal("care providers")))
    dcat_graph.add((dataset, DCAT.theme, EUROVOC["2185"]))

    publisher = NSR.publisher
    dcat_graph.add((publisher, RDF.type, FOAF.Agent))
    dcat_graph.add((publisher, FOAF.name, Literal("https://github.com/DuongXuanAnh")))
    dcat_graph.add((dataset, DCTERMS.publisher, publisher))

    distribution = NSR.CareProviders_distribution
    dcat_graph.add((distribution, RDF.type, DCAT.Distribution))
    dcat_graph.add((distribution, DCAT.accessURL, Literal("https://github.com/DuongXuanAnh", datatype=XSD.anyURI)))
    dcat_graph.add((distribution, DCAT.mediaType, AT.MEDIA_TYPE_TTL))

    dcat_graph.add((dataset, DCAT.distribution, distribution))

    return dcat_graph

def main():
    dcat_dataset = create_dcat_dataset()
    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/DCAT_Dataset.ttl", "wb") as file:
        dcat_dataset.serialize(file, "ttl")
        print(f"Success, created {file.name}")

if __name__ == "__main__":
    main()
