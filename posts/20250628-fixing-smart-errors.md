----
date: 2025-06-28
title: fixing 'Currently unreadable (pending) sectors' errors
subtitle: how not to fix a hard drive
----

Let's say you have a drive, and `smartctl -a` shows you some `197 Current_Pending_Sector` errors.

Here's a (hacky-as-all-fuck, using-`badblocks`-against-`man`-advice, against-best-practices, potentially-very-harmful) quick fix:

```sh
badblocks -vsb 4096 > bad-sectors
for x in $(cat bad-sectors);
	do sudo dd if=/dev/zero of=/dev/sdX bs=4096 count=1 seek=$x;
done
```

Just in case it's not abundantly clear from glancing at this: **do not run** any of that against any valuable, non-backed up data.
