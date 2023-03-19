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


def main():
    data = load_data("Population2021/130141-22data2021.csv")
    codelist_data = load_data("Population2021/číselník-okresů-vazba-101-nadřízený.csv")
    data_cube = as_data_cube(data, codelist_data)

    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/Population.ttl", "wb") as file:
        data_cube.serialize(file, "ttl")


def load_data(file_path: str):
    data = pd.read_csv(file_path, low_memory=False)
    return data


def as_data_cube(data, codelist):
    cube = Graph()
    dimensions = create_dimensions(cube)
    measures = create_measure(cube)
    structure = create_structure(cube, dimensions, measures)
    dataset = create_dataset(cube, structure)

    data = query_data(data)

    create_resources(cube, data, codelist)
    create_observations(cube, dataset, data, codelist)

    return cube

def query_data(data):
    return data.query('vuk == "DEM0004" and vuzemi_cis == 101')


def create_dimensions(cube: Graph):
    county = NS.county
    cube.add((county, RDF.type, RDFS.Property))
    cube.add((county, RDF.type, QB.DimensionProperty))
    cube.add((county, RDF.type, QB.CodedProperty))
    cube.add((county, RDFS.label, Literal("Okres", lang="cs")))
    cube.add((county, RDFS.label, Literal("County", lang="en")))
    cube.add((county, RDFS.range, NSR.County))
    cube.add((county, QB.codeList, NSR.county))
    cube.add((county, QB.concept, SDMX_DIM.refArea))

    region = NS.region
    cube.add((region, RDF.type, RDFS.Property))
    cube.add((region, RDF.type, QB.DimensionProperty))
    cube.add((region, RDF.type, QB.CodedProperty))
    cube.add((region, RDFS.label, Literal("Kraj", lang="cs")))
    cube.add((region, RDFS.label, Literal("Region", lang="en")))
    cube.add((region, RDFS.range, NSR.Region))
    cube.add((region, QB.codeList, NSR.region))
    cube.add((region, QB.concept, SDMX_DIM.refArea))

    return [county, region]


def create_measure(cube: Graph):
    mean_population = NS.mean_population

    cube.add((mean_population, RDF.type, RDF.Property))
    cube.add((mean_population, RDF.type, QB.MeasureProperty))
    cube.add((mean_population, RDFS.label, Literal("Střední stav obyvatel", lang="cs")))
    cube.add((mean_population, RDFS.label, Literal("Mean population", lang="en")))
    cube.add((mean_population, RDFS.range, XSD.integer))
    cube.add((mean_population, RDFS.subPropertyOf, SDMX_MES.obsValue))

    return [mean_population]


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
    dataset = NSR.Population_2021
    cube.add((dataset, RDF.type, QB.DataSet))
    cube.add((dataset, RDFS.label, Literal("Obyvatelé okresy 2021", lang="cs")))
    cube.add((dataset, RDFS.label, Literal("Population 2021", lang="en")))
    cube.add((dataset, QB.structure, structure))
    cube.add((dataset, DCTERMS.issued, Literal(datetime.date.today().isoformat(), datatype=XSD.date)))
    cube.add((dataset, DCTERMS.modified, Literal(datetime.date.today().isoformat(), datatype=XSD.date)))

    cube.add((dataset, DCTERMS.publisher, Literal("https://github.com/DuongXuanAnh", datatype=XSD.anyURI)))
    cube.add((dataset,DCTERMS.license,Literal("https://github.com/DuongXuanAnh", datatype=XSD.anyURI))
    )

    return dataset


def get_county_name_from_code(code, codelist):
    matching_rows = codelist[codelist["CHODNOTA2"] == code]
    if matching_rows.empty:
        return None
    else:
        return matching_rows.iloc[0]["CHODNOTA1"]


def create_resources(cube: Graph, data, codelist):
    for _, row in data.iterrows():
        code = get_county_name_from_code(row.vuzemi_kod, codelist)
        cube.add((NSR[code], RDF.type, NS.county))
        cube.add((NSR[code], SKOS.prefLabel, Literal(row.vuzemi_txt, lang="cs")))


    krajCode_kraj = load_data("CareProviders/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv")[["Kraj", "KrajCode"]]
    for _, row in krajCode_kraj.drop_duplicates().dropna().iterrows():
        region = row["KrajCode"]
        cube.add((NSR[region], RDF.type, NS.region))
        cube.add((NSR[region], SKOS.prefLabel, Literal(row["Kraj"], lang="cs")))


def create_observations(cube: Graph, dataset, data, codelist):
    relevant_code = create_relevant_code()
    for index, row in data.iterrows():
        resource = NSR["observation-" + str(index).zfill(4)]
        create_observation(cube, dataset, resource, row, relevant_code, codelist)

def create_relevant_code():
    relevant_code = {}
    krajCode_krajOkres = load_data("CareProviders/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv")[["KrajCode", "OkresCode"]]
    for _, row in krajCode_krajOkres.drop_duplicates().dropna().iterrows():
        relevant_code[row["OkresCode"]] = row["KrajCode"]
    return relevant_code

def create_observation(cube: Graph, dataset, resource, row, relevant_code, codelist):
    cube.add((resource, RDF.type, QB.Observation))
    cube.add((resource, QB.dataSet, dataset))
    cube.add((resource, QB.dataSet, dataset))

    county = get_county_name_from_code(row.vuzemi_kod, codelist)
    cube.add((resource, NS.county, NSR[county]))
    cube.add((resource, NS.region, NSR[relevant_code[county]]))

    cube.add((resource, NS.mean_population, Literal(row.hodnota, datatype=XSD.integer)))


if __name__ == "__main__":
    main()