# Transcript — « How to Send Sensor Data Over LoRa with Meshtastic ESP32 »

- **Source** : Shilleh
- **URL** : https://youtu.be/ET_vBzLNKu8
- **Durée** : 12:55
- **Date** : 2026-03-17
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 412

---

[00:00] Hey, what's up everyone, welcome back to the channel.
[00:12] In this video, I'm going to show you how to connect a BME 280 to a mesh-tastic ESP32
[00:17] LoRa board and send live temperature, humidity, and pressure data over a private LoRa mesh with
[00:22] no Wi-Fi and no internet.
[00:24] Now, LoRa is a low-power wireless technology that can send small amounts of data over
[00:28] several kilometers, which makes it great for remote sensors just like this.
[00:32] In this tutorial, we will wire everything up, flash the boards, set up a private
[00:35] channel, and verify that telemetry shows up on the second node.
[00:39] So this is a pretty interesting technology if you are in the IoT space and I suggest
[00:43] you tag along even better before we get into the tutorial today.
[00:47] We have the free blog on shilletech.com, which contains the steps and instructions
[00:51] in more detail.
[00:52] So if you don't feel like writing the commands off the screen or you just need a little
[00:55] more help, you can follow along on the free blog in the link down below at shilletech.com.
[01:00] Also be sure to like, comment, subscribe, and let's get started.
[01:03] Ok, so the first thing we want to do is we want to install the mesh-tastic-cli tool in our
[01:09] Python virtual environment.
[01:11] Now this is a tool that lets us configure, inspect, and control our mesh-tastic LoRa devices
[01:15] as you see here, which will enable us to run commands and set up the network and
[01:20] see if our devices are working as expected.
[01:23] So make sure you have Python installed on your computer and we could just run
[01:26] these commands in any terminal, and of course go ahead and set up an empty
[01:29] project where you can create your virtual environment.
[01:32] So I'm just going to go ahead and copy these commands, and you can see I just went
[01:35] into Visual Studio Code, which is just an editor, and I already have the mesh-tastic
[01:40] environment.
[01:41] We can go ahead and run it again.
[01:42] So what this command is going to do, at first, it's going to set up a virtual
[01:44] environment, which has your Python packages.
[01:47] Then we're going to source it, which enables us to have access to those
[01:51] packages.
[01:52] And finally, we're going to install mesh-tastic.
[01:53] So I'm going to go ahead and enter this.
[01:55] And because I already have it, you can see everything's already satisfied.
[01:59] So once you have this, you have your environment, and we'll be using this
[02:03] later on to interact with our mesh-tastic devices.
[02:06] OK, next thing we want to do is we want to install the mesh-tastic
[02:09] firmware on each device.
[02:10] So we could just use the web installer.
[02:12] Be sure you connect each device to your computer.
[02:15] So I'm just going to go ahead and connect this first one.
[02:17] It already has mesh-tastic on it from before, but we can go ahead
[02:20] and reflasher it.
[02:21] So go ahead and just open this flasher.mesh-tastic.org.
[02:25] And then we can select the target device.
[02:27] So all the instructions are back on this page.
[02:29] Click Connect and choose the serial port.
[02:31] So it's going to...
[02:34] Let's see auto-detect.
[02:35] I actually never tried this feature.
[02:37] OK, cool.
[02:38] So I believe this is the correct one.
[02:40] So on a Mac, it's cu.usb.
[02:43] So there's a one.
[02:43] So we can go ahead and connect this.
[02:46] I'm going to dismiss that.
[02:48] And I believe this is the Helltech v3.
[02:50] So let me just go ahead and double check.
[02:52] OK, so Helltech v3.
[02:53] So that's the one I got from Amazon.
[02:54] That is linked in the blog.
[02:56] So we have the Helltech v3.
[02:57] We're going to use this beta version as you see.
[02:59] And we're going to go ahead and flash the firmware.
[03:01] So all this stuff, we don't really care.
[03:05] Let's actually see something.
[03:07] Let's go ahead and continue.
[03:09] OK.
[03:11] So ensure your device is connected.
[03:12] Looks like it's good.
[03:13] Flash and Array.
[03:14] So we want to do that because we want to start from scratch.
[03:16] One thing I want to see is if there's actually other versions here.
[03:19] Let's actually just use the stable.
[03:21] That's the unstable version.
[03:24] Stable or...
[03:24] OK, so stable or beta is actually the stable version.
[03:27] So I just want to make sure because usually beta is the unstable version.
[03:31] Anyways, let's go ahead and flash this.
[03:34] New contributors.
[03:36] I don't know what's going on here.
[03:38] Let's go ahead and refresh this page a little slightly buggy.
[03:42] It's OK.
[03:43] So once again, Helltech v3.
[03:45] So the beta version flash.
[03:47] And continue.
[03:48] So that continue button is there.
[03:49] So let's go ahead full erase and install.
[03:52] Boudray is fine.
[03:54] And we can go ahead erase and flash.
[03:55] So go give that a moment.
[03:57] First of all, pair it here.
[03:59] And that should begin to flash.
[04:01] So once this is done, we should see a success message
[04:04] and then we could do the next device.
[04:06] OK, so looks like the device is done installing
[04:08] and we could see on the screen this little device has a screen here.
[04:12] Shows that it's successful.
[04:13] Let me go ahead and zoom in on to that.
[04:15] And you could see, we could just go ahead and click OK.
[04:17] So we could just hold the top left button there.
[04:20] And once that's done being held,
[04:23] we'll see that there are some other messages on the screen here.
[04:26] And there's a back button.
[04:27] There's US.
[04:28] Let's go ahead and click.
[04:31] The button, every time you click it, you can go to the next option.
[04:33] So I'm just going to go ahead and select US, as you see here.
[04:35] So go ahead and hold that button now.
[04:38] And I believe in different regions,
[04:39] it broadcasts a different type of frequency,
[04:42] but we're in the US, so I just select the US frequency.
[04:44] So it's rebooting.
[04:46] And that should be good for this device.
[04:48] And pretty much what we could do now is once that's installed,
[04:51] we could do the same on the other device.
[04:53] So once again, go ahead and go through the CLI tool,
[04:55] make sure the device is connected to the computer,
[04:57] and install the firmware on the other device.
[05:00] Once again, you click through the options on the screen
[05:03] and select US.
[05:04] If you are on the EU, select the EU option.
[05:06] And there you have it.
[05:07] You have the mesh-tastic firmware on the device.
[05:09] By this, we're going to run some mesh-tastic CLI commands
[05:12] that we'll be interacting with on the device
[05:15] to create the channel and prepare the device for telemetry.
[05:22] OK, actually, before we run these mesh-tastic commands,
[05:27] what we want to do is we want to wire the BME280 sensor.
[05:29] So I have the wiring here.
[05:30] I don't have a direct wiring diagram,
[05:32] but I show you which pins to connect.
[05:33] So we have the BME280.
[05:35] We want to connect these four pins.
[05:36] So these are for communication
[05:38] and these for power and ground.
[05:40] And we want to connect them respectively
[05:41] to the Heltec V3 pins like this.
[05:43] So these four pins,
[05:44] so just take four jumper wires and connect them.
[05:47] And you could see all those pins
[05:48] are on this side right here.
[05:50] So we have the 41 and the 42 pin, I believe.
[05:54] Yep, and then we have 3.3 volts and ground.
[05:56] And I also label the pins here.
[05:59] So you only need these top four pins.
[06:01] And the SHILTEC BME280 comes pre-soldered.
[06:04] So you can just plug it into the breadboard, as you see here.
[06:06] And that's how it'll look when it is connected.
[06:08] And you could see that in real life.
[06:09] So the second board, as you see here,
[06:11] actually has those connected like that.
[06:15] And that's pretty much it.
[06:15] So now, this thing is ready to start reading
[06:17] from the BME280.
[06:20] Okay, so jumping back to our Visual Studio Code,
[06:22] make sure you have the virtual environment activated.
[06:25] And the first one we're going to do
[06:26] is we're just going to connect to board one
[06:28] to keep it simple for you guys.
[06:29] And on this board,
[06:30] pretty much what we're going to do
[06:31] is we're going to set up the network,
[06:33] set up the encryption key
[06:34] and get the private channel URL
[06:36] that we're going to feed into board two
[06:38] to allow other nodes on the network
[06:41] to communicate with one another securely
[06:43] over the private Lora mesh network.
[06:45] So we're just going to run a series of commands.
[06:47] Once again, all these commands
[06:48] are available on our website.
[06:49] So here are the commands here.
[06:51] So it just connects to the port.
[06:54] It creates the channel,
[06:55] it creates a private key
[06:57] and it sets the region
[06:58] and commits it to the board.
[06:59] And finally, once it's created,
[07:00] we're going to get that primary channel URL
[07:03] because we need to pass that into the second board,
[07:05] which is the board with the BME280 on it.
[07:07] You could see the board right here
[07:09] is not in the breadboard right now.
[07:10] We don't really need a breadboard to be honest
[07:11] because there's no sensor on it.
[07:13] But this board is what's going to be
[07:14] retrieving the telemetry data
[07:17] from the other node within the network.
[07:19] So we can go ahead and click enter here.
[07:21] And before I do that,
[07:21] you may be wondering where I got this port here.
[07:24] I want a Mac, so you can simply get this ports.
[07:26] If I open a new terminal right here,
[07:29] you can do LS
[07:30] and then you could do dev cc usb url
[07:33] or usb serial, sorry.
[07:36] So let's just do LS, this.
[07:40] And we could do star.
[07:42] And then you could see that the board
[07:44] is connected at this port,
[07:45] specifically Windows and other operating systems
[07:48] have a different format.
[07:48] So go ahead and search that on your own.
[07:50] But for our Mac, this is the port for this board.
[07:53] So once we have that here,
[07:54] we can go ahead,
[07:55] let me just zoom in here to the commands.
[07:57] Once again, all these commands are on the website
[07:59] for free in the link down below.
[08:01] And we can go ahead and click enter here.
[08:02] So give that a moment.
[08:05] Okay, so looks like we have the channel URL
[08:07] as you see here.
[08:08] Now let's just go ahead and run a reboot.
[08:09] It's simply good practice
[08:10] after we do a large configuration change
[08:12] just to run a reboot
[08:14] to make sure things are working as expected.
[08:16] Let's go ahead and do that.
[08:17] And once we're running the reboot,
[08:18] you should see on the screen on the device
[08:20] that it says rebooting.
[08:21] So just give that a moment to reboot.
[08:22] And then once that's done,
[08:23] let's plug in a second device with the BME 280
[08:25] and configure things on that device.
[08:28] Okay, so second device is plugged in.
[08:30] First device is no longer plugged in.
[08:31] This device has the BME 280.
[08:33] So we're just gonna configure
[08:35] the private channel URL we got here.
[08:38] So we're gonna set that.
[08:39] And we're gonna set a few other parameters
[08:40] in terms of the telemetry as you see here.
[08:42] And then we're just going to reboot the device.
[08:45] So we can go ahead and just paste these commands.
[08:47] Once again, all these commands
[08:48] are on the Shilotec website.
[08:49] So first we set the channel,
[08:52] we set the region,
[08:53] we set the telemetry properties
[08:54] and then we just reboot.
[08:55] So go ahead and click enter here.
[08:59] And in a few moments,
[09:00] you should see the device begins to reboot
[09:03] after all these commands
[09:05] are registered on the ESP32.
[09:10] Give that a seconds.
[09:13] Okay, cool.
[09:15] So telemetry configuration is done
[09:18] and rebooting once again.
[09:19] So you should see on the screen rebooting.
[09:21] And that's it for device number two.
[09:23] Let's actually go back
[09:24] and run one more command on device number one.
[09:27] Okay, so the last command we have to run
[09:29] on device number one
[09:30] is we have to run
[09:31] the telemetry environment screen enabled
[09:34] just to show the telemetry
[09:35] on the screen for device number one.
[09:36] Forgot to run that.
[09:37] Just go ahead and plug device one back in.
[09:39] Click enter.
[09:44] And that's fine.
[09:44] Everything's ready to go
[09:45] in terms of the settings.
[09:46] Now, because I don't have enough wires
[09:47] to connect to my MacBook Air,
[09:50] which only has two ports,
[09:51] I'm gonna go ahead
[09:52] and actually unplug one of these
[09:53] and connect it to a battery
[09:54] which comes with this version of the ESP32.
[09:56] So this version you see right here,
[09:58] the first board,
[09:59] I'm just gonna plug it into the computer.
[10:01] And the other version right here,
[10:02] I'm going to plug into a battery.
[10:03] So this is board two with a BME 280.
[10:06] So I'm going to plug a battery
[10:07] in the back of the board.
[10:09] And what that's going to do
[10:11] is it's actually going to power it on.
[10:13] We don't have to have it connected to our Mac.
[10:15] If you see the tutorial on chilletech.com,
[10:17] we don't do that.
[10:18] But because I have a bunch of things
[10:20] wired to my computer right now,
[10:21] I have to connect one to a battery.
[10:22] But pretty much this is fine
[10:23] as long as it has a power source
[10:24] and all of your parameters
[10:26] are configurized on that device,
[10:29] you should be able to power these
[10:30] without your computer.
[10:31] So keep that in mind.
[10:32] You really don't need your computer
[10:33] at this point.
[10:34] You can have an off grid network
[10:36] as long as these things are within range,
[10:38] that is a few kilometers of one another,
[10:39] they can receive signal
[10:41] as long as they're powered on.
[10:42] So let's go ahead
[10:42] and attach the battery
[10:43] to this device right here.
[10:45] And we'll go ahead and make sure
[10:47] that the board one
[10:48] is receiving information
[10:49] from board two.
[10:51] Okay, so now that we have everything connected,
[10:54] you see I have board one
[10:55] plugged into my computer.
[10:56] And now we have board two here.
[10:58] As you can see now it's plugged
[11:00] into a power source,
[11:01] just a battery.
[11:03] So what you should typically do
[11:03] is just plug it into the battery
[11:05] or plug it into the computer
[11:06] even if you like,
[11:06] that is a power source.
[11:08] And you want to separate them
[11:09] at least maybe by a foot
[11:10] because Laura works better
[11:12] by a foot or more.
[11:13] Really it might work close
[11:14] but just keep them a little distance apart.
[11:16] So I'm gonna go ahead
[11:17] and move this over.
[11:19] And what you'd see
[11:19] as after some time
[11:21] maybe 30 to 60 seconds,
[11:23] the telemetry will be transmitted
[11:25] to the other board
[11:25] as you see here.
[11:27] So I'm just going to go ahead
[11:28] and show you this.
[11:29] So this is the environment section
[11:31] of the board.
[11:32] And you can get to the screen
[11:34] or you can move away
[11:34] from the screen
[11:35] by clicking this button
[11:36] as you see here.
[11:38] And you can go back
[11:38] to the telemetry section
[11:39] on the board.
[11:41] So I believe that's the,
[11:43] it's the screen right here.
[11:44] And this updates periodically
[11:45] I believe about a minute or so.
[11:47] And that's pretty much it.
[11:49] So the other board
[11:50] is sending that information
[11:51] to this board right here.
[11:53] And of course you can have
[11:54] other boards in the network.
[11:55] And you can go around
[11:56] and play around with this.
[11:57] You can use other sensors
[11:58] if you like.
[11:59] The BME 280 is the only
[12:01] sensor I've experimented
[12:02] so far with this board.
[12:03] It's pretty popular
[12:04] because it can measure
[12:05] environmental data
[12:07] and temperature pressure
[12:08] and humidity things
[12:09] that you would use
[12:10] in an agricultural project,
[12:12] which is really
[12:13] where a lot of these lower
[12:14] modules are used
[12:15] in open environment projects
[12:17] where you don't have access
[12:18] to internet or Wi-Fi.
[12:20] So pretty cool.
[12:21] I think it works as expected.
[12:23] So if you got this working,
[12:24] please be sure to like comment
[12:25] subscribe to the channel
[12:26] and be sure to check out
[12:28] the ShieldTech blog
[12:29] on our website
[12:31] along with other components
[12:32] related to that tutorial today
[12:33] such as pre-sider components
[12:35] that you can use
[12:35] to make your projects
[12:36] a little easier.
[12:37] In addition to that,
[12:38] we have other components
[12:39] for Raspberry Pi Arduino
[12:40] and all sorts of IoT projects
[12:42] that you guys can check out.
[12:44] If you want to see anything
[12:44] you need, let me know
[12:45] in the comment section
[12:45] down below
[12:46] and feel free to reach out
[12:47] our website as well
[12:48] in the context section
[12:49] if you have any questions
[12:50] or want more advanced
[12:51] help in your IoT projects.
[12:53] Thanks guys
[12:53] and I will see you
[12:54] in the next tutorial.
