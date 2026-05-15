---
tags:
  - type/project
  - status/active
---
# AI for Highlight Recovery

**Created:** 2026-01-26 12:54  
**Updated:** 2026-01-26 16:37  
**Messages:** 4

---

## Human
*2026-01-26 12:54*

I have a picture with burned highlights. I imagine that AI could "invent" burned highlights features how would you do

---

## Assistant
*2026-01-26 12:54*

As of 13:00 (Europe/Brussels).

Yes—AI can “invent” detail in blown highlights, but it is important to separate two cases:

If highlights are clipped (pure white, no channel detail), there is no true information to recover. Anything that appears as “recovered detail” is a plausible reconstruction. That can be acceptable for creative work, but it is not forensic/faithful restoration.

If highlights are not fully clipped (detail exists in at least one channel or in the RAW headroom), classic RAW recovery will usually outperform AI and will be more truthful.

How I would do it, in practice, in 3 tiers (from most faithful to most “inventive”)

1) Try to actually recover data first (best fidelity)
- Work from the RAW file if you have it (not JPEG).
- In Lightroom / Adobe Camera Raw:
  - Reduce Highlights aggressively.
  - Reduce Whites a bit.
  - Pull Exposure down slightly only if needed.
  - Use the Tone Curve to compress the top end (a gentle roll-off).
  - Enable/try the profile choice (Adobe Color vs Camera profiles) because some profiles clip earlier than others.
- Masking:
  - Select Sky / Select Subject / Luminance Range mask for the brightest areas, then lower Highlights/Whites locally.
  - Add a little Dehaze/Texture only after you’ve tamed clipping (otherwise you exaggerate ugly edges).
- If one channel still has information:
  - In Photoshop: use channel inspection to see if (for example) the blue channel retains cloud structure while red/green are clipped; you can sometimes rebuild luminance from the best channel (technical but very effective).

This route is “recovery,” not invention.

2) If it’s clipped: reconstruct with “plausible detail” (AI/inpainting approach)
This is where AI helps. The workflow is essentially: identify the blown region → ask an AI model to synthesize texture consistent with the surroundings → blend so it looks physically believable.

A robust method in Photoshop:
- Make a precise selection of the blown area (Select > Color Range for whites, then refine; or a luminosity mask).
- Expand the selection slightly (1–3 px) and feather it (0.5–2 px) to avoid seams.
- Create a new layer and use Generative Fill (or similar) with a constrained prompt, for example:
  - “Reconstruct subtle cloud texture consistent with surrounding sky, natural lighting, no dramatic clouds.”
  - Or for specular highlights on water: “Add fine ripple texture consistent with adjacent water, maintain same direction and scale.”
- Generate a few variants, pick the one that matches perspective and lighting.
- Blend:
  - Set the generated layer to “Luminosity” or “Normal” depending on results.
  - Use a soft mask to fade in, especially near transitions.
  - Add slight noise/grain to match the original (generated areas can look too clean).
  - Use Curves on the generated layer to match brightness roll-off; highlights should still feel bright, just not flat white.

Key point: do not ask AI for “more detail” generically. Constrain it to “subtle texture, consistent with surroundings,” otherwise you get unrealistic micro-contrast.

3) Hybrid “physically plausible” reconstruction (best-looking for demanding images)
For skies, reflective surfaces, and skin, the most convincing results usually come from a hybrid:
- AI synthesizes texture.
- You restore believable highlight falloff manually:
  - Paint a gentle gradient (on a separate layer) to recreate the light’s roll-off.
  - Then overlay AI texture at low opacity, so it looks like texture inside light, not pasted-on detail.

Practical decision rules
- If it is a documentary/wildlife record shot where truth matters: stay in Tier 1 as much as possible; avoid “inventing” detail that could be misleading.
- If it is an artistic image: Tier 2–3 is fine; just make the result consistent in direction of light, scale of texture, and noise.

If you want, upload the image (and tell me whether you have the RAW or only a JPEG). I can tell you which tier applies (clipped or recoverable) and give you an exact Photoshop/Lightroom step plan tailored to your photo (sky, water, feathers, etc.).

---

## Human
*2026-01-26 16:36*

[Image]
raw available

---

## Assistant
*2026-01-26 16:36*

Thank you. This image is a very good example, and having the RAW makes a substantial difference.

I will proceed in three parts:
1) Objective diagnosis of the highlights in *this specific image*
2) What can be genuinely recovered from the RAW (no invention)
3) Where and how AI “invention” makes sense here, with a controlled workflow adapted to water + backlight + birds

