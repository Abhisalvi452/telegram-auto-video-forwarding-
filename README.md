# Telegram Auto Message Forwarding Script

This repository contains a Python script to automatically forward messages from a Telegram channel to another channel or group. The script uses the Telethon library and allows users to customize which types of messages to forward and the delay between forwards.

## Features
- Forward messages of specific types (videos, photos, links, etc.)
- Set delay between message forwards
- Customize the script easily

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Abhisalvi452/telegram-auto-video-forwarding
    cd elegram-auto-video-forwarding
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your credentials and settings in `config.json`.

4. Run the script:
    ```bash
    python forwarder.py
    ```

## Configuration

The `config.json` file contains the necessary settings to run the script:

```json
{
    "api_id": "your_api_id",
    "api_hash": "your_api_hash",
    "source_channel": "https://t.me/your_source_channel",
    "destination_channel": "https://t.me/your_destination_channel",
    "message_types": ["video", "photo", "text", "document", "link"],
    "max_messages_per_run": 1000,
    "min_delay": 1,
    "max_delay": 3
}
```

## License

This project is licensed under the MIT License.
