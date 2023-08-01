---
title: 'Forming new relationships: Contributing to Open source'
author: Patrick Vale
draft: false
authors:
date: 2022-10-19
categories:
    - DOIs
    - Linking
    - Interoperability
    - Accessibility
    - Engineering
archives:
    - 2022
---


## TL;DR

One of the things that makes me glad to work at Crossref is the principles to which we hold ourselves, and the most public and measurable of those must be the [Principles of Open Scholarly Infrastructure](https://openscholarlyinfrastructure.org/), or POSI, for short. These ambitions lay out how we want to operate - to be open in our governance, in our membership and also in our source code and data. And it's that openness of source code that's the reason for my post today - on 26th September 2022, our first collaboration with the [JSON Forms](https://jsonforms.io/) open-source project was [released into the wild](https://github.com/eclipsesource/jsonforms/releases/tag/v3.0.0).

Like most organisations, we depend heavily on open-source software for our operations - the software is universally available, generally high quality and 'free'. And it's easy to take that dependency, and the associated dependency on free time and effort on the part of the maintainers, for granted - but that's not very sustainable. In fact, we believe relying on open-source software without helping to sustain it is an anti-pattern, and this project marks the start of our efforts to make funding open-source software a standard part of our technology budget.

This isn't the first time we've [supported](https://github.com/sckott/habanero) or [released](https://gitlab.com/crossref/rest_api) open-source software. Indeed for the past few years, all our new software is open source, and we're in the process of replacing old closed code with new, so that eventually all our code will be open source. But this is the first time we've contributed extensively to something that isn't focussed primarily on us, and our services. This is a project that we will find very useful, but it is a general purpose tool, and it's already gaining traction in the community.

## Background and motivations

A while back, I was tasked to do a quick [spike](http://agiledictionary.com/209/spike/) of work on testing the theory that we could use automated form generation tools to bring new interfaces to our users more quickly, and make them easier for "people who aren't devs" to adapt and manage. We wanted to build a new user interface for registering content, and especially we wanted to make it easier for funders to register the grants they were awarding. As well as being more approachable by a less-technical audience, we also wanted these forms to be accessible (in terms of [a11y](https://www.a11yproject.com/) and users of assistive technology) and localisable - we wanted a solution that would cater to the needs of our rapidly diversifying membership.

## Enter JSON Schema

We were clear about one side of the puzzle - we knew that we had to look beyond the XML ecosystem upon which much of our existing system is built - and landed on [JSON Schema](https://json-schema.org/). JSON Schema is a 'vocabulary that allows you to annotate and validate JSON documents'. This means you can describe the shape you expect your data to take, and apply constraints-based validation to that. Which means, in terms of a form library, that you can infer the structure of the form and test that the data entered into it matches what you expect. More than that, you can use that built-in validation to provide error messages to help people get the data right, first time.

Working backwards from the outcome, the argument for adopting JSON Schema is compelling. It provides a mechanism for checking that data you are handling (for example, receiving input from a form) conforms to the constraints that you declare, but also allows you to tell people up-front, in a human and machine-readable way, what structure and format you will accept. This closed-loop of data annotation and validation gets more appealing when you look at the wide adoption of JSON Schema across languages and libraries. You can pretty much guarantee that for whatever client or server -side technology you are using, there will be a JSON Schema validator for it. Being able to share schemas across your systems (and equally importantly, with third parties) moves JSON schema from 'just' being about data validation, to a key supportive technology.

Building a form derived from a JSON Schema is an equally attractive prospect. JSON Schema [was conceived](https://www.jviotti.com/assets/dissertation.pdf#page=23) during the AjaxWorld conference in 2007 as a 'JSON-based format for defining the structure of JSON data', and its use as a form-generation tool is relatively new, but there is growing community interest. There is even a [discussion](https://github.com/json-schema-org/community/discussions/70) about how to best create a JSON Schema vocabulary, specifically geared towards addressing some of the needs of form generation users. However, even in its current form, a JSON Schema can be passed to a library, and a very serviceable user interface appears. The devil is always in the detail, and the client-side libraries differ in their abilities to customise areas such as layout (you may not always want your form fields to appear in **exactly** the same order as they do in your JSON Schema), custom elements (you might want something that wasn't a form input, or that changes based on user input) and localisation. The ability to flexibly customise the appearance and behaviour of the interface was a key factor in our selection of a client-side form generation library.

## Choosing a library

The other side of the puzzle was less clear - choosing a UI library that would take this JSON Schema, and turn it into a useful, and usable, form. I made the prototype using the venerable [React JSON Schema form](https://github.com/rjsf-team/react-jsonschema-form). This worked well as a proof of concept, but veered dramatically off our chosen Frontend stack of [VueJS](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/), and had some architectural constraints that would limit the scope of customisations we could make to our forms. So I went off looking for libraries that would work with our stack and came up with [Vuetify JSON Schema Form](https://koumoul-dev.github.io/vuetify-jsonschema-form/latest/), and [JSON Forms](https://jsonforms.io/).

Vuetify JSON Schema Form matched our stack perfectly, but made some interesting decisions about the layout of data within the form, and that wouldn't suit our purposes without dramatic modification.

JSON Forms was an abstracted library, with a core handling the JSON Schema transformation and validation, and separate rendering libraries to handle the form generation. This was great - they had renderers for Angular, React, and even some support for VueJS. But not Vuetify.

Clearly, we were going to have to make something.

We made contact with the maintainers of both short-listed libraries to see how we could collaborate in creating a tool that would meet all of our (and hopefully, much of the wider community's) requirements. Both maintainers were very helpful, and we had constructive discussions in both cases. In the end, we decided that the abstracted nature of the JSON Forms project was a better fit for our needs, providing a flexible platform on which we - and others - could extend. We were fortunate to receive funding from the Gordon and Betty Moore Foundation (Grant Agreement #10485) in order to accelerate this work, so we could provide a Grant Registration UI more quickly. We paid a large portion of that funding to the library maintainers, and Crossref contributed a portion of my time on the project. This allowed us to enter into an agreement with [EclipseSource](https://eclipsesource.com/), the maintainers of JSON Forms, to collaboratively develop the new VueJS and Vuetify renderer library. Stefan Dirix, the lead maintainer, worked with me to build it.

We didn't forget about Vuetify JSON Schema Form though, and by way of appreciation for their help in the early stages, Crossref made a contribution towards the continued development of that library.

## JSON Forms - now with Vuetify

Work started on the [JSON Forms Vuetify renderer set](https://github.com/eclipsesource/jsonforms-vuetify-renderers) in September 2021 - Stefan quickly created the first early prototypes of the new form renderers - but then we had a stroke of luck. Our repository received more input from the community. The one that made us sit up and take real notice was the news that someone else had already ported the JSON Forms React renderer set to Vue/Vuetify - and was [offering this](https://jsonforms.discourse.group/t/unclear-on-how-to-implement-basic-styling-in-vue2-according-to-github-page/347/5) as a contribution. [Krasimir Chobantonov's](https://github.com/kchobantonov) fantastic first contribution got [merged in](https://github.com/eclipsesource/jsonforms-vuetify-renderers/pull/5) at the end of the month. This propelled the project forward massively, and was an early validation of the value of working in the open. Needless to say, we were very grateful. Another example of the open source value chain was that Stefan - as the maintainer - could take the time to carefully review and tidy up the incoming code, so what was merged was the product of two great developers.

Having this great head start meant we could turn our attention to one of the other big areas we wanted to get right - localisation. Traditionally, JSON Schema -generated forms have handled localisation (translation of text and adjustment of date and numerical formats) by wholesale duplication and translation of the schema. This is cumbersome, and doesn't integrate very well with custom error messages, nor external sources of interface messages (think form labels, descriptions, placeholders). So Stefan came up with a proposal, which we accepted, to add complete [i18n support](https://github.com/eclipsesource/jsonforms/pull/1825) to the library. We now have a mechanism by which you can hook up a translation engine of your choice, and JSON forms will use that to lookup messages, before falling back to the validator (also localised!) and finally, the JSON Schema's defaults. This gives much stronger integration and allows the community to plug in their existing localisation methods - no wasted effort.

Since the localisation addition, we've been working on fine-tuning the layout engine, making bug fixes, and integrating more closely with the underlying Vuetify library. This allows developers to more easily use the existing Vuetify parameters to change the style and behaviour of their form widgets. Again, no wasted effort. 

We're lucky to have an active community - [@kchobantonov](https://github.com/kchobantonov) continues to make great contributions and push the library forward in unexpected ways - and the library is gaining popularity, with an average of a few hundred downloads per day. 

Some of our funder members have already seen this work in action, and given their feedback on early iterations of the user interface that supports registering grant records. We'll be releasing this publicly very soon to get feedback from members - and then using that feedback to iterate on the grants registration form, and look towards extending it to other content types. 

## Open source POSItivity

A continuous theme throughout this project has been the willingness of people working on these open source projects to be generous with their time and experience. Whether it has been form generation libraries, the [JSON Schema project](https://json-schema.org/) or maintainers of [localisation plug-ins](https://fluent-vue.demivan.me/) - help, advice and encouragement have never been far away. And that's appreciated. But it's not something that we, or any other organisation who relies on the software they produce, should take for granted. Open source software helps everyone who uses it, and there's a real opportunity within our community to make meaningful steps towards supporting its sustainability. Ironically, it's often the most-used general purpose tools that get the least attention. We can change that.

## Look out for more

Look out for more posts from the [engineering](/categories/engineering/) team, coming soon!

### References

[JSON Binpack: A space-efficient schema-driven and schema-less binary serialization specification based on JSON Schema](https://www.jviotti.com/assets/dissertation.pdf) (Chapter 3.2.1 History and Relevance)

https://web.archive.org/web/20071026190426/http://www.json.com/2007/09/27/json-schema-proposal-collaboration/
