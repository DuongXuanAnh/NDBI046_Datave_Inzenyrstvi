
## First Assignment: Data Cube

-   Care providers
-   Population
## Data Cube: Care Providers

## Poskytovatelé zdravotních služeb

-   Dimension: county (okres)
-   Dimension: region (kraj)
-   Dimension: field of care (obor péče)
-   Measure: number of care providers (počet poskytovatelů péče)

----------

-   [Národní registr poskytovatelů zdravotních služeb](https://data.gov.cz/datov%C3%A1-sada?iri=https://data.gov.cz/zdroj/datov%C3%A9-sady/https---opendata.mzcr.cz-api-3-action-package_show-id-nrpzs)
-   Národní registr poskytovatelů zdravotních služeb  [schema](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv.schema.json)

----------

-   county - CountyCode
-   region - RegionCode
-   field of care - FieldOfCare
-   measure : count number of providers

## Data Cube: Population 2021

## Obyvatelé okresy 2021

-   Dimension: county (okres)
-   Dimension: region (kraj)
-   Measure: mean population (střední stav obyvatel)

----------

-   [Pohyb obyvatel za ČR, kraje, okresy, SO ORP a obce - rok 2021](https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F12032e1445fd74fa08da79b14137fc29)
-   Pohyb obyvatel za ČR, kraje, okresy, SO ORP a obce - rok 2021  [schema](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/pohyb-obyvatel-2021.csv.schema.json)

----------

-   county - 'vuzemi_cis' == 101
-   region - 'vuzemi_cis' == 100
-   measure : mean population where 'vuk' == 'DEM0004'

We need to convert the codes for county (101) and region (100) to NUTS from the first data cube (109). Use [County codelist](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/%C4%8D%C3%ADseln%C3%ADk-okres%C5%AF-vazba-101-nad%C5%99%C3%ADzen%C3%BD.csv).

```
"CS","Editační vazba","OKRES_LAU",109,"CZ0100","Praha","OKRES_NUTS",101,"40924","Praha"
```

This line map (109) CZ0100 to (101) 40924.
