# pr
*pr* programmatically publishes content on multiple social platforms.

If you need to publish the same content on tumblr, facebook, flickr, dribbble, instagram...
and you don't like repetitive jobs then you should probably use *pr*.

*pr* also scales and convert image format for you, using the magic
[ImageMagick](https://www.imagemagick.org/script/index.php).

Current supported platforms:

- tumblr

## Short intro

*pr* basically does the following. It takes the following parameters on the command-line:
- an image (multiple images should be supported)
- some content description (a title, a text, some tags...)
- a list of social accounts (eg. one tumblr blog, one facebook account and one behance account)

and then:
- creates media content to publish on the social platforms
- publishes the media using the API of each social platform.

Some platforms that we would like support:

- behance
- dribble
- facebook
- flickr
- instagram (can be problematic since no API for publising is officially available)
- tumblr


## Details
### Configuration file

The process is steered via a configuration file. The configuration file contains a section
for each _social account_. We distinguish between social platform (eg. _tumblr_) and a
_social account_. A _social account_ is an account on a social platform, since you may have
different accounts on the same platform, like multiple tumblr blogs or anyway want to be
able to publish on different accounts.

A sample section for a tumblr social account is the following:

```
[myblog.tumblr.com]
platform=tumblr
blogname=myblog.tumblr.com
consumer_key=<secret>
consumer_secret=<secret>
token=<secret>
token_secret=<secret>
out_type=jpg
resize_to=800
has_tags=True
```

The most important key is the `platform` that indicates what code to call for publishing
the content.

Of course, according to the specified platform different other configuration keys can be used.

By default the configuration file is `~/pr.ini` but a different one can be passed on the command line.

### help message

```
talamoigs-MacBook-Air:pr talamoig$ ./pub.py --help
usage: pub.py [-h] --what WHAT --where WHERE --title TITLE --tags TAGS
              --description DESCRIPTION [--config CONFIG]

Publish stuff in places

optional arguments:
  -h, --help            show this help message and exit
  --what WHAT           image to publish
  --where WHERE         destination accounts
  --title TITLE         title to publish
  --tags TAGS
  --description DESCRIPTION
  --config CONFIG
```

### sample execution

Here is a sample execution to put a image on my tumblr blog, using a tif as source and scaling it to 800px width.
My config file (`~/pr.ini`) contains the following:

```
[talamoig.tumblr.com]
platform=tumblr
blogname=talamoig.tumblr.com
consumer_key=<secret>
consumer_secret=<secret>
token=<secret>
token_secret=<secret>
out_type=jpg
state=draft
resize_to=800
has_tags=True
```

And this is the execution:

```
./pub.py --what 2017-06-zurigo.tif --where talamoig.tumblr.com --title 'summertime in zurich' --description ' ' --tags 'zurich,summer,sketchbook'
talamoig.tumblr.com: ok
```
