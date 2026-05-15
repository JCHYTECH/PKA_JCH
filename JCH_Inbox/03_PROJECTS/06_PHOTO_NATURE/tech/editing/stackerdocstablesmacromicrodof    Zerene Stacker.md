---
title: stacker:docs:tables:macromicrodof    [Zerene Stacker]
source: https://zerenesystems.com/cms/stacker/docs/tables/macromicrodof
author:
published:
created: 2026-04-14
description:
tags:
  - clippings
  - type/project
  - status/active
---
## DOF Estimates For Macro/Micro (depth of field, step sizes)

  
**NEW: –> [interactive calculator for macro/micro DOF](https://zerenesystems.com/cms/stacker/docs/dofcalculator "https://zerenesystems.com/cms/stacker/docs/dofcalculator")**

  
The best step size for macro/micro applications depends strongly on several things:

- Magnification
- Aperture setting
- Lens quality
- Resolution needed in the final result

So, if you need to determine an optimum step size for the purpose of shooting many similar stacks, then the best way to proceed is by a multi-step structured experiment:

1. Determine the magnification you need.
2. At that magnification, determine the smallest aperture (biggest f-number) that gives the resolution you need. A good way to do this is by running a short series of tests, varying the aperture setting.
3. At that magnification and aperture setting, determine the largest step size that does not give visible focus banding. A good way to do this is by shooting a single stack with a step size that is much smaller than you need, then processing the stack multiple times while changing the setting of Options > Preferences > Preprocessing > “Stack every N'th frame” to 1, 2, 3, 4, etc. Compare result images to find the largest N that does not give focus banding, then multiply the actual step size by N to find the optimum step size.

Take notes about what you find and you will quickly develop a table of settings and step sizes that are optimized for your own equipment, your own applications, and your own preferences. This table will be significantly different for different people.

However, if you're starting from scratch or doing a new type of stack, then surely you could use some guidance about what settings would be reasonable to start with. That's what the tables on this page are for.

Using these tables is essentially a three-step process with no experimentation:

1. Use Table 1 to determine magnification, by framing your subject and measuring the frame width.
2. Use a second table to choose an aperture setting and determine the associated DOF and maximum step size.
3. Adjust step size if desired, so as to give more overlap between focus bands and/or choose values that are simple to use with your setup. Many people like to use about 0.7 times the values given in these tables.

  
  
**Step 1: Determine Magnification From Frame Width**

To use Table 1, first frame your subject by adjusting lenses, bellows, etc. Measure the frame size by carefully placing a small ruler in front of the subject and adjusting the camera position to focus on the ruler. Then determine the approximate magnification by looking it up in this table. Probably your number will fall between two table entries. In that case just pick the closer value or interpolate to get a more accurate value.

Or if you like, you can just use a calculator: magnification = sensor width / frame width.

***Table 1*** – *Determine magnification from frame width and sensor size*

<table><tbody><tr><th></th><th colspan="3">Sensor Size</th></tr><tr><th>Frame Width</th><th>Four-Thirds</th><th>APS-C (1.6X crop)</th><th>Full Frame (36×24 mm)</th></tr><tr><th>500.0 mm</th><td>0.036</td><td>0.046</td><td>0.072</td></tr><tr><th>350.0 mm</th><td>0.051</td><td>0.066</td><td>0.10</td></tr><tr><th>250.0 mm</th><td>0.072</td><td>0.092</td><td>0.14</td></tr><tr><th>200.0 mm</th><td>0.090</td><td>0.12</td><td>0.18</td></tr><tr><th>140.0 mm</th><td>0.13</td><td>0.16</td><td>0.26</td></tr><tr><th>100.0 mm</th><td>0.18</td><td>0.23</td><td>0.36</td></tr><tr><th>70.0 mm</th><td>0.26</td><td>0.33</td><td>0.51</td></tr><tr><th>50.0 mm</th><td>0.36</td><td>0.46</td><td>0.72</td></tr><tr><th>35.0 mm</th><td>0.51</td><td>0.66</td><td>1.0</td></tr><tr><th>25.0 mm</th><td>0.72</td><td>0.92</td><td>1.4</td></tr><tr><th>20.0 mm</th><td>0.90</td><td>1.2</td><td>1.8</td></tr><tr><th>14.0 mm</th><td>1.3</td><td>1.6</td><td>2.6</td></tr><tr><th>10.0 mm</th><td>1.8</td><td>2.3</td><td>3.6</td></tr><tr><th>7.0 mm</th><td>2.6</td><td>3.3</td><td>5.1</td></tr><tr><th>5.0 mm</th><td>3.6</td><td>4.6</td><td>7.2</td></tr><tr><th>3.5 mm</th><td>5.1</td><td>6.6</td><td>10</td></tr><tr><th>2.5 mm</th><td>7.2</td><td>9.2</td><td>14</td></tr><tr><th>2.0 mm</th><td>9.0</td><td>12</td><td>18</td></tr><tr><th>1.4 mm</th><td>13</td><td>16</td><td>26</td></tr><tr><th>1.0 mm</th><td>18</td><td>23</td><td>36</td></tr></tbody></table>

Numbers in the above table can be reproduced as magnification = SensorWidth / FrameWidth.  
Example: Frame width 70 mm on full frame (sensor width 36 mm) computes as magnification = 36 / 70 = 0.5143.

  
  
**Step 2: Determine Aperture and Step Size**

Now that you know the magnification, you can use one of the following tables to estimate best aperture and step size.  
  

The first **Table 2-A** is for users who fit any of the following profiles:

- All users of twist-to-focus macro lenses, except for modern Nikons. (There's a separate table below for them.)
- All users of normal or enlarging lenses on bellows or extension tubes.

In most rows of the table, a range of values appears in bold face. If you're using a camera with an APS-C size sensor (“crop factor” 1.5 or 1.6), then you should pick a value near the middle of the bold range. Full-frame users should choose from the right side (larger f-numbers); Four-Thirds users choose from the left side (smaller f-numbers). Entries in italics should be avoided if possible because those combinations will lose significant sharpness from diffraction.

***Table 2-A*** – *Determine DOF (step size) from magnification and *nominal* f-number*

<table><tbody><tr><th colspan="9">Table for most twist-to-focus lenses, bellows or extension tubes</th></tr><tr><th></th><th colspan="8">Nominal f-number (Four-Thirds, APS-C, Full-Frame)</th></tr><tr><th>Magnification</th><th>f/2.0</th><th>f/2.8</th><th>f/4.0</th><th>f/5.6</th><th>f/8.0</th><th>f/11.0</th><th>f/16.0</th><th>f/22.0</th></tr><tr><th>0.035</th><td>7.7 mm</td><td>15 mm</td><td>31 mm</td><td>60 mm</td><td><strong>123 mm</strong></td><td><strong>233 mm</strong></td><td><strong>493 mm</strong></td><td><em>931 mm</em></td></tr><tr><th>0.050</th><td>3.9 mm</td><td>7.6 mm</td><td>16 mm</td><td>30 mm</td><td><strong>62 mm</strong></td><td><strong>117 mm</strong></td><td><strong>248 mm</strong></td><td><em>470 mm</em></td></tr><tr><th>0.070</th><td>2.1 mm</td><td>4.0 mm</td><td>8.2 mm</td><td>16 mm</td><td><strong>33 mm</strong></td><td><strong>62 mm</strong></td><td><strong>132 mm</strong></td><td><em>249 mm</em></td></tr><tr><th>0.10</th><td>1.1 mm</td><td>2.1 mm</td><td>4.3 mm</td><td>8.3 mm</td><td><strong>17 mm</strong></td><td><strong>32 mm</strong></td><td><strong>68 mm</strong></td><td><em>129 mm</em></td></tr><tr><th>0.14</th><td>0.58 mm</td><td>1.1 mm</td><td>2.3 mm</td><td>4.6 mm</td><td><strong>9.3 mm</strong></td><td><strong>18 mm</strong></td><td><em>37 mm</em></td><td><em>71 mm</em></td></tr><tr><th>0.20</th><td>0.32 mm</td><td>0.62 mm</td><td>1.3 mm</td><td>2.5 mm</td><td><strong>5.1 mm</strong></td><td><strong>9.6 mm</strong></td><td><em>20 mm</em></td><td><em>38 mm</em></td></tr><tr><th>0.25</th><td>0.22 mm</td><td>0.43 mm</td><td>0.88 mm</td><td>1.7 mm</td><td><strong>3.5 mm</strong></td><td><strong>6.7 mm</strong></td><td><em>14 mm</em></td><td><em>27 mm</em></td></tr><tr><th>0.35</th><td>0.13 mm</td><td>0.26 mm</td><td>0.52 mm</td><td><strong>1.0 mm</strong></td><td><strong>2.1 mm</strong></td><td><strong>4.0 mm</strong></td><td><em>8.4 mm</em></td><td><em>16 mm</em></td></tr><tr><th>0.50</th><td>0.079 mm</td><td>0.16 mm</td><td>0.32 mm</td><td><strong>0.62 mm</strong></td><td><strong>1.3 mm</strong></td><td><strong>2.4 mm</strong></td><td><em>5.1 mm</em></td><td><em>9.6 mm</em></td></tr><tr><th>0.70</th><td>0.052 mm</td><td>0.10 mm</td><td>0.21 mm</td><td><strong>0.41 mm</strong></td><td><strong>0.83 mm</strong></td><td><em>1.6 mm</em></td><td><em>3.3 mm</em></td><td><em>6.3 mm</em></td></tr><tr><th>1.0</th><td>0.035 mm</td><td>0.069 mm</td><td><strong>0.14 mm</strong></td><td><strong>0.28 mm</strong></td><td><strong>0.56 mm</strong></td><td><em>1.1 mm</em></td><td><em>2.3 mm</em></td><td><em>4.3 mm</em></td></tr><tr><th>1.4</th><td>0.026 mm</td><td>0.051 mm</td><td><strong>0.10 mm</strong></td><td><strong>0.20 mm</strong></td><td><em>0.41 mm</em></td><td><em>0.78 mm</em></td><td><em>1.7 mm</em></td><td><em>3.1 mm</em></td></tr><tr><th>2.0</th><td>0.020 mm</td><td><strong>0.039 mm</strong></td><td><strong>0.079 mm</strong></td><td><strong>0.16 mm</strong></td><td><em>0.32 mm</em></td><td><em>0.60 mm</em></td><td><em>1.3 mm</em></td><td><em>2.4 mm</em></td></tr><tr><th>2.5</th><td>0.017 mm</td><td><strong>0.034 mm</strong></td><td><strong>0.069 mm</strong></td><td><em>0.14 mm</em></td><td><em>0.28 mm</em></td><td><em>0.52 mm</em></td><td><em>1.1 mm</em></td><td><em>2.1 mm</em></td></tr><tr><th>3.5</th><td><strong>0.014 mm</strong></td><td><strong>0.028 mm</strong></td><td><strong>0.058 mm</strong></td><td><em>0.11 mm</em></td><td><em>0.23 mm</em></td><td><em>0.44 mm</em></td><td><em>0.93 mm</em></td><td><em>1.8 mm</em></td></tr><tr><th>5.0</th><td><strong>0.013 mm</strong></td><td><strong>0.025 mm</strong></td><td><em>0.051 mm</em></td><td><em>0.099 mm</em></td><td><em>0.20 mm</em></td><td><em>0.38 mm</em></td><td><em>0.81 mm</em></td><td><em>1.5 mm</em></td></tr><tr><th>7.0</th><td><strong>0.011 mm</strong></td><td><em>0.022 mm</em></td><td><em>0.046 mm</em></td><td><em>0.090 mm</em></td><td><em>0.18 mm</em></td><td><em>0.35 mm</em></td><td><em>0.74 mm</em></td><td><em>1.4 mm</em></td></tr><tr><th>10</th><td><em>0.011 mm</em></td><td><em>0.021 mm</em></td><td><em>0.042 mm</em></td><td><em>0.083 mm</em></td><td><em>0.17 mm</em></td><td><em>0.32 mm</em></td><td><em>0.68 mm</em></td><td><em>1.3 mm</em></td></tr><tr><th>14</th><td><em>0.0100 mm</em></td><td><em>0.020 mm</em></td><td><em>0.040 mm</em></td><td><em>0.079 mm</em></td><td><em>0.16 mm</em></td><td><em>0.31 mm</em></td><td><em>0.65 mm</em></td><td><em>1.2 mm</em></td></tr><tr><th>20</th><td><em>0.0096 mm</em></td><td><em>0.019 mm</em></td><td><em>0.039 mm</em></td><td><em>0.076 mm</em></td><td><em>0.16 mm</em></td><td><em>0.29 mm</em></td><td><em>0.62 mm</em></td><td><em>1.2 mm</em></td></tr></tbody></table>

Numbers in the above table can be closely reproduced by the simplified formula  
DOF = (0.0022\*N\*N\*(m+1)\*(m+1))/(m\*m), where N is the F-number and m is magnification.  
Example: F-number 5.6 and magnification 0.50 computes as DOF = (0.0022\*5.6\*5.6\*(0.50+1)\*(0.50+1))/(0.50\*0.50) = 0.6209.

  
  
The following **Table 2-B** is for users who fit any of the following profiles:

- All users of modern Nikon macro lenses whose minimum f-number changes depending on magnification. (When using these lenses, the value you set into the camera is actually the “effective aperture”, already corrected for magnification.)
- All users of add-on closeup lenses (“diopter filters”).
- All users of “reversed lens combos” (short reversed in front of long), when aperture is set on the rear lens.
- All users of “reversed lens combos”, when aperture is set on the front lens AND effective aperture is calculated as front lens f-number \* magnification.  
	Example: 50 mm f/5.6 on the front, 100 mm on the rear, magnification = 100/50 = 2.0, effective aperture = 2\*5.6 = f/11, use the f/11.0 column of the table to find DOF = 0.067 mm.

As before, a range of values appears in bold face. If you're using a camera with an APS-C size sensor (“crop factor” 1.5 or 1.6), then you should pick a value near the middle of the bold range. Full-frame users should choose from the right side (larger f-numbers); Four-Thirds users choose from the left side (smaller f-numbers). Entries in italics should be avoided if possible because those combinations will lose significant sharpness from diffraction.

***Table 2-B*** – *Determine DOF (step size) from magnification and *effective* f-number*

<table><tbody><tr><th colspan="9">Table for new Nikon twist-to-focus lenses, add-on closeup lenses, and combos by effective aperture</th></tr><tr><th></th><th colspan="8">Effective aperture = f-number shown on camera (Four-Thirds, APS-C, Full-Frame)</th></tr><tr><th>Magnification</th><th>f/2.0</th><th>f/2.8</th><th>f/4.0</th><th>f/5.6</th><th>f/8.0</th><th>f/11.0</th><th>f/16.0</th><th>f/22.0</th></tr><tr><th>0.10</th><td>0.88 mm</td><td>1.7 mm</td><td>3.5 mm</td><td>6.9 mm</td><td><strong>14 mm</strong></td><td><strong>27 mm</strong></td><td><strong>56 mm</strong></td><td><em>106 mm</em></td></tr><tr><th>0.14</th><td>0.45 mm</td><td>0.88 mm</td><td>1.8 mm</td><td>3.5 mm</td><td><strong>7.2 mm</strong></td><td><strong>14 mm</strong></td><td><strong>29 mm</strong></td><td><em>54 mm</em></td></tr><tr><th>0.20</th><td>0.22 mm</td><td>0.43 mm</td><td>0.88 mm</td><td>1.7 mm</td><td><strong>3.5 mm</strong></td><td><strong>6.7 mm</strong></td><td><strong>14 mm</strong></td><td><em>27 mm</em></td></tr><tr><th>0.25</th><td>0.14 mm</td><td>0.28 mm</td><td>0.56 mm</td><td>1.1 mm</td><td><strong>2.3 mm</strong></td><td><strong>4.3 mm</strong></td><td><strong>9.0 mm</strong></td><td><em>17 mm</em></td></tr><tr><th>0.35</th><td>0.072 mm</td><td>0.14 mm</td><td>0.29 mm</td><td>0.56 mm</td><td><strong>1.1 mm</strong></td><td><strong>2.2 mm</strong></td><td><strong>4.6 mm</strong></td><td><em>8.7 mm</em></td></tr><tr><th>0.50</th><td>0.035 mm</td><td>0.069 mm</td><td>0.14 mm</td><td>0.28 mm</td><td><strong>0.56 mm</strong></td><td><strong>1.1 mm</strong></td><td><strong>2.3 mm</strong></td><td><em>4.3 mm</em></td></tr><tr><th>0.70</th><td>0.018 mm</td><td>0.035 mm</td><td>0.072 mm</td><td>0.14 mm</td><td><strong>0.29 mm</strong></td><td><strong>0.54 mm</strong></td><td><strong>1.1 mm</strong></td><td><em>2.2 mm</em></td></tr><tr><th>1.0</th><td>0.0087 mm</td><td>0.017 mm</td><td>0.035 mm</td><td>0.069 mm</td><td><strong>0.14 mm</strong></td><td><strong>0.27 mm</strong></td><td><strong>0.56 mm</strong></td><td><em>1.1 mm</em></td></tr><tr><th>1.4</th><td>0.0043 mm</td><td>0.0087 mm</td><td>0.018 mm</td><td>0.035 mm</td><td><strong>0.072 mm</strong></td><td><strong>0.14 mm</strong></td><td><strong>0.29 mm</strong></td><td><em>0.54 mm</em></td></tr><tr><th>2.0</th><td>0.0021 mm</td><td>0.0042 mm</td><td>0.0087 mm</td><td>0.017 mm</td><td><strong>0.035 mm</strong></td><td><strong>0.066 mm</strong></td><td><strong>0.14 mm</strong></td><td><em>0.27 mm</em></td></tr><tr><th>2.5</th><td>0.0013 mm</td><td>0.0026 mm</td><td>0.0055 mm</td><td>0.011 mm</td><td><strong>0.022 mm</strong></td><td><strong>0.042 mm</strong></td><td><strong>0.090 mm</strong></td><td><em>0.17 mm</em></td></tr><tr><th>3.5</th><td>0.00053 mm</td><td>0.0013 mm</td><td>0.0027 mm</td><td>0.0055 mm</td><td><strong>0.011 mm</strong></td><td><strong>0.022 mm</strong></td><td><strong>0.046 mm</strong></td><td><em>0.087 mm</em></td></tr><tr><th>5.0</th><td>—</td><td>0.00050 mm</td><td>0.0013 mm</td><td>0.0026 mm</td><td><strong>0.0055 mm</strong></td><td><strong>0.011 mm</strong></td><td><strong>0.022 mm</strong></td><td><em>0.042 mm</em></td></tr></tbody></table>

Numbers in the above table can be closely reproduced by the simplified formula  
DOF = (0.0022\*N\*N)/(m\*m), where N is the F-number and m is magnification.  
Example: F-number 5.6 and magnification 0.50 computes as DOF = (0.0022\*5.6\*5.6)/(0.50\*0.50) = 0.2760.

  
  
This final Table 2-C is for users of microscope objectives. In this case, step size is estimated entirely from the NA rating (Numerical Aperture) of the objective.

***Table 2-C*** – *Determine DOF (step size) from Numerical Aperture (NA)*

<table><tbody><tr><th colspan="2">Microscope Objectives</th></tr><tr><th>NA</th><th>DOF</th></tr><tr><td>0.1</td><td>0.055 mm</td></tr><tr><td>0.14</td><td>0.028 mm</td></tr><tr><td>0.2</td><td>0.014 mm</td></tr><tr><td>0.25</td><td>0.0087 mm</td></tr><tr><td>0.3</td><td>0.0060 mm</td></tr><tr><td>0.4</td><td>0.0033 mm</td></tr><tr><td>0.5</td><td>0.0021 mm</td></tr><tr><td>0.55</td><td>0.0017 mm</td></tr></tbody></table>

Numbers in the above table can be closely reproduced by the simplified formula DOF = 0.00055/(NA\*NA).  
Example: NA 0.25 computes as DOF = 0.00055/(0.25\*0.25) = 0.0088.

  
  
**Notes:** You may be surprised that there's nothing in these tables about circle of confusion (COC), like you'd find in most DOF tables. That's because COC is essentially bundled into your choice of aperture. Once you've chosen the aperture setting, then using the numbers in these tables will guarantee that you won't see “focus banding” no matter how good a camera or lens you're using, or how closely you choose to look at the captured images. The math underlying these tables makes assumptions that are reasonable for most lenses, then proceeds using a math formulation that is based on wave optics and guarantees no more than 1/4-lambda wavefront error for green light at the worst focus distances. Roughly speaking, this corresponds to no loss of fine detail and no more than 26% reduction of MTF at any spatial frequency. If you need to operate far to the left of the bold section, say to get particularly soft bokeh, then the step sizes listed here will be unnecessarily small because resolution will be limited by the camera sensor and not the optics. In that case a better estimate would be provided by the [interactive DOF calculator](https://zerenesystems.com/cms/stacker/docs/dofcalculator "https://zerenesystems.com/cms/stacker/docs/dofcalculator"), using COC set to approximately twice the pixel pitch. Send email to [support@zerenesystems.com](mailto:support@zerenesystems.com "support@zerenesystems.com") if you want more information.