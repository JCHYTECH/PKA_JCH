# XENO-CANTO  
#   
# Introducing xcapi: A simple way to access Xeno-canto data from the command line and Python  
## By Burooj Ghani  
April 21, 2026  
Xeno-canto has become an essential resource for bioacoustics, with a vast collection of recordings contributed by a global community. It is an incredible platform for exploring species and soundscapes, but when it comes to working with larger sets of recordings - whether for analysis, dataset creation, or integration into workflows - the process can quickly become time-consuming.  
To make this easier, I developed ***xcapi***, a lightweight Python tool for searching and downloading Xeno-canto recordings programmatically. The idea is simple: take the flexibility of Xeno-canto’s search system (API) and make it directly usable from the command line or within Python, so that moving from a query to a structured dataset becomes straightforward.  
One of the main goals was to keep things as simple as possible. For many use cases, no programming is required at all. For example, the following command runs directly in the terminal and downloads high-quality bird songs from Spain:  
*xcapi --grp birds --cnt Spain --type song --q ">C" --output_dir ./data*  
This single command performs the search, downloads all matching recordings, and saves a metadata.csv file alongside the audio. In practice, this means that what would otherwise involve repeated manual downloads can be done in one step.  
```
For users working in Python, xcapi provides a small API that allows the same queries to be constructed programmatically inside a Python script. A query can be built in a readable way, executed, and the results downloaded:
from xcapi.query import QueryBuilder
from xcapi.client import XenoCantoClient
from xcapi.downloader import Downloader

query = QueryBuilder().group("birds").country("Spain").quality(">C").build()

client = XenoCantoClient()
recordings = client.search(query)

downloader = Downloader(output_dir="./data")
downloader.download_recordings(recordings)

```
This is particularly useful when building reproducible workflows, for example in machine learning applications or when analysing patterns across regions or time. The metadata that accompanies each download makes it easy to keep track of recording details and reuse datasets later.  
More broadly, tools like *xcapi* make it easier to move from individual recordings to structured collections of data. This can support a range of use cases, from building training datasets for species recognition to exploring ecological or geographic patterns, and integrating acoustic data into larger biodiversity monitoring workflows.  
xcapi is available via pip:  
*pip install xenocanto-api*  
The project is open source, and more details, examples, and documentation can be found here: **[https://github.com/bghani/xcapi](https://github.com/bghani/xcapi)**  
The goal is not to replace the Xeno-canto interface, but to complement it - providing a simple bridge between the archive and computational workflows. Feedback and suggestions are very welcome.  
*This article was last updated on April 21, 2026 at 15:11*  
  
  
# API functionality updated  
## By Bob Planqué and Willem-Pier Vellinga  
April 10, 2025  
As of April 10, 2025, the **[XC API](https://xeno-canto.org/explore/api)** has received a big update. This was necessary to alleviate the pressure on the server from bots and keep the site available to its users.  
In this article we give a short explanation of the most important changes and what they mean for XC users, researchers, app builders, and others that use the API.  
## Phasing out v2  
The old version v2 has gone off line on October 10, 2025. So please update your code if you have built the API into your app, or have written an API wrapper such as XenoPy to download recordings and metadata.  
The new API is available at  
**[https://xeno-canto.org/api/3/recordings](https://xeno-canto.org/api/3/recordings)**  
## Use your personal key to access the API  
The v3 API can only be used with your personal **key**. For example,  
**[https://xeno-canto.org/api/3/recordings?query=sp:"larus fuscus"&key=demo](https://xeno-canto.org/api/3/recordings?query=sp:%22larus%20fuscus%22&key=demo)**  
This key is available to registered users only, and may be found in your **[Account](https://xeno-canto.org/account)** page. The key will allow us to better monitor usage and improve the underlying queries whenever necessary.  
## Use at least one search tag in your query  
The **tag** system with which you can search for genus, location, recordist, etc, has been changed. You now always need to use **at least one tag**. So if you wish to find recordings of *Larus fuscus*, you should use either  
**[https://xeno-canto.org/api/3/recordings?query=sp:"larus fuscus"&key=demo](https://xeno-canto.org/api/3/recordings?query=sp:%22larus%20fuscus%22&key=demo)**  
or  
**[https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&per_page=50&page=3&key=demo](https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&per_page=50&page=3&key=demo)**  
The demo key should be replaced with your own personal key of course.  
The **[API page](https://xeno-canto.org/explore/api)** gives much more detail on the new situation, and read the **[Search tips](https://xeno-canto.org/help/search)** for full documentation on how to use the search tags.  
*This article was last updated on February 6, 2026 at 12:52*  
  
# A short introduction to Machine Learning results  
## By Bob Planqué and Willem-Pier Vellinga  
October 15, 2024  
From day 1 in 2005, Xeno-canto has been about recognising sounds as much as about collecting and curating them. In the mean time, recognising sounds, especially automatically, has proven to be a lot tougher than collecting and curating them :-) . Interestingly though, the fact that the collecting and curating part of XC has gone very well has been key in getting automatic recognition of the ground. Well, that and the fact that we chose an open format, which has made the recordings here available for research groups worldwide.  
Since 2014, important progress has been made during the yearly **[BirdCLEF](https://www.imageclef.org/node/316)** competitions for which Xeno-canto provided recordings for training and testing. The first Machine Learning (ML) algorithms **[appeared there](https://www.imageclef.org/lifeclef/2016/bird)** in 2016. All of you must be aware of their success and their use in various recognition apps for phones that allow one to identify bird sound. We are very pleased with the role of XC in that regard.  
Despite being involved from the get-go we've so far not managed to implement such algorithms in a meaningful way on XC. But here we are!! XC has started integrating ML algorithms for sound recognition into the platform by mid October 2024. It is the first cautious step on a trip in which we want to leverage automatic recognition on XC in various ways.  
The ideas executed now have been around ever since we started, so it seems for us to have taken a very long time. In the mean time the environment in which XC operates has changed considerably, with very large initiatives being set up to develop and support automatic recognition. For us the "**[Arise](https://www.naturalis.nl/wetenschap/arise-nederlandse-soorten-kennen-en-herkennen)**" project in which our main partner Naturalis cooperates is key. We've stayed the course, we are convinced it is still early days for sound recognition, and XC are there for the ride. Let's enjoy it :-)  
The first algorithm we introduce is **[AvesEcho v1](https://gitlab.com/arise-biodiversity/DSI/algorithms/avesecho-v1)**, created by **[Burooj Ghani](https://www.naturalis.nl/burooj-ghani)** and coworkers at **[Naturalis Biodiversity Center](https://www.naturalis.nl/)** as part of the EU Horizon projects **[MAMBO](https://mambo-project.eu/)** and **[GUARDEN](https://guarden.org/)**. This model focuses on European birds. At the moment, AvesEcho v1 is only run on XC to analyse mystery recordings of birds from Europe. After uploading a mystery recording, a message is posted on the forum only if AvesEcho detects one or more likely species in the recording. A list of these suggested species is visible for the recordist and admins on the recording page.  
Here we give a bit of background on ML algorithms, on the suggestions they give, how confident one should be about these, and on their limitations. For a more authorative account, see the books by I. Goodfellow, Y. Bengio and A. Courville (2016) or the more recent one by C. Bishop and H. Bishop (2023), both called "Deep Learning".  
## How are these ML algorithms made?  
AvesEcho v1 is built on top of the **[BirdNET](https://birdnet.cornell.edu/)** algorithm, developed by **[Stefan Kahl](https://www.researchgate.net/profile/Stefan-Kahl)** and co-workers at the Cornell Lab of Ornithology. Both models are convolutional neural networks that are specifically designed to classify sound recordings of birds to species level. The training data for BirdNET contains recordings derived from XC, the Macaulay Library, and additional recordings. For AvesEcho v1, European recordings from XC are used as the source for training. (In fact, XC is currently the main source for training material for building bioacoustics classifiers worldwide.)  
The training is done by giving example recordings to the algorithm, and subsequently updating its parameters to minimize a so-called "loss function" the value of which is designed to be low when classification is done well. More training data generally improves the performance of the model, but one has to be careful the model isn't 'too good' (giving excellent results on the training data but poor performance on test data) or 'not good enough' (simply performing poorly, usually because the model isn't able to capture the statistical properties of the data in a meaningful way). This is called "overfitting" and "underfitting", respectively.  
## When is a species suggested by the algorithm reported on XC?  
When AvesEcho v1 is run on a mystery, the recording is first cut into segments of three seconds. Each segment is then run through the model, and the output is a set of numbers, a "vector". The length of the vector is the number of species that the model is trained for. In the case of AvesEcho v1, this number is 585. The higher the number at a particular position, the higher the likelihood that the corresponding species occurs in the recording. That is the basic idea, but see below for the interpretation of these numbers. Also roughly speaking, when this number passes a threshold, that suggests that the species occurs and it is reported.  
In the design of AvesEcho v1, this cut-off threshold has been determined for each species individually, using the left-out test data derived from XC.  
The recordist of the mystery has access to more detailed output of AvesEcho v1, and sees per segment which suggested species has the highest score. This list of suggested detections makes it possible for the recordist to evaluate the three second snippet, and to ensure that the suggested species is indeed audible in the recording. Recordists are then able to set the foreground or background species labels using these suggestions.  
In XC, we log whether an identification is made after using a machine learning model. Such data gives proper context to the labels, and also provides various types of valuable new information to the people making the next version of the model.  
## What do the numbers mean?  
When a mystery recording is analysed and some species are detected, a list of results are displayed on the recording's page. At the end of each line, you notice a number between 0 and 1. Higher numbers are supposed to indicate that the suggested species is more likely to actually occur. However, we should be careful.  
It makes intuitive sense at first that one should interpret these scores as probabilities, with a single number in the vector being the likelihood that a species is found in the 3 seconds segment. This is incorrect, however. The numbers are produced in many so-called layers, the first of which is just the recording, and the last is the output vector. Each of these layers is just a vector of numbers. At the last stage (in the last layer), the numbers are passed through a sigmoid function, which squashes them into a range between 0 and 1. This makes it easy to compare one result with another, and higher scores are generally better, but that is all one can say about it.  
## Why are the results often obviously wrong?  
You will probably come across ML results that just have to be wrong. For example, an Atlantic Canary singing in the Dutch dunes, a Citrine Wagtail going at it for minutes in a soundscape from Spain, the appearance of some eagle species in a location that has no eagles anywhere near it, or a country-first in a list where common and clearly audible species are missing.  
These things happen, and it is often understandable on an acoustic level why this occurs: the 3 second segment contains a sound that actually is reminiscent of the reported species. AvesEcho v1 in fact has a feature to filter on location (i.e., if the recording is from France, say, the list of species reported contains only French species), but we have noticed this also causes many things to be missed. In particular, many migrant bird calls such as Dusky Warbler or Red-throated Pipit would be missed because they do not regularly occur at the recording location. For the moment we have therefore decided not to filter on location.  
The results from a machine learning model should therefore always be taken as suggestions only. On XC we have taken care to represent them as such.  
## What causes the current limitations of these algorithms?  
The main problem with the current generation of ML models, be it AvesEcho v1, BirdNET, or Google's **[Perch](https://github.com/google-research/perch)**, is that they are trained on 'weakly labeled data'.  
As mentioned, most training data for these models actually comes from XC, and all XC recordings have one foreground species as label for the entire recording. Only if recordists put in the additional effort there may also be one or more labeled background species, but even in that case those labels are not necessarily complete.  
XC recordings are called "weakly labeled" since the labels are for the entire recording, even though the birds probably do not vocalise continuously. When cut into three second segments for training these labels are routinely used for all segments, even though the species (foreground or background) may be absent on many of them. One can imagine that such a choice severely weakens how well these models can be trained.  
A clear way forward, is to generate stronger labels: noting when a particular species starts and stops vocalising in recordings, what the minimal and maximal frequencies are the bird uses, which sound type is audible, etc. Ideally, this should be done for all recordings on XC...! More news on that in 2025 :-)  
## More background on AvesEcho, BirdNET, Perch  
See  
* B. Ghani et al. 2023. **[Global birdsong embeddings enable superior transfer learning for bioacoustic classification](https://www.nature.com/articles/s41598-023-49989-z)** *Scientific Reports* **13**:22786.  
* S. Kahl et al. 2021. **++[BirdNET: A deep learning solution for avian diversity monitoring](https://www.sciencedirect.com/science/article/pii/S1574954121000273)++** *Ecological Informatics* **61**: 101236.  
