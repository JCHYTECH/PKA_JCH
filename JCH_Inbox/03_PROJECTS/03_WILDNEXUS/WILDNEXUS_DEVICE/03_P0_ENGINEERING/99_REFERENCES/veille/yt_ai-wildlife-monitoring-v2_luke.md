[https://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s](https://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s)  
[https://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s](https://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s)  
  
00:00:00  
in this video we're revisiting my AI Wildlife monitoring system so it's been a few months since I posted my first video on this and there been quite a few updates since then I've been posting some short form content on various social media platforms just updating my progress with this I haven't really had time unfortunately to post a full length video but now I think I'm at a stage where I've got enough to actually put something together so if you've been following along with that you'll know  
  
00:00:24  
there's been quite a few updates since my previous first prototype and I've also been in contact with a lot of you discussing what you would Ed something like this for I've even been in contact with some ecologists who might be interested in using something like this for their projects so it's been really great to hear some feedback on this so thanks to everyone for helping me out with that since the previous video as well I've actually traveled to New South Wales to help some ecologists on one of  
  
00:00:45  
their projects doing bat population studies so they were running a capture recapture program in order to estimate the population density for some Australian microbats so I got to hang out with them for a few days learn about what they do with the bats and some other species and talk to them about technology like this to see what sort of Technology they use and what else we could do so one interesting thing from that was that for bats and birds they actually commonly use audio or call data in order to identify species in the area  
  
00:01:14  
not so much cameras though they do use cameras in some situations but audio kind of makes sense you know it's kind of hard to know where to point your point your camera if you're looking at something that's flying through the air audio you can collect data from all around you so that might be an interesting direction to go in the future with this so what else has happening um my PhD thesis finally got uh certified ratified I don't know signified was a whole bunch of steps to do that so  
  
00:01:39  
technically now I'm Dr Luke uh was it worth it we'll see in any case let's see what changes I've made and what we've done here so one of the biggest changes you'll note is that I've switched now to using the [[Raspberry Pi]] and the [[Raspberry Pi]] ecosystem in that first video I talked about the limitations of that system you know power consumption lack of compute I was using quite old Jetson model since that video raspberry play has actually come out with a couple of bits of AI Hardware that is really  
  
00:02:06  
useful for what I'm doing here that being both the AI hat or the Halo accelerator and also the raspber [[Pi]] AI camera which actually uses that Sony IMX 500 intelligent image sensor that I talked about so it's a bit of a coincidence that they happen to produce this right after I talked about it in that video so with that I've also switched the raspby [[Pi]] 5 which is needed for that AI hat in some of those shorts I talked about why I'm not using the AI camera for now I am limited by the  
  
00:02:31  
resolution that I can put through the model even though this is a high resolution camera the model on here can only run at 4 640x 640 whereas I can kind of choose any resolution for this one I'm still using the high quality camera same as before so that gives me access to potentially up to 4K resolution images you can see now the whole design is a lot smaller and more compact I've got this UPS here for the [[Raspberry Pi 5]] that I've got off the shelf one of the issues with the old design was that I had all this custom  
  
00:02:58  
wiring and soldering there that was very messy things were coming out and I wanted some of those Compact and sort of click together nicely I didn't really have time to do a custom PCB yet so I just wanted to see what I could get off the shelf it's quite a few of these UPS's battery power supplies solar power supplies so one big issue I'm having with a lot of those is that none of them really do everything I want and this is kind of the issues with using off-the-shelf components the AI hat here  
  
00:03:21  
you can see it actually mounts to the top of the [[Raspberry Pi]] but it also blocks the GPI op pins for the [[Raspberry Pi]] meaning I can't put any more hats on top so a lot of the UPS's or power supplies for the [[Raspberry Pi]] that might be more suitable than what I'm using here can't use because they mount on the top and I chose this UPS which is just some generic sort of [[Raspberry Pi 5]] UPS because it has batteries in the back and also the [[Raspberry Pi]] mounts on top and has a DC Supply input and some output  
  
00:03:48  
5vt power as well that I can run my fan with and while this does has some basic battery monitoring it doesn't monitor power consumption or charge power from the solar panel and it also can't wake up to [[Raspberry Pi]] and as I've mentioned some of those shorts for some reason it has the feature that when the [[Raspberry Pi]] shuts down the butt converter that supplies the [[Raspberry Pi]] with power also shuts down so it means that the raspby [[Pi]] 5 which is the first raspby [[Pi]] to have a real time clock and can reboot  
  
00:04:13  
itself from shutdown after a period of time can't do that because once it shuts down it loses power so the only way to wake it up is to either manually press the button or disconnect and reconnect the DC power supply to charge the thing which in my case comes from the solar panel panel that I'm feeding via this little Buck converter here just to keep it regulated at 12 V the solar panel can go up to past 20 volts and the DC input can't handle that so I just got that there to regulate that so the current  
  
00:04:41  
operation is that just after Sunset the [[Raspberry Pi]] shuts itself down and I'm currently relying on the sun to come out in the morning start supplying enough power that the buuck converter switches on and start supplying a charge current so the whole thing boots up and at the moment it's summer here in Australia so that actually kind of works reliably and it's running from like 6:30 to 9:00 at night but obviously in a lot of situations that's just not going to cut it and so I'm still working on trying to  
  
00:05:06  
come up with something either off the shelf or potentially custom as I'll talk about soon that actually kind of solves all my problems so a big part of the project that I've been working on since the last video is actually getting my own custom trained model to run on this Hardware training the YOLO model itself isn't that difficult the difficult parts are actually collecting and labeling the data so I've been trying to work on some automated ways to collect the dat for the individual species I'm still going  
  
00:05:32  
with birds at the moment just because it's easy to get data images of the birds I won't go into too much detail about how I'm doing that here now but at the moment I'm using the gbif sort of global database repository it has basically a bunch of URLs for specific species that you can use their API and download images from that and so I'm organizing that via bird species and then I'm using an off the shelf zero shot object detector model I played around with Dino I'm currently Now using  
  
00:06:00  
using Al open world locator or something like that these models are basically text conditional object detectors so you can put your image in with a caption like bird or a picture of a bird and it will produce your bounding box for that bird now you might be thinking why don't you just deploy that well like a lot of these zero shot models these models tend to be like a jack of all trades master of none so they can't actually tell the difference between bird species but that can identify a bird so I'm currently  
  
00:06:27  
just relying on that gbif database and Hope Hing that all the birds of that species that I downloaded and put in that directory only contain birds of that species it doesn't and then just any bird I detect in that is going to be a bird of that species it's not perfect but it works okay and I'm kind of working on some other tricks as well in order to train the YOLO model I'm just using ultral litics at the moment a lot of the demos for this AI accelerator and this rasby [[Pi]] AI camera use ultral litic  
  
00:06:52  
models so it's just really quick and easy to do that you don't technically need to use those but at the moment I'm relying on them I really want to put together a tutorial on how you actually export and use your own trained model for both the AI camera and the AI hat because there isn't really a lot out there and from what I can tell a lot of people are having difficulty with that the AI camera is actually pretty straightforward especially if you're just using the Yolo v8n from Ultra ltic  
  
00:07:17  
basically exports it straight into a format that you can put on your R [[Pi]] and convert but for other custom models it's a bit more difficult and for the actual Halo accelerator it just seems unnecessarily difficult this company seems to be a sort of hardware company that hasn't really spent too much time working on their software their data flow compiler which is what you use to compile and Export the model for the actual Hardware I think it only got released like mid last year even though  
  
00:07:41  
they've been selling the chips for ages up until then you just had to use their trained model so at the moment it's a bit weird and I have worked out a sort of reliable pipeline so let me know if you want that tutorial video I might just make it anyway cuz I think a lot of people would find that useful for the current model I've got on here can detect and identify 30 common bird species that we've got here in Victor Toro and it's processing a resolution of 640x 1280 so that's height width and  
  
00:08:05  
this thing can easily run that at 30 frames a second while only using about 6 wats of power but I'm actually only running it at 5 frames a second and so it's using much less than five maybe four to 5 wats of power which is pretty good especially for a model of this size so I'm currently playing around with the models and the software and how I'm doing certain things but I've currently got it set up with the solar panel as well I've made a new Mount that's just a ground Spike that just sticks into the  
  
00:08:29  
ground that big heavy umbrella stand was just way too cumbersome to try and haul around so this new design is much easier and I can kind of put it in more locations but as I mentioned there's still work to be done there is still no Laura or long range Communications which is kind of one of the main features I wanted to include in this and again it's been difficult to incorporate that because a lot of the raspby [[Pie]] hats sit on top of the raspby [[Pie]] which I just can't use here and I didn't really want  
  
00:08:53  
to hack around tacking on solder wires and everything to a module so I've kind of put that on hold for now so the next Grand Step potenti entally is to design and create a custom PCB that not only does the power supply the battery management the solar charging with proper solar charging it has a microcontroller on board to manage the actual shutdown and reboot of the rasp [[Pie]] correctly and also has allowances for Aura module or potentially even 4G LTE to transmit any detections that have occurred and there are also other  
  
00:09:21  
features I'd like to include like a proper pwm controller for the fan and some additional switchable outputs to control things like lights and motors and things that you might want to use so that power supply PCB potentially also with the audio classification where they usually have like a grid of microphones at all a recording and you might want to do something like a mesh network of microphones in a single compute Hub I foresee some PCB design in my future luckily for me all PCB has agreed to  
  
00:09:49  
sign on to be our PCB sponsor all PCB will handle all of your PCB manufacturing and assembly needs all you need to do is upload your gerbal files choose the number of layers so thanks to all PCB you can check them out in the links in the description if you think you're interested in having that PCB power supply with Communications for the [[Raspberry Pi]] in order to build your own Edge computer device let me know I'm interested to see who else might be interested in wanting something like this and who knows we might develop it  
  
00:10:17  
into a product that we can actually sell to people who are interested in any case that's all I've got for you for this video today let me know your thoughts in the comments and subscribe to stay tuned for more thank you and I'll see you next time  
  
