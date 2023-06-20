---
title: 'Come and get your grant metadata!'
author: Rachael Lammey
draft: false
authors:
  - Rachael Lammey
  - Jennifer Kemp
date: 2021-11-08
categories:
  - Research Funders
  - Metadata
  - Grants
  - Infrastructure
Archives:
  - 2021
---

**Tl;dr**: Metadata for the (currently 26,000) grants that have been registered by our funder members is now available via the REST API. This is quite a milestone in our program to include funding in Crossref infrastructure and a step forward in our mission to connect all.the.things. This post gives you all the queries you might need to satisfy your curiosity and start to see what's possible with deeper analysis. So have the look and see what useful things you can discover.

## How it started

Back in 2017 we posted the outcomes of some discussions with a [newly-reformed Funder Advisory Group](/working-groups/funders/), [plotting Crossref's path](/blog/global-persistent-identifiers-for-grants-awards-and-facilities/). In 2018, [Wellcome described their rationale for supporting the grants effort](/blog/wellcome-explains-the-benefits-of-developing-an-open-and-global-grant-identifier/) with the help of Europe PMC, and in 2019 the sub-groups of the Advisory Board put out [a call for feedback on the metadata plan](/blog/request-for-feedback-on-grant-identifier-metadata/) as the fee model they created was also approved by our board.

Since late 2019, research funders have been registering metadata and identifiers for their grants with us. We currently have a healthy 26k grants registered with us, via 13 funding organisations. I’d specifically highlight Wellcome for volume ([registering via Europe PMC](http://blog.europepmc.org/2020/06/global-grant-ids-in-europe-pmc.html)), and the Australian Research Data Commons (ARDC) who was the first funder that included ROR IDs in their grant metadata, really getting the value of connecting all related entities and contributors.

The reasons for registering grants with Crossref? Let's recap:

* Support of open data and information about grants
* Streamlined discovery of funded content
* Improved analytics and data quality
* More complete picture of outputs and impact
* Better value from investments in reporting services
* Improved timeliness, completeness and accuracy of reporting: save time for researchers
* More complete information to support analysis and evaluation without relying on manual data entry

{{< figure src="/images/blog/2021/funder-visual.png" width="75%" >}}

## How it's going

For grant information to be used, it’s key that it is is openly available and disseminated as widely as possible. That work starts with funders registering their grants, and continues with us. Now that we’ve completed the REST API's [Elasticsearch migration](/blog/behind-the-scenes-improvements-to-the-rest-api/), we’re happy to announce that all our grant information is now available via our REST API.

Here’s a snippet of the kind of metadata you can see related to the grants registered with us. This is information related to grant record [https://doi.org/10.35802/218300](https://doi.org/10.35802/218300), found using [this request (https://api.crossref.org/works/10.35802/218300)](https://api.crossref.org/works/10.35802/218300) which you can use to see the full metadata record:

``` JSON
"publisher": "Wellcome",
"award": "107769",
"DOI": "10.35802/107769",
"type": "grant",
"created": {
"date-parts": [
[
2019,
9,
25
]
],
"date-time": "2019-09-25T07:17:20Z",
"timestamp": 1569395840000
},
"source": "Crossref",
"prefix": "10.35802",
"member": "13928",
"project": [
{
"project-title": [
{
"title": "Initiative to Develop African Research Leaders (IDeAL)"
}
],
"project-description": [
{
"description": "Research is key in tackling the heath challenges that Africa faces. In KWTRP we have been committed to building sustainable capacity alongside an active and diverse research programme covering social science, health services research, epidemiology, laboratory science including molecular biology and bioinformatics. Our strategy has been successful in delivering high quality PhD training, leveraging individual funding and programme funding in order to place students in productive groups and provide high quality supervision and mentorship. Here we plan to consolidate and build on these outputs to address long-term sustainability. We will emphasise the full career path needed to generate research leaders. KWTRP aims to address capacity building for research through an initiative that employs a progressive and long term outlook in the development of local research leadership. The overall aim of the \"Initiative to Develop African Research Leaders\" (IDeAL) is to build a critical mass of African researchers who are technically proficient as scientists and well-equipped to independently lead science at international level, able to engage with funders, policy makers and governments, and to act as supervisors and mentors for the next generation of researchers.",
"language": "en"
},
```

If you dig in, you can see information about the project, investigators (including their ORCID iDs), the funder, award type, amount, description of the grant, and a link to the public page showing information about the grant. More information on the required and optional fields is available in our [grants markup guide](/documentation/content-registration/content-type-markup-guide/grants/).

Here are some examples of the kind of things you can now ask:

#### Show me who is registering grants:

[https://api.crossref.org/types/grant/works?rows=0&facet=funder-name:*](https://api.crossref.org/types/grant/works?rows=0&facet=funder-name:*)  

#### Show me all of the grants registered by Wellcome:
<a href="https://api.crossref.org/works?query.funder-name=Wellcome&filter=type:grant">https://api.crossref.org/works?query.funder-name=Wellcome&filter=type:grant</a>  

#### Show me all of the grants associated with the investigator name Caldas:
<a href="https://api.crossref.org/works?query.contributor=Caldas&filter=type:grant">https://api.crossref.org/works?query.contributor=Caldas&filter=type:grant</a>  

And bibliographic queries finding entries in...

#### Award number:
<a href="https://api.crossref.org/works?query.bibliographic=7196&filter=type:grant">https://api.crossref.org/works?query.bibliographic=7196&filter=type:grant</a>   

#### Project title:
<a href="https://api.crossref.org/works?query.bibliographic=RIZ1&filter=type:grant">https://api.crossref.org/works?query.bibliographic=RIZ1&filter=type:grant</a>

## More to do

This is a milestone but it's not the end of the story. We have more to add relationships, encourage the use of this metadata amongst publishers and their platforms, and to add grant records to our tools such as Participation Reports and Metadata Search. But in the meantime, feel free to [get in touch](/contact) if you have queries about registering grants with us or about using the related metadata in your tools and services.

This information will grow over time as more funders join Crossref and add their grant metadata and as more analyses is possible. We're looking forward to the next steps!
