# ChatPage Component

The ChatPage is a full-screen chat interface component with a sticky footer, designed for dedicated chat applications or messaging interfaces in Anvil. It shares many features with the ChatBox component but is optimized for full-page layouts.

## Features

- Full-screen chat interface
- Sticky input footer
- Automatic scrolling to latest messages
- Message feedback system (thumbs up/down)
- Optional branding footer
- Flag button for message reporting
- Smart scroll behavior based on UI state

## Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `message_history` | list | List of message dictionaries | [] |
| `brand_message` | str | HTML content for branding footer | "Powered by..." |
| `show_branding` | bool | Toggle branding footer visibility | True |
| `show_flag` | bool | Toggle flag button visibility | True |
| `input_text` | str | Get/set the input textbox content | "" |

## Events

The ChatPage component raises several events that you can handle in your application:

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
from .ChatPage import ChatPage

class ChatForm(ChatForm):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Configure the chat page
        self.chat_page.show_branding = True
        self.chat_page.brand_message = "Powered by MyApp"

        # Set initial messages
        self.chat_page.message_history = [
            {"from": "bot", "text": "Welcome to the chat!"}
        ]

    def chat_page_send_message(self, **event_args):
        # Handle new message
        message = self.chat_page.input_text
        if message:
            # Add user message
            self.chat_page.message_history += [{"from": "user", "text": message}]
            # Clear input
            self.chat_page.input_text = ""
            # Show loading state
            self.chat_page.message_history += [{"from": "bot", "text": "Loading...", "img": True}]
            # Process message and update with response...
```

## Key Differences from ChatBox

1. **Full-Screen Design**: Optimized for full-page layouts rather than embedded chat widgets
2. **Sticky Footer**: Input area remains fixed at the bottom of the screen
3. **Smart Scrolling**: Automatically handles scroll behavior based on UI state:
   - Scrolls to flag button when visible
   - Otherwise scrolls to the last message
4. **No Fixed Height**: Unlike ChatBox, ChatPage adapts to the full viewport height

## Styling

The ChatPage uses the same CSS classes as ChatBox for consistency:

- `.chat-bubble`: Base class for message bubbles
- `.user-bubble`: Styling for user messages
- `.bot-bubble`: Styling for bot messages
- `.round-flow-panel`: Container with branding
- `.solo-flow-panel`: Container without branding
