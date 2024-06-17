
``French endpoint`` to DBPedia is https://fr.dbpedia.org/sparql

Query list of newspapers in France `Presse écrite régionale en France`



```
Les Saisons d'Alsace
http://fr.dbpedia.org/resource/Les_Saisons_d'Alsace


La Presse de la Manche
https://fr.dbpedia.org/page/La_Presse_de_la_Manche
```

```yml

newspaper:
    name:
        prop-fr:nom
        rdfs:label
        foaf:name 
    
    language: dbo:language

    type: prop-fr:genre

    founded: prop-fr:dateDeFondation

    distribution: prop-fr:diffusion

    owners: prop-fr:propriétaire

    frequency: prop-fr:périodicité

    website: 
        prop-fr:site
        foaf:homepage

    region: prop-fr:ville

```



```javascript

{
    "name" {
        "prop-fr:nom": "La Presse de La Manche (fr)",
        "rdfs:label": " La Presse de la Manche (fr)",
        "foaf:name": ["(fr)", "La Presse de la Manche (fr)"],
    },
    "type": {}
}
```


type:
    prop-fr:genre: dbpedia-fr:Presse_écrite_régionale_en_France
founded:
    prop-fr:dateDeFondation: 1944-07-03 (xsd:date) 
distribution:
    prop-fr:diffusion: 20709 (xsd:integer)  
owners:
    prop-fr:propriétaire:  dbpedia-fr:Groupe_Sipa_-_Ouest-France
frequency:
    prop-fr:périodicité: quotidien                      
website:
    prop-fr:site: http://www.lapressedelamanche.fr 
    foaf:homepage: http://www.lapressedelamanche.fr
    
region:
    prop-fr:ville: dbpedia-fr:Cherbourg-en-Cotentin


```