# Dewar

Dewar is a static site generator inspired by flask.

## About
### Why the name "dewar"?

Dewar (pronounced d-you-ah) is another name for a vacuum flask, or a thermos. Basically, it's a flask that keeps things frozen (or hot).

### Why would I use this?

To the moment, there have been a few ways of making a static site:

 - Roll your own custom solution, maybe using jinja, but maybe just formatting a html template solution.

This might work for a small site, or for a repetitive report; but maintainability is lost, and a lot of custom configuration has to be done.

 - Use a static site generator (a la jekyll or hyde).

These are great for making blogs, but are opinionated about what content they should host. They don't allow for computation inline, and they are their own ecosystem to learn.

### Just use flask!

 There are two major limitations to flask that this project solves:

 1) Flask only serves one page at a time.
 2) Flask requires a server to be running.

These limitaions are obvious, but they prevent a few use cases:
  - hosting a site that doesn't need to be continuously rendered
  - creating sites that can be easily downloaded
  - creating a server that can be seen without a server running
  - creating sites that rely entirely on client-side code, but want some convenient templating [in this case, it adds overhead of processing that's unnecessary]

## Setup

Installing Dewar is as simple as:

```
pip install dewar
```

And writing a program like
```python3
# named 'site.py'
import dewar

site = dewar.Site()

@site.register('index.html')
def index():
    return "<h1>Hello, World</h1>"

if __name__ == "__main__":
    dewar.render()
```

Then,

```
$ python3 site.py
```

That's it! Your static site is now in `dist/`.
