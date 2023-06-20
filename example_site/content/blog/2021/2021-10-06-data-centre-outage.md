---
title: 'Outage of October 6, 2021'
author: Geoffrey Bilder
draft: false
authors:
  - Geoffrey Bilder
date: 2021-10-06
categories:
  - Data Center
  - Post Mortem
Archives:
  - 2021
---

On October 6 at ~14:00 UTC, our data centre outside of Boston, MA went down. This affected most of our network services- even ones not hosted in the data centre. The problem was that both of our primary and backup network connections went down at the same time. We're not sure why yet. We are consulting with our network provider. It took us 2 hours to get our systems back online.

We are going to reprocess content that was in the process of being registered at the time of the outage in order to make sure everything gets registered correctly. This may take a few days to complete.

### Why did we have such a complete outage and why did it take us so long to fix it?

1. We still run a significant amount of our infrastructure in a data centre outside of Boston that we manage ourselves. Even though we've been moving many of our services to the cloud, all our traffic was still routed through the data centre - so when it went down, most of our cloud services were unavailable as well.

2. It took us a long time to fix this because our infrastructure team only has two people in it. Only one of them is located near the data centre and was at the doctor’s when the outage occurred. Although we were alerted to the problem immediately, we had to send one of our development team members to the data centre to diagnose and fix the problem.

We have been aware of these weaknesses in our system since I took the role of director of technology in 2019, and we have been putting most of our efforts over the past two years into fixing them.

We know that an organisation of our size has no business trying to run and maintain a physical data centre ourselves. One of the strengths of cloud-based systems is that they can be administered from anywhere and don't require anyone to physically go to a data centre to replace failed hardware or check that network connections are, in fact, live. We've been trying to move to the cloud as fast as we can. All new services that we build are cloud-based. At the same time we've been moving systems out of the data centre - starting with those that put the biggest load on our systems. To further aid this process we have budgeted to add an FTE to the infrastructure team in 2022.

What is really painful about this event is that we had just completed the last bit of work we needed to do before changing our traffic routing so that it would hit the cloud first instead of the data centre first. This would not have avoided the outage we just experienced, but it would have made it a bit less severe.

What is even more painful is that we had recently installed a *third* network connection with an entirely different provider because we were worried about just this kind of situation. But this third connection wasn’t yet active.

We already have a long list of tickets that we’ve created to address problems we faced in recovering from this outage. The list will undoubtedly grow as we complete a postmortem over the next few days. I will report back when we have more detail of what happened and have a solid plan for how to avoid anything similar in the future.

We know that an outage of this severity and duration has caused a lot of people who depend on our services extra work and anxiety. For this, we apologise profusely.

But at least we didn’t need to use an [angle grinder](https://twitter.com/cullend/status/1445156376934862848).
