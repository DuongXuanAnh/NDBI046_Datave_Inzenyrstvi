import pandas as pd
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SKOS, OWL, QB, RDF, SKOS
from pandas.errors import SettingWithCopyWarning
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

NSR = Namespace("https://DuongXuanAnh.github.io/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SDMX_CODE = Namespace("http://purl.org/linked-data/sdmx/2009/code#")


class County:
    def __init__(self, code, name, region_code):
        self.code = code
        self.name = name
        self.region_code = region_code


class Region:
    def __init__(self, code, name):
        self.code = code
        self.name = name


def load_csv_file(file_path: str):
    result = pd.read_csv(file_path, low_memory=False)
    result = result.loc[result["vuk"] == "DEM0004"]  # mean population data only
    return result


def set_region_per_county(data: pd.DataFrame):
    result = data.loc[data.vuzemi_cis == 101]

    care_providers_df = pd.read_csv("data/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv",
                                    usecols=["Kraj", "KrajCode", "OkresCode"])
    care_providers_df = care_providers_df.drop_duplicates(["OkresCode"]).dropna(subset=["OkresCode"])

    county_mapping_df = pd.read_csv("data/číselník-okresů-vazba-101-nadřízený.csv", usecols=["CHODNOTA1", "CHODNOTA2"])

    okres_lau_map = county_mapping_df.set_index('CHODNOTA2')['CHODNOTA1'].to_dict()
    kraj_kod_map = care_providers_df.set_index('OkresCode')['KrajCode'].to_dict()
    kraj_txt_map = care_providers_df.set_index('OkresCode')['Kraj'].to_dict()

    result["okres_lau"] = result["vuzemi_kod"].map(okres_lau_map)
    result["kraj_kod"] = result["okres_lau"].map(kraj_kod_map)
    result["kraj_txt"] = result["okres_lau"].map(kraj_txt_map)

    return result



def data_handle(data):
    result = Graph(bind_namespaces="rdflib")

    create_concept_schemes(result)
    create_resource_classes(result)
    create_resources(result, data)

    return result


def create_concept_schemes(collector: Graph):
    county = NSR.county
    collector.add((county, RDF.type, SKOS.ConceptScheme))
    collector.add((county, RDFS.label, Literal("Okres", lang="cs")))
    collector.add((county, RDFS.label, Literal("County", lang="en")))
    collector.add((county, SKOS.prefLabel, Literal("Okres", lang="cs")))
    collector.add((county, SKOS.prefLabel, Literal("County", lang="en")))
    collector.add((county, RDFS.range, NSR.County))
    collector.add((county, QB.codeList, NSR.County))


    region = NSR.region
    collector.add((region, RDF.type, SKOS.ConceptScheme))
    collector.add((region, RDFS.label, Literal("Kraj", lang="cs")))
    collector.add((region, RDFS.label, Literal("Region", lang="en")))
    collector.add((region, SKOS.prefLabel, Literal("Kraj", lang="cs")))
    collector.add((region, SKOS.prefLabel, Literal("Region", lang="en")))
    collector.add((region, RDFS.range, NSR.Region))
    collector.add((region, QB.codeList, NSR.Region))


def create_resource_classes(collector: Graph):

    def add_attributes(entity, entity_type, label, pref_label, code_list=None, subclass_of=None):
        collector.add((entity, RDF.type, RDFS.Class))
        collector.add((entity, RDF.type, OWL.Class))
        collector.add((entity, RDFS.label, Literal(label, lang="cs")))
        collector.add((entity, RDFS.label, Literal(pref_label, lang="en")))
        collector.add((entity, SKOS.prefLabel, Literal(label, lang="cs")))
        collector.add((entity, SKOS.prefLabel, Literal(pref_label, lang="en")))
        if code_list:
            collector.add((entity, QB.codeList, code_list))
        if subclass_of:
            collector.add((entity, RDFS.subClassOf, subclass_of))

    country = NSR.Country
    add_attributes(country, NSR.Country, "Krajina", "Country")

    county = NSR.County
    add_attributes(county, NSR.County, "Okres", "County", NSR.county, country)
    collector.add((county, RDFS.range, NSR.County))

    region = NSR.Region
    add_attributes(region, NSR.Region, "Kraj", "Region", NSR.region, country)



def create_resources(collector: Graph, data: pd.DataFrame):

    def add_attributes(entity, entity_type, label, in_scheme, notation, match=None):
        collector.add((entity, RDF.type, SKOS.Concept))
        collector.add((entity, RDF.type, SDMX_CODE.Area))
        collector.add((entity, RDF.type, entity_type))
        collector.add((entity, RDFS.label, Literal(label, lang="cs")))
        collector.add((entity, SKOS.prefLabel, Literal(label, lang="cs")))
        collector.add((entity, SKOS.inScheme, in_scheme))
        collector.add((entity, SKOS.inScheme, SDMX_CODE.area))
        collector.add((entity, SKOS.notation, Literal(notation)))
        if match:
            collector.add((entity, SKOS.narrowMatch, match))

    for _, c in data.iterrows():
        county = NSR[f"county/{c['okres_lau']}"]
        add_attributes(county, NSR.County, c["vuzemi_txt"], NSR.county, c["okres_lau"], NSR[f"region/{c['kraj_kod']}"])

    regions = data.drop_duplicates("kraj_kod")
    for _, r in regions.iterrows():
        region = NSR[f"region/{r['kraj_kod']}"]
        add_attributes(region, NSR.Region, r["kraj_txt"], NSR.region, r["kraj_kod"])
        collector.add((region, SKOS.broader, NSR["country/CZ"]))



def main():
    data = load_csv_file("data/130141-22data2021.csv")
    data = set_region_per_county(data)
    collector = data_handle(data)
    collector.serialize("./output/RegionCodeList.ttl", format="turtle")


if __name__ == "__main__":
    main()