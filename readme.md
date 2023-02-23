# Rock Band 3 Deluxe

![Header Image](dependencies/header.png)

# Table of Contents  
- [Rock Band 3 Deluxe](#rock-band-3-deluxe)
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Features](#features)
    - [Quality of Life](#quality-of-life)
    - [Authoring](#authoring)
    - [Additional Modifications](#additional-modifications)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Pre-Built Versions](#pre-built-versions)
  - [Repo Setup](#repo-setup)
- [Install](#install)
  - [Xenia Emulator](#xenia-emulator)
  - [RPCS3 Emulator](#rpcs3-emulator)
  - [PS3 Hardware](#ps3-hardware)
  - [Xbox 360 Hardware](#xbox-360-hardware)
- [Optional Upgrades](#optional-upgrades)
  - [Songs](#songs)
  - [rb3_plus Keys Upgrades](#rb3_plus-keys-upgrades)
  - [Installing Custom Textures](#installing-custom-textures)
- [Dependencies](#dependencies)

# Introduction

This repo contains everything you need to build Rock Band 3 Deluxe for PS3 or Xbox 360. For Wii, see the [Wii Branch](https://github.com/hmxmilohax/rock-band-3-deluxe/tree/wii).

## Features

### Quality of Life
* Max song limit increased to 8000. Above 5000 can lead to instability issues, use with caution.
* Song select ambient noise modifier, default disabled
* New menu, "RB3DX Settings", in game for additional modifications
* Selectable song speed and track speed by 5% increments
* Selectable venue framerate up to 60fps
* Selectable venues, including a "Black Venue" with decreased load times and system load
* Fast start executable modification by ihatecompvir
* Additional intro skip scripting to load the main menu by default and automatically start loading installed content
* Press select to restart the section in practice mode
* Default difficulty on first load is Expert
* Song title always visible modifier
* Keys on Guitar unlocked without meeting requirements
* Manual calibration adjusts by 1ms instad of 5ms


### Authoring
* Autoplay modifier for chart demos
* Gameplay watermarks to deter abuse of autoplay including -
    * Disabling autosave
    * Replacing endgame percentage with `BOT`
    * Manipulating MTV Overlay
* Cycle camera menu button - available in-game when autoplay is enabled
* Rock Revolution drums register as Pro Keys on PS3/RPCS3, to allow easy demos for pro instruments
* Guitar Hero World Tour drums register as Pro Guitar/Bass on PS3/RPCS3, to allow easy demo for pro instruments

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
* New main menu music pulled from other Rock Band titles
* No crowd modifier
* No whammy effect modifier
* No sustain trails modifier
* Rock Band 2 Sustain look modifier
* Upgrades/fixes for tons of songs from [rb3_plus](https://github.com/rjkiv/rb3_plus)
* Compatibility with [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced) for Xbox 360
* Fast start, Song Blacklist, UGC Demo, Anti Debugger patches from [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced) Embedded directly into DX binaries.

# Prerequisites

### You will need...

- **A vanilla copy of Rock Band 3** for PS3 or Xbox 360 that you can extract onto your PC
- For Console: A **modded/hacked PS3 or Xbox 360** and a way to transfer files to it, we reccomend using FTP
- For Emulator: A **mid-to-high-end PC** capable of running RPCS3 or Xenia

# Setup

There are a couple different ways you can set up Rock Band 3 Deluxe, you can download a [Pre-Built Version](#pre-built-versions) or [set up the Repo](#repo-setup).

Pick which one is best for you.

## Pre-Built Versions

There pre-compiled versions of Rock Band 3 Deluxe available in many flavors in the [Actions](https://github.com/hmxmilohax/rock-band-3-deluxe/actions) tab of this repo and in the [Nightly link](https://nightly.link/hmxmilohax/rock-band-3-deluxe/workflows/build/main). These are ready-to-install files for Rock Band 3 Deluxe for both platforms.

These are reccomended if you have no way of setting up the repo (unspported platform, no administrator privelages, etc) or if you get stuck at any point.

### The different flavors are as follows:

* RB3DX-*platform*-Base - The default build of Rock Band 3 Deluxe
* RB3DX-*platform*-original-mids - Rock Band 3 Deluxe, but without any harmonies or chart updates
* RB3DX-*platform*-keys - A build of Rock Band 3 Deluxe with included additional keys upgrades from [rb3_plus](https://github.com/rjkiv/rb3_plus)
* RB3DX-PS3-stock-instrument-mapping - A build of Rock Band 3 Deluxe where Guitar Hero and Rock Revolution drum kits on PS3 are restored to their correct controller mapping. Only useful if you have either of these two instruments and are playing on PS3 hardware

If you're going to be using a pre-built patch, skip down to the [Install](#install) section. Any mention of `_build` is the contents of the zip file you downloaded from the Actions tab or Nightly link.

## Repo Setup
Setting up the Rock Band 3 Deluxe repo for the first time is meant to be as easy as possible.
As well, it is designed to allow you to automatically receive updates as the repo is updated.

Simply go to the [Releases](https://github.com/hmxmilohax/rock-band-3-deluxe/releases) of this repo and grab the `_init_repo` script for your platform. Currently there is a `.bat` file for Windows and a `.sh` file for linux, as well as a specific one for the Wii branch.

Included on the release are a couple dependencies, [Git for Windows](https://gitforwindows.org/), and [Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime). **These are both required in order to properly build Rock Band 3 Deluxe**.

In addition to this, you will also need to install [Python](https://www.python.org/downloads/). We reccomend version **3.9 or later**.

**Install all three of these with their default options.** If you're unable to, head back to [Pre-Built Versions](#pre-built-versions) and follow those instructions instaed.

Once they are all installed, in **an empty folder**, run `_init_repo.bat` if you're on Windows or `_init_repo.sh` if you're on Linux. This will pull the repo down for you and make sure you're completely up to date. This will take some time. If it opens and immediately closes, make sure you have [Git for Windows](https://gitforwindows.org/) installed.

**The folder should now look like this:**

![Repo Folder](dependencies/images/repofolder.png)

From then on, navigate to the `user_scripts` folder and simply run `build_ps3.py`, `build_xbox.py`, or `build_xenia.py` depending on your platform to stay updated and build Rock Band 3 Deluxe.

**If any of these open and immediately close, make sure you have all the required dependencies installed.**

After that, everything you need to run the mod (minus the vanilla game) will be in `\_build\xbox\gen` or `\_build\ps3\USRDIR\gen`.

# Install

## Xenia Emulator

Xenia is the most convenient way for us to test our mods, and we reccomend you do so if you ever decide to contribute to this project.

To install on Xenia, first extract your vanilla Rock Band 3 game disc and extract **ONLY** the *contents* of the `gen` folder in `\_build\xbox\gen`.

Then, navigate to `user_scripts` and run `build_xenia.py` to automatically build and run Rock Band 3 Deluxe. If it opens and immediately closes, make sure you have [Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime) installed.

If it opens to a black screen, that means you don't have your vanilla Rock Band 3 disc's `gen` folder extracted to `\_build\xbox\gen`.

**`_build/xbox/gen` should now look like this:**

![Xbox Repo](dependencies/images/xboxrepo.png)

NOTE: If you experience bugs regarding textures or models, navigate to `_xenia`, open `xenia-canary.config.toml` in your text editor of choice, and change `gpu` from `vulkan` to `d3d12` and `d3d12_readback_resolve` from `false` to `true` (you may need to press `CTRL + F` to find these). This will fix all texture issues but will drasticly affect the framerate, you also may experience BSODs. If you don't want to deal with any of this, we reccomend using [RPCS3](#rpcs3-emulator) instead.

![D3D12](dependencies/images/d3d12.png)
![Readback Resolve](dependencies/images/readbackresolve.png)

## RPCS3 Emulator

To install on RPCS3, first extract your vanilla Rock Band 3 game disc and place it in the `games` folder in your RPCS3 directory. **Do NOT touch this folder once it's installed, it is needed to run Rock Band 3 Deluxe as it installs as a PS3 update and must be installed in its own respective folder, shown below.*

Then, copy the contents of `_build/ps3/` to `/dev_hdd0/game/BLUS30463/`.

If the `BLUS30463` folder does not exist, create it.

If you are asked to overwrite any files, click `Yes`.

**`/dev_hdd0/game/BLUS30463/` should now look like this:**

![RPCS3 Path](dependencies/images/rpcs3path.png)

To update Rock Band 3 Deluxe, repeat [the above steps](#rpcs3-emulator). You can click the `Watch` button (All Activity) to be notified about any updates that occur.

NOTE: If you experience bugs regarding textures or models, right-click Rock Band 3 in your RPCS3 games list and create a custom configuration. Then, go to the `GPU` tab and enable `Write Color Buffers`. This will not affect the framerate nearly as much as it does on Xenia.

![Custom Configuration](dependencies/images/customconfig.png)
![GPU Tab](dependencies/images/gputab.png)
![Write Color Buffers](dependencies/images/writecolorbuffers.png)

## PS3 Hardware

**NOTE: You WILL need a HACKED/MODDED (CFW or HFW/HEN) PS3 in order to play this mod on console. We hope this is clear.**

**NOTE: Do NOT touch any of the contents of your vanilla game, Rock Band 3 Deluxe installs as a PS3 update and must be installed in its respective folder, shown below.*

**If you are using a Guitar Hero or Rock Revolution drum kit, navigate to `_ark\config` and delete `joypad.dta` or head back to [Pre-Built Versions](pre-built-versions) and download `RB3DX-PS3-stock-instrument-mapping`.**

To install on a real PS3, first you need to make sure you have Rock Band 3 version `1.05` installed on your system. You can check this by inserting your disc, pressing `Triangle`, and scrolling down to `Check for Update`. If it asks you to update, do so here.

Then, copy the contents of `_build/ps3/` to `/dev_hdd0/game/BLUS30463/`.

If the folder does not exist, that means you have not installed Rock Band 3 version `1.05`.

If you are asked to overwrite any files, click `Yes`.

**`/dev_hdd0/game/BLUS30463/` should now look like this:**

![RPCS3 Path](dependencies/images/rpcs3path.png)

To update Rock Band 3 Deluxe, repeat [the above steps](#ps3-hardware). You can click the `Watch` button (All Activity) to be notified about any updates that occur.

## Xbox 360 Hardware

**NOTE: You WILL need a HACKED/MODDED (RGH or JTAG) Xbox 360 in order to play this mod on console. We hope this is clear**

On Xbox, copy the contents of `_build/xbox/` to the location where your vanilla copy of Rock Band 3 is.

**Your `gen` folder should now look like this:**

![Xbox Repo](dependencies/images/xboxrepo.png)

If you're installing Rock Band 3 Deluxe for the first time, it is reccomended that you rename the vanilla `default.xex` to `default_vanilla.xex` for safety.

Make sure you clear your song cache, as well as your system cache.

To clear your song cache, navigate to `System Settings > Storage > Rock Band 3` and delete the song cache.

To clear your system cache, navigate to `System Settings > Storage` and press `Y` to clear the system cache.

Also, make sure to `disable` updates for Rock Band 3 in Aurora. Rock Band 3 Deluxe rolls `TU5` into its base installation.

If you are also running [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced), grab the optional folders in `/_build/_optional-xbox-rb3e-rawfiles/` and place the `config` and `ui` folders next to the `gen` folder on your Xbox.

To update Rock Band 3 Deluxe, repeat [the above steps](#xbox-360-hardware). You can click the `Watch` button (All Activity) to be notified about any updates that occur.

# Optional Upgrades

## Songs

You can find song packs compatible with all Rock Band titles for both platforms on this [Spreadsheet](https://docs.google.com/spreadsheets/d/1-3lo2ASxM-3yVr_JH14F7-Lc1v2_FcS5Rv_yDCANEmk/edit#gid=0).

You can also use [Onyx Music Game Toolkit](https://github.com/mtolly/onyxite-customs) to generate your own custom song packs for Rock Band games.

## [rb3_plus](https://github.com/rjkiv/rb3_plus) Keys Upgrades

[rb3_plus](https://github.com/rjkiv/rb3_plus) features optional Keys and Pro Keys upgrades that you can install alongside Rock Band 3 Deluxe fairly easily. These upgrades include new audio files (.mogg's) for the upgraded songs. These take up additional file size and generally are a generation removed from the original audio mix with additional processing, but can be a great addition for any Keys or Pro Keys player.

You can download a build of Rock Band 3 Deluxe containing these upgrades from the [Actions](https://github.com/hmxmilohax/rock-band-3-deluxe/actions) tab of this repo and in the the [Nightly link](https://nightly.link/hmxmilohax/rock-band-3-deluxe/workflows/build/main).

## Installing Custom Textures

This repo also supports the import of custom highways and groove/spotlights via the use of a script.

Rock Band 3 Deluxe includes a variety of custom highways by default, available in the `RB3DX Settings` menu in-game, but you can also add your own with the following steps.

Simply drag in a .jpg/.png/.bmp into the `highways` folder in `custom_textures`, then navigate back to `user_scripts` and run `process_textures_highway.py`.

Or, drag in a .jpg/.png/.bmp into the `spotlights` folder in `custom_textures`, then navigate back to `user_scripts` and run `process_textures_spotlight.py`.

This will size your images accordingly, including those with arbitrary resolutions, and convert them to the proper format for Rock Band 3 Deluxe to read. Spotlights will be set to 50% opacity.

**You will need to rebuild Rock Band 3 Deluxe in order for these to take effect.**

## Dependencies

[Git for Windows](https://gitforwindows.org/) - CLI application to allow auto updating Deluxe repo files

[Dot Net 6.0 Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime) - Needed to run ArkHelper

[Python](https://www.python.org/downloads/) - For user script functionality (NOTE: 3.9 or newer is highly recommended!)

[Mackiloha](https://github.com/PikminGuts92/Mackiloha) - ArkHelper for building Deluxe - SuperFreq for building .bmp_xbox highway images

[swap_rb_art_bytes.py](https://github.com/PikminGuts92/re-notes/blob/master/scripts/swap_rb_art_bytes.py) - Python script for converting Xbox images to PS3

[dtab](https://github.com/mtolly/dtab) - For serializing `.dtb` script files
