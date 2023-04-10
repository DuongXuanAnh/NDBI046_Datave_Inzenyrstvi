# What?

Create provenance document using PROV-O. The document must contain following.

Save the provenance as RDF TriG file.
Employ resources from first assignment.
Include prov:Entity - for each dataset / digital artefact.
Use IRI of the Data Cube for prov:Entity.
Include prov:Activity - there must be at least one Activity.
Include prov:Agent - at least two (person and script/software).
Include prov:qualifiedUsage/prov:qualifiedAssociation/...
Use at least one of the qualified properties.
Define and use custom roles.
Make sure the file is valid!

## System requirements


 - Python3 (>=3.10)

 - Modules in requirements.txt

 - Internet connection (to download dependencies and datasets)

## Installation instructions

 - Clone repository

 - pip install .

 - Run the program
   - careProvidesProvenance.py -> careProvidersProvenance.trig
   - populationProvenance.py -> populationProvenance.trig
