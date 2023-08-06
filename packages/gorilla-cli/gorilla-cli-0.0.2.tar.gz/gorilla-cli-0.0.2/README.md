# Gorilla CLI

Gorilla CLI is a user-friendly command-line interface (CLI) tool that helps you to interact with your system using natural language. Just tell Gorilla CLI what you want to do, and it will suggest possible commands for you. No need to memorize complex command line arguments!

## Get Started

Gorilla CLI can be installed via pip. 

```
pip install gorilla-cli
```

## Usage

Using Gorilla CLI is as simple as typing `go` followed by your command in plain English.

For example, if you want to list all files in the current directory, simply type:

```
go I want to list all files in the current directory
```

Gorilla CLI will then suggest possible commands, which you can select using the arrow keys and then press enter to execute the command. 

```
🦍  Welcome to Gorilla. Use arrows to select
 » ls
   ls -l
   ls -al
```

## How It Works

Gorilla CLI is tool that combines the power of [Gorilla LLM](https://github.com/ShishirPatil/gorilla/), and other LLMs including OpenAI's GPT-4, Claude v1, to provide a user-friendly interface to the command line. It then presents these commands to you, and you can select the one that suits your needs.

## Contributions

Contributions to Gorilla CLI are welcome. Please submit a pull request on GitHub if you have made improvements to the tool. 

## License

Gorilla CLI is licensed under the Apache 2.0 license. See the LICENSE file for more details. Thanks to [questionary](https://github.com/tmbo/questionary) for the great UI! 
