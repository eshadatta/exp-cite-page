---
title: '2023 public data file now available with new and improved retrieval options'
author: Patrick Polischuk
draft: false

authors:
  - Patrick Polischuk
date: 2023-05-02
categories:
  - Metadata
  - Community
  - APIs

Archives:
  - 2023
---

We have some exciting news for fans of big batches of metadata: this year’s public data file is now available. Like [in](https://www.crossref.org/blog/free-public-data-file-of-112-million-crossref-records/) [years](https://www.crossref.org/blog/new-public-data-file-120-million-metadata-records/) [past](https://www.crossref.org/blog/2022-public-data-file-of-more-than-134-million-metadata-records-now-available/), we’ve wrapped up all of our metadata records into a single download for those who want to get started using all Crossref metadata records.

We’ve once again made [this year’s public data file available via Academic Torrents](https://academictorrents.com/details/d9e554f4f0c3047d9f49e448a7004f7aa1701b69), and in response to some feedback we’ve received from public data file users, we’ve taken a few additional steps to make accessing this 185 gb file a little easier. 

First, we’re proactively hosting seeds in a few locations around the world to improve torrent download performance in terms of both speed and reliability. 

And second, we’ve added an option to download this year’s public data file directly from Amazon S3 for a small transaction fee paid by the recipient, bypassing the need to use the torrent altogether. The fee just covers the AWS cost of the download. Instructions for downloading the public data file via the "Requester Pays" method are available on the ["Tips for working with Crossref public data files and Plus snapshots"](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-public-data-files-and-plus-snapshots/) page.

The 2023 public data file features over 140 million metadata records deposited with Crossref through the end of March 2023, including over 76,000 grant records. Because Crossref metadata is always openly available, you can use our API to keep your local copy of our metadata corpus up to date with new and updated records.

In previous years, closed and limited references were removed from the public data file. Since we [updated our membership terms](https://www.crossref.org/blog/amendments-to-membership-terms-to-open-reference-distribution-and-include-uk-jurisdiction/) to make all deposited references open in 2022, the 2023 public data file for the first time includes all references deposited with us.

We hope you find this public data file useful. Should you have any questions about how to access or use the file, please see the tips below, or bring your questions to our community forum.

### Tips for using the torrent and retrieving incremental updates

-   Use the public data file if you want all Crossref metadata records. Everyone is welcome to the metadata, but it will be much faster for you and much easier on our APIs to get so many records in one file. Here are some [tips on how to work with the file](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-public-data-files-and-plus-snapshots/).

-   Use the REST API to incrementally add new and updated records once you have the initial file. Here is [how to get started](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) (and avoid getting blocked in your enthusiasm to use all this great metadata!).

-   While bibliographic metadata is generally required, because lots of metadata is optional, records will vary in quality and completeness.

Questions, comments, and feedback are welcome at [support@crossref.org](mailto:support@crossref.org).