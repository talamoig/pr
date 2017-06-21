#!/usr/bin/env python

from __future__ import print_function
from PIL import Image
import os
import re
import sys
import pytumblr
import argparse
import ConfigParser
from subprocess import call

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def tumblr_pub(config, account, filename, title, description, tags):
    allowed_state = ['published', 'draft', 'queue', 'private']
    blogname = config.get(account,'blogname')
    state = config.get(account,'state')
    if state not in allowed_state:
        return "state %s not in %s"%(state, ", ".join(allowed_state))
    client = pytumblr.TumblrRestClient(
        config.get(account, 'consumer_key'),
        config.get(account, 'consumer_secret'),
        config.get(account, 'token'),
        config.get(account, 'token_secret')
    )
    result=client.create_photo(blogname, caption=title, state=state, tags=tags, tweet=description, data=filename)
    if result.has_key('id'):
        return "ok"
    return result

def conf_configfile(configfile):
    config = ConfigParser.RawConfigParser()
    if configfile.startswith('~'):
        configfile=os.path.expanduser('~')+configfile[1:]
    if not os.path.isfile(configfile):
        eprint('Cannot find config file %s'%configfile)
        sys.exit(1)
    config.read(configfile)
    return config


def parseargs():

    parser = argparse.ArgumentParser(description='Publish stuff in places')

    parser.add_argument('--what',
                        help='image to publish',
                        required=True,
    )
    parser.add_argument('--where',
                        help='destination accounts',
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

    parser.add_argument('--config',
                        default='~/pr.ini',
                        required=False
    )

    args = parser.parse_args()
    config_file = args.config
    image = args.what
    accounts = args.where
    title = args.title
    tags = args.tags.split(',')
    description = args.description
    config=conf_configfile(config_file)

    return (config,
            image,
            accounts,
            title,
            description,
            tags)

def main():
    (config, image, accounts, title, description, tags) = parseargs()

    if not os.path.isfile(image):
        eprint("File %s not found"%image)
        sys.exit(1)

    im=Image.open(image)
    width,height=(im.size)

    all_accounts=config.sections()
    all_accounts.remove('general')

    if accounts=='all':
        account=all_accounts
    else:
        accounts=accounts.split(',')

    for a in accounts:
        if a not in all_accounts:
            eprint("No section for account %s found in the config file"%a)
            sys.exit(1)

    base_filename=os.path.splitext(image)[0]
    convert_cmd=config.get('general','convert')

    for a in accounts:
        try:
            resize_to=config.get(a,'resize_to')
            resize_cmd='-resize %s'%resize_to
        except e:
            resize_cmd=''
        try:
            out_type=config.get(a,'out_type')
        except e:
            eprint('out_type not defined for %s'%a)
            sys.exit(1)

        destination_filename='%s_%s.%s'%(base_filename,a,out_type)
        command="%s %s %s %s"%(convert_cmd,image,resize_cmd,destination_filename)
        command_list=command.split(' ')
        call(command_list)
        platform=config.get(a,'platform')
        method_name='%s_pub'%platform
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(method_name)
        if not method:
            raise NotImplementedError("Method %s not implemented" % method_name)

        result=method(config, a, destination_filename, title, description, tags)
        print("%s: %s"%(a,result))

if __name__ == "__main__":
    main()
