# pr
code to publish content (images with maybe text) on different social platforms

It should be a program that takes:
- a project directory
- a project description (through json file)

and accordingly to the project description it:
- creates media content to publish on different social platforms 
- publishes the media using the API of each social platform.

At least the following platforms should be included:

- tumblr
- instagram
- facebook
- behance

It may be necessary to have also a general configuration file that includes social-platform specific things.
Eg. API details or media specific things, like resize informations (tumblr), tags (instagram), project name (behance).
