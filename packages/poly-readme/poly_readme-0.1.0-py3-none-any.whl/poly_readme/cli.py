#!/usr/bin/env python3

import os
import sys
import openai
import argparse
import questionary
import json
import yaml
from pathlib import Path
import keyring
import time
import threading
import itertools

LANGUAGES = {
    "ko": "Korean",
    "ja": "Japanese",
    "zh": "Chinese Simplified", 
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "vi": "Vietnamese"
}

class Spinner:
    def __init__(self, message=""):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.running = False
        self.message = message
        self.thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{self.message} {next(self.spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r\033[K')  # Clear line

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

def get_config_dir():
    return Path.home() / '.config' / 'poly-readme'

def get_config_file():
    return get_config_dir() / 'config.json'

def load_config():
    config_file = get_config_file()
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    
    with open(get_config_file(), 'w') as f:
        json.dump(config, f)

def setup_api_key():
    # Check if API key already exists
    existing_key = keyring.get_password("poly-readme", "openai_api_key")
    if existing_key:
        should_update = questionary.confirm(
            "API key already exists. Do you want to update it?",
            default=False
        ).ask()
        
        if not should_update:
            print("Keeping existing API key.")
            return existing_key

    # Get new API key
    api_key = questionary.password("Please enter your OpenAI API key:").ask()
    keyring.set_password("poly-readme", "openai_api_key", api_key)
    return api_key

def get_api_key():
    # First try environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
        
    # Then try system keyring
    api_key = keyring.get_password("poly-readme", "openai_api_key")
    if not api_key:
        print("OpenAI API key not found. Please run 'poly-readme install' first.")
        sys.exit(1)
    return api_key

def setup_project():
    try:
        # Load existing settings
        existing_config = {}
        try:
            with open('.polyreadme.yaml', 'r') as f:
                existing_config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass
        
        # Initialize config dictionary
        config = {
            'source_file': existing_config.get('source_file', 'README.md'),
            'target_languages': [],
            'output_pattern': existing_config.get('output_pattern', 'README_{lang}.md')
        }
        
        # Set default for previously selected languages
        existing_languages = existing_config.get('target_languages', [])
        
        # Create choice objects with checked parameter for existing languages
        LANGUAGE_CHOICES = [
            questionary.Choice(
                f"{name} ({code})", 
                code,
                checked=(code in existing_languages)  # Add checked parameter here
            )
            for code, name in LANGUAGES.items()
        ]
        LANGUAGE_CHOICES.append(questionary.Choice("Custom language", "custom"))

        selected_languages = questionary.checkbox(
            "Select target languages for translation:",
            choices=LANGUAGE_CHOICES
        ).ask()

        if selected_languages is None:
            print("\nSetup cancelled.")
            return

        # Handle custom language input if selected
        if "custom" in selected_languages:
            selected_languages.remove("custom")
            while True:
                custom_code = questionary.text(
                    "Enter custom language code (e.g., vi for Vietnamese):"
                ).ask().lower()
                
                if not custom_code:
                    print("Language code cannot be empty")
                    continue

                if not (2 <= len(custom_code) <= 3 and custom_code.isalpha()):
                    print("Language code must be 2-3 letters")
                    continue

                selected_languages.append(custom_code)
                break

        config['target_languages'] = selected_languages

        # Select output pattern (set default if existing value)
        existing_pattern = existing_config.get('output_pattern', "README_{lang}.md")
        pattern_choices = [
            questionary.Choice("README_{lang}.md (lowercase)", "README_{lang}.md"),
            questionary.Choice("README_{LANG}.md (uppercase)", "README_{LANG}.md"),
            questionary.Choice("Custom pattern", "custom")
        ]
        
        # Handle custom if existing pattern is not default
        default_pattern = next(
            (choice.value for choice in pattern_choices if choice.value == existing_pattern),
            "custom"
        )
        
        pattern_choice = questionary.select(
            "Choose output filename pattern type:",
            choices=pattern_choices,
            default=default_pattern
        ).ask()
        
        if pattern_choice == "custom":
            while True:
                pattern = questionary.text(
                    "Enter custom pattern (must include {lang} or {LANG}):",
                    default=existing_pattern if default_pattern == "custom" else None
                ).ask()
                
                if "{lang}" not in pattern and "{LANG}" not in pattern:
                    print("Error: Pattern must include either {lang} or {LANG}")
                    continue
                    
                if pattern.count("{lang}") + pattern.count("{LANG}") > 1:
                    print("Error: Pattern should include language placeholder only once")
                    continue
                    
                if not pattern.endswith(".md"):
                    print("Error: Pattern must end with .md extension")
                    continue
                    
                config['output_pattern'] = pattern
                break
        else:
            config['output_pattern'] = pattern_choice
        
        with open('.polyreadme.yaml', 'w') as f:
            yaml.dump(config, f)
        print("Project configuration saved to .polyreadme.yaml")

    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        return

def load_project_config():
    try:
        with open('.polyreadme.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: Project configuration not found. Please run 'poly-readme setup' first.")
        sys.exit(1)

def translate_readme(): 
    config = load_project_config()
    
    try:
        with open(config['source_file'], 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Could not find source file: {config['source_file']}")
        sys.exit(1)

    openai.api_key = get_api_key()
        
    for lang in config['target_languages']:
        spinner = Spinner(f"Translating {config['source_file']} to {LANGUAGES[lang]}")
        spinner.start()
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a professional translator specializing in translating technical documentation from English to {LANGUAGES[lang]}. Please maintain the original Markdown formatting and ensure technical terms are accurately translated."},
                    {"role": "user", "content": content}
                ],
            )
            translated_content = response.choices[0].message.content
            
            output_pattern = config['output_pattern']
            if '{LANG}' in output_pattern:
                output_filename = output_pattern.replace('{LANG}', lang.upper())
            else:
                output_filename = output_pattern.replace('{lang}', lang.lower())
                
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            spinner.stop()
            print(f"\r✓ Translation completed. {output_filename} has been created.")
            
        except Exception as e:
            spinner.stop()
            print(f"\r✗ An error occurred during translation to {LANGUAGES[lang]}: {str(e)}")

def main():
    # Create parser for top-level commands
    parser = argparse.ArgumentParser(
        description='Poly-README - Translate README files into multiple languages.',
        usage='poly-readme <command> [<args>]',
        add_help=False  # Disable default help
    )
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit.')

    # Create parser for managing subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # install subcommand
    parser_install = subparsers.add_parser(
        'install',
        help='Configure OpenAI API key'
    )

    # setup subcommand
    parser_setup = subparsers.add_parser(
        'setup',
        help='Configure project settings'
    )

    # translate subcommand
    parser_translate = subparsers.add_parser(
        'translate',
        help='Translate README files'
    )

    # help subcommand
    parser_help = subparsers.add_parser(
        'help',
        help='Show help for a specific command'
    )
    parser_help.add_argument(
        'topic',
        nargs='?',
        choices=['install', 'setup', 'translate'],
        help='Command to get help for'
    )

    # Parse commands
    args = parser.parse_args()

    # If -h or --help is provided
    if args.help or args.command is None:
        print("poly-readme 0.1.0")
        print("Usage: poly-readme <command> [<args>]")
        print("\nSome useful poly-readme commands are:")
        print("   install     Configure OpenAI API key")
        print("   setup       Configure project settings")
        print("   translate   Translate README files")
        print("\nSee 'poly-readme help <command>' for information on a specific command.")
        sys.exit(0)

    # Command processing
    if args.command == 'help':
        if not hasattr(args, 'topic') or args.topic is None:
            print("Usage: poly-readme <command> [<args>]")
            print("\nSome useful poly-readme commands are:")
            print("   install     Configure OpenAI API key")
            print("   setup       Configure project settings")
            print("   translate   Translate README files")
            print("\nSee 'poly-readme help <command>' for information on a specific command.")
        elif args.topic == 'install':
            print("Usage: poly-readme install")
            print("\nConfigure and save your OpenAI API key for translation.")
        elif args.topic == 'setup':
            print("Usage: poly-readme setup")
            print("\nConfigure project settings including:")
            print("- Source README file location")
            print("- Target languages for translation")
            print("- Output filename pattern")
        elif args.topic == 'translate':
            print("Usage: poly-readme translate")
            print("\nTranslate your README file into configured target languages.")
        else:
            print(f"Unknown help topic '{args.topic}'")
        sys.exit(0)

    elif args.command == 'install':
        setup_api_key()
        print("OpenAI API key has been saved successfully.")

    elif args.command == 'setup':
        setup_project()

    elif args.command == 'translate':
        translate_readme()

if __name__ == '__main__':
    main()