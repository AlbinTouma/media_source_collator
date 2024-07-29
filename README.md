<p align="center">


  <h3 align="center">📰 Cartier </h3>

  <p align="center">
    Cartier is the Adverse Media team's research tool for conducting country reviews
  </p>
</p>

<img src="hero_am.jpg">

## Overview

**Cartier** is a tool designed to assist the adverse media team conduct thorough country reviews by collating and comparing media sources against the domains covered by Comply Advantage. 



## Research Process

The research process involves identifying lists of media sources in a country and labelling those sources according to our taxonomy, and compiling a master list. 

Below is a diagram of each research step. Repeat these steps until every media source in each research sheets has a taxonomy label.

```mermaid
graph LR;

DBPedia("DBPedia scraper") --> B[Add each list of sources in its own Excel tab]
Comply("Comply Articles DB Store") --> B
GovernmentDirectory(Government sources) --> B
Other(Other scrapers) --> B
B --> Taxonomy[Label media sources according to taxonomy]
Taxonomy --> Compiler[Compile sources in a master list]
Compiler --> CountryReport{Country Report}
```


### Data Collection

We have a list of sources in comply data that we want to compare to "what's out there". Sources that can tell us what media exists in a country range from open source directories, government directories (usually press ombudsman) and DBPedia.

At the collection stage we use or build scrapers and save each list of sources in tabs on the research sheet.


### Taxonomy & Collation

We have a taxonomy of media sources. Classifying sources is a two step process. We classify sources in the different sheets, starting with the dataset that is easiest to classify. For example, media ombudsman usually lists which sources are national or regional. Once we have classified those sources, we run the collator to create a master list. 

With the help of the master list, we can filter for sources in the comply list that did not merge with sources that have a classification. These domains are then manually classified. 

The collate and classify steps are repeated until all comply sources have been labelled. 

### Merge 

As part of the process, we merge all of the sheets to create one source of truth in the master list. This is done merging on both the source's name and url and the result is combined data. 

```mermaid
graph LR;

URLs --- MATCH 

Names --- MATCH 

MATCH --- True --> merge
MATCH --- FALSE --> reject


```

**Example**

Comply data

Provider | Name | URL | Taxonomy
-----|---- | ---- | ----
comply | The Guardian | https://www.guardian.com | international newspaper

Wiki data

Provider | Name | URL | Circulation | Taxonomy
-----| -----|----|---- | -----
wikipedia | The Guardian | https://www.guardian.com | 20000 | international newspaper

Master list

Source B:

Provider | Name | URL | Circulation | Taxonomy
-----| -----|----|---- | -----
[comply, wikipedia] | The Guardian | https://www.guardian.com | 20000 | [international newspaper, international newspaper]




## Manual resolution

Throughout the classifying of sources, we often come across domains with similar names or the same name but different url. At present, we manually resolve these sources by ensuring that the name is consistent across all sheets. Upon rerunning collator, these sources are resolved. 

### Country Review Report

When the above steps are completed,  we breakdown the number of sources that Comply covers by type in a table. This table is then shared with clients along with a few examples of sources from each class.

The table is generated manually. Below the table of sources that Comply covers, the report lists domains that comply does not cover. These domains are slated for review. 




# Adverse Media Reviewer




Adverse Media country reviews aim to produce a master list of sources that Comply covers and an estimate of the sources that exist in a country. 

The result if a country report with a table of the number of sources we cover by their taxonomy type and the estimated number of sources out there. 

In addition,the report flags domains that we miss and should review and consider adding. 


## Research Process

### Data Collection

We have a list of sources in comply data that we want to compare to "what's out there". Sources that can tell us what media exists in a country range from open source directories, government directories (usually press ombudsman) and DBPedia.

At the collection stage we use or build scrapers and save each list of sources in tabs on the research sheet.


### Taxonomy & Collation

We have a taxonomy of media sources. Classifying sources is a two step process. We classify sources in the different sheets, starting with the dataset that is easiest to classify. For example, media ombudsman usually lists which sources are national or regional. Once we have classified those sources, we run the collator to create a master list. 

With the help of the master list, we can filter for sources in the comply list that did not merge with sources that have a classification. These domains are then manually classified. 

The collate and classify steps are repeated until all comply sources have been labelled. 

### Manual resolution

Throughout the classifying of sources, we often come across domains with similar names or the same name but different url. At present, we manually resolve these sources by ensuring that the name is consistent across all sheets. Upon rerunning collator, these sources are resolved. 






```mermaid
graph LR;

DBPedia("DBPedia scraper") --> B[Source lists]
Comply("Comply Articles DB Store") --> B
GovernmentDirectory(Government sources) --> B
Other(Other scrapers) --> B

B --> Taxonomy{Taxonomy} --> Label(Class sources)


Label --> Compiler{Collator}
Compiler --> Taxonomy

Compiler <--> Checks{Checks}
Checks <--> Manual[Manual resolution of soruces]
Checks <--> ParentDomain[Parent domain checker]

Compiler --> MasterList
MasterList --> CountryReport{Report}
```
