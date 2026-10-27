# Contributing to Rock Band 3 Deluxe
Doc adapted from [RB3Enhanced](https://github.com/RBEnhanced/RB3Enhanced/blob/master/CONTRIBUTING.md)

We welcome all contributions to help make Rock Band 3 Deluxe a better mod, by improving
existing features or adding new ones. Collaboration, knowledge sharing, and passion
are the lifeblood of our community.

## Codebase

* Rock Band 3 Deluxe is a series of .dta script mods ran by the Harmonix game engine.
   Engine modifications to the executable are typically out of scope for "Deluxe" projects.
   Some specific cases do exist to change executables, however the Deluxe projects
   focus an overwhelming majority of attention on script modifications.
* Script mods are laid out in a fashion that mimic the layout of vanilla game scripts,
   which override the vanilla scripts via arks created by the build flow.
   When needed, a vanilla script may be added to the project structure to apply
   changes to the game. When this is done, compatibility should always be tested against
   supported platforms, Xbox 360, and PS3.
   * Ideally, all script handles being referenced in a single dta/scene, should be defined
   at the top of the same file.
   * Wii is primarily used for development with a debug build, but additional compatibility
   with Wii is always favorable.
* When adding a new vanilla DTA to the project, you must ensure the dta at the base vanilla level,
   before new changes are added, properly accounts for all differences in platforms.
   You will see this all over the repo as `#ifdef HX_{PLATFORM}`/`#ifndef HX_{PLATFORM}`.
* As Harmonix DTA is an in-house scripting language, we do provide [language syntax](https://github.com/hmxmilohax/tools/tree/main/syntax) for several different editors, to make things easier to read.
* All indentations should be 3 spaces.
* Try to adhere to any existing script styling already used in the codebase. However,
   a lot of legacy scripting could be written much better at this point, so keep
   this in mind when comparing to different scripting already written.

## Pull requests

* Test your changes before submitting them as a pull request, to ensure that
   they don't crash.
   * Emulators may mask fault behaviour, or return different results compared
   to a real console, so it's advised to use real hardware if possible.
   * Let us know what platform you've tested on.
* If possible, try to ensure the changes made work across all supported platforms.
   * If you can't do this, guard the implementation behind
   `#ifdef HX_{PLATFORM}`/`#ifndef HX_{PLATFORM}`.
* It's recommended that you enable "Allow contributors to edit code" in your
   pull request, so quick fixes can be added by us before merging.
* Try to keep a clean Git history.
   * Don't make excessive commits and don't force push too often.
   * If your PR hasn't been merged, try to keep it up to date with changes
   in the `develop` branch.

## LLM Policy

Responsible usage of LLMs to contribute code into Rock Band 3 Deluxe is highly
discouraged, but allowed. The best case scenario here is bug fixes to existing code.
We do not endorse or approve our mods being used in, or supported with bad faith
ai-driven projects such as ai recompilations.
When working on and submitting pull requests to Rock Band 3 Deluxe using
Large Language Models (or "Generative AI"), please keep the following in mind:

* **Purely "agentic" PRs with no human involvement are strictly forbidden and
   will be rejected. A human must be the one sending the PR.**
* When making the PR, you must at minimum disclose that LLMs were used in their
   creation, as well as the following:
   * Which model/service was used
   * How much the LLM was relied on (whether only to provide a few lines, or
   if it was entirely prompt driven / "vibe coded", for example)
   * **Trying to submit LLM code without disclosing will result in a ban.**
* LLMs can *not* be used to make large changes (e.g. "cleanups") to the codebase
   unprompted. The only changed code must be directly relevant to the PR.
* LLMs **must not** make tests. Tests written by LLMs are **strictly forbidden**
   as they will bloat the repo excessively.
* All text in the PR body must be human-written. Do not use an LLM to describe
   your changes.
* All user-facing text must be written by a human.
* You must ensure the code builds across all supported platforms and does the
   intended behaviour.
* You're expected to be able to point to any given line of code in your own
   change and explain why a certain decision was made - the answer should not be
   "IDK, the AI did it."
* LLMs are known to emit some amounts of code from copyrighted projects. If we
   suspect the output has enough copyrightable code from an incompatibly licensed
   project, we can't accept it.
* New files designed to assist with LLM development (e.g. `CLAUDE.md`,
   `AGENTS.md`, or any skills) will be rejected.
