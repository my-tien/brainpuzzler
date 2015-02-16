---
title: Brainpuzzler Tutorial
layout: page
permalink: /tutorial/
---

<div class="row">
<div class="12u">
The Interactive Brainpuzzler Tutorial
=====================================

Hello,

And thanks for your interest! In this tutorial you will learn how to help researchers uncover the mysteries of the brain with just a few mouse clicks.

If you haven’t already done so, please follow the 1-minute introductory video to understand, what this is all about:

**Important:** the brainpuzzler jobs on microworkers.com require this tutorial as a prerequisite!

Recognizing brain cells
-----------------------

Our goal is to reconstruct as many brain cells, or neurons, as possible. First, let us understand, how they look like. In general, all closed shapes with at least some round features most likely are brain cells. Below, we have highlighted some of them for you. Each color denotes a different neuron.
</div>
</div>


<div class="row">
<div class="3u">
Original image

<img src="{{ "/images/tutorial/neuron_no_mito.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
Highlighted neurons

<img src="{{ "/images/tutorial/neuron_no_mito_seg.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
Examples of neurons identifiable by their mainly round or oval shape.

Note, that it is even possible for neurons to enclose other neurons (green and blue neurons at the bottom).
</div>
</div>

<div class="row">
<div class="3u">
<img src="{{ "/images/tutorial/neuron_mito.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
<img src="{{ "/images/tutorial/neuron_mito_SEG.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
Many cells contain *mitochondria*, dark grey shapes within the neuron (indicated by the red arrows). As you can see, they have strong edges and a pattern of stripes and dots within. The shape next to the `X` might look like a mitochondrion at first glance. But its edge is fuzzier and it misses the characteristic texture inside.

When you see a Mitochondrion, you know that it must be enclosed by a neuron.
</div>
</div>

<div class="row">
<div class="3u">
<img src="{{ "/images/tutorial/neuron_myelin.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
<img src="{{ "/images/tutorial/neuron_myelin_seg.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
Probably, most easily recognizable *are myelinated brain cells* or *axons*. The neuron here is already identifiable by its mitochondrion at the top. But even more striking is its thick dark myelin "belt".
</div>
</div>


<div class="row">
<div class="3u">
<img src="{{ "/images/tutorial/ecs.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
<img src="{{ "/images/tutorial/ecs_seg.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
Finally, an example of *extracellular space*, the space *between* neurons: You can see that it is not very oval, but has many thin arms. We can intuitively see, that it does not look closed.

Being able to recognize extracellular space helps you to recognize neurons!
</div>
</div>

<div class="row">
<div class="12u">
While comparing the images you might feel unconfident about recognizing the shapes so easily. Don’t worry! When provided with moving images, your brain will automatically recognize connected objects.

Brain Reconstruction with **Knossos**
-------------------------------------

Let’s see how we can earn money with this knowledge and KNOSSOS, a free brain reconstruction tool:

1\.  Download **Knossos** (you will need it for all brainpuzzler jobs):
2\.  Download the tutorial job:
3\.  Start **Knossos** and drag the job into the KNOSSOS window. You should see something like this now:
</div>
</div>


<div class="row">
<div class="6u">
<img src="{{ "/images/tutorial/jobmode_initial.png" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
**Knossos** shows you a cube of brain data, where the center is brighter than the surrounding data. This center is your work area. Within it, you can already see an attempt on brain cell reconstruction (here in pink).

**Your job is to analyze the reconstruction and correct mistakes in it.**

The red label in the toolbar reading "`x more left`" shows you how many cases you have to look at.
</div>
</div>

<div class="row">
<div class="4u">
<img src="{{ "/images/tutorial/tutorial_pos_z2640.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="8u">
4\.  In the toolbar you see your current position in x, y and z coordinates. Scroll your mouse forward until you are at `z = 2640` (image left).
</div>
</div>

