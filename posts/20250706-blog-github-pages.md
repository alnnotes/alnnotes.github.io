-----
title: "BLOG: setting up github pages"
date: 2025-07-06
-----


**WIP WIP WIP**

for the first proof-of-concept hosting i figured i'd just go for github pages. follws is a description of how to take the following folder structure, and make it nicely browsable as a website hosted with github pages. **note:** for parsimony and conciseness, the following guide describes the steps to take to set up exactly this blog; if you wish to follow them, you must adjust as necessary.

note: i have _very_ limited and _very_ out-of-date experience with github (specifically -hub), so bear with, but below should be a reasonably comprehensive set of instructions.

wrote this post simultaneously along working out what i was doing, and doing it. most steps below had an implicit 'i think' when writing, esp anything relating to github or actions/pipelines/build jobs - still haven't worked out the correct terminology for all this stuff

```text
static/posts/on-linux.md
            /on-cats.md
      /templates/post-template.html
                /about-page.html
      /includes/base.css
               /font.woff
      /built/on-linux.html        ┐ 
            /on-cats.html         │ compiled .html files, ready to be
            /post-template.html   │ served. these are the only files
            /about-page.html      │ that the webserver need concern
            /base.css             │ itself with
            /font.woff            ┘ 
      /static.py ─────────────────┬ an executable python file the CICD 
                                  │ pipeline should run to generate the 
                                  └ /build directory above

```

## github setup
- create an account with name `alnnotes`
- create a repository with name `alnnotes.github.io`

## git setup
- from within `static/`:
- `git init`
- `git remote add origin https://github.com/alnnotes/alnnotes.github.io`
- `git pull`
- `git checkout -f main`
- `git branch --set-upstream-to=origin/main`

## keys
switch to ssh key authentication, as I forgot that would be required

- if you've already configured git and github with an ssh key, this can all be skipped
- make a key: `ssh-keygen -t ed25519 -C "<github signup email>"`
- save to `~/.ssh/id_FOO` and `id_FOO.pub` as prompted
- `eval "$(ssh-agent -s)"`
- `ssh-add ~/.ssh/id_FOO`
- on the github website: account settings > 'SSH and GPG keys': add it
- add the following to `~/.ssh/config`:
```text
Host github.com
  	User git
  	IdentityFile ~/.ssh/id_ed25519
```
- back in `static/`: `git remote set-url origin git@github.com:alnnotes/alnnotes.github.io.git`

## test it
- create `index.html` with some content, `commit` and `push` (note: only `index.html` for now)
- go to the actions tab on the repo and see the pipeline
- when it finishes (it took some time (mostly queueing to start) for me, but it's a free service, so it's hard to complain), go to alnnotes.github.io in a browser and see your `index.html` content

## .gitignore
 - make a `.gitignore`. i like <http://gitignore.io> - pop some relevant words into the bar and get a nice `.gitignore` to save in `static/` (i used `python`, `linux`, `emacs`)
 - **add `built/` to .gitignore`**

## setting up a building pipeline
- website: repo settings > pages > source: github actions
seems the classic behaviour of pushing whatever's on the configured branch to pages doesn't allow customising the pipeline, and we need to get it to run `static.py`, so we need to change to 'github actions'
- 'browse all workflows' > filter 'pages' > see a big list of workflows for building then deploying the output from various static site generators, but unfortunately not the one i've just hacked togehter
- borrow the 'static html: deploy static files in a repository without a build' workflow; 'configure'

above 'deploy:' add:

```yaml
# custom build job
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13' 
      - name: install pip prereqs
        run: |
          python -m pip install --upgrade pip
          pip install -r .github/workflows/requirements.txt
      - name: run static
        run: python .github/workflows/static.py
```
push that to `main` and it should trigger that yaml
- oh god this does take quite a while. at least it dies quickly if there are syntax errors
- i have a new-found respect for dave at my last job, whose domain cicd was
- stop telling me 'job started'; joining a queue doesn't constitute having 'started', in much the same way as i wouldn't tell someone i was 'having dinner' if i was in fact waiting for the restaurant to finish serving the current diners (plus those in front of me outside)

- hooray first successful run (<https://github.com/alnnotes/alnnotes.github.io/actions/runs/16105033443>)
- now `build` dired thrown away with job container
