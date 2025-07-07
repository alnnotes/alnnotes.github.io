----
date: 2025-07-03
title: cleaning a music directory
subtitle: strictly for directories full of legally-obtained music
----

a couple of quick `find` tricks, using a music folder as an example

## find and delete non-music tracks

my music folder tends to be filled with `.cue`, `.m3u`, `.txt`, and `.jpg` files. find them all:

```sh
find . -type f \! \( -name '*.flac' -o -name '*.mp3' \)
```

delete them: append `-delete`

## clear out empty folders

most of those images, for instance, were in folders called 'cover art' or 'scans' or similar. find empty folders:

```sh
find . -type d -empty
```

delete them: append `-delete`