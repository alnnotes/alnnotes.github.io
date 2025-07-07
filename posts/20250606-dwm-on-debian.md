----
title: dwm on debian bookworm
date: 2025-06-06
subtitle: some lessons learned from decades of running an obsolescent tiling window manager
----

For a long time, I was using `dwm5.6` (2009-2022ish), because I had hand-patched `dwm.c` to support a particular workflow quirk re multi-monitor tag behaviour, and didn't feel too much like doing it again.

Working as I am now with a single desktop monitor, I decided to just get rid of it and install `dwm6.5` (2024). Follows are notes, honed from years of compiling years-out-of-date `dwm` instances on dozens of machines. *Note: I started this guide with the idea of it being a 'how to install in 2025' sort of guide, but that turns out to be pretty straight-forward, so this instead contains tips-and-tricks, gotchas, and some less-than-intuitive stuff that still remains in the most-recent version.* This is not a particularly-'beginner friendly' guide; basic \*nix administration is assumed. I will add to this post whenever I find myself doing anything wm-related.

## Downloading and installing 

- I strongly recommend working from a `~/dwm` working directory, or similar
- I also strongly recommend setting this directory up as a VCS repo, especially if you have any longer-term plans for using it
- Fetch from <https://dwm.suckless.org>. `tar -xf` it, and `cd` into `dwm-6.5`
- `make` and fix any missing prereqs. Here are the ones I had to (on `bookworm`, and these are all `bookworm` packages):

|  |  |
-|-
`X11/Xlib.h`	| `libx11-dev`
`X11/Xft/Xft.h`	| `libxft-dev`
`X11/extensions/Xinerama.h`	| `libxinerama-dev`

- `sudo make clean install`
- fetch `dmenu` (5.3 was the most-recent at time of writing) from <https://tools.suckless.org/dmenu>
- extract, `make`, `sudo make clean install`

## `.desktop` file

To support `lightdm` and `gdm` (and doubtlessly others), create a `.desktop` file in `/usr/share/xsessions/` with the following content:

```text
[Desktop Entry]
Encoding=UTF-8
name=dwm
comment=dwm
Exec=<rundwm script>
Type=XSession
```

- `chmod a+r` it

## `rundwm` script

as referenced in the `.desktop`, create an auxillary running script. the following is a barebones example that should at least give you an ideal of what it might contain:

```sh
while true; do
    xsetroot -name "$( date +"%a %d %b %Y  %R")"
    sleep 0.5m
done &
 
vivaldi &
thunderbird & 
 
exec dwm
```

- also `chmod a+r`

## configuration

most configuration can be achieved by editing `config.h`; only much-deeper changes to the fundamental behaviour require changes to `dwm.c`. it's largely self-explanatory, other than some unintuitive bits described below:

- run `xprop` and click on a target instance/window
- `WM_CLASS(STRING)` will give you `(<instance>, <class>)`
- `WM_NAME(STRING)` (if it exists, which it likely won't) will give you `<title>`
- fill in one (but not multiple) of those into the `rules[]` `const` and control which tags things start with

<!--  -->

- for tag masking, the tags are zero-indexed left-to-right
- `0` is the first tag (or `0`)
- `1 << 3` is the fifth tag (or `4`)

<!--  -->

- `#define MODKEY Mod4Mask`. `MODKEY` is the primary modifier; setting it to `Mod4Mask` uses `super`, which I think works pretty well alongside shift.

<!--  -->

- to issue `custom --command` on keypress:
- declare the following: `static const char *foo[] = {'custom', '--command', NULL}` (that's right; do your own null-terminating). the important thing to note here is that spaces get swallowed into an array of space-separated command elements
- then add it to `keys[]` as such: `{MODKEY|ShiftMask, XK_Delete, spawn {.v = foo }}` (for `MODKEY`+shift+del, for example)
- get the `XK_foo` value for your desired key from an `xev -event keyboard` query; follow the `MODKEY|ShiftMask` stuff from examples already in `keys[]`

## patching

- download a patch diff from suckless, add it to a `patches/` subdirectory
- in the `dwm.c` directory: `patch -p1 < patches/foo-patch.diff`
- note: the diff for `swapfocus` is broken, but it can be fixed by partially applying it, then opening `dwm.c.rej` and manually applying the logic to the conditional it fails on. the logic has changed since the version it was compiled for, but a bit of common sense will get you there. bonus: you get to boast ‘oh, you just customise by editing `config.h`? if i’m having a problem with `dwm`, i just edit the `c` source. no biggie.’ **if you fail here, try using the stacker patch. its features are a superset of `swapfocus`‘s** – just modify the conf a little.

## miscellaneous hints and tips

- the `rundwm` script above just throws some basic information into `X`'s `WM_NAME`/’status bar’. if you want something more complex there, it’s probably easiest to branch out from that bash script and use `dwmstatus`. see: <https://dwm.suckless.org/status_monitor/>
- <https://github.com/kolbusa/stalonetray> works very well if you wish to occasionally (there are better solutions if this is part of your workflow, but it’s not part of mine, so I don’t know what they are) use the system tray/access something through the system tray. I prefer not to remember network configuration commands, and I haven’t come across anything simpler than `nm-applet`, so O use `stalonetray` almost exclusively for that (probably less than once a month)
- <https://gist.github.com/nic0-lab/c435dd4e77b2b3d274d142b126899525> is a good page to ctrl+f a keyword to find a patch
- download `wmname` from <https://tools.suckless.org/x/wmname/>; extract it; `make` and `make clean install`. if you run into any application that misbehaves, **your first attempt to fix it should be `wmname LG3D`**. this commandlet will work in >95% of cases, in my experience.