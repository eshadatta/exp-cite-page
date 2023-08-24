---
title: 'Metadata connects the global community – summary of our Community update 2023'
author: Kornelia Korzec
draft: false

authors:
  - Kornelia Korzec
date: 2023-05-12
categories:
  - Metadata
  - Community

Archives:
  - 2023
---

We were delighted to engage with over 200 community members in our latest Community update calls. We aimed to present a diverse selection of highlights on our progress and discuss your questions about participating in the Research Nexus. For those who didn’t get a chance to join us, I’ll briefly summarise the content of the sessions here and I invite you to join the conversations on the Community Forum. 

You can take a look at the slides here and the recordings of the calls are available [here](https://zenodo.org/record/7921925#.ZFzh3OzMKrc). 

### TL;DR

* The membership is growing, including that in the GEM programme countries, and we focus on adding new Sponsors in areas where we have insufficient coverage to support prospective members
* The grant registration form is available for funders who don’t use XML, and we’re working to expand to other content types
* The preview of the Relationship API endpoint is available – start exploring relationships between different records and record types, from citations to funding, and more
* Usefulness of metadata records for inferring integrity of the content or publisher relies on all members of the community contributing to this effort. Crossref will continue to enrich our schema to capture new types of relevant information and to promote the best metadata practices. 
* Cited-by is now open for everyone to use 🎉 – no need for additional authorisation steps – **Registering your references will have even greater impact now!**
* The Labs participation report is available and it’s been a hit. Please note that this tool is still underdevelopment – new functionalities can be added but there might also be bugs that we are yet to resolve, so don’t hold off with feedback.
* We’ve received close to 1,000 responses in our first ever Metadata Priorities Survey. It’s still open until 18th of May and we encourage all members to take it. So far we’ve learnt that majority of our respondents are keen to deposit as much metadata as possible – and some would like to register more than we currently enable. 

### Metadata completeness and integrity
A key theme of the call was encouraging greater participation in the Research Nexus and the importance of complete metadata. One particular benefit of a rich and transparent metadata network is the opportunity to infer judgments on the integrity of the scholarly record (ISR). Amanda Bartell, Head of Member Experience, highlighted that the community agrees that availability of information about relationships between research outputs, institutions and other elements of the scholarly ecosystem together provide essential context for deciding about trustworthiness of organisations and their published content. Conversely, it can make it harder for parties to pass off information as trustworthy when that context is missing. Amanda summarised community feedback related to Crossref’s role in the integrity of the scholarly record in [her recent blog post](/blog/isr-part-four-working-together-as-a-community-to-preserve-the-integrity-of-the-scholarly-record/). 

Our members can contribute to that rich network of relationships by curating their metadata and providing contextual information – especially the highly sought for elements highlighted in the presentation.

{{< figure src="/images/blog/2023/help-context.png" alt="Screenshot of slide how can you help start adding text" width="75%">}}


### Our community
Since LIVE22, we have had 1,130 new members join us. That includes 51 organisations from countries included in our Global Equitable Membership (GEM) programme. You can find out more in [the latest news about the programme on our Community Forum](https://community.crossref.org/t/global-equitable-membership-gem-program-update/3518) from Susan Collins, Community Engagement Manager. 

We see great opportunities with enriching our metadata corpus with works carried out in some of the least economically-advantaged regions of the world. Registering their content with us will increase its discoverability for the global scholarship, while adding important relationships into the Research Nexus. We’re glad at the new members joining us under the auspices of the Global Equitable Membership (GEM) programme and we’re reaching out to existing and new communities with our Ambassadors, to encourage more metadata registrations.

Our Sponsors and Ambassadors, alongside our Outreach and Membership Team, support members to participate as effectively as possible in the Research Nexus. We’re delighted to see both programmes growing, with eight new Sponsors and seven new Ambassadors having joined us since October. 

Simultaneously, we’re working with like-minded organisations to provide useful resources for the growing and changing scholarly communications community. The recent launch of the online forum for new publishers seeking to learn about best practices in the industry, [The PLACE](https://theplace.discourse.group/), is another way in which we hope to support wider participation in the Research Nexus, and promote open and sustainable practices. 

With our growing community, there’s always interest in We have planned [a webinar](/events/) later this month to provide an overview of Crossref – including the members benefits and obligations, and how to use our services. 

### Service news 

References metadata is essential for connecting works with one another. It enables provision of citation information, aids discoverability for researchers, as well as assessment and evaluation for institutions and funders. It’s almost a year since all the references metadata deposited with Crossref has been made openly available. At the moment, 52.0% of journal articles, and 44.5% of all works have references. Martyn Rittman, Product Manager for the Cited-by service says “It’s not bad, but we can do better!” 

With three different mechanisms for doing it available to our members, we hope that all have a suitable tool to fit with their needs. You can register references with XML via HTTPS POST (structured or unstructured), with the dedicated OJS Plugin if you’re an OJS user, or with our Simple Text Query (unstructured text) – this is especially relevant to the Web Deposit Form users. We find that journal articles with deposited references seem to be cited more than those without, and by a lot: 21.8 vs. 6.1 incoming citations on average! 

We have now made our Cited-by service open to all. To realise its full benefit, it is essential to register your references.

{{< figure src="/images/blog/2023/citedby-blog.png" alt="Screenshot of slide Cited by" width="75%">}}

<br>There were concerns in the community about references ‘lost’ as part of supplementary material that may not be registered in its own right. Colleagues advised that if the data has an identifier, such as a DataCite DOI, you can add a relationship to say that it's supplementary material (see [https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/relationships/](/documentation/schema-library/markup-guide-metadata-segments/relationships/)) or add them as a reference. Martyn is curious to hear from others in the community on this topic. There is an increasing focus on data citations and we'd like to see how we can better support them.

Many members have questions related to plans for [replacing Metadata Manager](/blog/next-steps-for-content-registration/). Rachael Lammey, Director of Product, explained that we’re working on broadening our new [Grant Registration Form](/documentation/register-maintain-records/grant-registration-form/) to include more content types over the course of 2023. It has a few advantages over the current Web Deposit Form. It allows you to save a local copy once you first register a piece of content. It makes updating your records easier, as you can drop that file onto the form to add the metadata so that you can update it and redeposit rather than having to fill out the information all over again, and we have started adding automatic lookup fields to help users populate information on affiliations using ROR IDs more accurately. We will keep you posted on the progress with new developments and ask for beta testers for new content types as they are added.

Metadata information about individual work is not as useful as the opportunity to interrogate the relationships between works and within the global scholarly output. [The preview of the Relationship API endpoint](https://community.crossref.org/t/relationships-are-here/3523, modest as it is at this stage – with only 1% of our relationship metadata included (or 10 mln relationships) – offers a powerful demonstration of the way in which metadata contextualises research outputs within the entangled network of ever-progressing scholarship. 

{{< figure src="/images/blog/2023/code-for-blog.png" alt="Screenshot of code" width="50%">}}

<br>We’ve also mentioned the recent [transition of our website to GitLab](https://community.crossref.org/t/get-in-on-the-action-help-shape-our-website-with-your-feedback/3431), which allows everyone to contribute by creating merge requests and issues. Through this open collaboration, which supports our commitment to meet the Principles of Open Scholarly Infrastructure, we aim to cultivate a sense of ownership among contributors and make our information and documentation more useful and efficient for everyone. 

### Labs participation report

For organisations who wish to keep a close eye on their metadata – to understand what they deposit, how that compares with other members, and what could be improved, can start using our Lab participation reports. We encourage you to test this not-yet-finished tool and let us know your feedback. Participants at our updates found it very informative, with the opportunity to preview contents of recent deposits, see the participation breakdowns by a prefix, and improved data visualisation. 
We had questions about how data citation counts are generated in the report. Martyn Rittman explained that: “This is a prototype and that's one of the issues we need to tidy up! We know via Event Data and our Scholix endpoint what is a dataset, but that hasn't yet been incorporated to the Labs Reports”. There was also a suggestion of enabling export of simple lists of all member’s DOIs with respective URLs from the report and the team might look into that. Yet, lists of DOIs missing specific metadata types are already downloadable. 

To learn more about the reports, try them out, and to provide feedback, please take a look at [the information shared recently by Paul Davis](https://community.crossref.org/t/ticket-of-the-month-april-2023-the-new-labs-reports-are-here/3528), Tech Support Specialist & R&D Support Analyst. 

### Metadata priorities

Patricia Feeney, Head of Metadata, shared some updates about the current metadata corpus registered with Crossref, and some recent trends. 

{{< figure src="/images/blog/2023/metadata-trends-blog.png" alt="Screenshot of side titled metadata trends" width="75%">}}

<br>She then went on to summarise some preliminary results of our ongoing [metadata priorities survey](https://community.crossref.org/t/take-our-metadata-priorities-survey-by-may-18/3498), which all members are encouraged to take part in by **18th of May**. So far, we’ve received close to 1,000 responses. We’ve learnt that majority of our respondents are keen to deposit as much metadata as possible – and some would like to register more than we currently enable. Close to a half of the respondents who did not express an interest in sharing all metadata are still interested to learn more about the value of their metadata. 

She then went on to summarise some preliminary results of our ongoing [metadata priorities survey](https://community.crossref.org/t/take-our-metadata-priorities-survey-by-may-18/3498), which all members are encouraged to take part in by **18th of May**. So far, We’ve received close to 1,000 responses. We’ve learnt that majority of our respondents are keen to deposit as much metadata as possible – and some would like to register more than we currently enable. However, close to a half of the respondents are interested to learn more about the value of their metadata. 

The survey consults our members about their preferences for developing any of the potential projects under consideration: 
* Contributor IDs
* Contributor roles/ CRediT
* Alternate names
* Multilingual metadata
* Expand abstract support
* Citation types (content)
* Conference event IDs

It appears that support for citation types is the strongest among our respondents, while very polarised views have been shared about multilingual metadata and expanding support for abstracts. Among other suggestions, we received a lot of comments related to keywords. Overall, support for all projects was strong.

The verdicts are not in yet – still time to respond to the survey and make your metadata priorities known!

### Thank you and keep in touch

With much of the content shared ahead of the time through our Community Forum, the sessions were bubbling with questions and valuable comments from the community. We look forward to continuing the conversations asynchronously on the Community Forum. Please don’t hesitate to share your thoughts and ask further questions. We’d also love to hear suggestions for topics of the most interest for our future updates.

The more complete the metadata we collect together, the more connections in the ecosystem become transparent. This creates opportunities for discovery and collaborations, and greater insights about the scholarly process. Our community is growing in numbers, diversity, and technical capacity for building the Research Nexus together. We welcome your questions and suggestions of initiatives that support the fullest participation possible.
