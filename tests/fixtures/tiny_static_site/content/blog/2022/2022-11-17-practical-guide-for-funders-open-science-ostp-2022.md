---
title: 'How funding agencies can meet OSTP (and Open Science) guidance using existing open infrastructure'
author: Ed Pentz
draft: false
authors:
  - Ed Pentz
  - Ginny Hendricks
date: 2022-11-17
categories:
  - Research Nexus
  - Research Funders
  - Grants
  - Metadata
  - Identifiers
  - Community
archives:
    - 2022
---

In August 2022, the United States Office of Science and Technology Policy (OSTP) issued a [memo (PDF)](https://www.whitehouse.gov/wp-content/uploads/2022/08/08-2022-OSTP-Public-Access-Memo.pdf) on ensuring free, immediate, and equitable access to federally funded research (a.k.a. the “Nelson memo”). Crossref is particularly interested in and relevant for the areas of this guidance that cover metadata and persistent identifiers—and the infrastructure and services that make them useful. 

Funding bodies worldwide are increasingly involved in research infrastructure for dissemination and discovery. While this post does respond to the OSTP guidelines point-by-point, the information here applies to all funding bodies in all countries. It will be equally useful for publishers and other systems that operate in the scholarly research ecosystem.

In response to calls from our community for more specifics, this post:

1. Provides an overview of the specific ways that Crossref (along with organisations and initiatives like [DataCite](https://datacite.org/), [ORCID](https://orcid.org/), and [ROR](https://ror.org/)) helps U.S. federal agencies---and indeed any other funder---meet critical aspects of the recommendations.
2. Restates our intent to collaborate with all stakeholders in the scholarly research ecosystem, including the OSTP, the US federal agencies, our existing funder, publisher, and university members, to support the recommendation as plans develop.
3. References the [work and adoption of Crossref Grant DOIs](/categories/grants), including analyses of existing metadata matching funding to outputs.
4. Highlights that what’s outlined in the memo aligns with our longstanding mission to capture and maintain the scholarly record and our vision of the Research Nexus, as we describe in our current blog series, regarding our [role in preserving the integrity of the scholarly record (ISR)](/blog/isr-part-one-what-is-our-role-in-preserving-the-integrity-of-the-scholarly-record/).


## Infrastructure already exists to support funder goals; it just needs more adoption

Ensuring free, immediate, and equitable access to metadata that captures the scholarly record is an essential part of meeting the aims of the memo but also supporting Open Science globally. 

In September, Crossref ORCID, DataCite, and ROR participated in the [2022 Forum on Global Grants Management](https://altum.com/forum-on-grants-management/) run by Altum and the summary provides a good example of the importance of open infrastructure and open metadata to the goals of Open Science:

{{% divwrap blue-highlight %}}

Open Science begins with open infrastructure: Attendees agreed that Open Science relies on many other 'opens’ – most notably, open metadata, open infrastructure, and open governance. Metadata and DOIs (digital object identifiers) for publications, grants, and research outputs, are essential to illuminate the connections that exist between funding and outcomes. That metadata runs on infrastructure powered by organizations such as Crossref, ORCID, ROR, and DataCite.  

{{% /divwrap %}}

As a foundational scholarly infrastructure committed to meeting the [Principles of Open Scholarly Infrastructure (POSI)](https://openscholarlyinfrastructure.org/) of governance, insurance, and sustainability, Crossref plays an essential role in implementing and supporting key aspects of the guidance. For many years, we have been focused on the integrity of the scholarly record (ISR), and the shared vision to collectively achieve what we call the [Research Nexus](/documentation/research-nexus/), which is described as

 > A rich and reusable open network of relationships connecting research organisations, people, things, and actions; a scholarly record that the global community can build on forever, for the benefit of society.

Metadata---including persistent identifiers and relationships between different research objects---is the foundation of the Research Nexus and is critical to openly and sustainably fulfilling the OSTP memo's recommendations. 

This topic of open metadata and identifiers isn’t just an issue for research resulting from US federal funding. We are working to implement open scholarly infrastructure globally, bringing significant benefits to the whole scholarly research ecosystem. 

The current situation brings to mind the William Gibson quote, “[The future is already here - it’s just not evenly distributed yet](https://quoteinvestigator.com/2012/01/24/future-has-arrived/)”. Much of the open infrastructure to support the identifier, metadata and reporting requirements of the OSTP memo already exists, but it is unevenly implemented. Increased collaboration and effort will be needed to bring this all to fruition. 

We set out below some steps that all stakeholders can take to meet not just the OSTP guidelines, but Open Science goals more broadly, and globally.


## What does ‘adoption’ look like? How exactly do funders and other stakeholders work with this infrastructure?

The OSTP memo calls for specific actions concerning metadata and identifiers where, fortunately, open and global solutions already exist. 

For example, item 4 a) says, “_Collect and make publicly available appropriate metadata associated with scholarly publications and data resulting from federally funded research._” Crossref and DataCite make metadata, including persistent identifiers (DOIs to be specific), openly available for a broad range of research objects from [publications](https://search.crossref.org/) to [data](https://search.datacite.org/). Item 4 b) reads, “_Assign unique digital persistent identifiers to all scientific research and development awards and intramural research protocols_”. Again, federal agencies and other funders are already [joining](/community/grants/) to register awards and grants and [distribute these records openly](/blog/come-and-get-your-grant-metadata) through Crossref. However, this is an example of uneven adoption as registering awards and grants with DOIs is only being done by a few funders so far, which needs to increase. 

#### Here is an ideal workflow that funders and publishers can already follow

1. Funders join Crossref to register grants and awards (or indeed any other object such as reports). They apply on our website, accept our terms, and provide key information such as contact details. An annual membership fee ranges from $200-$1200 USD.
2. Funders and publishers collect ROR IDs and authenticated ORCID iDs for all authors/awardees and their affiliations.
3. Funders register a Crossref DOI for the award/grant, including awardees’ ORCID iDs and ROR IDs. They send us XML information about the grant (note that we will imminently release an online form to make it easier for the less technical funders). Many funder members register the metadata through a third party, such as Altum (if they use ProposalCentral) or Europe PMC.
4. At the same time, funders update the awardees’ ORCID record directly with the Crossref Grant DOI and metadata.
5. Grantees produce research objects and outputs such as data, protocols, code, preprints, articles, conference papers, book chapters, etc. 
6. These objects are registered with Crossref or DataCite, and DOIs are created by the publisher or repository members who include ORCID iDs, Crossref Grant DOIs (gathered from the author), ROR IDs for affiliations for all contributors, and other key metadata such as licensing information, and in the case of publications - references and abstracts. Note that the publisher works its magic (actually, publishers do a lot of editorial and production work, such as including data citations in the references using DataCite DOIs for the data in data repositories). 
7. On the Crossref side, we do a bunch of processing and matching and are planning to refine this and do more. Sometimes relationships are notified and added, such as data citation, preprints related to articles or funding acknowledgements converted from free text to [Open Funder Registry IDs](/services/funder-registry/) and names.
8. Grant records with Crossref DOIs are now part of the scholarly record. All stakeholders may retrieve the open metadata and relationships through our public APIs. Crossref and DataCite will always provide open metadata, as safeguarded by our respective commitments to POSI.

{{% divwrap blue-highlight %}}

Anyone can use the open metadata registered with Crossref, DataCite and ORCID as connections have been established between (ideally all) research objects and entities through open metadata and identifiers. This means that:

* Funding agencies can monitor compliance with their policies 
* Publishers can identify the funder and meet their requirements
* Funding agencies can assess and report on the reach and return of their funding programs
* The provenance and integrity of the scholarly record is preserved and discoverable, benefitting all stakeholders.

{{% /divwrap %}}


## Suggestions for meeting OSTP and Open Science guidance, point by point


<table>
  <tr>
   <td><strong>OSTP Recommendation</strong>
   </td>
   <td><strong>Publishers should…</strong>
   </td>
   <td><strong>Funding agencies should…</strong>
   </td>
  </tr>
  <tr>
   <td>4 a) Collect and make publicly available appropriate metadata associated with scholarly publications and data resulting from federally funded research
   </td>
   <td>
<ul>

<li>For scholarly publications: register comprehensive metadata & DOIs with Crossref.

<li>For scholarly data: register comprehensive metadata and DOIs with DataCite.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Use Crossref’s API to retrieve publication and other metadata.

<li>Use DataCite’s API to retrieve data/repository metadata.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>
    i) all author and co-author names, affiliations, and sources of funding, referencing digital persistent identifiers, as appropriate;
   </td>
   <td>
<ul>

<li>Collect and validate the following from authors at manuscript submission: ROR & ORCiD IDs, Crossref Grant DOIs.

<li>Include data citations in reference lists, preferably with DataCite DOIs.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Register awards and grants with Crossref and create DOI records for them.

<li>Use ORCID’s API to retrieve validated contributor metadata.

<li>Update contributors’ ORCID records with Crossref Grant DOIs and metadata.

<li>Use ROR API to retrieve and verify affiliation metadata.
    
<li>Recommend data citations be included in published outputs.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>ii) the date of publication; and,
   </td>
   <td>
<ul>

<li>Include acceptance and publication dates in Crossref metadata.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Use Crossref’s API to retrieve publication dates.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>
    iii) a unique digital persistent identifier for the research output;
   </td>
   <td>
<ul>

<li>For scholarly publications and research outputs: register full metadata & DOIs with Crossref.

<li>For scholarly data: register full metadata and DOIs with DataCite.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Use Crossref and DataCite APIs to retrieve DOIs for research outputs.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>4 b) Instruct federally funded researchers to obtain a digital persistent identifier that meets the common/core standards of a digital persistent identifier service defined in the NSPM-33 Implementation Guidance, include it in published research outputs when available, and provide federal agencies with the metadata associated with all published research outputs they produce, consistent with the law, privacy, and security considerations.
   </td>
   <td>
<ul>

<li>Collect ORCID iDs on manuscript submission for all authors.

<li>Register Crossref and DataCite DOIs and metadata for research outputs, including data.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Recommend that researchers applying for funding obtain an ORCID iD and collect them upon grant application for all applicants.

<li>Prepopulate grant applications with CV and publication information from applicants’ ORCID records.

<li>ORCID iDs should be included in the grants registered by the agencies with Crossref.

<li>Agencies can use our open APIs to retrieve the metadata on publications and data rather than ask researchers to do it, saving time and effort.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>4 c) Assign unique digital persistent identifiers to all scientific research and development awards and intramural research protocols that have appropriate metadata linking the funding agency and their awardees through their digital persistent identifiers.
   </td>
   <td>
   </td>
   <td>
