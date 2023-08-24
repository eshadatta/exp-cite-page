---
title: 'Shooting for the stars – ASM’s journey towards complete metadata'
author: Kornelia Korzec
draft: false
authors:
  - Kornelia Korzec
  - David Haber
  - Deborah Plavin
date: 2023-03-14
categories:
  - Metadata
  - Community
  - Publishing
  - Research Nexus
  - Content registration
archives:
      - 2023
---

At Crossref, we care a lot about the completeness and quality of metadata. Gathering robust metadata from across the global network of scholarly communication is essential for effective co-creation of the research nexus and making the inner workings of academia traceable and transparent. We invest time in community initiatives such as [Metadata 20/20](https://metadata2020.org) and [Better Together webinars](https://zenodo.org/communities/better-together/?page=1&size=20). We encourage members to take time to look up their [participation reports](/documentation/reports/participation-reports/), and [our team can support you](https://community.crossref.org/c/reports/30) if you’re looking to understand and improve any aspects of metadata coverage of your content.
 
In 2022, we have observed with delight the growth of one of our members from basic coverage of their publications to over 90% in most areas, and no less than 70% of the corpus is covered by all key types of metadata Crossref enables (see [their own participation report](/members/prep/235) for details). Here, Deborah Plavin and David Haber share the story of ASM’s success and lessons learnt along the way.
 
### Could you introduce your organization? 
 
The American Society for Microbiology publishes 16 peer-reviewed journals advancing the microbial sciences, from food microbiology, to genomics and the microbiome, comprising 14% of all microbiology articles. Six of those are open-access journals, and 56% of ASM’s published papers are open access. Together, our journals contribute 25% of all microbiology citations. 
 
### Would you tell us a little more about yourselves?
 
DH: David Haber, Publishing Operations Director at the American Society for Microbiology. I live in a century-old house that is in a perpetual state of renovation due to my inability to stop starting new projects before I complete old ones.
 
DP: Deborah Plavin, Digital Publishing Manager at the American Society for Microbiology. Following David’s example, my apartment in Washington D.C. is just up the block from one of the homes Duke Ellington lived in [https://www.hmdb.org/m.asp?m=142334](https://www.hmdb.org/m.asp?m=142334).
 
 
### What value do society publishers in general see in metadata in your view?
 
DP: In my view, robust metadata allows publishers to look at changes over time, do comparative analysis within and across research areas, more easily identify trends, and plan for future analysis (e.g., if we deposit data citation information and we change our processes to make it more straightforward, do we see any change in the percentage of articles that include that information, etc.).
 
DH: To echo Deborah's point, to be able to name something distinctly and clearly identify its specific attributes is vital to understanding past research and planning for future possibilities. One of our fundamental roles as a publisher for a non-profit society is to properly lay this metadata foundation so that we can provide services and new venues for our members, authors, and readers that match their needs and track with the trends in research. Without good and robust metadata, it is impossible to truly understand the direction in which our community is pointing us.
 
### Metadata for your own published content in the last year has grown rapidly. Why such focus on metadata in 2022?
 
DP: This is something that ASM has been chipping away at over time. Years ago we found that it wasn’t always easy to take advantage of deposits that included new kinds of metadata. That was either because we needed to work out how and where to capture it in the process or because platform providers weren’t always ready — coming up with ways to process the XML that publishers supply in many different ways takes time. These back-end processes that feed the infrastructure aren’t usually of great interest to stakeholders, and so it allowed us to play around, flounder, fail, refine, and try again.
 
We looked at having 3rd parties deposit metadata for us, and while that helped expand the kind of metadata we were delivering, it created workflow challenges of its own. What turned out to be most effective was budgeting for content cleanup projects and depositing updated and more robust metadata to Crossref.
 
We also benefited from a platform migration, which allowed us to take advantage of additional resources during that process.
 
DH: Coming from a production background, I have always been fascinated with the when and how of capturing key metadata during the publishing process. When are those data good and valuable, and when should they be tossed or cleaned up for downstream deliveries? Because Deborah and ASM directors saw a more complete Crossref metadata set for our corpus as a truly valuable target, we were able to really think hard about what kind of data we were capturing and when, how those requirements may have influenced our various policies and copyediting requirements over the years, and how best to re-engineer our processes with the goal of good metadata capture throughout our publishing workflows. From our perspective, Crossref gave us a target, a “this-is-cool-bit-of-info" that Crossref can collect in a deposit; therefore, how can we capture that during our processes while driving further efficiencies? ASM journals had been so driven by legacy print workflows that such a change in perspective (toward metadata as a publishing object) really allowed us to re-imagine almost everything we do as a publisher.
 
### Has the OSTP memo influenced your effort?

DP: I think that the Nelson memo hasn’t changed our focus; instead, I think it’s been another data point supporting our efforts and work in this area.
 
DH: Deborah is exactly right. The release of this memo only re-affirmed our commitment to creating complete and rich metadata. The Nelson memo points to many possible paths forward, in terms of both Open Access and Open Science, but we feel our work on improving our metadata outputs positions us well to pick a path that best suits our goals as a non-profit society publisher.
 
### How big was this effort? Could you draw us a picture of how many colleagues or parts of the organization were involved? Did you involve any external stakeholders, such as authors, editors, or others?
 
DH: It was simple. Took five minutes…
In all seriousness, the key is having the support of the organization as a whole. To do this properly, it is vitally important to know the end from the beginning, so to speak. It is one thing to say let’s start capturing ORCID IDs and deliver them to Crossref, but it is completely another to create a cohesive process in which those IDs are authenticated and validated throughout the workflow. So something as simple as a statement “ORCID IDs seem cool, let’s try to capture them” could affect how researchers submit files, how reviewers log into various systems (i.e., ORCID as SSO), how data are passed to production vendors, what copyeditors and XML QC people need to be focused on, and what integrations authors may expect at the time of publication. Being part of an organization that embraced such change allowed us to proceed with care with each improvement to the metadata we made.
 
But that is more about incremental improvement. The beginning of this process started when we were making upgrades to our online publishing platform, and we were trying to figure out how best to get DOIs registered for our older content. When we started looking at this, we soon realized that, sure, we could do the bare minimum and just assign DOIs to this older content outside the source XML/SGML, but did that make sense? Wouldn’t it make more sense, especially since we were updating the corpus to a new DTD, to populate the source content with these newly assigned DOIs? Once we decided that we were going to revise the older content with DOIs, it made sense for us to create a custom XSL transform routine to generate Crossref deposits that would capture as much metadata as possible. So, working with a vendor to clean and update our content for one project (an online platform update) allowed us also to make massive improvements to our Crossref metadata as a side benefit.
 
Of course, I do have to apologize to the STM community for the Crossref outages in late 2019. That was just me depositing thousands of records in batches one sleepless night.
 
### What were the key challenges you encountered in this project, and how did you overcome them?
 
DH: Resources and time are always an issue. Much of the work was done in-house in spare moments captured here and there. But there are great resources in github and at Crossref to help focus on defining what is important and what is possible in such a project. And, honestly, defining what was important and weighing that against the effort to find said important bit in the corpus of articles we have was the most challenging part of this process. In other words, limiting the focus. Once one decides to start looking at the inconsistencies in older content, it is hard not to say: “Oh, look. That semi-important footnote was treated as a generic author note rather than a conflict-of-interest statement; let’s fix that.” Once you start down that path, you can spend years fiddling with stuff. For me, a key mantra was: “We now have access to the content. We can always do another Crossref metadata update if things change or shift over time.”
 
### Have there been any important milestones along the way you were able to celebrate? Or any set-backs you had to resolve in the process?
 
DP: For as long as I can remember, the importance of good metadata has been among the loudest messages of best practice in the industry. I don’t think that I have been able to really quantify/ demonstrate the value of that work. Looking at the consistent increases in the Crossref monthly resolution reports that we saw between 2015 and 2022 and looking at our participation reports has helped provide some measure of progress. For example, the number of average monthly successful resolutions in that Crossref report in 2015 was ~390,000. The last time I checked, the 2022 numbers were ~ 3.7 million. In 2023, I hope that we will be able to leverage Event Data for this as well.
 
The setbacks have fallen into two categories: timing and process. Our internal resourcing to get this done within our preferred time frame, to have the content loaded and delivered, and triage problems—it’s a battle between the calendar and competing priorities.
 
DH: When Deborah first shared those stats with me, I was floored. I don’t think either of us suspected such an increase was possible. For me, the biggest setback was mistakenly sending about ~50,000 DOI records to queue and watching them all fail because I grabbed the wrong batch. Ooops. I never made that mistake again, though.
 
### Was any specific type of metadata or any part of the schema particularly easy or particularly difficult to get right in ASM’s production process?
 
DH: For us, the most difficult piece of metadata revolves around data availability and how we capture linked data resources (outside of data citation resources). Because of our current editorial style (which had been print-centric for years), we did not do a good job of identifying whether there are data associated with published content in a consistent machine-readable way. We did some experiments with one of our journals to capture this outside of our normal Crossref deposit routine, but that was not as accurate or sustainable as we would have liked. But, in that experiment, we learned a few things about how we treat these data throughout our publishing process and we have plans to create a sustainable integrated workflow for this to capture resource/data linkages in our Crossref deposits.
 
### What were your thoughts on last year’s move to open references metadata? Has that impacted on your project in any way?
 
DP: We were really excited about this; based on the rather limited approach to sorting out impact at the moment, the more metadata we push out into the ecosystem, the more it appears to be used. In my view, that is at the core of what society publishers want to do—ensure that research is accessible and discoverable wherever our users expect to find it.
 
DH: 100% agree.
 
### How did you keep motivated and on-course throughout?
 
DP: These kinds of things are never done; for example, we have placeholders for CRediT roles, and getting ready for that work as part of a DTD migration will be the next big thing. The motivation for that is really meeting our commitment to the community, seeing the impact of the author metadata versus article metadata, and seeing what we can learn.
 
DH: Metadata at its core is one of the pillars of our service as a publisher. To provide the best service, we need to provide the best metadata possible. Just remembering that this can be incremental, allows us to celebrate the large moments and the small. And whether one is partying with a massive 7 layer cake or a smaller cake pop, both are sweet and motivating.
 
### Now that the project is completed, are you seeing the benefits you were hoping to achieve?

DP: This is a hard one to answer as we are using limited measurements at this time. At a high level, I am pleased.  While I am eager to leverage event data in the coming year, it would be really helpful to get feedback from the community on how we can improve as well as other ways to evaluate impact.
 
DH: I want to take up this idea of metadata as a service once more. I don’t mean in terms of discoverability or searchability, either. Let’s take ORCID  deposited into Crossref as an example. When done properly (with the proper authentication and validation occurring in the background), we are able to integrate citation data directly to an author's ORCID profile. We have found that this small service is really appreciated.
 
### Is there any metadata that you’d like to be able to include with your publishing records in the future that isn’t possible currently? What would it be and why?
 
DP: CRediT roles would be great because it could give greater insight into collaboration within and across disciplines, it could allow for some automation and integration opportunities in the peer review process, and maybe it would visualize aspects of authors’ careers.
 
DH: I second capturing CRediT roles. What would be really interesting is also creating a standard that quantifies the accessibility conformance/rating of content and passing that into Crossref.
 
### What was the key lesson you learned from this project?
 
DP: Incremental change can be just as challenging as a massive overhaul, and so it’s important to reevaluate your goals along the way—things always change. There have been cases where we were able to do things that we hadn’t initially thought were feasible.
 
DH: Always keep the larger goal in mind and remember that any project can birth a new project. Everything does not happen at once.
 
### What’s your next big challenge for 2023?
 
DP:  There is a lot to contend with in the industry right now, and in addition to that we are going through some serious infrastructure changes in our program. With all that madness comes many opportunities. For that reason, when I take a step back from the tactical implications of all that and what we are interested in doing, I think our biggest challenge in 2023 will be identifying what has made an impact and why.  
 
DH: In the short-term, it is making sure that none of our production process changes has negatively affected the past metadata work we spent so much time honing. Once that settles down, it will be determining the best way forward from a publishing perspective in handling true versioning and capturing accurate event data.
 
### Based on your experience, what would be your advice for colleagues from other scholarly publishing organizations?

DP: It can seem daunting, but the small wins can create momentum and do not have to be expensive. Remembering that your publishing program benefits as much as everyone else’s when you deposit more metadata can help refine your short-term and long-term priorities.  

DH: Don’t be afraid of making a mess of things. Messes are okay. They aren’t risky. They just reveal the clutter. And clutter gives one reason to clean things up.  
 
 
THANK YOU for the interview!

***
 
### About the American Society for Microbiology

The American Society for Microbiology is one of the largest professional societies dedicated to the life sciences and is composed of 30,000 scientists and health practitioners. ASM's mission is to promote and advance the microbial sciences.  

ASM advances the microbial sciences through conferences, publications, certifications and educational opportunities. It enhances laboratory capacity around the globe through training and resources. It provides a network for scientists in academia, industry and clinical settings. Additionally, ASM promotes a deeper understanding of the microbial sciences to diverse audiences. 
For more information about ASM visit [asm.org](https://asm.org/).  
