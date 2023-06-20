---
title: 'Event Data now with added references'
author: Martyn Rittman
draft: false
authors:
  - Martyn Rittman
date: 2021-11-10
categories:
  - Event Data
  - References
  - Enrich services
archives:
    - 2021
---

Event Data is our service to capture online mentions of Crossref records. We monitor data archives, Wikipedia, social media, blogs, news, and other sources. Our main focus has been on gathering data from external sources, however we know that there is a great deal of Crossref metadata that can be made available as events. Earlier this year we started adding [relationship metadata](/blog/doing-more-with-relationships-via-event-data/), and over the last few months we have been working on bringing in citations between records.

Our members deposit references alongside other metadata, and we have a lot of them. In fact, we have over 1.2 billion, with hundreds of thousands of new references added each day. While our metadata APIs make it easy to see which works are cited, it is much more difficult to find a list of citations to a specific work. We can make this easier by presenting citations as events in Event Data. Now that the huge majority of our members have responded positively to the [Initiative for Open Citations (I4OC)](https://i4oc.org/) campaign and Crossref’s open-by-default reference policy, the move to make this data available via Event Data is a natural step.

## A bumpy ride, but we got there

Adding such a large amount of data means a significant increase in the data coming into Event Data, which has presented some challenges. We’ve known for some time that Event Data is [not very stable](https://www.crossref.org/blog/event-data-a-plan-of-action/), but we expected it to cope with the new data coming in. We have mitigated by initially only looking at new data, not trying to immediately back-fill with old references. Unfortunately, even with this limitation it hasn’t been a smooth ride, and our first effort to put references into Event Data uncovered bugs we didn’t know about and we had to walk back the changes.
We tried again and found that we were hitting rate limits for our own APIs. This is a sure sign of technical debt: we shouldn’t need to be shifting large amounts of our own data from one place to another, and not at rates that could be putting stress on APIs used by others in the community.

We have managed to work around these problems and I’m pleased to say that we are now adding metadata from reference lists to Event Data. They can be accessed via the Event Data API:
<a href="https://api.eventdata.crossref.org/v1/events?rows=10&source=crossref&relation-type=references&from-collected-date=2021-10-01">https://api.eventdata.crossref.org/v1/events?rows=10&source=crossref&relation-type=references&from-collected-date=2021-10-01</a>

## Where to next?

There remains work to be done. We would like to backfill references, and there is also further work to include relationships to objects that have identifiers other than Crossref records (genes, proteins, ArXiv identifiers, and so on). Our work on [investigating sources](/blog/event-data-help-us-fill-in-the-gaps/) is proceeding and we will be looking to add more next year. While possible, these steps will be costly and time-consuming if we proceed without significant changes to the infrastructure supporting Event Data.

When we started Event Data the volumes of data were much smaller and our infrastructure coped well, but as [we’ve said here before](/blog/doing-more-with-relationships-via-event-data/), it’s in need of an overhaul. In fact, our recent experience and some other considerations are making us look at some very fundamental changes in how we record events.

We are therefore working on a new data model that will allow events to be stored alongside the rest of our metadata. This work is still in the early stages, but if we are successful it will mean that we won’t need to move data between databases. It will also make it easier to provide access to all of our reference metadata along with other relationships that we’re not currently able to provide, and give us the capacity to add new data sources.

## Open references
_[EDIT 6th June 2022 - all references are now open by default with the March 2022 board vote to remove any restrictions on reference distribution]._

It is worth noting that only *open* references will be available via Event Data. This covers 88% of works with references at present. Members have the option to deposit references with *limited* visibility, meaning only [Metadata Plus](/documentation/metadata-plus/) users can access them; or *closed* visibility, meaning that only the member who owns the cited work can retrieve the citation, via [Cited-by](/documentation/cited-by/).

We encourage our members to make their references open and deposit them as metadata. It makes them usable downstream by thousands of tools that researchers use. Including open references also improves the quality of metadata, and there are reciprocal benefits for the large number of members who openly share their reference data: they contribute to a large, openly available pool of data with many applications that advance research, and drives usage of the content published by our members.

If you are a Crossref member and unsure whether your reference metadata is open or not, check your [participation report](https://www.crossref.org/members/prep/). This will tell you the percentage of your records with deposited references, and the percentage of those that are open. You can change the reference visibility preference for each DOI prefix that you own by contacting our [support team](https://support.crossref.org/hc/en-us/requests/new?ticket_form_id=360001642691). For guidance on how to deposit references, [see our user documentation](/documentation/register-maintain-records/maintaining-your-metadata/add-references/).
