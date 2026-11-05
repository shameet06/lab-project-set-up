import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def llm(messages, temperature=1):
    completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-20b",
        temperature=temperature,
    )
    return completion.choices[0].message.content


class Chat:
    def __init__(self, system="You are a helpful assistant."):
        self.messages = [
            {"role": "system", "content": system}
        ]

    def send_message(self, message, temperature=0.8):
        """Send a message and remember the conversation.

        >>> from unittest.mock import MagicMock, patch
        >>> first = MagicMock()
        >>> first.choices[0].message.content = "Bayern Munich fan!"
        >>> second = MagicMock()
        >>> second.choices[0].message.content = "You support Bayern Munich."
        >>> chat = Chat(system="Keep answers short.")
        >>> with patch.object(client.chat.completions, "create",
        ...                   side_effect=[first, second]):
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
        reply = llm(self.messages, temperature=temperature)
        self.messages.append({
            "role": "assistant",
            "content": reply,
        })
        return reply


def repl(temperature=0.8):
    """Run a conversation and exit cleanly.


    >>> from unittest.mock import MagicMock, patch
    >>> first = MagicMock()
    >>> first.choices[0].message.content = "Have fun playing Halo!"
    >>> second = MagicMock()
    >>> second.choices[0].message.content = "You are playing Halo."
    >>> replies = [first, second]
    >>> requests = []
    >>> def fake_create(messages, model, temperature):
    ...     saved = []
    ...     for message in messages:
    ...         saved.append(message.copy())
    ...     requests.append(saved)
    ...     return replies[len(requests) - 1]
    >>> with patch("builtins.input",
    ...            side_effect=["I am playing Halo.", "What game?", EOFError]):
    ...     with patch.object(client.chat.completions, "create",
    ...                       side_effect=fake_create):
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
            print(chat.send_message(
                user_input,
                temperature=temperature,
            ))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    repl()