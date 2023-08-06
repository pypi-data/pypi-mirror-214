# LLM-Toolbox

LLM-Toolbox is a collection of command line tools that harness the power of large language models to perform various tasks. This repository houses scripts that utilize OpenAI's ChatGPT for tasks such as dictionary and thesaurus queries, text translation, proofreading, enriching language learning, automating shell commands, and more.

<!-- TOC -->
## Table of Contents

1. [Installation](#installation)
1. [Usage](#usage)
    1. [ShellGenius](#shellgenius)
    1. [Thesaurus](#thesaurus)
    1. [Define](#define)
    1. [Proofread](#proofread)
    1. [Translate](#translate)
1. [License](#license)
<!-- /TOC -->

## Installation

To use these scripts, you need to clone this repository and ensure you have installed all necessary dependencies.

For some of the scripts, you'll need to install `llm`. You can find [its repository here](https://github.com/simonw/llm). Follow the instructions in its README for the official installation details and documentation.

### Install `llm` with `pipx`

I recommend using [pipx](https://pypa.github.io/pipx/installation/) for the installation of `llm`.

You can either install the latest stable version:

```bash
pipx install llm
```

Or install from the GitHub repository to follow its main branch:

```bash
pipx install git+https://github.com/simonw/llm.git
```

### Cloning the LLM-Toolbox Repository

You can clone this repository with the following command:

```bash
git clone https://github.com/sderev/llm-toolbox.git
```

## Usage

Instructions on how to use each of the scripts are included in the individual directories under [tools/](https://github.com/sderev/llm-toolbox/tree/main/tools). Here's a brief overview:

### ShellGenius

[ShellGenius](https://github.com/sderev/shellgenius) is an intuitive CLI tool designed to enhance your command-line experience by turning your task descriptions into efficient shell commands. Check out the project on [its dedicated repository](https://github.com/sderev/shellgenius).

### Vocabmaster

Master new languages with [VocabMaster](https://github.com/sderev/vocabmaster), a CLI tool designed to help you record vocabulary, access translations and examples, and seamlessly import them into Anki for an optimized language learning experience. Check out the project on [its dedicated repository](https://github.com/sderev/vocabmaster).

### Thesaurus

The [`thesaurus`](https://github.com/sderev/llm-toolbox/tree/main/tools/thesaurus) script takes a word or a phrase as input and provides a list of synonyms and antonyms.

### Define

The [`define`](https://github.com/sderev/llm-toolbox/tree/main/tools/define) script takes a word as input and provides its definition along with an example sentence using the word.

### Proofread

The [`proofread`](https://github.com/sderev/llm-toolbox/tree/main/tools/proofread) script takes a sentence as input and provides a corrected version of it, if needed, along with an explanation of the corrections.

### Translate

The [`translate`](https://github.com/sderev/llm-toolbox/tree/main/tools/translate) script takes a sentence and a target language as input and provides the translated sentence in the target language.

## License

This project is licensed under the terms of the Apache License 2.0.

