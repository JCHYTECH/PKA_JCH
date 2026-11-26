# Transcript — « Ultra Long Battery Life for ESPHome/Arduino »

- **Source** : Tech Dregs
- **URL** : https://youtu.be/oVrDZNoOu6s
- **Durée** : 14:37
- **Date** : 2026-03-08
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 377

---

[00:01] Hey kid, you want some battery life?
[00:05] So I made another little product that some people might be interested in.
[00:10] So a lot of home automation sensors that you make for projects like ESP Home to work with Home Assistant,
[00:17] they run on batteries and they don't really need to do much most of the time.
[00:21] So think of like a a window sensor, a leak detector, some sort of monitoring system.
[00:27] It really only needs to like send you data when a state changes or a threshold is crossed.
[00:34] And other than that, really it just needs to send like a heartbeat once a day.
[00:38] And that means those types of devices stay off like 99% of their life.
[00:45] They just don't do anything unless something happens they need to let you know about.
[00:49] And if those things are running on a battery, that means one of the major factors
[00:53] in the amount of battery life that you're going to get is how much power they use
[00:56] when they're in those ultra low power states like deep sleep.
[01:00] And it turns out that things like the ESP32,
[01:04] they're okay as far as their deep sleep power efficiency, but not that great.
[01:10] And when they're in those low power deep sleep states,
[01:12] they can chew through battery a little quicker than you might expect.
[01:16] You know, that's one of the trade-offs with using stuff like an ESP32s.
[01:20] They do tend to use a little bit more power.
[01:22] Now, if that's something you're concerned about,
[01:24] you really want to maximize battery life for being able to use smaller batteries,
[01:28] this little board might come in handy
[01:32] because it can reduce deep sleep power consumption on ESP32
[01:37] by a factor of like 50 or 100,
[01:41] which can increase battery life quite significantly.
[01:45] Now, even though I am talking mostly about ESP32 and ESP Home Focus stuff,
[01:50] just so you're aware, I have also written C libraries for this device
[01:56] so that you can use it on STM32 or Arduino projects.
[02:00] So let's take a look at this thing and I'll show you what's going on.
[02:03] So this is a power supply designed for embedded projects.
[02:07] So this is a JSTPH connector,
[02:09] which is pretty standard on lipo little pouch cells
[02:11] that you can get off at Amazon or AliExpress or anywhere like that.
[02:15] We've got built-in battery charging
[02:18] and so this will help make sure that your battery is managed well and not overcharged.
[02:22] Now, it's got a little onboard 3.3 volt regulator
[02:25] also and that's capable of outputting up to 1 amp of current
[02:29] because I figured if I'm going to make a standalone power supply,
[02:32] it ought to be able to handle most projects.
[02:35] So on the backside,
[02:36] you'll see that there's an input for 5 volts and an output for 3.3 volts.
[02:40] So do be aware, if you power this thing off of a 5 volt input,
[02:44] it's not going to produce a 3.3 volt output.
[02:47] The 3.3 volt output only comes from the battery line
[02:51] and that's because in most cases,
[02:53] if you connect this to a dev board and you power the dev board from USB
[02:57] and you tie that to this 5 volt input,
[03:00] you're going to get into a fight between the onboard voltage regulator
[03:04] on your dev board and this power supply.
[03:06] So to prevent that,
[03:07] the 3.3 volt will be disabled on this board
[03:11] if you're powering your dev board from 5 volts and this from 5 volts.
[03:15] That just avoids any problems with those regulators fighting each other.
[03:19] So the next pin on here is a little battery sense pin.
[03:23] That will be for a voltage divider
[03:25] so that you can measure your battery voltage at any point you want.
[03:29] And so now I should probably explain
[03:30] what's actually going on on this board
[03:32] and how it's able to achieve such low current draws.
[03:34] So right here is an RTC, a real time clock chip.
[03:39] Specifically, this is an Epson RX8111CE chip.
[03:44] This thing draws phenomenally low current.
[03:47] Something on the order of 100 nanoamps.
[03:51] In my testing, this board ends up drawing
[03:54] somewhere around 160 to 170 nanoamps
[03:58] when used as intended, which is.
[04:01] This little chip has some unique features.
[04:03] One of them is that you can set alarms on it.
[04:06] The alarms can last up to a month
[04:09] and when the alarm goes off, it pulls a pin low
[04:12] and I've got a little power MOSFET here
[04:14] so that when that pin goes low,
[04:17] it turns on the power to your device.
[04:20] And so what this is intended to do
[04:22] is basically replace the deep sleep of your ESP32.
[04:27] Instead of putting your device into deep sleep,
[04:29] you set a timer on the RTC
[04:32] and then the RTC can turn off power to your entire system.
[04:37] Now it stays on because it can be powered
[04:40] directly from battery current.
[04:42] It can accept anything from somewhere
[04:45] around like one and a half volts all the way up to,
[04:47] I don't know, five or six volts direct.
[04:49] It doesn't need a voltage regulator
[04:51] and that means it can stay powered on
[04:53] during phenomenally low currents
[04:56] while the rest of your system draws literally nothing.
[04:59] And so with this, you're able to have a device
[05:03] which puts itself into deep sleep,
[05:06] draws well under 200 nanoamps of current
[05:09] and still has the ability to wake itself up
[05:12] at any time you want for as long as one month.
[05:16] Okay, so let's do a little demo
[05:19] and I have one of these hooked up to a regular ESP32
[05:24] and you're seeing Nordic power profiler on the screen
[05:27] and I'm beating it four volts
[05:29] and so you can see the power draw,
[05:31] normal ESP32 power draw here.
[05:33] So let's show you what happens
[05:35] whenever you kick on the RTC
[05:37] and turn the device off.
[05:39] So I've got a 15 second timer and there we've started.
[05:43] So you can see that this thing will sleep for a bit.
[05:46] I'm calling it sleep.
[05:47] It's not really a sleep.
[05:48] It's a power off state and then it will wake itself back up
[05:53] and again, that's the RTC turning the device back on.
[05:57] So there we go.
[05:57] So now we can show the average power draw 0.19 microamps.
[06:03] That's 190 nanoamps.
[06:05] Now in my testing,
[06:07] I've been seeing somewhere around 0.16.
[06:10] One thing to note about what's going on here
[06:13] is that the Nordic power profiler
[06:15] is only accurate to within like 100 nanoamps.
[06:19] So it actually isn't designed
[06:22] to measure quite this low level of current
[06:25] and so the accuracy here again,
[06:28] I've seen anywhere from like 0.15 to 0.2 microamps of current.
[06:34] As an example, I just ran another shot
[06:36] and it's down to 0.18 microamps or 180.
[06:41] At this low of power draw anything from,
[06:43] you know, a little bit of oxidation on the connections
[06:47] or it's a little warmer in the room
[06:50] or the wires are a little longer
[06:52] or anything like that can make slight differences
[06:57] to the amount of current at this level.
[06:58] To give you a comparison,
[07:00] some of the best ESP32 boards for deep sleep current
[07:05] draw something like 20 to 30 microamps
[07:10] which means this is 100 times less current draw.
[07:14] The ESP32 chip itself,
[07:17] not including any extras on a board,
[07:20] usually draws somewhere between 8 and 10 microamps of current.
[07:24] And so the best board I've built so far
[07:27] pulls around 16 to 17 microamps de current.
[07:32] And again, you're looking at something
[07:33] that is like two orders of magnitude lower here.
[07:36] The very lowest deep sleep claim
[07:39] I have seen on an ESP32 dev board
[07:41] is from the ESP32 E-Pulse Feather.
[07:45] This thing claims anywhere from 12 to 27 microamps.
[07:49] Now, again, I've managed to get boards
[07:52] down into like 16 to 17 microamps.
[07:54] They're claiming as low as 12.
[07:57] Well, even at the high end on the RTC
[08:00] where it's pulling maybe 200 nanoamps,
[08:04] that's still well over 50 times lower power
[08:07] than, again, the best ESP32.
[08:11] So that's where I think the advantage comes in.
[08:13] Now, I also do want to give some credit.
[08:15] I did not come up with the idea of using RTCs
[08:19] to do this type of deep sleep behavior.
[08:21] I actually saw on a video by Priceless Toolkit
[08:24] when I was doing some research into soil moisture sensors.
[08:28] They have developed a soil moisture sensor
[08:30] that uses a Texas Instrument RTC or Timer
[08:34] to do basically the same thing that I'm doing,
[08:37] but they're doing it on this soil moisture sensor.
[08:39] And the chip that they're using
[08:41] is a Texas Instruments TPL5110.
[08:44] And that is a very good chip.
[08:46] As a matter of fact, it is even lower power
[08:48] than what I'm using.
[08:50] However, the problem with this chip for my implementation
[08:53] is that this only allows up to a two-hour timer.
[08:57] And for a lot of devices,
[08:58] you really only want it to wake up once a day
[09:01] or twice a day, maybe.
[09:02] And this just isn't capable of putting the device
[09:06] in an off-state long enough.
[09:07] And so that's why I didn't go for that chip.
[09:10] There are also some RTCs
[09:12] from a company called MicroCrystal
[09:14] that are even smaller
[09:15] and do use less power than the Epson chips I'm using.
[09:19] However, they're pretty darn expensive.
[09:21] Something on the order like two times the price
[09:25] and the RTC from Epson
[09:26] is already kind of an expensive little chip.
[09:29] And I didn't want to make these things
[09:31] even more expensive.
[09:32] And so that's why I'm not using those.
[09:34] Now, I've also tried to focus
[09:36] a little bit on keeping the packaging
[09:37] pretty tight on this thing,
[09:39] simply because I know
[09:39] it's probably going to be used
[09:41] in conjunction with other devices
[09:43] and sensors and dev boards.
[09:45] So what we've got is a board
[09:47] that's about 24 millimeters long
[09:49] and about 17.5 millimeters wide there.
[09:54] And that is significantly impacted
[09:57] by the connectors.
[09:58] You can tell how much space
[09:59] this JSTPH connector takes
[10:02] and this regular pin header
[10:05] just because I didn't want
[10:06] to make this thing a pain to work with.
[10:09] So I did give it regular 2.54 millimeter
[10:12] pin spacing or 10th of an inch.
[10:14] You've also got a little mounting hole here
[10:17] that can take a 2 millimeter screw.
[10:19] And so just to make it usable,
[10:22] it did roughly double the board size
[10:25] compared to just the bare components
[10:27] that I would need.
[10:28] If I just wanted to give you traces
[10:30] de solder to on the back of a board,
[10:32] I could have actually made this thing
[10:33] quite a bit smaller.
[10:34] Now, I'll also point out
[10:35] these RTC chips
[10:37] like this Epson that I'm using
[10:38] are fairly complicated.
[10:40] And so I've written an ESP home component
[10:43] that you can use
[10:44] to implement pretty much
[10:46] all the functionality
[10:47] that is included on this chip,
[10:49] which, again,
[10:49] it's got quite a bit of stuff
[10:51] on there.
[10:52] And I added a lot of things
[10:53] beyond just what would be necessary
[10:56] for this particular implementation
[10:58] of getting good low power consumption.
[11:01] So one of the features
[11:02] has got, obviously,
[11:03] it's an RTC, a real time clock.
[11:05] And so you can use it
[11:06] to store actual date times
[11:08] that do not require connecting
[11:11] back to your home assistant server.
[11:13] So you can do offline,
[11:14] basically,
[11:15] real time
[11:16] and it will keep track
[11:17] of that for you.
[11:18] It also can provide
[11:19] a frequency output
[11:21] that has selectable frequency.
[11:23] So you can use it
[11:23] as a frequency source
[11:25] for other things
[11:25] that may need that.
[11:26] I've also written the components
[11:28] that it can also be used
[11:29] with a different version
[11:30] of this chip,
[11:30] the RX 8130.
[11:33] I haven't actually
[11:33] gotten my hands on one of those,
[11:35] but based on the datasheet,
[11:37] they're pretty similar
[11:38] with just slightly
[11:38] different functionality.
[11:40] And so I went ahead
[11:41] and I made the components
[11:42] that it would also work with that.
[11:44] And again,
[11:45] I've also got a separate C library
[11:47] if you just want to use it
[11:48] for a normal embedded project
[11:50] outside of ESP home.
[11:51] Now we come to the kicker.
[11:53] How much does this thing cost?
[11:54] And this is not as cheap
[11:56] as I would like it to be.
[11:57] Those little RTC chips
[11:59] are just not very cheap.
[12:02] In addition,
[12:03] I tried to use
[12:03] pretty good quality components
[12:05] and I tried to spec
[12:06] everything well
[12:07] so that it's capable
[12:08] of really doing a good job.
[12:10] And inevitably,
[12:11] I tried to wait
[12:13] to order it until
[12:14] after the Supreme Court decision
[12:15] on tariffs,
[12:16] hoping that that might be able
[12:17] to lower the cost.
[12:19] Alas, the decision came
[12:20] but the tariffs didn't really go away.
[12:22] So, the price.
[12:24] My plan is to sell
[12:25] two of these for $20 shipped,
[12:28] which again
[12:29] is more than I wish it were.
[12:31] But please understand
[12:32] out of that $20,
[12:33] about $9 of that
[12:35] is nothing but
[12:37] shipping cost,
[12:38] taxes,
[12:39] tariffs and fees.
[12:42] Before I even actually pay
[12:45] to get this board assembled.
[12:46] That's right.
[12:48] About $9 out of those $20
[12:50] has nothing to do
[12:51] with actually manufacturing the board.
[12:54] That's just how much
[12:55] all that other stuff cost.
[12:57] In addition,
[12:58] that $20 includes shipping.
[13:00] And so, because of that,
[13:02] that just is the price.
[13:03] Again, I wish it were cheaper.
[13:05] I wish I could offer bigger discounts.
[13:07] But they just aren't as inexpensive
[13:09] as I wish they were.
[13:10] I'll put the links down below
[13:12] to the Etsy link
[13:13] in case you want to purchase one of these.
[13:15] I'll also put a link
[13:16] to the component
[13:17] that you can use
[13:19] for your own ESP home
[13:21] or the library for the Arduino.
[13:23] In addition,
[13:23] I'll have a little CAD model of the board
[13:25] so that you can use that
[13:27] in a 3D modeling programs.
[13:29] You can know exactly
[13:30] how much space it's going to take up
[13:32] in any design you want to implement it in.
[13:34] And I'll put the data sheets
[13:36] for the RX-8111
[13:38] and the RX-8130
[13:40] out there with it.
[13:42] I've tried to write up
[13:43] pretty good documentation
[13:44] because, like I said,
[13:45] these things are kind of complicated.
[13:47] The way the alarms work
[13:48] is a little tricky.
[13:50] So I've actually also
[13:51] written an action
[13:52] for ESP home
[13:53] that allows you to set an alarm
[13:55] by a time offset,
[13:56] which is not one of the
[13:57] included features on this board.
[13:59] What that means
[14:00] is you can program
[14:01] something like,
[14:01] hey, go to sleep
[14:03] for 12 hours
[14:04] and then wake up.
[14:05] The way the alarms normally work
[14:07] is you have to tell it
[14:07] exactement what time
[14:09] you want it to wake up.
[14:10] This way, you can just say
[14:11] how long you want it to sleep
[14:13] and it will still work
[14:14] pretty much like a deep sleep component.
[14:16] So, that'll wrap this up.
[14:18] I know it's a bit of a shill
[14:19] because I am selling these things,
[14:21] but I will post up
[14:22] also the schematic
[14:23] for these things.
[14:24] So, I mean, hey,
[14:25] if you want to take and go
[14:26] make it yourself,
[14:27] good luck making it cheaper
[14:29] than I'm selling them.
[14:30] That's all I'll say.
[14:31] But that's it for me.
[14:33] As always,
[14:34] I appreciate your time.
[14:35] Thanks.
