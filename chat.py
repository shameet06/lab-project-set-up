"""Run a command-line assistant that answers questions about local files."""
import os
from dotenv import load_dotenv
from groq import Groq
import shlex
from tools.calculate import calculate
from tools.cat import cat
from tools.grep import grep
from tools.ls import ls
import json
import argparse

FUNCTIONS = {
    "calculate": calculate,
    "cat": cat,
    "grep": grep,
    "ls": ls,
}

def describe_tool(name, description, parameters, required):

    """Example tool desc.

    >>> tool = describe_tool("cat", "Read a file.", {"path": "File to read."}, ["path"])
    >>> tool["function"]["parameters"]["required"]
    ['path']
    """
    properties = {}
    for parameter, explanation in parameters.items():
        properties[parameter] = {
            "type": "string",
            "description": explanation,
        }

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


TOOLS = [
    describe_tool(
        "calculate",
        "Evaluate an arithmetic expression.",
        {"expression": "An expression such as 2 + 3."},
        ["expression"],
    ),
    describe_tool(
        "ls",
        "List the entries in a folder.",
        {"path": "The relative folder to list. Defaults to the current folder."},
        [],
    ),
    describe_tool(
        "cat",
        "Read the contents of a text file.",
        {"path": "The relative path to the file."},
        ["path"],
    ),
    describe_tool(
        "grep",
        "Find lines in text files that match a regular expression.",
        {"regex": "The pattern to search for.", "path": "A relative path or glob."},
        ["regex", "path"],
    ),
]

load_dotenv()

def llm(messages, temperature=1, debug=False):
    """Send the conversation to the model and run any tools it requests.

    >>> from unittest.mock import Mock, patch
    >>> reply = Mock(content="Hello!", tool_calls=None)
    >>> with patch("chat.Groq") as fake_groq:
    ...     create = fake_groq.return_value.chat.completions.create
    ...     create.return_value = Mock(choices=[Mock(message=reply)])
    ...     llm([{"role": "user", "content": "Say hello."}])
    'Hello!'
    """
    client = Groq()

    while True:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOLS,
            temperature=temperature,
            timeout=30,
        )

        message = completion.choices[0].message
        if not getattr(message, "tool_calls", None):
            return message.content

        request = message.model_dump(exclude_none=True)
        messages.append(request)

        for call in request["tool_calls"]:
            function = call["function"]
            try:
                arguments = json.loads(function["arguments"])
                name = function["name"]
                tool = FUNCTIONS[name]
                if debug:
                    print(f"[debug] {name} {arguments}")
                result = tool(**arguments)
            except (KeyError, TypeError, ValueError) as error:
                result = f"Tool error: {error}"

            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": str(result),
            })


class Chat:
    """Store the messages in one conversation.

    Each instance keeps its own history for follow-up questions.

    >>> Chat("Be brief.").messages
    [{'role': 'system', 'content': 'Be brief.'}]
    """

    def __init__(self, system="You are a helpful assistant."):
        """Start a new conversation with the given system message."""
        self.messages = [
            {"role": "system", "content": system}
        ]

    def send_message(self, message, temperature=0.8, debug=False):
        """Send a message and remember the conversation.

        >>> from unittest.mock import MagicMock, patch
        >>> first = MagicMock()
        >>> first.choices[0].message.content = "Bayern Munich fan!"
        >>> second = MagicMock()
        >>> second.choices[0].message.content = "You support Bayern Munich."
        >>> first.choices[0].message.tool_calls = None
        >>> second.choices[0].message.tool_calls = None
        >>> chat = Chat(system="Keep answers short.")
        >>> with patch("chat.Groq") as fake_groq:
        ...     fake_groq.return_value.chat.completions.create.side_effect = [first, second]
        ...     print(chat.send_message("I support Bayern Munich.", temperature=0))
        ...     print(chat.send_message("Which team do I support?", temperature=0))
        Bayern Munich fan!
        You support Bayern Munich.


        >>> chat.messages == [
        ...     {"role": "system", "content": "Keep answers short."},
        ...     {"role": "user", "content": "I support Bayern Munich."},
        ...     {"role": "assistant", "content": "Bayern Munich fan!"},
        ...     {"role": "user", "content": "Which team do I support?"},
        ...     {"role": "assistant", "content": "You support Bayern Munich."},
        ... ]
        True
        """
        self.messages.append({
            "role": "user",
            "content": message,
        })
        reply = llm(self.messages, temperature=temperature, debug=debug)
        self.messages.append({
            "role": "assistant",
            "content": reply,
        })
        return reply