<ul>

<li>Join Crossref to register Crossref Grant DOIs, including ROR IDs and ORCID iDs 

<li>Ensure grant proposal and assessment systems integrate with Crossref, ROR for affiliations and with ORCID for applicants/awardees.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 a) coordinate between federal science agencies to enhance efficiency and reduce redundancy in public access plans and policies, including as it relates to digital repository access;
   </td>
   <td>
<ul>

<li>Work with agencies to ensure a smooth, automated workflow.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Using and supporting existing open scholarly infrastructure and using open identifiers will avoid duplication of effort and make the overall ecosystem more efficient .
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 b) improve awareness of federally funded research results by all potential users and communities;
   </td>
   <td>
<ul>

<li>Collect Crossref Grant DOIs from authors and use them to link from publications to grant information.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Communicate your Crossref Grant DOIs and open grant metadata widely via human and machine interfaces. Inclusion in the Crossref API will enhance dissemination and discoverability

<li>Update contributors’ ORCID records with Crossref Grant DOIs and metadata
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 c) consider measures to reduce inequities in the publishing of, and access to, federally funded research and data, especially among individuals from underserved backgrounds and those who are early in their careers;  
   </td>
   <td>
   </td>
   <td>
<ul>

<li>Registering grants and sharing metadata through Crossref means it’s part of the world’s largest open community-governed metadata exchange and makes it available to the entire world without restriction.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 d) develop procedures and practices to reduce the burden on federally funded researchers in complying with public access requirements;
   </td>
   <td>
