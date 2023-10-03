# MTGate

MTGate is an attempt on [MTGA](https://magic.wizards.com/en/mtgarena) API reverse engineering. For now it is just a single Python script `mtga_simu.py`, with which I can 
- log in with my credential token loaded from Windows registry,
- establish a TLS connection with the server and get account information,
- and begin a "Standard play" pairing with my last used deck.

As stated above, there are some limitations now.
- It only applies to Windows "directly installed" version of MTGA (to acquire tokens and DLLs), while the Steam and Epic versions need little tweaks.
- There should be a recently used account that has created a "remember me" token in the registry, while the username and password (full login) need middle tweaks.
- There should be a recently used deck in the "Standard Play" mode, while other constructed formats and decks need minor tweaks and other limited formats large tweaks.
- The script provides no interaction so far, and advances to pairing directly. The actual card play part is still worked on.

## TODOs

[ ] structured code
[ ] testcases

[x] mock official client traffic
[ ] wiretapping official client using `mitmproxy`
[ ] built-in card play
[ ] re-connect and custom network route support
[ ] (T)UI
    - [ ] advanced and customizable information display
    - [ ] REPL
[ ] more format and deck support
    - [ ] interactive and explorable stuffs
[ ] connection to other MTGA simulators (Forge, Xmage, TTS)
[ ] programmable AI support
[ ] cheating

## Current progress

I'm trying to understand card play APIs. I'm using official DLLs to decode the traffic, and see if I can know the game state and play a card with only scripts.

## About the name

You can pronouce "MTGate" as "mitigate", and abbreviate it as "MTGT". I hope it can mitigate the pain of frequent loss of connection with the official client.

I came up with this name one sleepless night, along with some other names like "MTG Barebone", "MeTaGaMe (MTGM)", "MTG Arena Lite". I think if I somehow manage to make a more playable thing, I can use the MTGM name then. And you can propose your name if you want.

## About the design

MTGA is a server-based game, and any cheating comes with a risk (which is therefore not the primary goal). I try to make this script, because MTGA official client has poor support for re-connecting after network errors. This project should mock the network traffic of MTGA client, and make it possible to finish a match without opening the GUI client.

There are many ways to customize the client. Many people have tried to use key deamons (like [this](https://github.com/hornsilk/BreyaBot)) to click inside the client. This does not solve my problem, however, as my problem comes with poor connection and terrible offline detection of MTGA client. The key deamon can not improve the waiting experience.

Injecting the game DLL is also cool, in which way [Dan found a lot of interesting things](https://www.mayer.cool/writings/I-Hacked-Magic-the-Gathering/). I also modified the `Assembly-CSharp.dll` a little bit with dnSpyEx to print the logs, but I don't have the confidence to rewire the whole GUI logic to skip the nonsense by myself.

Starting a separate client from scratch is as flexible as hijacking client network connections. I finally decided to do a minimal customized client, because I only need to deal with the network protocol then. The separate client can be easily transformed to a network hijacker with `mitmproxy`.

I choose Python to write the script because I feel for its easy grammar and believe in Python's marvelous package ecosystem. Of course the official client is written in C# with Unity support, but after a failure to call MTGA's DLLs from Visual Studio, I gave up the idea to write C# dependent on Mono. As Python is the most convenient standalone script language, it serves best with a proof-of-concept implementation.

## Acknowledgement

The project relies on the elegant [dnSpy(Ex)](https://github.com/dnSpyEx/dnSpy) to reverse engineer the MTGA network API inside C# DLL, the powerful[mitmproxy](https://mitmproxy.org/) to inspect real network traffic of MTGA, the constant updating [MTGA protocol repo](https://github.com/riQQ/MtgaProto/blob/master/messages.proto) for the protobuf implementation as well as [Python.NET](https://pythonnet.github.io/) to call MTGA's C# DLL functions to decrypt the protobuf data. Many thanks also to Python's `json`, `requests`, `ssl`, `winreg`, `socket` and `enum` packages.