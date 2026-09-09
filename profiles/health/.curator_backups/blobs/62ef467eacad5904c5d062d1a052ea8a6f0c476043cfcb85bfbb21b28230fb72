---
name: messaging-gateway-configuration
description: Configure and verify isolated Hermes messaging gateways.
version: 0.1.0
author: Dean Radcliffe, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, messaging, gateway, Telegram, profiles]
    related_skills: []
---

# Messaging Gateway Configuration

Use this skill to connect a Hermes profile to a messaging platform and verify that the profile's gateway genuinely receives traffic. Keep profile credentials, sessions, and gateway processes isolated.

## When to Use

- A user asks to set up Telegram or another messaging platform for a Hermes profile.
- A profile gateway is installed but cannot connect, start, or stay running.
- Multiple Hermes profiles need simultaneous messaging access.

Do not use this for model/provider setup or for configuring a non-Hermes bot framework.

## Prerequisites

- Load the `hermes-agent` skill and consult the current official messaging documentation.
- Resolve the active profile home from `HERMES_HOME`; do not place profile credentials in another profile's `.env`.
- Never print or read a bot token back to the user. Check only whether the relevant secret is present.
- Verify the intended profile's existing gateway status before changing services.

## Procedure

1. Confirm the platform secret is present only for the target profile and identify whether the platform is already configured. Completion: the secret presence and platform configuration are known without exposing the secret.
2. Run `hermes gateway setup` with the target `HERMES_HOME` and retain existing platform settings unless the user explicitly asks to change them. Completion: the setup flow reports the selected platform configured.
3. Choose automatic launch only when the user intends the bot to stay available after login/reboot. Completion: the platform's profile-specific service is installed and loaded.
4. Verify `hermes gateway status`, then inspect the profile-specific gateway log and error log for a successful platform connection. Completion: the process is active and the log confirms the platform connected; service installation alone is not sufficient.
5. Ask the user to send a test message to the bot and verify that a new inbound session or gateway-log entry appears. Completion: the profile, rather than merely the service, has processed a real message.

## Telegram Profile Isolation

- A Telegram bot token may be used by only one active Hermes gateway. Do not start a second profile gateway using a token already owned by another profile.
- For separate agents, use a separate BotFather token for each profile. This is the default and preserves distinct memories, sessions, and failure domains.
- If the user instead wants to move an existing bot, obtain explicit consent before stopping its current profile gateway; stop it, reassign the token, then start and verify the target profile gateway.
- If a new gateway reports a token conflict, stop the newly created failing service to avoid a restart loop while awaiting the user's token/migration decision.

## Pitfalls

- A successful interactive setup can install a launchd/systemd service even though the platform connection later fails.
- Do not conclude a bot is working from a registered service definition or a clean setup exit alone; logs must show an actual connection.
- Do not stop an existing profile's gateway merely to resolve a token conflict unless the user selected token migration.
- Keep direct-message access restricted with the platform's allowed-user setting; do not enable public access by default.

## Verification

- The target profile has its own platform secret and the current profile does not share an active token with another gateway.
- The installed profile service is registered and active.
- The gateway log confirms a successful platform connection without token-conflict errors.
- A test message produces a new inbound session or log record for the target profile.
