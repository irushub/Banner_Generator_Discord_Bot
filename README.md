# 🎨 Banner Bot

The **Banner Bot** is a Discord bot that allows users to create custom banners for NFTs by providing a token ID. The bot fetches the relevant NFT data and generates a visually appealing banner that can be shared in Discord.

## 🚀 Features

- **Dynamic Banner Creation**: Generates a banner using the NFT's image and background color.
- **Seamless Integration**: Works directly within Discord, allowing users to generate banners with a simple command.
- **User Notifications**: Notifies the bot owner when a user creates a banner.

## 🛠️ Technologies Used

- **Discord.py**: A powerful Python library for creating Discord bots.
- **Pillow**: A Python Imaging Library (PIL) for image processing tasks.
- **SQLite**: A lightweight database for storing NFT data.
- **Requests**: A simple HTTP library for making API calls.

## 📁 Code Overview

### Key Functions

- **`fetch_background_color(token_id)`**: Retrieves the background color for the specified NFT token ID.
  
- **`fetch_nft_image_link(token_id)`**: Fetches the image link for the specified NFT token ID.
  
- **`create_discord_banner(token_id)`**: 
  - Generates a banner using the NFT image and background color.
  - Downloads the NFT image from the provided link.
  - Resizes and mirrors the image before pasting it onto the banner.
  - Saves the final banner as a PNG file.

### Command

- **`/generate_banner`**: This command takes a token ID as input and generates a banner. If successful, it sends the banner to the user, and if there’s an error, it informs the user.

### Bot Initialization

- The bot uses default intents to operate and can respond to commands prefixed with `!`.
- Upon successful startup, the bot syncs the command tree and logs its status.

## ⚙️ Getting Started

- Configure your Discord bot token as an environment variable named `BOT_TOKEN`.

## 📫 Contact

For any questions or suggestions, please reach out via [your email] or create an issue in the repository.

---

Happy banner generating! 🎉
