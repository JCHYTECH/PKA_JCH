# Transcript — « DIY: ESP32 AI Sound Recognition Step-by-Step | TinyML »

- **Source** : Smart Mercury Labz
- **URL** : https://youtu.be/hQpPTWAd1QY
- **Durée** : 16:35
- **Date** : 2026-08-31
- **Moteur** : Whisper local (small, faster-whisper)
- **Segments** : 234

---

[00:04] Ce que vous regardez maintenant n'est pas connecté à un PC, un serveur ou un cloud.
[00:10] Mais, ce USB 32 microchip est en train de faire sa propre réel numérique, complètement offlée.
[00:16] Vous voyez comment il s'ignore complètement le background noise.
[00:26] Mais le moment où il s'éteint, il s'éteint rapidement.
[00:31] Dans ce vidéo, je vais vous tourner le processus entier,
[00:42] collecter la data, entraîner un modèle tiny ML, optimiser le hardware pour le USB 32
[00:48] et placer le stand-alone.
[00:50] Faire sureur de ne pas le couper.
[00:52] Lissons-vous en 1 étape.
[00:54] Dans ce workflow, il sera installé dans un mètre.
[00:58] Bienvenue à SmartMercule Lab.
[01:00] Aujourd'hui, nous sommes en train de prendre la customisation de l'AI de la PC
[01:03] et de l'améliorer sur le stand-alone de l'USB 32.
[01:07] Let's jump straight into the hardware components.
[01:10] First, we need a digital microphone module.
[01:13] I2S delivers clean digital, first density audio.
[01:17] Directly to microcontroller.
[01:19] Secondly, we require ESP32 development board.
[01:22] Wiring is simple.
[01:24] This is a table of pin connection of ESP32 and microphone.
[01:28] You can pause the video and check the connection.
[01:31] Now we will create a data model.
[01:37] For that, we need to log in to the Edge impulse website.
[01:43] Registration is free, anyone can register.
[01:53] There are different options of login.
[01:55] You can log in through Google, GitHub
[01:59] or any other email id.
[02:15] So already I have registered
[02:17] and this is the main page.
[02:23] For here you can create a new project.
[02:25] Clicking on that.
[02:27] Enter your project name
[02:35] and enter value.
[02:43] So here I have selected personal
[02:45] and the files will be private.
[02:47] Now create a new project.
[03:04] So this is a dashboard of our project.
[03:13] Now we have to upload our data files.
[03:15] That is audio files.
[03:20] Every machine learning model
[03:22] is only as good as its training data.
[03:24] For a robust single sounds detector
[03:27] we need two distinct audio classes.
[03:29] Target sound and background noise.
[03:32] So here there are two audio files.
[03:41] Bell and noise.
[03:43] Bell is a sound that we want to recognize
[03:46] when the bell rings.
[03:48] And noise is a sound that we don't want to recognize.
[03:51] And whatever data,
[03:53] whatever audio files you need uploading
[03:55] will be in wave format.
[03:57] I will quickly show you
[03:59] what this file contains.
[04:01] This bell file contains
[04:03] a different sounds of bell
[04:05] taken from different locations
[04:07] with different variations.
[04:16] The noise file contains
[04:18] the noise which is there
[04:20] in our surrounding
[04:22] like fan noise
[04:24] lesser noise
[04:26] like people talking
[04:28] or there is some
[04:30] something falling
[04:32] anything.
[04:34] Now back to our edge website.
[04:42] We will be adding our data
[04:44] using ad existing data.
[04:49] Select the file in the browse
[04:59] and give the label
[05:01] bell. Everything should be in
[05:03] smaller case.
[05:08] Here you can see the job completed message.
[05:10] Means the file is uploaded successfully.
[05:12] Now we will upload noise file
[05:14] the same way.
[05:16] But the label will be noise.
[05:18] Here you can see
[05:30] both the files are uploaded successfully
[05:32] under training tab.
[05:35] Now we will split our files
[05:37] in small chunks
[05:39] using split samples
[05:41] but why we need to split our files
[05:43] because an ML model needs
[05:45] individual training examples
[05:47] rather than one long recording
[05:49] contains multiple events.
[05:53] So this process may take some time
[05:55] because it is breaking your file
[05:57] in one second duration
[05:59] and we will get errors
[06:01] but don't worry your files
[06:03] are getting generated.
[06:12] You can see the files are still generating.
[06:14] This is done now.
[06:22] Now the same process we will do
[06:24] with bell file.
[06:53] Here you can see the bell files
[06:55] are also successfully created.
[07:04] Now click on create impulse
[07:09] Now click on add processing vlog
[07:11] and select
[07:14] mfd section
[07:16] Well mfd section
[07:18] is specially used for sound classification
[07:20] Now click on add a learning vlog
[07:32] and add classification
[07:34] Now save impulse
[07:43] Now you will see
[07:49] mfd section
[07:51] left navigation
[07:53] Click on that
[08:02] Here you have to change
[08:04] fftlend to 512
[08:20] Save parameters
[08:27] Click on generate features
[08:55] Now we are present in the audio samples
[08:57] after the feature have been extracted
[08:59] Go to classify section
[09:04] left navigation
[09:06] Now click on save and train
[09:13] at the bottom of the page
[09:41] So now we are done with our data models
[09:43] with 97% accuracy
[09:45] This is a good accuracy
[09:47] So now we will build this
[09:49] and download it
[09:51] Before going further
[09:53] I want you to check
[09:55] one more thing
[09:59] Now click on data sets split
[10:01] Check the training and test percentage
[10:03] It should be 80 and 20
[10:05] If it is not, you change it to 80 and 20
[10:07] and click on strategy
[10:09] sampling by label
[10:11] and create data sets split
[10:13] Now click on the train model
[10:20] and train model
[10:26] So downloading
[10:28] go to deployment link
[10:30] on the left navigation
[10:32] Deployment target
[10:34] click
[10:44] and click on build
[10:46] Here the build is successfully created
[11:01] and it is downloaded
[11:03] in download folder
[11:11] Now we have to copy this zip file
[11:13] and put it in the library folder
[11:15] of the project
[11:21] Now extract the folder
[11:34] Now copy this well folder
[11:36] to the root of library folder
[11:49] The folder name well inferencing
[11:51] is also the name of our
[11:53] data model that we have to include
[11:55] in our project
[11:59] Here you can see
[12:01] how it is included
[12:16] Now we will delete
[12:18] all the unnecessary folder
[12:20] from our list folder
[12:31] If you are not familiar with using vs core
[12:33] with plugin platform IO
[12:35] Check my video of esp32 setup
[12:37] in 60 seconds
[12:39] The link is in the description
[12:45] First we will build the project
[12:47] by clicking on the tick icon
[12:49] Once the build is completed, we will upload the code
[12:51] to the esp32
[13:01] I will upload the complete code
[13:03] on my grid repository
[13:05] and I will provide the link
[13:07] in video description
[13:11] I will also explain how the code works
[13:13] and walk you through the logic step by step
[13:31] Now the build is ready
[13:33] and we will upload it to the esp32
[13:35] Before uploading, let me give you
[13:37] a brief overview of the code
[13:43] Here we have included android library
[13:45] then the driver of microphones
[13:47] then
[13:49] the data model
[13:51] These all are the main connections
[13:58] of esp32
[14:00] Then we will setup of a microphone
[14:08] This is a default setup of a microphone
[14:10] You know it to change in this code
[14:13] Then this is setup
[14:15] of our esp32 project
[14:17] This is a looking code
[14:21] So here we are checking the
[14:23] data model
[14:40] and our input
[14:59] So here we are checking the
[15:01] data model and our input
[15:03] So if you are checking
[15:05] whether the sound is good
[15:07] if it is yes
[15:09] then we check
[15:11] what is the strength of the sound
[15:13] it is more than 90
[15:15] then only it will trigger
[15:18] it will go
[15:20] and if not it will not
[15:24] So
[15:28] that was a brief overview of the code
[15:30] Now let's upload the build to the esp32
[15:32] Now that the build has been
[15:45] uploaded successfully
[15:47] Let's check if everything is working properly
[15:49] You will open the monitor in platform I.O
[15:51] and see the output
[15:53] from the esp32
[15:55] And that's it
[16:10] the project is running properly
[16:12] which means our setup and crew
[16:14] are working as expected
[16:16] We have successfully built, uploaded
[16:18] and tested the project with the esp32
[16:20] I hope you found this project useful
[16:22] and enjoyed following alone
[16:24] If you like the video
[16:26] hit the like button
[16:28] and subscribe to the channel
[16:30] for more electronics project tutorials and experiments
[16:32] Thanks for watching
[16:34] and I'll see you in the next video
