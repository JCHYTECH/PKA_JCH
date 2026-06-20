# https://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-05-19 05:55

�e�e�chttps://www.youtube.com/watch?v=Cd_yplR1hcI&t=56s

00:00:00
in this video we're revisiting my AI Wildlife monitoring system so it's been a few months since I posted my first video on this and there been quite a few updates since then I've been posting some short form content on various social media platforms just updating my progress with this I haven't really had time unfortunately to post a full length video but now I think I'm at a stage where I've got enough to actually put something together so if you've been following along with that you'll know

00:00:24
there's been quite a few updates since my previous first prototype and I've also been in contact with a lot of you discussing what you would Ed something like this for I've even been in contact with some ecologists who might be interested in using something like this for their projects so it's been really great to hear some feedback on this so thanks to everyone for helping me out with that since the previous video as well I've actually traveled to New South Wales to help some ecologists on one of

00:00:45
their projects doing bat population studies so they were running a capture recapture program in order to estimate the population density for some Australian microbats so I got to hang out with them for a few days learn about what they do with the bats and some other species and talk to them about technology like this to see what sort of Technology they use and what else we could do so one interesting thing from that was that for bats and birds they actually commonly use audio or call data in order to identify species in the area

00:01:14
not so much cameras though they do use cameras in some situations but audio kind of makes sense you know it's kind of hard to know where to point your point your camera if you're looking at something that's flying through the air audio you can collect data from all around you so that might be an interesting direction to go in the future with this so what else has happening um my PhD thesis finally got uh certified ratified I don't know signified was a whole bunch of steps to do that so

00:01:39
technically now I'm Dr Luke uh was it worth it we'll see in any case let's see what changes I've made and what we've done here so one of the biggest changes you'll note is that I've switched now to using the raspberry pi and the Raspberry Pi ecosystem in that first video I talked about the limitations of that system you know power consumption lack of compute I was using quite old Jetson model since that video raspberry play has actually come out with a couple of bits of AI Hardware that is really

00:02:06
useful for what I'm doing here that being both the AI hat or the Halo accelerator and also the raspber pi AI camera which actually uses that Sony IMX 500 intelligent image sensor that I talked about so it's a bit of a coincidence that they happen to produce this right after I talked about it in that video so with that I've also switched the raspby pi 5 which is needed for that AI hat in some of those shorts I talked about why I'm not using the AI camera for now I am limited by the

00:02:31
resolution that I can put through the model even though this is a high resolution camera the model on here can only run at 4 640x 640 whereas I can kind of choose any resolution for this one I'm still using the high quality camera same as before so that gives me access to potentially up to 4K resolution images you can see now the whole design is a lot smaller and more compact I've got this UPS here for the Raspberry Pi 5 that I've got off the shelf one of the issues with the old design was that I had all this custom

00:02:58
wiring and soldering there that was very messy things were coming out and I wanted some of those Compact and sort of click together nicely I didn't really have time to do a custom PCB yet so I just wanted to see what I could get off the shelf it's quite a few of these UPS's battery power supplies solar power supplies so one big issue I'm having with a lot of those is that none of them really do everything I want and this is kind of the issues with using off-the-shelf components the AI hat here

00:03:21
you can see it actually mounts to the top of the Raspberry Pi but it also blocks the GPI op pins for the Raspberry Pi meaning I can't put any more hats on top so a lot of the UPS's or power supplies for the Raspberry Pi that might be more suitable than what I'm using here can't use because they mount on the top and I chose this UPS which is just some generic sort of Raspberry Pi 5 UPS because it has batteries in the back and also the Raspberry Pi mounts on top and has a DC Supply input and some output

00:03:48
5vt power as well that I can run my fan with and while this does has some basic battery monitoring it doesn't monitor power consumption or charge power from the solar panel and it also can't wake up to Raspberry Pi and as I've mentioned some of those shorts for some reason it has the feature that whe
