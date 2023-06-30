# **SoMeSci**: **So**ftware **Me**ntions in **Sci**entific Articles

SoMeSci is a manually labelled corpus of Software Mentions in scientific articles.
Overall, it contains 3756 software annotations in 1367 articles.
Moreover, additional information (version, extension, release, developer, url, license, citation, abbreviation, alternative name) associated with the software is annotated and linked to the software by relations. 
For an exact configuration of the annotation take a look in the `conf` folder. 
Annotated texts are given as BRAT stand-off format in `PLoS_methods`, `PLoS_sentences`, `Pubmed_fulltext`, and `Creation_sentences`. 
All annotations of software, citations, developers, and licenses are also linked through provided unique identifiers in the folder `Linking`. 

For further information on how to work with the data visit [SoMeSci_Code](https://github.com/dave-s477/SoMeSci_Code) and [SoMeNLP](https://github.com/dave-s477/SoMeNLP) or have a look at the website including an interactive SPARQL Endpoint: https://data.gesis.org/somesci

## Formal Citation Extension

The original SoMeSci data was further extended to cover formal citations, with the folder `Formal_Citation` containing the corresponding data. 

The file `software_citation_type_annotation.csv` contains information on referenced resources for all formal citations connected to in-text software. 
The file `software_citation_type_annotation_without_intext_mention` contains further formal software citations that are not connected to in-text software mentions, which were identified by analyzing all existing references in the sets. 
`original_data_matching.csv` contains information necessary to match the formal citation annotations to the original SoMeSci data. 
`creation_file_list.csv` and `fulltext_and_methods_list.csv` are simple file lists summarizing all articles contained in specific SoMeSci subsets, which are useful for specific analyses.
The folder `data_accurracy_annotation` contains annotations for data quality, regarding completeness, publisher, and database representation by Crossref and Semantic Scholar. 
The files `ìnfo_summary_*.csv` summarize this annotation, and can be generated with the script `analyze_completeness.py`. 
The file `software_article_reference_availability.csv` contains information on how often software articles, cited same as regular articles are missing from bibliographic databases. 
Lastly, `software_sparql.csv` contains a summary of the original data, which was obtained by running the following query on the [SPARQL Endpoint](https://data.gesis.org/somesci): 
```
PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>
PREFIX sms: <http://data.gesis.org/somesci/>
PREFIX its: <http://www.w3.org/2005/11/its/rdf#>

SELECT ?sw_identity ?spelling ?article ?ver_string ?dev_string ?cit_string ?url_string ?ext_string ?rel_string ?lic_string ?abb_string ?alt_string
WHERE{
	?sw_phrase a nif:Phrase .
	?sw_phrase its:taClassRef [ rdfs:subClassOf sms:Software ] .
	?sw_phrase its:taIdentRef ?sw_identity .
	?sw_phrase nif:anchorOf ?spelling .
    ?sw_phrase nif:referenceContext ?sentence .
    ?sentence nif:broaderContext ?article .
    OPTIONAL{
	    ?sw_phrase sms:referredToByVersion ?ver .
        ?ver nif:anchorOf ?ver_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByDeveloper ?dev .
        ?dev nif:anchorOf ?dev_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByCitation ?cit .
        ?cit nif:anchorOf ?cit_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByURL ?url .
        ?url nif:anchorOf ?url_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByRelease ?rel .
        ?rel nif:anchorOf ?rel_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByExtension ?ext .
        ?ext nif:anchorOf ?ext_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByLicense ?lic .
        ?lic nif:anchorOf ?lic_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByAbbreviation ?abb .
        ?abb nif:anchorOf ?abb_string
	}
OPTIONAL{
	    ?sw_phrase sms:referredToByAlternativeName ?alt .
        ?alt nif:anchorOf ?alt_string
	}
}
```
Note that this file contains more entries than software is contained in SoMeSci because a single software can have more than one meta-data per type associated to it, which needs to be taken into account when utilizing it for analyses. 

For further information on how to work with the formal citation data visit [SoMeSci_Citation](https://github.com/dave-s477/SoMeSci_Citation).

The corresponding data is also available through [Zenodo](https://doi.org/10.5281/zenodo.4968738).

[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
