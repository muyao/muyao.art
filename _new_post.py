#!/usr/bin/env python3

import argparse
import datetime
import os
import sys
import urllib.request


def main():
    arg = _parse_args()
    _prepare_images(arg)
    _write_post(arg)


def _prepare_images(arg):
    year = arg.date[:4]
    os.makedirs(f'media/{year}', exist_ok=True)

    urls = arg.image or []
    images = _image_pathnames(arg)

    for i in range(len(urls)):
        print(f'Downloading {urls[i]} -> media/{images[i]}')
        urllib.request.urlretrieve(urls[i], f'media/{images[i]}')


def _write_post(arg):
    post = _post(arg)
    title = _post_slug(arg)
    post_file = f'_posts/{arg.date}-{title}.md'
    print(f'Writing {post_file} with content:\n')
    print(post)

    with open(post_file, 'w') as f:
        f.write(post)


def _post_slug(arg):
    return arg.title.replace(' ', '-').lower()


def _image_pathnames(arg):
    year = arg.date[:4]
    image_prefix = _post_slug(arg)
    if not arg.image:
        return []
    if len(arg.image) == 1:
        return [f'{year}/{image_prefix}.jpg']

    # Note: only support up to 99 images
    return [f'{year}/{image_prefix}-{i+1:02d}.jpg'
            for i in range(len(arg.image))]


def _post(arg):
    layout = 'post'
    post = []

    post.append('---')
    post.append(f'layout: {layout}')
    post.append(f'title: {arg.title.title()}')

    images = _image_pathnames(arg)
    featimg = images[0] if images else 'null'
    post.append(f'featimg: {featimg}')

    tags = sorted(arg.tag or [])
    post.append(f'tags: {tags}')

    post.append('---')
    post.append('')

    if featimg == 'null':
        post.append('TODO: describe the story.')
    else:
        post.append(f'TODO: describe cover image {featimg}.')

    for img in images[1:]:
        post.append('')
        post.append(f'<img src="/media/{img}">')
        post.append('')
        post.append(f'TODO: descrbe image {img}.')

    return '\n'.join(post) + '\n'


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('title')
    parser.add_argument('-d', '--date',
                        default=datetime.date.today().strftime('%F'),
                        help='Date in YYYY-mm-dd format, default is today')
    parser.add_argument('-i', '--image',
                        action='append',
                        help='Image URL(s) to download')
    parser.add_argument('-t', '--tag',
                        action='append',
                        help='Tag(s) to apply to the post')
    return parser.parse_args()


if __name__ == '__main__':
    main()
