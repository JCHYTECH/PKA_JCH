# XENO-CANTO

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-06-13 18:37

�����oXENO-CANTO

Introducing xcapi: A simple way to access Xeno-canto data from the command line and Python
By Burooj Ghani
April 21, 2026
Xeno-canto has become an essential resource for bioacoustics, with a vast collection of recordings contributed by a global community. It is an incredible platform for exploring species and soundscapes, but when it comes to working with larger sets of recordings - whether for analysis, dataset creation, or integration into workflows - the process can quickly become time-consuming.
To make this easier, I developed xcapi, a lightweight Python tool for searching and downloading Xeno-canto recordings programmatically. The idea is simple: take the flexibility of Xeno-canto’s search system (API) and make it directly usable from the command line or within Python, so that moving from a query to a structured dataset becomes straightforward.
One of the main goals was to keep things as simple as possible. For many use cases, no programming is required at all. For example, the following command runs directly in the terminal and downloads high-quality bird songs from Spain:
xcapi --grp birds --cnt Spain --type song --q ">C" --output_dir ./data
This single command performs the search, downloads all matching recordings, and saves a metadata.csv file alongside the audio. In practice, this means that what would otherwise involve repeated manual downloads can be done in one step.
For users working in Python, xcapi provides a small API that allows the same queries to be constructed programmatically inside a Python script. A query can be built in a readable way, executed, and the results downloaded:
from xcapi.query import QueryBuilder
from xcapi.client import XenoCantoClient
from xcapi.downloader import Downloader

query = QueryBuilder().group("birds").country("Spain").quality(">C").build()

client = XenoCantoClient()
recordings = client.search(query)

downloader = Downloader(output_dir="./data")
downloader.download_recordings(recordings)
This is particularly useful when building reproducible workflows, for example in machine learning applications or when analysing patterns across regions or time. The metadata that accompanies each download makes it easy to keep track of recording details and reuse datasets later.
More broadly, tools like xcapi make it easier to move from individual recordings to structured collections of data. This can support a range of use cases, from building training datasets for species recognition to exploring ecological or geographic patterns, and integrating acoustic data into larger biodiversity monitoring workflows.
xcapi is available via pip:
pip install xenocanto-api
The project is open source, and more details, examples, and documentation can be found here: https://github.com/bghani/xcapi
The goal is not to replace the Xeno-canto interface, but to complement it - providing a simple bridge between the archive and computational workflows. Feedback and suggestions are very welcome.
This article was last updated on April 21, 2026 at 15:11


API functionality updated
By Bob Planqué and Willem-Pier Vellinga
April 10, 2025
As of April 10, 2025, the XC API has received a big update. This was necessary to alleviate the pressure on the server from bots and keep the site available to its users.
In this article we give a short explanation of the most important changes and what they mean for XC users, researchers, app builders, and others that use the API.
Phasing out v2
The old version v2 has gone off line on October 10, 2025. So please update your code if you have built the API into your app, or have written an API wrapper such as XenoPy to download recordings and metadata.
The new API is available at
https://xeno-canto.org/api/3/recordings
Use your personal key to access the API
The v3 API can only be used with your personal key. For example,
https://xeno-canto.org/api/3/recordings?query=sp:"larus fuscus"&key=demo
This key is available to registered users only, and may be found in your Account page. The key will allow us to better monitor usage and improve the underlying queries whenever necessary.
Use at least one search tag in your query
The tag system with which you can search for genus, location, recordist, etc, has been changed. You now always need to use at least one tag. So if you wish to find recordings of Larus fuscus, you should use either
https://xeno-canto.org/api/3/recordings?query=sp:"larus fuscus"&key=demo
or
https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&per_page=50&page=3&key=demo
The demo key should be replaced with your own personal key of course.
The API page gives much more detail on the new situation, and read the Search tips for full documentation on how to use the search tags.
This article was last updated on February 6, 2026 at 12:52

A short introduction to Machine Learning results
By Bob Planqué and Willem-Pier Vellinga
October 15, 2024
From day 1 in 2005, Xeno-canto has been about recognising sounds as much as about collec
