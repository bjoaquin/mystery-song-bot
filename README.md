# 🎧 Mystery Song Bot

A Slack bot that posts mystery Spotify songs to your channel.

## 🔧 Setup

### 1️⃣ Slack App

- Create a Slack app at https://api.slack.com/apps
- Add scopes: `chat:write`
- Install app to workspace
- Get your Bot Token (`xoxb-...`)

### 2️⃣ Web Host

- Deploy `web/index.html` to Netlify or Vercel.
- Note the URL (e.g. `https://your-site.netlify.app`)

### 3️⃣ Environment variables

Create a `.env` file:

```env
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=your-channel-id
WEB_HOST_URL=https://your-site.netlify.app
