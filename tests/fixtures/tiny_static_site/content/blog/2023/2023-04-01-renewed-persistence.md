---
archives:
- 2023
author: Joe Wass
authors:
- Joe Wass
categories:
- Engineering
date: 2023-04-01
draft: false
title: Renewed Persistence
---

**We believe in Persistent Identifiers. We believe in defence in depth. Today we're excited to announce an upgrade to our data resilience strategy.**


{{% imagewrap right %}}
{{<figure src="/images/blog/2023/2023-04-01-renewed-persistence/single-floppy-small.jpg" width="200px" alt="5¼ inch floppy disk with Crossref logo" >}}
 {{% /imagewrap %}}  

[Defence in depth](https://en.wikipedia.org/wiki/Defense_in_depth_(computing)) means layers of security and resilience, and that means layers of backups. For some years now, our last line of defence has been a reliable, tried-and-tested technology. One that's been around for a while. Yes, I'm talking about the humble [5¼ inch floppy disk](https://en.wikipedia.org/wiki/Floppy_disk#8-inch_and_5%C2%BC-inch_disks). 

This may come as surprise to some. When things go well, you're probably never aware of them. In day to day use, the only time a typical Crossref user sees a floppy disk is when they click 'save' (yes, some journals still require submissions in Microsoft Word).

## History

But why? 

Let me take you back to the early days of Crossref. The technology scene was different. This data was too important to trust to new and unproven technologies like Zip disks, CD-Rs or USB Thumb Drives. So we started with punched cards.

{{<figure src="/images/blog/2023/2023-04-01-renewed-persistence/punched-card.jpg" width="100%" caption="IBM 5081-style punched card." >}}

Punched cards are reliable and durable as long as you don't [fold, spindle or mutilate](https://en.wikipedia.org/wiki/Punched_card#Do_Not_Fold,_Spindle_or_Mutilate) them. But even in 2001 we knew that punched cards' days were numbered. The capacity of 80 characters kept DOIs short. Translating DOIs into [EBCDIC](https://en.wikipedia.org/wiki/EBCDIC) made [ASCII](https://en.wikipedia.org/wiki/ASCII) a challenge, let alone [SICI](https://en.wikipedia.org/wiki/Serial_Item_and_Contribution_Identifier)s. We kept a close eye on the nascent Unicode.

## Breathing Room

In 2017 the change of DOI display guidelines from `http://dx.doi.org` to `https://doi.org` shortened each DOI by 2 characters, buying us some time. But eventually we knew we had to upgrade to something more modern. 

So we migrated to 5¼ inch floppy disks. 

{{< figure src="/images/blog/2023/2023-04-01-renewed-persistence/floppy-in-drive.jpg" caption="5¼ Floppy disk in drive" width="100%" >}}

At 640 KB per disk these were a huge improvement. We could fit around 20,000 DOIs on one floppy. Today we only need around 10,000 floppy disks to store all of our DOIs (not the metadata, just the DOIs). Surprisingly this only takes about 20 metres of shelf space to store.

{{<figure src="/images/blog/2023/2023-04-01-renewed-persistence/desktop.jpg" width="100%" alt="laptop computer connected to floppy disk drive, pile of disks next to it" caption="Typical work from home setup. Getting ready to backup some DOIs!">}}

The move to working-from-home brought an unexpected benefit. Staff mail floppy disks to each other and keep them in constant rotation, which produces a distributed fault tolerant system. 

## Persistence Means Change

But it can't last forever. DOIs registration shows no sign of slowing down. It's clear we need a new, compact storage medium. So, after months of research, we've invested in new equipment. 

**Today we announce our migration to 3½ inch floppies.**

{{<figure src="/images/blog/2023/2023-04-01-renewed-persistence/new-equipment.jpg" alt="dual format floppy disk drive, with 5¼ inch and 3½ inch floppy disks" width="100%" >}} 

<br>

If it goes to plan you won't even notice the change.

{{<figure src="/images/blog/2023/2023-04-01-renewed-persistence/old-new.jpg" alt="two stacks of disks" width="100%" >}}


### Image credits

Punched card: IBM 5081-style punched card. Derived from [public domain by Gwern](https://en.wikipedia.org/wiki/File:Blue-punch-card-front-horiz_top-char-contrast-stretched.png).