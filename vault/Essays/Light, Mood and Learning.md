---
title: Light, Mood and Learning
subtitle: Two routes from the eye that have nothing to do with seeing
date: 2026-11-23
publish: true
abstract: >
  Light does more than let us see. A small class of retinal cells measures brightness and sends it to parts of the brain that never form an image. A 2018 study in mice traced two of these routes: one through the suprachiasmatic nucleus that affects learning, and one through a thalamic nucleus called the perihabenular nucleus that affects mood. This essay follows how those cells were found, what the two routes are, what the experiments do and do not show, and why a model of the visual cortex cannot see either of them.
---

## A third photoreceptor

For most of the history of vision science the retina had two kinds of light sensor, rods and cones. Everything the brain knew about light was assumed to start there. In 2002 that changed. David Berson and colleagues recorded from the retinal ganglion cells that project to the suprachiasmatic nucleus (SCN), the brain's circadian clock, and found that they responded to light on their own, even when cut off from rods and cones[^1]. In the same issue of *Science*, Samer Hattar and colleagues showed that these cells contain the photopigment melanopsin and mapped where their axons go[^2].

The cells are now called *intrinsically photosensitive retinal ganglion cells*, or ipRGCs. They are a small minority of ganglion cells and they are bad at what we usually mean by vision. They respond slowly and they do not resolve detail. What they do well is report how bright the world is over long stretches of time. That is the signal a clock needs. Light acts as the *zeitgeber*, the time-giver, and ipRGCs are how it reaches the SCN to set the clock to the day.

%% YOUR VOICE: when did you first learn that the eye has a third kind of photoreceptor? What did you think? %%

So from the start these cells were filed under circadian rhythm and sleep. The more interesting question came later: is that all they do?

## Light at the wrong time

It is hard to separate light from sleep. If you keep an animal in bad lighting and it becomes depressed or learns poorly, the obvious explanation is that its clock was disrupted, it slept badly, and everything else followed.

A 2012 study from Hattar's group was designed to pull those apart. Mice were kept on a cycle of 3.5 hours of light and 3.5 hours of dark, instead of the usual 12 and 12. The cycle was chosen because it puts light at the wrong times of day without breaking the clock. The mice kept a working circadian rhythm, and the amount and structure of their sleep did not change. They still showed depression-like behaviour and they still learned worse. Mice without ipRGCs were protected from both[^3].

That result is the reason the word *directly* is in the paper's title. Light was reaching mood and learning through ipRGCs, and not only by way of lost sleep or a broken clock. What the study could not say was where in the brain the signal went.

## Two routes

The answer came in 2018, in a paper by Diego Fernandez and colleagues, including my mentor Daniel Severin[^4]. It found that the effects on learning and the effects on mood travel by different routes.

%% YOUR VOICE: how did you come to this paper? Did Daniel point you to it? What part of the work came from the Kirkwood lab? (Ask him before you say.) %%

![Two non-image-forming routes from the retina: one to the SCN, affecting learning, and one to the perihabenular nucleus, affecting mood.](light-pathways.svg)

The learning route runs through the SCN. The ipRGCs that project there carry light's effect on learning, and they do it independently of the SCN's pacemaker function. In mice whose ipRGCs reached the SCN but not their other targets, the abnormal light cycle still impaired learning, and the mood effects were gone. This is the part I find strangest. The SCN is known as a clock, but here it is behaving more like a relay, passing a light signal on without that signal having to go through its timekeeping.

The mood route skips the SCN altogether. A different set of ipRGCs projects to a region of the dorsal thalamus that the paper named the *perihabenular nucleus*, or PHb. In mice the PHb was both necessary and sufficient for light's effects on mood-related behaviour: without its activity the abnormal light no longer changed mood, and driving it was enough to produce the change. The PHb is wired into regions already tied to mood. It connects with the prelimbic and infralimbic parts of the prefrontal cortex and projects to the dorsomedial striatum and the nucleus accumbens.

Put together, the retina has at least three jobs for light. One is seeing. One is telling the SCN something that matters for learning. One is telling the PHb something that matters for mood. Only the first is what we would call vision.

