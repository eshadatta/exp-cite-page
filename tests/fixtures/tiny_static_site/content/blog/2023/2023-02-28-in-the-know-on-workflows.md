---
title: 'In the know on workflows: The metadata user working group'
author: Jennifer Kemp
draft: false
authors:
  - Jennifer Kemp
date: 2023-02-28
categories:
  - Users
  - Metadata
  - Community
archives:
      - 2023
---

What’s in the metadata matters because it is So.Heavily.Used.

You might be tired of hearing me say it but that doesn’t make it any less true. Our open APIs now see over 1 _billion_ queries per month. The metadata is ingested, displayed and redistributed by a vast, global array of systems and services that in whole or in part are often designed to point users to relevant content.  It’s also heavily used by researchers, who author the content that is described in the metadata they analyze. It’s an interconnected supply chain of users large and small, occasional and entirely reliant on regular querying.

## Tl;dr

Crossref recently wrapped up our first [Working Group](https://www.crossref.org/working-groups/metadata-user/) for users of the metadata, a group that plays a key role in discoverability and the metadata supply chain. You can jump directly to the [stakeholder-specific recommendations](#what-are-the-recommendations) or take a moment to share your [use case](https://docs.google.com/forms/d/1bHO7gGYC-HqObkXgD5xrSUIjE-m93cTZ8Bp1RBJXgwo/edit) or [feedback](mailto:feedback@crossref.org).

## Why a metadata user group? Why now?

A majority of Crossref metadata users rely on our [free, open APIs](https://www.crossref.org/services/metadata-retrieval/) and many are anonymous. A small but growing group of users pay for a [guaranteed service level option](https://www.crossref.org/services/metadata-retrieval/metadata-plus/) and while their individual needs and feedback have long been integrated into Crossref’s work, as a group they provide a window into the workflows and use cases for the metadata of the scholarly record. As this use grows in [strategic importance](https://www.crossref.org/strategy/), to both Crossref and the wider community, it was clear that we might be overdue for a deeper dive into user workflows.

In 2021, we surveyed these subscribers for their feedback and brought together a few volunteers over a series of 5 calls to dig into a number of topics specific to regular users of metadata. This group, the first primarily non-member [working group](https://www.crossref.org/working-groups/metadata-user/) at Crossref, wrapped up in December 2022, and we are grateful for their time:

* Achraf Azhar, Centre pour la Communication Scientifique Directe (CCSD)
* Satam Choudhury, HighWire Press
* Nees Jan van Eck, CWTS-Leiden University
* Bethany Harris, Jisc
* Ajay Kumar, Nova Techset
* David Levy, Pubmill
* Bruno Ohana, biologit
* Michael Parkin, European Bioinformatics Institute (EMBL-EBI)
* Axton Pitt, Litmaps
* Dave Schott, Copyright Clearance Center (CCC)
* Stephan Stahlschmidt, German Centre for Higher Education Research and Science Studies (DZHW)

This post is intended to summarize the work we did, to highlight the role of metadata users in research communications, to provide a few ideas for future efforts and, crucially, to get your feedback on the findings and recommendations. Though this particular group set out to meet for a limited time, we hope this report helps facilitate ongoing conversations with the user community.

## Survey Highlights

If you’re looking for an easy overview of users and use cases, here’s a great starting point.

<figure><img src='/images/documentation/metadata-users-uses.png' alt='Metadata users and uses: metadata from Crossref APIs is used for a variety of purposes by many tools and services' title='' width='75%'></figure>
<button id="show-img" type="button" class="btn btn-default" data-toggle="modal" data-target="#image32">Show image</button>
<div id="image32" class="modal fade" aria-labelledby="my-modalLabel" aria-hidden="true" tabindex="-1" role="dialog">
    <div class="modal-dialog" data-dismiss="modal">
        <div class="modal-content"  >              
            <div class="modal-body">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <img src="/images/documentation/metadata-users-uses.png" class="img-responsive" style="width: 100%;">
            </div>
        </div>
    </div>
</div>  


If you interpret this graphic to mean that there is a lot of variety centered on a few high level use cases, the survey and our experiences with users certainly supports that. A few key takeaways from the 2021 survey may be useful context:

* __Frequency of use__: At least 60% of respondents query metadata on a daily basis
* __Use cases__   
  * Finding and enhancing metadata as well as using it for general discovery are all common use cases  
  * For most users, matching DOIs and citations is a common need but for a significant group, it is their primary use case
  * Analyzing the corpus for research was a consistent use case for 13% of respondents
* __Metadata of particular interest__  
  * Abstracts are the most desirable non-bibliographic metadata, followed by affiliation information, including RORs
    * Some other elements (beyond citation information) that respondents find useful are:
      * Corrections and retractions
      * [Relationship metadata](/documentation/principles-practices/best-practices/relationships/)
      * Book chapters
      * [Grant information](/blog/come-and-get-your-grant-metadata/)

NB: The survey did not ask about references but we are frequently asked why they’re not included more often.

It’s also worth noting that about a third of respondents said that correct metadata is more important to them than any particular element.

There is more to this survey that isn’t covered here but it was kept fairly short to help with the response rate. Knowing we would have some focused time to discuss issues too numerous or nuanced to reasonably address in a survey, we compiled a long list of questions and topics for the Working Group then followed up with a second, more detailed survey to kick off the meeting series.

## What we set out to address

We had three primary goals for this Working Group:

* Highlight the efforts of metadata users in enabling discovery and discoverability
* Determine direction(s) for improved engagement
* Inform the Crossref product development [roadmap](https://trello.com/b/02zsQaeA/crossref-roadmap) for [metadata retrieval services](/services/metadata-retrieval/)

Of course, everyone involved had some questions and topics of interest to cover, including (but not limited to):

* Understanding publisher workflows
* How best to introduce changes, e.g. for a high volume of updated records
* Understanding the Crossref schema
* Query efficiencies, i.e. ‘tips and tricks’ (here for the REST API)
* Which scripts, tools and/or programs are used in workflows
* What other metadata sources are used
* What kind of normalization or processing is done on ingest
* How metadata errors are handled

## What did we learn?

__Workflows__  
I started with the admittedly ambitious goal of collecting a library of workflows. After a few years of working with users, I learned never to assume what a user was doing with the metadata, why or how. For example, some subscribers use Plus snapshots (a monthly set of all records), regularly or occasionally and some don’t use them at all. Understanding why users make the choices they do is always helpful.

In my experience, workflows are frequently characterized as “set it and forget it.” It’s hard to know how often and how easily they might be adapted when, for example, a new record type like peer review reports becomes available. So, it’s worth exploring when and how to highlight to users changes that might be of interest.

 As it turned out, half the group had their workflows mostly or fully documented. The rest are partially documented, not documented at all or the availability of documentation was unknown. Helping users document their workflows, to the extent possible, should be a mutually beneficial effort to explore going forward. We're doing similar work with the aim of making ours more transparent and replicable.

 __Feedback on subscriber services__  
 User feedback might be the most obvious and directly consequential work of this group, at least for Crossref - understanding how well the services used meet their needs and what might be improved.

One frequent suggestion for improvement is faster response time on queries. This is an area we’ve focused on for some time, because refining queries to be [more efficient](/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) is often the most straightforward way to improve response times and one reason for the emphasis on workflows.

We also discussed the possibility of whether or how to notify users of changes of interest. Just defining “change” is complex since they are so frequent and may often be considered very minor. We’ve been experimenting a bit over the past few years with notifying these users in cases where we’re aware of upcoming large volumes of changes, which is sometimes the case when landing page URLs are updated due to a platform change, for example. It was incredibly useful to discuss with the group what volume of records would be a useful threshold to trigger a notification (100K if you’re curious).

But perhaps the most common feedback we get from all users is on the metadata itself and the myriad [quality issues](/blog/flies-in-your-metadata-ointment/) involved. The group spent a fair amount of time discussing how this affects their work and shared a few examples of notable concerns:

* Author name issues, e.g. ‘Anonymous’ is an option for authors but that or things like ‘n/a’ are sometimes used in surname fields
* Invalid DOIs are sometimes found in reference lists
* Garbled characters from text not rendering properly
* Affiliation information is often not included or incomplete (e.g. doesn’t include RORs)
* Inconsistencies in commonly included information, e.g. ISSNs

It’s worth noting that a common misunderstanding - not just among users -  is [what is required](/documentation/schema-library/required-recommended-elements/) in the metadata. Users nearly always expect more metadata and more consistency than is actually available. The introduction of [Participation Reports](/members/prep/) a few years ago was a very useful start to what is an ongoing discussion about the variable nature of metadata quality and completeness.

__Users in the metadata supply chain__  
A few years ago, our colleague Joe Wass used [Event Data](/services/event-data/) to put together this chart of [referrals from non-publisher sources](/blog/where-do-doi-clicks-come-from/) in 2015.  

<img src="/wp/blog/uploads/2016/05/month-top-10-filtered-domains-1.png" alt="month-top-10-filtered-domains" class="img-responsive" />   


The role of metadata users in discoverability of content is key in my view and one that often doesn’t get enough attention, especially given that the systems and services that use this information often use it to point their own users to relevant resources. And because they work so closely with the metadata, users frequently report errors and so serve as a sort of de facto quality control. So, unfortunately, the effects of incomplete or incorrect metadata on these users might be the most powerful way to highlight the need for more and better metadata.

## What are the recommendations?

In discussions with the Working Group, a few themes emerged, largely around best practices, which, by their nature, tend to be aspirational.

If you’re not already familiar with the [personas](https://metadata2020.org/resources/metadata-personas/) and [Best Practices](https://metadata2020.org/resources/metadata-practices/) and [Principles](https://metadata2020.org/resources/metadata-principles/) of Metadata 2020, that is a useful starting point (I am admittedly biased here!) and many are echoed in the following recommendations:  

__For users:__

* Document and periodically review workflows
* Report errors to members or to [Crossref support](mailto:support@crossref.org) and reflect corrections when they’re made (metadata and content)
* Understand what [is and isn’t](/documentation/schema-library/required-recommended-elements/) in the metadata
* Follow [best practices](/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) for using APIs

__For Crossref:__

* Define a set of metadata changes, e.g. to affiliations, to further the discussion around thresholds for notifying users of ‘high volumes’ of changes
* Provide an output schema.
* Continue refining the input schema to include information like preprint server name, journal article sub types (research article, review article, letter, editorial, etc.), corresponding author flags, raw funding statement texts, provenance information, etc.
* Collaborate on improving processes for reporting [metadata errors](/blog/flies-in-your-metadata-ointment/) and making corrections and enhancements

__For metadata providers (publishers, funders and their service providers):__

* Follow [Metadata 2020 Metadata Principles and Practices](https://metadata2020.org/learn-more/outcomes/)
* Consistency is important, e.g. using the same, correct relationship for preprint to VoR links for all records
  * Workarounds such as putting information into a field that is ‘close’ but not meant for it can be considered a kind of error
* Understand the roles and needs of users in amplifying your outputs
* Respond promptly to reports of metadata errors
* Whenever possible, provide PIDs (ORCID IDs, ROR IDs, etc.) in addition to (not as a substitute for) textual metadata  

## What is still unclear or unfinished?  

Honestly, a lot. We knew from the outset that the group would conclude with much more work to be done, in part because there is so much variety under the umbrella of metadata users and many answers lead to more questions and in part because the metadata and the user community will continue to evolve. Even without a standing group that meets regularly, it’s very much an ongoing conversation and we invite you to join it.

## Now it’s your turn–can you help fill in the blanks?  

Does any or all of this resonate with you? Do you take exception to any of it? Do you have suggestions for continuing the conversation?

Specifically, can you help fill in any of the literal blanks? We've prepared a [short survey](https://docs.google.com/forms/d/1bHO7gGYC-HqObkXgD5xrSUIjE-m93cTZ8Bp1RBJXgwo/edit) that we hope can serve as a template for collecting (anonymous) workflows. Please take just a few minutes to answer a few short questions such as how often you query for metadata.


If you are willing to share examples of your queries or have questions or further comments, please [get in touch](mailto:feedback@crossref.org).
