# ChatBox Component

The ChatBox is a flexible, height-adjustable chat widget that can be integrated into any Anvil application. It provides a complete chat interface with support for message history, branding, and interactive features.

## Features

- Height-adjustable chat container
- Message input with send button
- Support for bot and user messages
- Optional branding footer
- Flag button for message reporting
- Thumbs up/down feedback system
- Auto-scrolling to latest messages

## Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `height` | int | Height of the chat container in pixels | 300 |
| `message_history` | list | List of message dictionaries | [] |
| `brand_message` | str | HTML content for branding footer | "Powered by..." |
| `show_branding` | bool | Toggle branding footer visibility | True |
| `show_flag` | bool | Toggle flag button visibility | True |
| `input_text` | str | Get/set the input textbox content | "" |

## Events

The ChatBox component raises several events that you can handle in your application:

- `send_message`: Triggered when the send button is clicked or Enter is pressed
- `flag_click`: Triggered when the flag button is clicked
- `thumbs_up_click`: Triggered when a message's thumbs up button is clicked
- `thumbs_down_click`: Triggered when a message's thumbs down button is clicked

## Message Format

Messages in the `message_history` should be dictionaries with the following structure:

```python
{
    "from": "bot" | "user",  # Source of the message
    "text": "Message content",  # Text content
    "img": bool  # Optional, set True to display loading indicator
}
```

## Usage Example

```python
from anvil import *
from .ChatBox import ChatBox

class MyForm(MyFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Configure the chat box
        self.chat_box.height = 400
        self.chat_box.show_branding = False

        # Set initial messages
        self.chat_box.message_history = [
            {"from": "bot", "text": "Hello! How can I help you today?"},
            {"from": "user", "text": "I have a question..."}
        ]

    def chat_box_send_message(self, **event_args):
        # Handle new message
        message = self.chat_box.input_text
        if message:
            # Add user message to history
            self.chat_box.message_history += [{"from": "user", "text": message}]
            # Clear input
            self.chat_box.input_text = ""
            # Add loading indicator
            self.chat_box.message_history += [{"from": "bot", "text": "Loading...", "img": True}]
            # Process message and update with bot response...
```

## Styling

The ChatBox uses custom CSS classes for styling:

- `.chat-bubble`: Base class for message bubbles
- `.user-bubble`: Styling for user messages
- `.bot-bubble`: Styling for bot messages
- `.round-flow-panel`: Container with branding
- `.solo-flow-panel`: Container without branding

You can customize these classes in your app's theme to match your application's design.
