# Poly-README

Poly-README is a command-line tool that automatically translates your README.md files into multiple languages using OpenAI's GPT-4 model.

## Features

- Automatic translation of README.md files
- Support for multiple target languages
- Simple command-line interface
- Maintains markdown formatting
- Uses OpenAI's GPT-4 for high-quality translations
- Secure API key management using system keyring
- Project-level configuration using YAML
- Progress indicator during translation
- Support for custom output filename patterns

## Installation

```bash
pip install poly-readme
```

## Prerequisites

Before using Poly-README, you need to:

1. Have an OpenAI API key
2. Either:
   - Set your OpenAI API key as an environment variable:
     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```
   - Or install it securely using the CLI:
     ```bash
     poly-readme install
     ```

## Usage

### Initial Setup

Configure your project settings:

```bash
poly-readme setup
```

This will guide you through:

- Setting the source README file location
- Selecting target languages for translation
- Configuring output filename pattern

### Translation

Translate your README according to your project configuration:

```bash
poly-readme translate
```

### Available Language Codes

- `ko`: Korean
- `ja`: Japanese
- `zh`: Chinese Simplified
- `es`: Spanish
- `fr`: French
- `de`: German
- `it`: Italian
- `pt`: Portuguese
- `ru`: Russian
- `ar`: Arabic
- `vi`: Vietnamese

The translated files will be saved according to your configured pattern (default: `README_{lang}.md`).

## Commands

- `poly-readme install` - Configure OpenAI API key
- `poly-readme setup` - Configure project settings
- `poly-readme translate` - Translate README files
- `poly-readme help [command]` - Show help information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Chad Lee
- Email: think.bicycle@gmail.com
- GitHub: [drllr/poly-readme](https://github.com/drllr/poly-readme)

## Acknowledgments

- This tool uses OpenAI's GPT-4 model for translations