## What the experiments do not show

Three cautions belong here.

The first is that these are mice. Mice are nocturnal, and light means something different to an animal that sleeps through the day. Humans have ipRGCs and an SCN, but nobody has shown that the human PHb does the same job.

The second is that a mouse cannot report its mood. The measures are behavioural proxies, such as how much a mouse prefers sugar water to plain water and how long it stays immobile in a forced swim. They are standard and useful, but they are not the same thing as depression in a person.

The third is the one I got wrong in my first notes on this paper. It is tempting to read it as saying you can boost learning with light. It does not say that. It shows that *aberrant* light *impairs* learning. Whether well-timed light could improve learning was not tested. It is a fair question to ask, and I would like to know the answer, but it is a question and not a finding.

The same goes for sleep. The easy takeaway is that light matters because sleep matters. The 2012 result points the other way: the mice slept normally and were still affected[^3]. Sleep is important for plenty of other reasons. The point of this work is that light has its own line into mood and learning.

## What a cortical model cannot see

This connects to a project of mine. I have been working with TRIBE v2, a model from Meta that predicts how the human cortex responds to what a person sees and hears. My code is at [github.com/RehanKrish21/Neuro-engagement-forecasts](https://github.com/RehanKrish21/Neuro-engagement-forecasts).

TRIBE v2 models the image-forming route: retina, thalamus, visual cortex and onward. Its released weights cover cortex only. The two routes in this paper are non-image-forming and they run below the cortex, from ipRGCs to the SCN and from ipRGCs to the PHb. A cortex-only model has no way to represent them.

%% YOUR VOICE: something you have actually seen running TRIBE. Keep it honest: so far the pipeline has only run on synthetic data. %%

That matters for what such a model can claim. Given a video, it can predict the cortical response to the content. It knows nothing about what the brightness and timing of that same screen are doing through the other two routes. The same clip watched in the middle of the day and in the middle of the night would get the same prediction, even though the light is arriving at very different points in the viewer's day. I think that is a real limit of the model and worth naming, and it is a question I want to carry into the project.

## My thoughts

%% YOUR SECTION. Nothing here shows on the site until you write text under this heading.
Write a few short paragraphs in your own voice, not a summary of the papers:
- Which finding surprised you most, and why?
- Is there anything you disagree with, or think is overstated?
- If you had your own lab for a year, what would you test first?
- How does this connect to something you have actually done or seen?
Specific beats general: a moment, a result, a conversation. %%

## What is not known

Three questions seem open to me. The first is whether the PHb route exists in people and does the same job. The second is the one above: whether light can be used to help learning, and not only to harm it. The third is how the SCN passes on a light signal for learning without using its clock, and where that signal goes next.

I came to this paper because of who wrote it. I am staying with it because it changes what I think the eye is for.

[^1]: D. M. Berson, F. A. Dunn, M. Takao. *Phototransduction by retinal ganglion cells that set the circadian clock.* Science 295, 1070–1073 (2002). [doi:10.1126/science.1067262](https://doi.org/10.1126/science.1067262)
[^2]: S. Hattar, H.-W. Liao, M. Takao, D. M. Berson, K.-W. Yau. *Melanopsin-containing retinal ganglion cells: architecture, projections, and intrinsic photosensitivity.* Science 295, 1065–1070 (2002). [doi:10.1126/science.1069609](https://doi.org/10.1126/science.1069609)
[^3]: T. A. LeGates et al. *Aberrant light directly impairs mood and learning through melanopsin-expressing neurons.* Nature 491, 594–598 (2012). [doi:10.1038/nature11673](https://doi.org/10.1038/nature11673)
[^4]: D. C. Fernandez, P. M. Fogerson, L. Lazzerini Ospri, M. B. Thomsen, R. M. Layne, D. Severin, J. Zhan, J. H. Singer, A. Kirkwood, H. Zhao, D. M. Berson, S. Hattar. *Light affects mood and learning through distinct retina-brain pathways.* Cell 175, 71–84 (2018). [doi:10.1016/j.cell.2018.08.004](https://doi.org/10.1016/j.cell.2018.08.004)
