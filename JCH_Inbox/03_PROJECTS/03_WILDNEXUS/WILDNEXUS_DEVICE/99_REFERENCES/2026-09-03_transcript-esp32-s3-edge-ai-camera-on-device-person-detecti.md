# Transcript — « ESP32 S3 Edge AI Camera On Device Person Detection No Cloud! #esp32s3 »

- **Source** : IoT Journal
- **URL** : https://youtu.be/554BfgEMc9A
- **Durée** : 07:22
- **Date** : 2026-09-03
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 168

---

[00:03] Welcome to a very special IoT Journal deep dive explainer.
[00:07] Today, we are stepping away from our regular numbered ESP32 series
[00:11] to look at a completely new tier of engineering.
[00:14] We're going to unlock true offline artificial intelligence
[00:18] right on a microcontroller.
[00:20] If you've ever wanted to build a device that can actually see and recognize a person
[00:24] without relying on the cloud at all, you are absolutely in the right place.
[00:28] Here is our roadmap for today.
[00:30] We'll start with the intro and required components, move on to edge impulse model training,
[00:35] then cover the Arduino IDE setup, walk through the code, do a live test with some troubleshooting,
[00:41] and wrap up with the summary of the S3 advantage.
[00:44] All right, part one, intro and required components.
[00:47] Now you might be wondering, why can't I just use that regular trusty ESP32 I already have?
[00:53] Well, the older chips basically fail at heavy AI math.
[00:56] It's just too much for them.
[00:58] But the ESP32 S3 architecture includes dedicated AI and DSP vector instructions
[01:03] baked right into the hardware.
[01:05] These instructions act like a supercharger for neural network mathematics,
[01:08] making real-time machine learning inference totally possible directly on the chip.
[01:12] We're talking no cloud, no Wi-Fi completely offline.
[01:16] And to build this, you don't need a massive server rack.
[01:19] You really just need a compatible S3 camera board.
[01:22] Models like the FreeNove ESP32 S3W Room,
[01:26] or the ZIO ESP32 S3 Sense,
[01:29] are absolutely perfect for this.
[01:31] Pair that with a standard USB-C cable
[01:33] and a completely free account over at edgeimpulse.com
[01:36] and you are fully equipped to build a smart camera.
[01:40] Let's jump into section two, Edge Impulse Model Training.
[01:44] The Edge Impulse Training Dashboard makes this whole process incredibly easy.
[01:49] First up, you just collect sample images of a person and no person
[01:52] right from your board's camera or you can just upload existing photos.
[01:56] Next, we train an image classification model.
[01:59] We use what's called a MobileNet v2 transfer learning model,
[02:02] basically because it's highly optimized to run on tiny microcontrollers.
[02:05] You can actually test its accuracy right there in your browser.
[02:07] And once you're perfectly happy with how smart your model is,
[02:10] you export it straight out of the deployment tab
[02:12] as a neat, ready-to-use Arduino SIP library.
[02:15] Moving right along to section three, Arduino IDE and Setup.
[02:20] This setup is just beautifully simple.
[02:23] First, make sure you have the standard ESP32 board package installed in your IDE.
[02:28] Then, you just go to Sketch, Include Library
[02:31] and hit Add.Zip Library to import your custom Edge Impulse file.
[02:36] What's so fantastic about this is that the ZIP
[02:39] automatically bundles a camera example sketch right inside it.
[02:42] So you literally just open that up
[02:44] and the foundation of your code is already written for you.
[02:47] Now for the really fun part.
[02:49] Section four, the code walkthrough.
[02:52] Look, don't worry if you're totally new to machine learning.
[02:54] We're going to take this step by step.
[02:56] Phase one is crucial,
[02:57] bringing in our libraries and mapping the hardware.
[03:00] We include the Edge Impulse inferencing library we just installed
[03:03] along with the ESP32 camera driver.
[03:06] Then, we absolutely must define the exact camera pin mapping.
[03:10] See, different S3 boards wire their cameras slightly differently.
[03:13] So making sure these pins match your specific board model
[03:16] is literally the first secret to success here.
[03:19] Down inside the Setup function, we hit a critical requirement.
[03:22] We have to initialize the camera
[03:24] to match exactly what our new AI brain expects to see.
[03:27] For example, if you trained your Edge Impulse model
[03:30] on 96x96 pixel square images,
[03:33] you configure the S3 camera resolution in pixel format
[03:36] to match that identically.
[03:38] It's really just about giving the AI the exact visual diet
[03:41] it's used to processing.
[03:43] Now for phase three,
[03:44] which happens continuously inside our main loop.
[03:47] The code grabs a picture, just a single frame from the camera.
[03:50] But a raw image file isn't quite ready for neural network yet.
[03:54] The code steps in and mathematically formats
[03:56] and converts this image into a specific array of numbers.
[03:59] It strips away all the unnecessary data
[04:01] and reshapes the pixels into the precise mathematical input
[04:05] that our MobileNet V2 model can actually digest.
[04:08] Phase four is where the magic really happens.
[04:10] We call a function named run underscore classifier.
[04:14] Running inference is honestly just a fancy way
[04:16] of asking our model a mathematical question
[04:19] based on the image we just formatted.
[04:21] We're essentially asking, hey, is there a person here?
[04:24] The model does its heavy math
[04:25] using those vector instructions we talked about earlier
[04:28] and hands us back a numerical confidence score
[04:30] for the person class.
[04:32] Finally, phase five, we get to act on that score.
[04:35] We write a simple if statement.
[04:37] If the confidence score is high enough, let's say over 0.8,
[04:40] we tell the ESP32 to print person detected to the serial monitor.
[04:45] And because this is a microcontroller,
[04:47] we can so easily trigger a standard GPIO pin
[04:50] to light up an LED, sound abuser, or even unlock a door.
[04:53] You've just successfully bridged the gap
[04:55] between software AI and physical hardware.
[04:58] All right, section five, live test and troubleshooting.
[05:03] Just imagine watching this happen on your screen.
[05:06] You step in front of the camera
[05:07] and this confidence score just spikes
[05:09] in your serial monitor in real time.
[05:12] Seeing a 0.98 means the S3 is 98% sure
[05:15] it's looking at a person.
[05:17] Then you step out of frame
[05:18] and it drops right back down to near zero.
[05:21] Honestly, seeing this happen
[05:22] smoothly entirely offline on a tiny microcontroller,
[05:25] it's just incredibly satisfying.
[05:28] It perfectly proves the offline power of this chip.
[05:31] Now, if things don't work perfectly on the very first try,
[05:34] seriously don't panic.
[05:35] This simple troubleshooting matrix
[05:36] from our source material is going to help you out.
[05:39] If you're getting false detections,
[05:40] your model probably just needs
[05:41] more varied training images.
[05:43] Different lighting, different backgrounds.
[05:45] If you hit a camera in it failure 99 times out of 100,
[05:48] your pin mapping just doesn't match
[05:50] your specific board model.
[05:51] And if you get out of memory errors,
[05:53] you simply need to lower your camera resolution
[05:55] or go back into edge impulse
[05:57] and select a smaller machine learning model
[05:59] to fit the S3's memory footprint.
[06:01] Let's wrap things up with section six,
[06:03] Summary and the S3 Advantage.
[06:05] We absolutely have to bookend
[06:07] this explainer with the S3 Advantage.
[06:09] This quote right here is the entire reason
[06:11] this project is even possible.
[06:13] This specific chip unlocks completely
[06:15] new frontiers for us purely
[06:16] because of its AI and DSP vector instructions.
[06:19] It turns through neural network math
[06:21] at a speed that just leaves
[06:22] the original older ESP32 silicon
[06:24] completely in the dust.
[06:25] You simply cannot do this
[06:26] effectively on the older chips.
[06:28] If you want to replicate
[06:29] this exact setup yourself,
[06:30] you can find the full written tutorial
[06:32] alongside those absolutely crucial
[06:34] exact pin mappings for all
[06:35] the popular S3 boards
[06:37] over at IoTJournal.net.
[06:39] It is an incredible time
[06:40] to be building hardware, isn't it?
[06:42] We've gone from wiring up basic sensors
[06:44] to programming microcontrollers
[06:45] that can literally see and recognize us
[06:47] all while staying entirely offline.
[06:49] So with that kind of power
[06:51] sitting right there on your desk,
[06:52] what offline AI project
[06:53] are you going to build next?
[06:55] Welcome to IoTJournal.net,
[06:58] your ultimate hub for practical
[07:00] ESP32 and IoT engineering.
[07:03] Here, every single project
[07:05] comes with crystal clear schematics,
[07:07] step-by-step build guides
[07:08] and fully updated source code,
[07:11] continuously refreshed
[07:12] with the latest library versions
[07:14] so your builds work without any errors.
