import os
import requests
import sys
from argparse import ArgumentParser
from comment_parser import comment_parser
from glob import glob


def translate_comment(api_key, text, source_lang, target_lang):
    params = {
        'auth_key': api_key,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    request = requests.post(
        'https://api-free.deepl.com/v2/translate', data=params)
    result = request.json()
    return result['translations'][0]['text']


def translate(api_key, args, path):
    try:
        comments = comment_parser.extract_comments(path, mime=args.mime)
        if not comments:
            return
    except Exception as e:
        print(f'Translation failed ({e}): {path}', file=sys.stderr)
        return

    # Convert zero origin line number dict
    comments_dict = {comment.line_number() - 1: comment.text()
                     for comment in comments if not comment.is_multiline()}

    translated_lines = []

    with open(path) as f:
        for line_no, line in enumerate(f.readlines()):
            if line_no in comments_dict:
                try:
                    translated_text = translate_comment(
                        api_key, comments_dict[line_no], args.source_lang, args.target_lang)
                except Exception as e:
                    print(
                        f'Translation failed ({e}): {path}', file=sys.stderr)
                    return

                translated_line = line.replace(
                    comments_dict[line_no], translated_text)
                if args.verbose:
                    print(f'< {line.strip()}')
                    print(f'> {translated_line.strip()}')
                translated_lines.append(translated_line)
            else:
                translated_lines.append(line)

    with open(path, 'w') as f:
        f.writelines(translated_lines)

    if args.verbose:
        print(f'Translated {path}')


def main():
    api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        print('environment variable DEEPL_API_KEY is required', file=sys.stderr)
        sys.exit(-1)

    parser = ArgumentParser(prog='trans_comment.py')
    parser.add_argument('--ext', '-e', type=str,
                        help='target extention', required=True)
    parser.add_argument('--mime', '-m', type=str, help='target mime')
    parser.add_argument('--source_lang', '-s', type=str,
                        help='source lang', required=True)
    parser.add_argument('--target_lang', '-t', type=str,
                        help='target lang', required=True)
    parser.add_argument('--verbose', help='Verbose',
                        action='store_true', default=False)
    parser.add_argument('root_path')
    args = parser.parse_args()

    target_paths = glob(os.path.join(
        args.root_path, f'**/*.{args.ext}'), recursive=True)

    print("The script will translate the files:")
    print("\n".join(target_paths))
    print("Are you sure to proceed? (y/n): ", end='')
    answer = input()
    if answer != "y":
        exit()

    for path in target_paths:
        translate(api_key, args, path)


if __name__ == '__main__':
    main()
