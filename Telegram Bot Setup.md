# Setting Up a Telegram Bot for FileMonitorApp Notifications

This guide explains how to create and configure a Telegram bot to receive alerts from the `FileMonitorApp`.

## 1. Create Your Telegram Bot

1. Open Telegram and search for **@BotFather**.
2. Start a chat and send the command: `/newbot`
3. Choose a **name** for your bot (e.g., `File Monitor Bot`).
4. Choose a **username** that ends with `bot` (e.g., `filemonitor_alertbot`).
5. You will receive a **token** that looks like:
   ```
   123456789:ABCdefGhIJKlmnoPQRstuVWxyZ
   ```
   Save this token.

## 2. Get Your Telegram Chat ID

1. Search Telegram for **@userinfobot**.
2. Start the bot and note the line:
   ```
   Your ID: 123456789
   ```
   This is your personal `chat_id`.

## 3. Start a Chat with Your Bot

Before your bot can send you messages, you **must start a chat with it** manually in Telegram:

1. Open Telegram and search for your bot (e.g., `@filemonitor_alertbot`).
2. Open the chat and click the **Start** button or send any message.

If you skip this step, the bot **will not be able to send you notifications** even if the token and chat ID are correct.

## 4. Update `config.properties`

Open the `config.properties` file and add or update these lines:
```ini
telegram_token = 123456789:ABCdefGhIJKlmnoPQRstuVWxyZ
telegram_chat_id = 123456789
```

## 5. Done!

Now, whenever a keyword is detected in the monitored file, the app will send an alert to your Telegram account.

---

> ⚠️ Note: Make sure the bot is not blocked and that you have started a chat with it at least once, or it won’t be able to send you messages.