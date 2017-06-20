#!/usr/bin/env python

from __future__ import print_function
from PIL import Image
import os
import re
import sys
import pytumblr
import oauth2 as oauth
import argparse
import ConfigParser
from subprocess import call

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def tumblr_pub(config, filename, title, description, tags):
    blogname=config.get('tumblr','blogname')
    print ("[tumblr] Publishing %s on %s"%(filename, blogname))

    client = pytumblr.TumblrRestClient(
        config.get('tumblr','consumer_key'),
        config.get('tumblr','consumer_secret'),
        config.get('tumblr','token'),
        config.get('tumblr','token_secret')
    )
    result=client.create_photo(blogname, caption=title, state='draft', tags=tags, tweet=description, data=filename)
    print(result)
    
CONFIGFILE='pr.ini'
    
config = ConfigParser.RawConfigParser()
if not os.path.isfile(CONFIGFILE):
    eprint('Cannot find config file %s'%CONFIGFILE)
    sys.exit(1)
config.read(CONFIGFILE)

parser = argparse.ArgumentParser(description='Publish stuff in places')

parser.add_argument('--what',
                    help='image to publish',
                    required=True,
)
parser.add_argument('--where',
                    help='destination platform',
                    required=True
)
parser.add_argument('--title',
                    help='title to publish',
                    default='',
                    required=True
)
parser.add_argument('--tags',
                    required=True
)
parser.add_argument('--description',
                    default='',
                    required=True
)

args = parser.parse_args()

image=args.what
platforms=args.where
title=args.title
tags=args.tags.split(',')
description=args.description

if not os.path.isfile(image):
    eprint("File %s not found"%image)
    sys.exit(1)

im=Image.open(image)
width,height=(im.size)

all_platforms=config.sections()
all_platforms.remove('general')

if platforms=='all':
    platforms=all_platforms
else:
    platforms=platforms.split(',')
    for p in platforms:
        if p not in all_platforms:
            eprint("No section for platform %s found in the config file %s"%(p,CONFIGFILE))
            sys.exit(1)

base_filename=os.path.splitext(image)[0]
convert_cmd=config.get('general','convert')

for p in platforms:
    try:
        resize_to=config.get(p,'resize_to')
        resize_cmd='-resize %s'%resize_to
    except e:
        resize_cmd=''
    try:
        out_type=config.get(p,'out_type')
    except e:
        eprint('out_type not defined for %s'%p)
        sys.exit(1)

    destination_filename='%s_%s.%s'%(base_filename,p,out_type)
    command="%s %s %s %s"%(convert_cmd,image,resize_cmd,destination_filename)
    command_list=command.split(' ')
    call(command_list)
    method_name='%s_pub'%p
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % method_name)
    method(config, destination_filename, title, description, tags)    
