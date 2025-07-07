----
title: Essential bash hacks
date: 2025-06-02
subtitle: for me, at least
----

Create `~/.inputrc` with the following:

```sh
$include /etc/inputrc

set completion-ignore-case On
"\e[A":history-search-backward
"\e[B":history-search-forward
```

- to ignore case when completing directory names, binary names, etc. (_e.g._, in `cd`)
- to reverse-history-search starting from a partial command, using up- and down-arrows (_e.g._, `whoa ↑` may show `whoami` if it had been previously typed. use arrow keys to navigate back and forth between historical partial matches)

Add `export QUOTING_STYLE=literal` to `.bashrc` to get back to `coreutils` pre-8.25 `ls` behaviour (before a **BUG** was included; see <https://unix.stackexchange.com/a/262162> for a nice dose of vitriol).
