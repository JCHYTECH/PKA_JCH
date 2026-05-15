---
tags:
  - type/project
  - status/active
---
# WeMacro rail settle time

**Created:** 2026-03-14 19:52  
**Updated:** 2026-03-14 19:53  
**Messages:** 5

---

## Human
*2026-03-14 19:52*

using we macro rail. if I put a value 0 in the field stable after movement, is will work ?

---

## Assistant
*2026-03-14 19:52*

Je vérifie la signification exacte de ce paramètre dans l’écosystème WeMacro, puis je te dis dans quels cas 0 fonctionne réellement et quand c’est une mauvaise idée.

---

## Assistant
*2026-03-14 19:52*

Yes, usually it will still run.

On the WeMacro rail, that field corresponds to the settle time after each movement step before the shutter is triggered. The manual defines it as the waiting time after each step, and notes that it depends on camera behavior and sometimes flash recharge time. citeturn954925view3turn115421view3

So if you put `0`, the rail will generally interpret that as “no extra waiting.” That can work when:
- the setup is very rigid,
- magnification is not extreme,
- there is no residual vibration,
- the camera is ready immediately,
- and the flash has fully recycled in time. citeturn954925view3turn456265search16

But `0` can also cause problems:
- slight blur from vibration,
- inconsistent sharpness at high magnification,
- missed or weak flash exposures if recycle time is too short,
- occasional timing issues if the camera needs a moment to process frames. citeturn954925view3turn456265search16

My practical advice:
start with `0` only for testing. If you see softness or irregular frames, increase it a little, for example by small increments, until the stack becomes fully consistent. With high-mag macro, some non-zero settle time is often safer. This is an inference from the parameter’s purpose and the manual’s timing notes. citeturn954925view3turn456265search16

20:52

If you want, I can suggest a good starting value for your specific setup, for example flash/no flash, magnification, and whether you use the 90D or the R10.

---

## Human
*2026-03-14 19:53*

ok

---

## Assistant
*2026-03-14 19:53*

Here is a practical starting grid for the WeMacro rail parameter “stable after movement”.

For `0 ms`:
use it only for quick tests, low magnification, and a very rigid setup. It may work, but it is not my preferred production value.

Good starting values:

With flash:
- 1:1 to 2:1 → `100 to 200 ms`
- 2:1 to 5:1 → `200 to 400 ms`
- above 5:1 → `300 to 600 ms`

Without flash:
- 1:1 to 2:1 → `200 to 400 ms`
- 2:1 to 5:1 → `400 to 800 ms`
- above 5:1 → `800 ms to 1500 ms`

Why flash often needs less:
the flash duration freezes motion, so the main issue is rail/camera settling and flash recycle. Without flash, any residual vibration during the exposure is more critical.

For your cameras:
- Canon 90D: start at `200 ms`
- Canon R10: start at `150–200 ms`

If you use a heavy setup on the rail, or a long lens, increase the delay a bit.

My default recommendation for a safe first test:
- macro with flash: `200 ms`
- high magnification with flash: `300 ms`
- macro without flash: `500 ms`

Simple method to optimize:
shoot the same short stack at `0`, `100`, `200`, and `300 ms`. Then compare one frame near the middle at 100% magnification. Keep the lowest value that gives perfectly repeatable sharpness.

If your flash is not always fully recycled, then the issue is not only “stable after movement”; you may need more delay mainly for flash recharge.

20:54

Tell me your exact configuration, for example lens, magnification, flash or continuous light, and camera body, and I’ll give you a tighter recommended value.

---
