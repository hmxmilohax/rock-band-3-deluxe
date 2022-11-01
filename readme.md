# Rock-Band-3-Deluxe

![Header Image](dependencies/header.png)

## Introduction

This Repo contains everything you need to build an ark for Rock Band 3 Deluxe for Wii.

## Features

### Quality of Life
* Max song limit increased to 5000. Tested up to 2k (twice default) On a real Wii
* Song select ambient noise modifier, default disabled
* New menu, "RB3DX Menu", in game for additional modifications
* Selectable song speed and track speed by 5% increments
* Selectable venue framerate up to 60fps
* Selectable venues, including a "Black Venue" with decreased load times and system load
* Fast start executable modification by ihatecompvir
* Additional intro skip scripting to load the main menu by default and automatically start loading installed content
* Press select to restart the section in practice mode
* Default difficulty on first load is Expert
* Song title always visible modifier
* Keys on Guitar unlocked without meeting requirements


### Authoring
* Autoplay modifier for chart demos
* Gameplay watermarks to deter abuse of autoplay including -
    * Disabling autosave
    * Replacing endgame percentage with "BOT"
    * Manipulating MTV Overlay
* Cycle camera menu button - available in-game when autoplay is enabled

### Additional Modifications
* Selectable colors per fret/note/sustain (It works on Pro Drums/non-Pro Keys too!)
* Huge variety of custom song sources supported
* All official exports, DLC, and RBN sorted into individual sources
* Auto activating drum modifier (no fills mode)
* Translations for Spanish, French, German
* Post processing toggle - disables/reenables post processing in-game, or in menus
* Screensaver mode - remove UI elements from menus to view the background vingette unobstructed (it will softlock your game, so be careful!)
* Nice (69%) and Awesome Choke (98-99%) callouts on solo completion
* No crowd modifier
* No whammy effect modifier
* No sustain trails modifier
* Rock Band 2 Sustain look modifier
* Upgrades/fixes for tons of songs from [RB3_plus](https://github.com/rjkiv/rb3_plus)
* Compatibility with [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced)

## Install

Setting up the Rock Band 3 Deluxe repo for the first time is meant to be as easy as possible.

Download this branch by clicking the green "Code" button above.

in the Dependencies folder, there are two exe's that are needed for install. [Git for Windows](https://gitforwindows.org/), and [Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime).
Git is required for you to take advantage of auto updating via github pulls. Dot Net is required to build an ARK file, the archive format the game needs to run.
You can setup git with all default options, same with dot net.

On Wii (PROS ONLY), extract your Rock Band 3 ISO using [WIT](https://wit.wiimm.de/download.html), copy the files in "extracted_rb3/DATA/files/gen" to "_build/wii/".
Once copied, run "_build_wii.bat", then copy all the files in "_build/wii/" back to "extracted_rb3/DATA/files/gen" and repack using the "copy" command in wit.
Subsequent builds do not require copying the files from your extracted iso to "_build/wii/".
Copy to your wii using whatever method you usually use, or drag the ISO onto Dolphin to boot.

Run the build script again to pull any new updates committed to the repo and rebuild a new ark.

## Songs

~~You can find song packs compatible with all Rock Band titles for both platforms on the [Spreadsheet](https://docs.google.com/spreadsheets/d/1-3lo2ASxM-3yVr_JH14F7-Lc1v2_FcS5Rv_yDCANEmk/edit#gid=0).~~

There are currently no Wii songs available on the spreadsheet, instead use [Onyx Music Game Toolkit](https://github.com/mtolly/onyxite-customs) to convert/generate your own custom song packs for Rock Band 3 on Wii.

## Included Dependencies

[Git for Windows](https://gitforwindows.org/) - CLI application to allow auto updating rb3dx repo files

[Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime) - Needed to run ArkHelper

[Mackiloha](https://github.com/PikminGuts92/Mackiloha) - ArkHelper for building Rock Band 3 ARK - Superfreq for building .bmp_xbox highway images

[dtab](https://github.com/mtolly/dtab) - For serializing Rock Band dtb files