<ul>

<li>Ensure your systems and those you work with make it as easy as possible for authors to provide the necessary metadata and persistent identifiers - work towards as much automation as possible and pulling from other systems rather than asking for data to be re-keyed. 
</li>
</ul>
   </td>
   <td>
<ul>

<li>Ensure the platforms you work with, such as grant proposal or assessment systems, retrieve and prepopulate ROR IDs, ORCID iDs, and Crossref and DataCite DOIs and associated metadata whenever possible so that the researchers don’t have to manually rekey or reformat data.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 e) recommend standard consistent benchmarks and metrics to monitor and assess implementation and iterative improvement of public access policies over time;
   </td>
   <td>
   </td>
   <td>
<ul>

<li>Ensure that platforms and systems integrate with ROR, ORCID, Crossref, and DataCite so that this open metadata can lead to the creation of benchmarks and metrics.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 f) improve monitoring and encourage compliance with public access policies and plans;
   </td>
   <td>
<ul>

<li>Use open infrastructure to help authors easily comply with public access and funder/institution policies. Automate systems as much as possible.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Using the open infrastructure, metadata, and identifiers outlined in this post will make monitoring more straightforward and compliance easier for all stakeholders. The community can build services on open infrastructure and metadata.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 g) coordinate engagement with stakeholders, including but not limited to publishers, libraries, museums, professional societies, researchers, and other interested non-governmental parties on federal agency public access efforts;
   </td>
   <td>