def repl(temperature=0.8, debug=False):
    """Run a conversation and exit cleanly.


    >>> from unittest.mock import MagicMock, patch
    >>> first = MagicMock()
    >>> first.choices[0].message.content = "Have fun playing Halo!"
    >>> second = MagicMock()
    >>> second.choices[0].message.content = "You are playing Halo."
    >>> first.choices[0].message.tool_calls = None
    >>> second.choices[0].message.tool_calls = None
    >>> replies = [first, second]
    >>> requests = []
    >>> def fake_create(messages, model, temperature, **kwargs):
    ...     saved = []
    ...     for message in messages:
    ...         saved.append(message.copy())
    ...     requests.append(saved)
    ...     return replies[len(requests) - 1]
    >>> with patch("builtins.input",
    ...            side_effect=["I am playing Halo.", "What game?", EOFError]):
    ...     with patch("chat.Groq") as fake_groq:
    ...         fake_groq.return_value.chat.completions.create.side_effect = fake_create
    ...         repl(temperature=0)
    Have fun playing Halo!
    You are playing Halo.
    <BLANKLINE>

    >>> len(requests)
    2

    >>> requests[0][1:] == [
    ...     {"role": "user", "content": "I am playing Halo."}
    ... ]
    True

    >>> requests[1][1:] == [
    ...     {"role": "user", "content": "I am playing Halo."},
    ...     {"role": "assistant", "content": "Have fun playing Halo!"},
    ...     {"role": "user", "content": "What game?"},
    ... ]
    True


    >>> with patch("builtins.input", side_effect=KeyboardInterrupt):
    ...     repl(temperature=0)
    <BLANKLINE>
    """
    chat = Chat(
        system=(
            "You are a helpful assistant. "
            "You provide answers in a concise manner but with detail where applicable"
        )
    )
    try:
        while True:
            user_input = input("chat> ")
            if user_input.startswith("/"):
                result = run_command(user_input, debug=debug)
                chat.messages.append({"role": "user", "content": user_input})
                chat.messages.append({"role": "assistant", "content": result})
                print(result)
            else:
                print(chat.send_message(user_input, temperature=temperature, debug=debug))
    except (KeyboardInterrupt, EOFError):
        print()


def run_command(command, debug=False):
    """Example slash command

    >>> run_command("/calculate 2 + 3 * 4")
    '14'
    >>> run_command("/cat")
    'Wrong number of arguments for /cat'
    >>> run_command("/hello")
    'Unknown command: /hello'
    """
    try:
        parts = shlex.split(command)
    except ValueError:
        return "Invalid command syntax"

    name = parts[0][1:]
    arguments = parts[1:]

    if name not in FUNCTIONS:
        return f"Unknown command: /{name}"

    if name == "calculate" and arguments:
        arguments = [" ".join(arguments)]

    try:
        if debug:
            print(f"[debug] {name} {arguments}")
        return FUNCTIONS[name](*arguments)
    except TypeError:
        return f"Wrong number of arguments for /{name}"
    

def main(argv=None):
    """Run one message or start an interactive chat

    >>> from unittest.mock import patch
    >>> with patch("chat.repl") as mock_repl:
    ...     main(["--debug"])
    ...     mock_repl.assert_called_once_with(debug=True)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("message", nargs="?")
    args = parser.parse_args(argv)

    if args.message is None:
        repl(debug=args.debug)
    else:
        chat = Chat()
        print(chat.send_message(args.message, debug=args.debug))


if __name__ == "__main__":
    main()
