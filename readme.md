# Rock-Band-3-Deluxe

![Header Image](dependencies/header.png)

# Table of Contents  
* [Introduction](#introduction)
* [Features](#features)
* [Setup](#setup)
* [Builds](#actions)
* [Repo Setup](#repo-setup)
* [Install](#install)
* [Install RPCS3](#rpcs3-emulator)
* [Install PS3](#ps3-hardware)
* [Install Xbox](#xbox)
* [Optional install custom highways](#optional-install-custom-highways)
* [Optional rb3_plus Keys Upgrades](#optional-rb3_plus-keys-upgrades)
* [Songs](#songs)
* [Dependencies](#dependencies)

# Introduction

This Repo contains everything you need to build an ark for Rock Band 3 Deluxe for PS3 or Xbox 360. For Wii, see the [Wii Branch](https://github.com/jnackmclain/rock-band-3-deluxe/tree/wii)

## Features

### Quality of Life
* Max song limit increased to 32767. Tested up to 11.2k in RPCS3
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
    * Replacing endgame percentage with `BOT`
    * Manipulating MTV Overlay
* Cycle camera menu button - available in-game when autoplay is enabled
* Rock Revolution drums register as Pro Keys on PS3/RPCS3, to allow easy demos for pro instruments
* Guitar Hero World Tour drums register as Pro Guitar/Bass on PS3/RPCS3, to allow easy demos for pro instruments

### Additional Modifications
* Selectable colors per fret/note/sustain (It works on Pro Drums/non-Pro Keys too!)
* Selectable Overshell colors
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
* Upgrades/fixes for tons of songs from [rb3_plus](https://github.com/rjkiv/rb3_plus)
* Compatibility with [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced)

## Setup

NOTE: You WILL need a modded/hacked console to play this mod on console. I hope this is clear

### Actions

There are now pre compiled ARK files available in many flavors in the [Actions](https://github.com/jnackmclain/rock-band-3-deluxe/actions) tab of this repo. These are ready to install files for RB3DX per platform. These arks have the following pre-built parameters.

* RB3DX-Base-*platform* - The default build of Rock Band 3 Deluxe
* RB3DX-*platform*-additional-keys - A build of Rock Band 3 Deluxe with included additional keys upgrades from [rb3_plus](https://github.com/rjkiv/rb3_plus)
* RB3DX-*platform*-pad-is-guitar - A build of Rock Band 3 Deluxe where joypad controllers are forced to act as guitars for traditional pad play
* RB3DX-PS3-stock-instrument-mapping - A build of Rock Band 3 Deluxe where GHWT and Rock Revolution kits on PS3 are restored to their correct controller mapping. Only useful if you have either of these two instruments and are playing on PS3 real hardware.

If using pre built actions, skip down to the `Install` section and assume any mention of `_build` is the contents of your zip file you downloaded from the Actions tab.

### Repo-Setup

Setting up the Rock Band 3 Deluxe repo for the first time is meant to be as easy as possible.
As well, it is designed to allow you to automatically receive updates as the repo is updated.

Simply go to the [Releases](https://github.com/jnackmclain/rock-band-3-deluxe/releases) of this repo and grab the `_init_repo` script for your platform. Currently there are .bat files for Windows and .sh files for linux, as well as a specific branch for Wii.

Included on the release page for ease of install are a couple dependencies, [Git for Windows](https://gitforwindows.org/), and [Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime).
Git is required for you to take advantage of auto updating via github pulls. Dot Net is required to build an ARK/HDR file, the archive format the game needs to run. You cannot run any deluxe title without building an ark first.

You can setup git with all default options, same with dot net.

Once the dependencies are installed, run `_init_repo.bat` in an **empty folder**. git will pull the repo and make sure you are completely up to date.

From then on simply run `_build_ps3.bat` or `_build_xbox.bat`, depending on the platform you are building for. This script will pull the repo again for updates, and build the ARK for you and spit it out in `\_build\xbox\gen` or `\_build\ps3\USRDIR\gen`

## Install

### RPCS3-Emulator

To install on rpcs3, copy all files/folders in `_build/ps3/` to `/dev_hdd0/game/BLUS30463/`

If the folder does not exist, create it. The game will need the included .bin file, and a built .ark/.hdr to function. The folder format in `/_build/ps3` matches how it should be installed.

Overwrite files if asked.

Run the build script again to pull any new updates committed to the repo and rebuild a new ark/hdr.

### PS3-Hardware

**NOTE: You WILL need a modded/hacked console to play this mod on console. I hope this is clear**

To install on real PS3, you will have to install vanilla patch 1.05 on your ps3 first to register the update in your system.

Next, copy all files/folders in `_build/ps3/` to `/dev_hdd0/game/BLUS30463/`

If the folder does not exist, you have not installed vanilla patch 1.05. You need to do this first. The game will need the included .bin file, and a built .ark/.hdr to function. The folder format in `/_build/ps3` matches how it should be installed.

Overwrite files if asked.

Run the build script again to pull any new updates committed to the repo and rebuild a new ark/hdr.

### Xbox

**NOTE: You WILL need a modded/hacked console to play this mod on console. I hope this is clear**

On Xbox, copy the gen folder and the xex from `_build/xbox/` to the same location your base copy of Rock Band 3 lives.

If installing for the first time, make sure you rename the vanilla `default.xex` to `default_vanilla.xex` for safety.

Make sure you clear your song cache, as well as your system cache.

To clear song cache, navigate to `System Settings>Storage>Rock Band 3` and delete the song cache.

To clear system cache, navigate to `System Settings>Storage` and press Y to clear the system cache.

Also make sure to `disable` any enabled updates for Rock Band 3 in Aurora. Rock Band 3 deluxe rolls TU5 into its base installation.

If you are also running [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced), grab the optional folders in `/_build/_optional-xbox-rb3e-rawfiles/` and place the `config` and `ui` folders next to the `gen` folder on your Xbox.

Run the build script again to pull any new updates committed to the repo and rebuild a new ark/hdr.

## Optional-rb3_plus-Keys-Upgrades

[rb3_plus](https://github.com/rjkiv/rb3_plus) features optional key upgrades that you can install alongside RB3DX fairly easily. These upgrades include new audio files (moggs) for the upgraded songs. These take up additional file size and generally are a generation removed from the original audio mix with additional processing, but can be a great addition for any keys player.

You can simply download a build of Rock Band 3 Deluxe containing these upgrades from the [Actions](https://github.com/jnackmclain/rock-band-3-deluxe/actions) tab of this repo. The following steps are for a manual install with a local copy of the [Repo Setup](#repo-setup).

To take advantage of these upgrades, first ensure [python](https://www.python.org/downloads/) is downloaded, and installed into PATH. Click the checkbox presented during python install to ensure this.

Head to the `/dependencies/` folder in this repo and run the install_gitpython.bat, or run `pip install gitpython` in cmd.

Next simply run the `enable_keys.bat` or `disable_keys.bat` to download the new mogg files and enable their additions.

Rebuild your ark and reinstall Rock Band 3 Deluxe to see your new keys upgrades!

## Optional-Install-Custom-Highways

This repo also supports the import of custom highways and groove/spotlights via the use of a bat script, python script, manual dta editing and a couple external dependencies included, but it's way easier than it sounds to create your own.

RB3DX includes a variety of custom highways by default, available via the "RB3DX Menu", but you can add your own with the following steps.

Simply drag in a .jpg/.png/.bmp into the `highways` folder at the root of the repo, then run `highways.bat`.
Or, drag in a .jpg/.png/.bmp into the `spotlights` folder at the root of the repo, then run `spotlights.bat`.

This will size your images accordingly (supports arbitrary resolutions), and convert them to the proper format for rb3 to read. Spotlights will be set to 50% opacity.

A .dta file will be generated for a list of your custom highways/spotlights.
You must copy and paste the contents of the generated dta, and overwrite the similar data in another dta.

For highways, copy all contents from `_ark/ui/track/surfaces/highways.dta`.
For spotlights, copy all contents from `_ark/ui/track/surfaces/spotlights.dta`.

Next go to `_ark/ui/overshell/slot_states.dta` and search for `highways.dta` or `spotlights.dta`.
Being careful to stay within the parenthesis, highlight and delete existing custom highways. All existing custom highways are within quotation marks.

Paste your desired block of highways over the existing block.

You will need to run the build script to again to create your new ARK and reinstall RB3DX to your desired platform.


## Songs

You can find song packs compatible with all Rock Band titles for both platforms on the [Spreadsheet](https://docs.google.com/spreadsheets/d/1-3lo2ASxM-3yVr_JH14F7-Lc1v2_FcS5Rv_yDCANEmk/edit#gid=0).

You can also use [Onyx Music Game Toolkit](https://github.com/mtolly/onyxite-customs) to generate your own custom song packs for Rock Band games.

## Dependencies

[Git for Windows](https://gitforwindows.org/) - CLI application to allow auto updating rb3dx repo files

[Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime) - Needed to run ArkHelper

[Mackiloha](https://github.com/PikminGuts92/Mackiloha) - ArkHelper for building Rock Band 3 ARK - Superfreq for building .bmp_xbox highway images

[dtab](https://github.com/mtolly/dtab) - For serializing Rock Band dtb files

[python](https://www.python.org/downloads/) - for more detailed script functions such as enabling/disabling extra keys support
