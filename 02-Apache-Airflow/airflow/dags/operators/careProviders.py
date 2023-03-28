import os
import pandas as pd
import datetime

from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import QB, RDF, XSD, SKOS, DCTERMS


NS = Namespace("https://DuongXuanAnh.github.io/ontology#")
NSR = Namespace("https://DuongXuanAnh.github.io/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

SDMX_DIM = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMX_MES = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
SDMX_CON = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")


def care_providers_main(output_path = "/opt/airflow/dags/"):
    file_path = "./narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"
    data = load_data(file_path)
    data_cube = as_data_cube(data)
    data_cube.serialize(format="ttl", destination = output_path.rstrip("/") + "/CareProviders.ttl")


def load_data(file_path: str):
    data = pd.read_csv(file_path, low_memory=False)
    return data


def as_data_cube(data):
    cube = Graph()
    dimensions = create_dimensions(cube)
    measures = create_measure(cube)
    structure = create_structure(cube, dimensions, measures)
    dataset = create_dataset(cube, structure)
    create_resources(cube, data)
    create_observations(cube, dataset, data.groupby(["OkresCode", "KrajCode", "OborPece"]))

    return cube


def create_dimensions(cube: Graph):
    county = NS.county
    cube.add((county, RDF.type, RDFS.Property))
    cube.add((county, RDF.type, QB.DimensionProperty))
    cube.add((county, RDFS.label, Literal("Okres", lang="cs")))
    cube.add((county, RDFS.label, Literal("County", lang="en")))
    cube.add((county, RDFS.range, NSR.County))
    cube.add((county, QB.codeList, NSR.county))
    cube.add((county, QB.concept, SDMX_DIM.refArea))

    region = NS.region
    cube.add((region, RDF.type, RDFS.Property))
    cube.add((region, RDF.type, QB.DimensionProperty))
    cube.add((region, RDFS.label, Literal("Kraj", lang="cs")))
    cube.add((region, RDFS.label, Literal("Region", lang="en")))
    cube.add((region, RDFS.range, NSR.region))
    cube.add((region, QB.codeList, NSR.region))
    cube.add((region, QB.concept, SDMX_DIM.refArea))

    field_of_care = NS.fieldOfCare
    cube.add((field_of_care, RDF.type, RDFS.Property))
    cube.add((field_of_care, RDF.type, QB.DimensionProperty))
    cube.add((field_of_care, RDFS.label, Literal("Obor péče", lang="cs")))
    cube.add((field_of_care, RDFS.label, Literal("Field of care", lang="en")))
    cube.add((field_of_care, RDFS.range, NSR.FieldOfCare))
    cube.add((field_of_care, QB.codeList, NSR.fieldOfCare))

    return [county, region, field_of_care]


def create_measure(cube: Graph):
    num_of_care_providers = NS.numberOfCareProviders
    cube.add(( num_of_care_providers, RDF.type, RDFS.Property))
    cube.add(( num_of_care_providers, RDF.type, QB.MeasureProperty))
    cube.add(( num_of_care_providers, RDFS.label, Literal("Počet poskytovatelů péče", lang="cs")))
    cube.add(( num_of_care_providers, RDFS.label, Literal("Number of care providers", lang="en")))
    cube.add((num_of_care_providers, RDFS.subPropertyOf, SDMX_MES.obsValue))
    cube.add(( num_of_care_providers, RDFS.range, XSD.integer))

    return [num_of_care_providers]


def create_structure(cube: Graph, dimensions, measures):
    structure = NS.structure
    cube.add((structure, RDF.type, QB.DataStructureDefinition))

    for dimension in dimensions:
        component = BNode()
        cube.add((structure, QB.component, component))
        cube.add((component, QB.dimension, dimension))

    for measure in measures:
        component = BNode()
        cube.add((structure, QB.component, component))
        cube.add((component, QB.measure, measure))

    return structure


def create_dataset(cube: Graph, structure):
    dataset = NSR.CareProviders
    cube.add((dataset, RDF.type, QB.DataSet))
    cube.add((dataset, RDFS.label, Literal("Poskytovatelé zdravotních služeb", lang="cs")))
    cube.add((dataset, RDFS.label, Literal("Care Providers", lang="en")))

    cube.add((dataset, QB.structure, structure))

    cube.add((dataset, DCTERMS.issued, Literal(datetime.date.today().isoformat(), datatype=XSD.date)))
    cube.add((dataset, DCTERMS.modified, Literal(datetime.date.today().isoformat(), datatype=XSD.date)))
    cube.add((dataset, DCTERMS.title, Literal("Poskytovatelé zdravotních služeb", lang="cs")))
    cube.add((dataset, DCTERMS.title, Literal("Care Providers", lang="en")))
    cube.add((dataset, DCTERMS.publisher, Literal("https://github.com/DuongXuanAnh", datatype=XSD.anyURI)))
    cube.add(
        (
            dataset,
            DCTERMS.license, 
            Literal("https://github.com/DuongXuanAnh", datatype=XSD.anyURI)
        )
    )

    return dataset


def format_converter(obj: any):
    return str(obj).replace(",", "").replace(" ", "_").lower()


def add_resource(cube: Graph, resource_type, label: str, lang: str, resource: str):
    uri = NSR[resource]
    cube.add((uri, RDF.type, resource_type))
    cube.add((uri, SKOS.prefLabel, Literal(label, lang=lang)))


def create_resources(cube: Graph, data):
    for _, row in data[["Okres", "OkresCode"]].drop_duplicates().dropna().iterrows():
        county = format_converter(row["OkresCode"])
        county_label = str(row["Okres"])
        add_resource(cube, NS.county, county_label, "cs", county)

    for _, row in data[["Kraj", "KrajCode"]].drop_duplicates().dropna().iterrows():
        region = format_converter(row["KrajCode"])
        region_label = str(row["Kraj"])
        add_resource(cube, NS.region, region_label, "cs", region)

    for _, row in data[["OborPece"]].drop_duplicates().dropna().iterrows():
        fieldOfCare = format_converter(row["OborPece"])
        field_label = str(row["OborPece"])
        add_resource(cube, NS.field_of_care, field_label, "cs", fieldOfCare)


def create_observations(cube: Graph, dataset, data):
    for index, ((county, region, field_of_care), group) in enumerate(data):
        resource = NSR["observation-" + str(index).zfill(4)]
        create_observation(cube, dataset, resource, county, region, field_of_care, group)

def create_observation(cube: Graph, dataset, resource, county, region, field_of_care, group):
    cube.add((resource, RDF.type, QB.Observation))
    cube.add((resource, QB.dataSet, dataset))
    cube.add((resource, NS.county, NSR[format_converter(county)]))
    cube.add((resource, NS.region, NSR[format_converter(region)]))
    cube.add((resource, NS.field_of_care, NSR[format_converter(field_of_care)]))
    cube.add((resource, NS.number_of_care_providers,Literal(len(group), datatype=XSD.integer)))


if __name__ == "__main__":
    care_providers_main()