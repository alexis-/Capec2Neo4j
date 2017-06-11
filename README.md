[![](https://github.com/alexis-/Capec2Neo4j/raw/master/capec2neo4j.png)](https://github.com/alexis-/Capec2Neo4j/raw/master/capec2neo4j.png)

# Capec2Neo4j
[Neo4j](https://neo4j.com/) graph for [CAPEC](https://capec.mitre.org/) data.

- Converts CAPEC XML data into cypher scripts
- Partial implementation of CAPEC v2.10 data (about 60%)
- Based on [Xml2Cypher](https://github.com/alexis-/Xml2Cypher)

### Usage

To generate the scripts yourself:
- Download and follow instructions at [Xml2Cypher](https://github.com/alexis-/Xml2Cypher),
- Download Capec2Neo4j,
- Run ```python Capec2Neo4j.py```

Alternatively:
- Download pre-generated scripts from the [output](/output) directory,
- Import in Neo4j using ```neo4j-shell -file <file>```