<div class="row">
<div class="8u">
5\.  Then press and hold the `[space]` key. This will hide the color overlay to reveal the structure beneath (image right). Remember the note about recognizing moving objects is easy for humans? This is **very** important here. Scroll forwards and
backwards fast while still holding the space key. You will make out the shape and see, that it is very round. It also contains a mitochondrion. It must be a neuron!
</div>
<div class="4u">
<img src="{{ "/images/tutorial/tutorial_pos_z2640_hidden.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
</div>

<div class="row">
<div class="4u">
6\.  Now again scroll around while pressing and releasing the [space] key repeatedly. This lets you compare the color overlay with the neuron. You will notice, that the shape was not successfully reconstructed:
</div>

<div class="4u">
<img src="{{ "/images/tutorial/tutorial_pos_z2640_neuron_highlight.png" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
<div class="4u">
<img src="{{ "/images/tutorial/tutorial_pos_z2640_overlay_errorhighlight.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
</div>


<div class="row">
<div class="4u">
<img src="{{ "/images/tutorial/tutorial_pos_z2640_fixed.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="8u">

7\.  Right click on the two missing puzzle pieces to add them to the reconstruction (image left). You can remove accidentally added pieces with \[Shift\] + Right Click.

8\.  Scroll to both ends of your work area to find all mistakes.

    Tip: There is still one more missing piece around z = 2650.

9\.  When satisfied with this reconstruction, press the [N] key for “next”. This will transport you to the next to-do item.

</div>
</div>

<div class="row">
<div class="8u">
10\. Again, the first step is to determine if this is a neuron. Scroll around while pressing/releasing [space]. You will notice the concave shape and thin arms. This most likely is extracellular space. Since we are only interested in neurons, always skip these cases by pressing [N].
</div>

<div class="4u">
<img src="{{ "/images/tutorial/tutorial_ecs_object.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
</div>


<div class="row">
<div class="12u">
11\. Examine the next case like the others before with scrolling and the [space] key. You will soon come to the conclusion, that this is no extracellular space. But still something is odd. It looks like the reconstruction has accidentally merged two neurons together!
</div>
</div>


<div class="row">
<div class="3u">
<img src="{{ "/images/tutorial/tutorial_merger_no_overlay_highlighted.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
<img src="{{ "/images/tutorial/tutorial_merger_overlay_error_highlighted.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="6u">
We call this a “wrong merger”, it can occur between neurons as well as neurons and extracellular space. If you encounter this, click on the button “split required >” in the toolbar. KNOSSOS remembers your note and provides you with the next case.
</div>
</div>

<div class="row tutorial__box--important">
<div class="6u">
When reconstructing neurons, you will notice that puzzle pieces rarely fit perfectly into a neuron’s shape. You don’t need to click “split required >” if a piece still mainly belongs to one neuron or extracellular space. Only use this functionality if you cannot tell to which shape the piece belongs. In this example no split is required:
</div>

<div class="3u">
<img src="{{ "/images/tutorial/no_split1.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>

<div class="3u">
<img src="{{ "/images/tutorial/no_split2.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
</div>

<div class="row">
<div class="12u">
12\. This time, there is nothing left to do, so KNOSSOS asks you to submit your work. Press “Yes” and wait a bit until a message box appears with your personal verification code (image below). Copy it and enter it on microworkers.com.

</div>

<div class="row">
<div class="6u">
<img src="{{ "/images/tutorial/tutorial_verification.PNG" | prepend: site.baseurl }}" alt="" class="image fit">
</div>
<div class="6u">
Within a week we will validate your work and issue payment for good reconstructions.
</div>
</div>

<div class="row">
<div class="12u">
KNOSSOS Commands Table
----------------------

| Command | Function |
|:--------|:---------|
| `Mouse scroll` | Move along z-axis
| `Left click and drag` | Move along x/y-axis
| `Space` | Hide puzzle overlay
| `Right click` | Add puzzle piece
| `Shift + Right click` | Remove puzzle piece
| `N` | Object finished, go to next one
| \[<Previous\] button | Go back to previous object
| \[?>\] button | Wrong piece, go to next


</div>
</div>