<ul>

<li>Work with the global open infrastructure organisations (Crossref, DataCite and ORCID) whose members include funding agencies, societies, publishers, universities, libraries, repositories, museums, NGOs, and many other stakeholders - all looking to improve the efficiency of the research ecosystem.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Work with the global open infrastructure organisations (Crossref, DataCite and ORCID) whose members include funding agencies, societies, publishers, universities, libraries, repositories, museums, NGOs, and many other stakeholders - all looking to improve the efficiency of the research ecosystem.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 h) develop guidance on desirable characteristics of—and best practices for sharing in—online digital publication repositories;
   </td>
   <td>
<ul>

<li>Support automated systems that use metadata and identifiers to populate repositories automatically.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Collaborate with publishers, Crossref and others to develop automated systems to populate repositories.
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>5 j) develop strategies to make federally funded publications, data, and other such research outputs and their metadata are findable, accessible, interoperable, and re-useable, to the American public and the scientific community in an equitable and secure manner.
   </td>
   <td>
<ul>

<li>Provide and support a range of discovery services based on open infrastructure.
</li>
</ul>
   </td>
   <td>
<ul>

<li>Encourage discovery services - and develop services - that use the open infrastructure, metadata and persistent identifiers to enable.
</li>
</ul>
   </td>
  </tr>
</table>


## Everybody needs to play their part 

A lot of the work on making the above happen is already underway, and there is widespread adoption of open identifiers and metadata, but as noted above, funders are still early in the adoption journey, and implementation among all stakeholders is patchy. 

Critical parts of the infrastructure rely on third-party platforms that supply tools and systems to authors, funders, and publishers - so coordinating the support for the appropriate metadata and identifiers in these systems and tools is very important. 

We are emphasising how our existing open scholarly infrastructure systems are helping. But we also know that it’s not all perfect yet. Infrastructure is always evolving, metadata is never complete, refactoring workflows and systems can be costly, and integration can always be smoother. But our existing open infrastructure has already delivered significant benefits, and broader adoption will bring additional benefits to the whole scholarly research and communications ecosystem and help achieve the promise of Open Science in advancing human knowledge. 

While working on this coordination and integration, we all try to remember that it should minimise work for researchers, and processes should be as automated as possible.

Collaboration is key to making this all work. 

We already work with many funders through our [Advisory Group](/working-groups/funders), our 30 funder members, [25 of whom](https://api.crossref.org/types/grant/works?rows=0&facet=funder-name:*) have so far collectively registered around [40,000 Crossref Grant DOIs, retrievable from our open API](https://api.crossref.org/works?filter=type:grant). Some grants are even [matched](/blog/follow-the-money-or-how-to-link-grants-to-research-outputs/) to resulting outputs already, and some funders have recently dug into Crossref metadata to analyse outcomes from their investments, such as the [Dutch Research Council (NWO) which presents findings and makes a case for greater emphasis on Crossref funding metadata](https://doi.org/10.31222/osf.io/gj4hq).

We also work closely with partners [Europe PMC](http://blog.europepmc.org/2020/06/global-grant-ids-in-europe-pmc.html) and [Altum](https://altum.com/), and we engage in community research and discussion, for example, through the [Open Research Funders Group](https://www.orfg.org/). 

Alongside our fellow infrastructures and open identifier registries ORCID, DataCite, and ROR, we integrate with and support each other operationally and out in the community. 

We will continue focusing our resources and efforts on engaging with funders, including US federal agencies responding by the OSTP guidelines, and all stakeholders to support the entire global scholarly research ecosystem. 

#### Everyone has a part to play, and we must all pull together to prioritize this work. 

> Who’s in?

Please [get in touch](mailto:feedback@crossref.org) with Ed, Ginny, or Jennifer (or indeed DataCite or ORCID or ROR) if you’d like to have a discussion about the workflows described here, or just to make sure you’re up to date on the latest developments and opportunities we describe. We look forward to working with all funding agencies to support them as they develop their plans.