I will not generate an edited image yet; this is the technical reading first, as you requested earlier.

---

1) Technical diagnosis of your highlights

Looking at the image, there are **three different highlight regimes**, and they must not be treated the same way:

A) The glitter path on the water (horizontal bright band)  
- Many pixels are **fully clipped** (pure white or near-white in all RGB channels).
- These are specular reflections of the sun → physically, they *are allowed* to be pure white.
- Trying to “recover” all of this would destroy the realism.

B) The rim light on the ducks (edges of head, neck, back)  
- These highlights are **not fully clipped** in the RAW in most cases.
- There is feather structure hidden in at least one channel.
- This is recoverable, not invented.

C) The bright halo around the waterline near the bodies  
- Mixed case: partially clipped + bloom.
- Needs compression, not texture reconstruction.

Conclusion:  
Only **part of the bright water band** is a candidate for AI reconstruction. The birds themselves should be handled almost entirely with classical RAW recovery.

---

2) What I would do first in Lightroom / ACR (truthful recovery)

Work only on the RAW at this stage.

Global settings (starting point, not dogma):
- Exposure: do NOT lower aggressively (−0.1 to −0.2 max)
- Highlights: −80 to −100
- Whites: −20 to −35
- Contrast: slightly down (−5 to −10)
- Texture: 0 for now
- Clarity: −5 (important to avoid crunchy halos)
- Dehaze: 0 (do not touch yet)

Tone Curve:
- Add a soft highlight roll-off:
  - Pull the top-right point slightly down
  - Add a control point just below highlights to maintain midtone separation
This preserves “sun intensity” while killing the hard clipping feel.

Masks:
- Subject mask (ducks):
  - Highlights −60 to −80
  - Whites −20
  - Texture +10 to +15 (only here)
- Luminance range mask on brightest pixels (water glitter):
  - Do NOT try to recover detail
  - Simply reduce Highlights −30 to −40 to soften the burn

At this point, you will already see:
- More feather structure on rim-lit areas
- Less aggressive glare
- Still some pure white sparkles (this is correct)

If you see zebra warnings disappear on the ducks but remain on the water, that is the expected outcome.

---

3) Where AI reconstruction actually makes sense here

Now the important part: **where invention is acceptable and useful**.

Do NOT use AI on:
- The ducks’ bodies or heads
- Feather edges
These must remain faithful.

Use AI ONLY on:
- The *horizontal specular band on the water*, and only partially
- Goal: replace dead white plates with *micro-structure* consistent with surrounding ripples

Why this works artistically:
- Water highlights are chaotic by nature
- The viewer has no reference expectation for exact sparkle placement
- This is a perfect domain for plausible synthesis

---

4) Controlled AI workflow (Photoshop, professional approach)

Preparation:
- Send the image to Photoshop as a Smart Object.
- Duplicate the layer.

Selection:
- Use Select > Color Range > Highlights
- Refine manually to isolate only the **blown water band**
- Exclude birds completely
- Expand selection 2 px, feather 1 px

AI generation (Generative Fill or equivalent):
Prompt example (important to be restrained):
“Subtle water ripple texture consistent with surrounding surface, same lighting direction, no dramatic highlights”

Key rules:
- Avoid words like “sunlight,” “sparkle,” or “bright”
- You want texture *inside* light, not more light

Generate several variants and choose the calmest one.

Blending:
- Reduce opacity to 30–60%
- Add a layer mask and gently fade near the birds
- Add noise (Gaussian, monochromatic, very low) to match sensor grain
- Optionally set blend mode to **Luminosity** if color shifts appear

Final physical plausibility pass:
- Add a very gentle Curves adjustment above everything:
  - Ensure highlights still peak near white
  - Do not flatten the image

---

5) What not to do (important)

- Do not globally “AI enhance” the image.
- Do not ask AI to “recover highlights” generically.
- Do not remove all pure white points: specular highlights must remain.
- Do not sharpen before highlight reconstruction.

---

6) Ethical / documentary note (since you do wildlife)

For wildlife photography, this workflow is defensible if:
- AI is restricted to water or background
- The animal’s morphology and lighting remain untouched
- The result respects the original light direction and intensity

This would be unacceptable only if you invented feather detail or changed the bird’s appearance—which you are not doing here.

---

If you want, next steps could be:
- I give you **exact Lightroom numeric values** tailored to this RAW
- Or I define a **dedicated “Backlit Water – Highlight Repair” preset**
- Or we do a **before/after conceptual diagram** explaining where AI is allowed vs forbidden (useful if you ever publish)

Tell me how far you want to go.

---
