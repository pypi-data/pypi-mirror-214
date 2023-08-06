import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cligpt.cligpt import CLIGPT
import os
import shutil
import readline
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description='Example script to demonstrate argparse usage.')

    parser.add_argument('-l', '--context_length', type=int, default=6, help='The numebr of Prompts/Responses that should be remembered.')
    parser.add_argument('-na', '--no_auto_copy', action='store_false', help='Whether to disable automatically copying the output to clipboard.')
    parser.add_argument('-ns', '--no_stream', action='store_false', help='Whether to disable stream mode.')
    parser.add_argument('-p', '--proxy', type=str, default='', help='The proxy to use for OpenAI API.')
    parser.add_argument('-q', '--quick_prompt', type=str, default='', help='Get response directly without entering interactive mode.')

    args = parser.parse_args()

    # obatin OPENAI_API_KEY variable from Environment
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not provided, please `export OPENAI_API_KEY=[Your API KEY]`")

    if args.quick_prompt != '':
        import openai
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{args.quick_prompt}"}], stream=False)
        response_text = response.choices[0].message.content.lstrip().strip()
        print(response_text)
        return
    else:
        # interactive mode
        # create config file ~/.cligpt/config.json  if not exists
        config_dir = os.path.expanduser('~/.cligpt')
        config_file = os.path.join(config_dir, 'config.json')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(config_file):
            shutil.copyfile(os.path.join(os.path.dirname(__file__), 'config.json'), config_file)

        cligpt = CLIGPT(
            openai_api_key=OPENAI_API_KEY,
            config_file=config_file,
            context_length=args.context_length,
            auto_copy=args.no_auto_copy,
            proxy=args.proxy
            )
        cligpt.start()


if __name__ == "__main__":
    main()