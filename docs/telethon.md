# Telethon Data Map — Telegram Supergroup

Complete inventory of all data available via Telethon for a Telegram **Supergroup** (megagroup).

---

## Table of Contents

1. [Channel (Supergroup) Object](#1-channel-supergroup-object)
2. [ChannelFull (Extended Info)](#2-channelfull-extended-info)
3. [Forum Topics](#3-forum-topics)
4. [Messages](#4-messages)
5. [Message Entities (Inline Markup)](#5-message-entities)
6. [Message Media Types](#6-message-media-types)
7. [Message Forward Headers](#7-message-forward-headers)
8. [Reply Headers & Threads](#8-reply-headers--threads)
9. [Reactions](#9-reactions)
10. [Service Messages & Actions](#10-service-messages--actions)
11. [Users](#11-users)
12. [UserFull (Extended Info)](#12-userfull-extended-info)
13. [Participants & Permissions](#13-participants--permissions)
14. [Client API Methods (Data Retrieval)](#14-client-api-methods)
15. [Admin Log Events](#15-admin-log-events)
16. [Statistics](#16-statistics)

---

## 1. Channel (Supergroup) Object

Retrieved via `client.get_entity()`. Supergroups are `Channel` objects with `megagroup=True`.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | Channel numeric identifier |
| `title` | string | Channel display name |
| `photo` | ChatPhoto | Avatar/profile image |
| `date` | date | Creation timestamp |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `access_hash` | long | Access hash for API calls |
| `username` | string | Public @username handle |
| `usernames` | Vector\<Username\> | Additional/collectible usernames |
| `participants_count` | int | Member count |
| `restriction_reason` | Vector\<RestrictionReason\> | Content restriction details |
| `admin_rights` | ChatAdminRights | Current user's admin permissions |
| `banned_rights` | ChatBannedRights | Current user's restrictions |
| `default_banned_rights` | ChatBannedRights | Default member restrictions |
| `color` | PeerColor | Profile accent color |
| `profile_color` | PeerColor | Profile background color |
| `emoji_status` | EmojiStatus | Emoji status indicator |
| `level` | int | Boost/verification level |
| `subscription_until_date` | date | Subscription expiration |
| `send_paid_messages_stars` | long | Cost for paid messages in stars |
| `linked_monoforum_id` | long | Linked monoforum ID |
| `stories_max_id` | int | Latest story ID |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `creator` | Current user created this channel |
| `left` | Current user has left |
| `broadcast` | Is a broadcast channel (false for supergroups) |
| `verified` | Officially verified |
| `megagroup` | **Is a supergroup** (always true for our case) |
| `restricted` | Has content restrictions |
| `signatures` | Shows sender signatures on posts |
| `min` | Minimal info only |
| `scam` | Marked as scam |
| `fake` | Marked as fake/impersonator |
| `has_link` | Has a linked chat/channel |
| `has_geo` | Has a physical location |
| `slowmode_enabled` | Slow mode is active |
| `call_active` | Voice/video chat is active |
| `call_not_empty` | Active call has participants |
| `gigagroup` | Is a broadcast-style supergroup (>200k members) |
| `noforwards` | Message forwarding is disabled |
| `join_to_send` | Must join to send messages |
| `join_request` | Membership requires approval |
| `forum` | **Is a forum** (has topics) |
| `stories_hidden` | Stories are hidden |
| `stories_unavailable` | Stories unavailable |
| `signature_profiles` | Signature profiles enabled |
| `autotranslation` | Auto-translation enabled |
| `broadcast_messages_allowed` | Broadcast messages permitted |
| `monoforum` | Is a monoforum |
| `forum_tabs` | Forum tabs enabled |

---

## 2. ChannelFull (Extended Info)

Retrieved via `client(GetFullChannelRequest(channel))`. Contains rich metadata not in the basic Channel object.

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | Channel ID |
| `about` | string | **Channel description/bio** |
| `participants_count` | int | Member count |
| `admins_count` | int | Admin count |
| `kicked_count` | int | Kicked user count |
| `banned_count` | int | Banned user count |
| `online_count` | int | Currently online members |
| `pts` | int | Update sequence number |

### Read State

| Field | Type | Description |
|-------|------|-------------|
| `read_inbox_max_id` | int | Last read incoming message ID |
| `read_outbox_max_id` | int | Last read outgoing message ID |
| `unread_count` | int | Unread message count |

### Media & Customization

| Field | Type | Description |
|-------|------|-------------|
| `chat_photo` | Photo | Full-res channel photo |
| `stickerset` | StickerSet | Associated sticker pack |
| `emojiset` | StickerSet | Custom emoji pack |
| `wallpaper` | WallPaper | Channel wallpaper |
| `theme_emoticon` | string | Theme emoticon |

### Linked & Migration

| Field | Type | Description |
|-------|------|-------------|
| `linked_chat_id` | long | Linked discussion/broadcast channel ID |
| `migrated_from_chat_id` | long | Original basic group ID (if migrated) |
| `migrated_from_max_id` | int | Last message ID from original group |
| `location` | ChannelLocation | Physical location (geo-groups) |

### Moderation & Settings

| Field | Type | Description |
|-------|------|-------------|
| `exported_invite` | ExportedChatInvite | Primary invite link |
| `bot_info` | Vector\<BotInfo\> | Info about bots in the group |
| `pinned_msg_id` | int | Currently pinned message ID |
| `slowmode_seconds` | int | Slowmode delay in seconds |
| `slowmode_next_send_date` | date | Next allowed send time (under slowmode) |
| `available_min_id` | int | Oldest available message ID |
| `folder_id` | int | Chat folder ID |
| `ttl_period` | int | Auto-delete timer (seconds) |
| `available_reactions` | ChatReactions | Allowed reaction set |
| `reactions_limit` | int | Max reactions per message |
| `default_send_as` | Peer | Default "send as" identity |
| `groupcall_default_join_as` | Peer | Default identity for calls |
| `notify_settings` | PeerNotifySettings | Notification config |
| `pending_suggestions` | Vector\<string\> | Pending admin suggestions |
| `requests_pending` | int | Pending join requests |
| `recent_requesters` | Vector\<long\> | Recent requester user IDs |
| `call` | InputGroupCall | Active group call reference |
| `stats_dc` | int | Datacenter for statistics |
| `stories` | PeerStories | Channel stories |

### Monetization

| Field | Type | Description |
|-------|------|-------------|
| `boosts_applied` | int | Applied boosts count |
| `boosts_unrestrict` | int | Boosts needed to lift restrictions |
| `stargifts_count` | int | Star gifts count |
| `send_paid_messages_stars` | long | Paid message cost in stars |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `can_view_participants` | Can see member list |
| `can_set_username` | Can set public username |
| `can_set_stickers` | Can set sticker pack |
| `can_set_location` | Can set physical location |
| `can_view_stats` | Can view statistics |
| `can_delete_channel` | Can delete the channel |
| `can_view_revenue` | Can view revenue data |
| `can_view_stars_revenue` | Can view stars revenue |
| `hidden_prehistory` | History hidden for new members |
| `has_scheduled` | Has scheduled messages |
| `blocked` | Channel is blocked |
| `antispam` | Anti-spam enabled |
| `participants_hidden` | Member list is hidden |
| `translations_disabled` | Translations disabled |
| `stories_pinned_available` | Has pinned stories |
| `view_forum_as_messages` | View forum as flat messages |
| `restricted_sponsored` | Restricted sponsored messages |
| `paid_media_allowed` | Paid media allowed |
| `paid_reactions_available` | Paid reactions available |
| `stargifts_available` | Star gifts available |
| `paid_messages_available` | Paid messages available |

---

## 3. Forum Topics

Retrieved via `client(GetForumTopicsRequest(...))`. Only available when `channel.forum == True`.

### ForumTopic Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Topic ID (matches `reply_to_top_id` in messages) |
| `date` | date | Creation timestamp |
| `title` | string | Topic title |
| `icon_color` | int | Icon color value |
| `icon_emoji_id` | long | Custom emoji for icon |
| `top_message` | int | Highest message ID in topic |
| `read_inbox_max_id` | int | Last read incoming msg ID |
| `read_outbox_max_id` | int | Last read outgoing msg ID |
| `unread_count` | int | Unread messages |
| `unread_mentions_count` | int | Unread @mentions |
| `unread_reactions_count` | int | Unread reactions |
| `from_id` | Peer | Topic creator |
| `peer` | Peer | Parent channel |
| `notify_settings` | PeerNotifySettings | Notification config |
| `draft` | DraftMessage | Unsent draft |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `my` | Created by current user |
| `closed` | Topic is closed |
| `pinned` | Topic is pinned |
| `short` | Short-form topic |
| `hidden` | Topic is hidden (e.g. "General") |
| `title_missing` | Title not available |

### Topic Lifecycle (via Service Messages)

| Action | Fields |
|--------|--------|
| `MessageActionTopicCreate` | `title`, `icon_color`, `icon_emoji_id`, `title_missing` |
| `MessageActionTopicEdit` | `title`, `icon_emoji_id`, `closed`, `hidden` |

---

## 4. Messages

The core data object. Retrieved via `client.iter_messages()` / `client.get_messages()`.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique message ID (within the chat) |
| `peer_id` | Peer | Chat this message belongs to |
| `date` | date | Send timestamp (UTC) |
| `message` | string | **Text content** (can be empty) |

### Sender & Context

| Field | Type | Description |
|-------|------|-------------|
| `from_id` | Peer | Sender (user, channel, or anonymous) |
| `fwd_from` | MessageFwdHeader | Forward metadata (see §7) |
| `via_bot_id` | long | Bot used to send (inline bots) |
| `via_business_bot_id` | long | Business bot ID |
| `reply_to` | MessageReplyHeader | Reply/thread info (see §8) |
| `saved_peer_id` | Peer | Saved messages peer |
| `from_boosts_applied` | int | Boosts applied by sender |
| `post_author` | string | Author signature (channel posts) |

### Content

| Field | Type | Description |
|-------|------|-------------|
| `media` | MessageMedia | Attached media (see §6) |
| `entities` | Vector\<MessageEntity\> | Inline text formatting & links (see §5) |
| `reply_markup` | ReplyMarkup | Inline keyboard / buttons |

### Engagement Metrics

| Field | Type | Description |
|-------|------|-------------|
| `views` | int | **View count** |
| `forwards` | int | **Forward count** |
| `replies` | MessageReplies | Reply thread info & count (see §8) |
| `reactions` | MessageReactions | Emoji reactions (see §9) |

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `edit_date` | date | Last edit timestamp |
| `grouped_id` | long | Album/media group ID |
| `restriction_reason` | Vector\<RestrictionReason\> | Content restrictions |
| `ttl_period` | int | Self-destruct timer (seconds) |
| `effect` | long | Message animation effect |
| `factcheck` | FactCheck | Attached fact-check |
| `quick_reply_shortcut_id` | int | Quick reply reference |
| `paid_message_stars` | long | Stars payment amount |
| `suggested_post` | SuggestedPost | Suggested post data |
| `report_delivery_until_date` | date | Report delivery deadline |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `out` | Sent by current user |
| `mentioned` | Current user was @mentioned |
| `media_unread` | Media not yet viewed |
| `silent` | Sent without notification |
| `post` | Is a channel post (vs group message) |
| `from_scheduled` | Was a scheduled message |
| `legacy` | Legacy format |
| `edit_hide` | Edit indicator hidden |
| `pinned` | **Message is pinned** |
| `noforwards` | Forwarding disabled for this message |
| `invert_media` | Invert media position |
| `offline` | Sent while sender was offline |
| `video_processing_pending` | Video still processing |

---

## 5. Message Entities

Inline markup within `message.entities`. Each entity has `offset` (int) and `length` (int) marking the text span.

| Entity Type | Extra Fields | Description |
|-------------|-------------|-------------|
| `MessageEntityMention` | — | `@username` mention |
| `MessageEntityMentionName` | `user_id` (long) | Mention with resolved user ID |
| `MessageEntityHashtag` | — | `#hashtag` |
| `MessageEntityCashtag` | — | `$CASHTAG` (stocks/crypto) |
| `MessageEntityBotCommand` | — | `/command` |
| `MessageEntityUrl` | — | Auto-detected URL |
| `MessageEntityTextUrl` | `url` (string) | Hyperlinked text (hidden URL) |
| `MessageEntityEmail` | — | Email address |
| `MessageEntityPhone` | — | Phone number |
| `MessageEntityBold` | — | **Bold** formatting |
| `MessageEntityItalic` | — | *Italic* formatting |
| `MessageEntityUnderline` | — | Underline formatting |
| `MessageEntityStrike` | — | ~~Strikethrough~~ formatting |
| `MessageEntityCode` | — | `Inline code` |
| `MessageEntityPre` | `language` (string) | ```Code block``` with language |
| `MessageEntityBlockquote` | — | Block quote |
| `MessageEntitySpoiler` | — | Spoiler text |
| `MessageEntityCustomEmoji` | `document_id` (long) | Custom/premium emoji |
| `MessageEntityBankCard` | — | Bank card number |
| `MessageEntityUnknown` | — | Unrecognized entity |

---

## 6. Message Media Types

The `message.media` field can be one of 18 types:

| Media Type | Key Fields | Description |
|------------|-----------|-------------|
| `MessageMediaPhoto` | `photo` (Photo), `spoiler`, `ttl_seconds` | Image attachment |
| `MessageMediaDocument` | `document` (Document), `spoiler`, `ttl_seconds`, `nopremium`, `video`, `round`, `voice` | File, video, audio, sticker, GIF, voice note |
| `MessageMediaWebPage` | `webpage` (WebPage) | **Link preview** (see §6.1) |
| `MessageMediaGeo` | `geo` (GeoPoint) | Static location (lat/long) |
| `MessageMediaGeoLive` | `geo`, `heading`, `period`, `proximity_notification_radius` | Live location sharing |
| `MessageMediaVenue` | `geo`, `title`, `address`, `provider`, `venue_id`, `venue_type` | Named venue/place |
| `MessageMediaContact` | `phone_number`, `first_name`, `last_name`, `vcard`, `user_id` | Shared contact |
| `MessageMediaPoll` | `poll` (Poll), `results` (PollResults) | **Poll/quiz** (see §6.2) |
| `MessageMediaDice` | `value`, `emoticon` | Dice/slot machine animation |
| `MessageMediaGame` | `game` (Game) | Inline game |
| `MessageMediaInvoice` | `title`, `description`, `currency`, `total_amount`, etc. | Payment invoice |
| `MessageMediaStory` | `peer`, `id`, `story` | Shared story |
| `MessageMediaGiveaway` | `channels`, `quantity`, `months`, etc. | Giveaway campaign |
| `MessageMediaGiveawayResults` | `winners`, `unclaimed_count`, etc. | Giveaway results |
| `MessageMediaPaidMedia` | `stars_amount`, `extended_media` | Premium/paid content |
| `MessageMediaToDo` | — | Task/checklist |
| `MessageMediaEmpty` | — | No media |
| `MessageMediaUnsupported` | — | Unsupported type |

### 6.1 WebPage (Link Preview)

Rich metadata extracted from shared URLs:

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | Page ID |
| `url` | string | **Canonical URL** |
| `display_url` | string | Display URL |
| `type` | string | Content type (article, photo, video, etc.) |
| `site_name` | string | Website name |
| `title` | string | Page title |
| `description` | string | Page description/excerpt |
| `photo` | Photo | Preview image |
| `author` | string | Content author |
| `embed_url` | string | Embeddable content URL |
| `embed_type` | string | Embed format |
| `embed_width` | int | Embed width px |
| `embed_height` | int | Embed height px |
| `duration` | int | Media duration (seconds) |
| `document` | Document | Attached document |
| `cached_page` | Page | Instant View cached page |
| `attributes` | Vector\<WebPageAttribute\> | Additional attributes |

### 6.2 Poll

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | Poll ID |
| `question` | TextWithEntities | Question text with formatting |
| `answers` | Vector\<PollAnswer\> | Available options |
| `closed` | flag | Voting is closed |
| `public_voters` | flag | Votes are public |
| `multiple_choice` | flag | Multiple answers allowed |
| `quiz` | flag | Quiz mode (one correct answer) |
| `close_period` | int | Auto-close after N seconds |
| `close_date` | date | Specific close timestamp |

`PollResults` contains per-option vote counts and total voter count.

---

## 7. Message Forward Headers

When `message.fwd_from` is set, the message was forwarded. Fields:

| Field | Type | Description |
|-------|------|-------------|
| `date` | date | **Original send date** |
| `from_id` | Peer | Original sender (user/channel) |
| `from_name` | string | Original sender name (if privacy hides ID) |
| `channel_post` | int | Original message ID in source channel |
| `post_author` | string | Original author signature |
| `saved_from_peer` | Peer | Chat it was saved/forwarded from |
| `saved_from_msg_id` | int | Message ID in that chat |
| `saved_from_id` | Peer | Saved-from identity |
| `saved_from_name` | string | Saved-from display name |
| `saved_date` | date | Date saved |
| `psa_type` | string | Public service announcement type |
| `imported` | flag | Imported from another platform |
| `saved_out` | flag | Saved outgoing message |

---

## 8. Reply Headers & Threads

### MessageReplyHeader

When `message.reply_to` is set:

| Field | Type | Description |
|-------|------|-------------|
| `reply_to_msg_id` | int | **ID of message being replied to** |
| `reply_to_peer_id` | Peer | Chat of the replied-to message (cross-chat replies) |
| `reply_to_top_id` | int | **Top-level message ID of the thread** (crucial for forum topics) |
| `reply_from` | MessageFwdHeader | Forward info of the quoted message |
| `reply_media` | MessageMedia | Media from the quoted message |
| `quote_text` | string | Quoted text excerpt |
| `quote_entities` | Vector\<MessageEntity\> | Formatting in quoted text |
| `quote_offset` | int | Offset in original message |
| `forum_topic` | flag | Reply is within a forum topic |
| `reply_to_scheduled` | flag | Replying to a scheduled message |
| `quote` | flag | Contains a quote |

### MessageReplies (Thread Summary)

Attached to the **root message** of a thread:

| Field | Type | Description |
|-------|------|-------------|
| `replies` | int | **Total reply count** |
| `replies_pts` | int | PTS value |
| `comments` | flag | Are these comments (linked channel) |
| `recent_repliers` | Vector\<Peer\> | **Last few repliers** (user/channel IDs) |
| `channel_id` | long | Discussion channel ID |
| `max_id` | int | Highest reply message ID |
| `read_max_id` | int | Last read reply ID |

---

## 9. Reactions

### MessageReactions

| Field | Type | Description |
|-------|------|-------------|
| `results` | Vector\<ReactionCount\> | **Per-reaction counts** |
| `recent_reactions` | Vector\<MessagePeerReaction\> | Recent individual reactions (who reacted) |
| `top_reactors` | Vector\<MessageReactor\> | Top reactors |
| `min` | flag | Minimal info |
| `can_see_list` | flag | Full reactor list available |
| `reactions_as_tags` | flag | Reactions used as tags |

### ReactionCount

| Field | Type | Description |
|-------|------|-------------|
| `reaction` | Reaction | The reaction itself |
| `count` | int | **How many times used** |
| `chosen_order` | int | Order if current user chose this |

### Reaction Types

| Type | Fields | Description |
|------|--------|-------------|
| `ReactionEmoji` | `emoticon` (string) | Standard Unicode emoji |
| `ReactionCustomEmoji` | `document_id` (long) | Premium custom emoji |
| `ReactionPaid` | — | Paid/stars reaction |
| `ReactionEmpty` | — | No reaction |

---

## 10. Service Messages & Actions

Service messages (`MessageService`) represent group events. Same base fields as Message (`id`, `from_id`, `peer_id`, `date`, `reply_to`, `reactions`) plus an `action` field.

### All 58 MessageAction Types

#### Group Lifecycle
| Action | Description |
|--------|-------------|
| `MessageActionChatCreate` | Group was created |
| `MessageActionChatEditTitle` | Group title changed |
| `MessageActionChatEditPhoto` | Group photo changed |
| `MessageActionChatDeletePhoto` | Group photo removed |
| `MessageActionChatMigrateTo` | Basic group → supergroup migration |
| `MessageActionChannelMigrateFrom` | Supergroup created from basic group |
| `MessageActionChannelCreate` | Channel/supergroup created |

#### Membership
| Action | Description |
|--------|-------------|
| `MessageActionChatAddUser` | User(s) added |
| `MessageActionChatDeleteUser` | User removed/left |
| `MessageActionChatJoinedByLink` | User joined via invite link |
| `MessageActionChatJoinedByRequest` | User approved to join |

#### Forum Topics
| Action | Fields | Description |
|--------|--------|-------------|
| `MessageActionTopicCreate` | `title`, `icon_color`, `icon_emoji_id` | Topic created |
| `MessageActionTopicEdit` | `title`, `icon_emoji_id`, `closed`, `hidden` | Topic modified |

#### Moderation
| Action | Description |
|--------|-------------|
| `MessageActionPinMessage` | Message was pinned |
| `MessageActionHistoryClear` | Chat history cleared |
| `MessageActionSetMessagesTTL` | Auto-delete timer set |
| `MessageActionSetChatTheme` | Chat theme changed |
| `MessageActionSetChatWallPaper` | Wallpaper changed |

#### Calls
| Action | Description |
|--------|-------------|
| `MessageActionGroupCall` | Group voice/video call started/ended |
| `MessageActionGroupCallScheduled` | Group call scheduled |
| `MessageActionInviteToGroupCall` | User invited to call |
| `MessageActionConferenceCall` | Conference call event |
| `MessageActionPhoneCall` | 1:1 phone call |

#### Payments & Gifts
| Action | Description |
|--------|-------------|
| `MessageActionPaymentSent` | Payment sent |
| `MessageActionPaymentSentMe` | Payment received |
| `MessageActionPaymentRefunded` | Payment refunded |
| `MessageActionGiftPremium` | Premium subscription gifted |
| `MessageActionGiftCode` | Gift code sent |
| `MessageActionGiftStars` | Stars gifted |
| `MessageActionGiftTon` | TON gifted |
| `MessageActionStarGift` | Star gift |
| `MessageActionStarGiftUnique` | Unique star gift |
| `MessageActionPrizeStars` | Prize in stars |
| `MessageActionPaidMessagesPrice` | Paid message pricing set |
| `MessageActionPaidMessagesRefunded` | Paid message refunded |

#### Giveaways
| Action | Description |
|--------|-------------|
| `MessageActionGiveawayLaunch` | Giveaway started |
| `MessageActionGiveawayResults` | Giveaway results announced |

#### Tasks/To-Do
| Action | Description |
|--------|-------------|
| `MessageActionTodoAppendTasks` | Tasks added to to-do list |
| `MessageActionTodoCompletions` | Tasks marked complete |

#### Bots & Misc
| Action | Description |
|--------|-------------|
| `MessageActionBotAllowed` | Bot authorized |
| `MessageActionGameScore` | Game high score |
| `MessageActionGeoProximityReached` | Location proximity alert |
| `MessageActionContactSignUp` | Contact registered on Telegram |
| `MessageActionScreenshotTaken` | Screenshot taken |
| `MessageActionSecureValuesSent` | Passport docs sent |
| `MessageActionCustomAction` | Custom action string |
| `MessageActionBoostApply` | Boost applied |
| `MessageActionRequestedPeer` | Peer shared via keyboard button |
| `MessageActionSuggestProfilePhoto` | Profile photo suggestion |
| `MessageActionSuggestBirthday` | Birthday suggestion |
| `MessageActionSuggestedPostApproval` | Suggested post approved |
| `MessageActionSuggestedPostRefund` | Suggested post refunded |
| `MessageActionSuggestedPostSuccess` | Suggested post succeeded |
| `MessageActionWebViewDataSent` | Web app data sent |
| `MessageActionEmpty` | No action |

---

## 11. Users

Retrieved alongside messages (in the `users` list of API responses) or via `client.get_entity()`.

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | **User ID** |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `username` | string | @username |
| `usernames` | Vector\<Username\> | Additional usernames |
| `phone` | string | Phone number (if contact/self) |
| `photo` | UserProfilePhoto | Profile photo reference |
| `status` | UserStatus | Online/offline status |
| `lang_code` | string | Language code |
| `access_hash` | long | Access hash |

### Status Types

| Type | Fields | Description |
|------|--------|-------------|
| `UserStatusOnline` | `expires` (date) | Currently online, expires at |
| `UserStatusOffline` | `was_online` (date) | Last seen timestamp |
| `UserStatusRecently` | — | Last seen recently |
| `UserStatusLastWeek` | — | Last seen within a week |
| `UserStatusLastMonth` | — | Last seen within a month |
| `UserStatusEmpty` | — | No status available |

### Customization

| Field | Type | Description |
|-------|------|-------------|
| `color` | PeerColor | Name accent color |
| `profile_color` | PeerColor | Profile page color |
| `emoji_status` | EmojiStatus | Custom emoji status |
| `stories_max_id` | int | Latest story ID |
| `bot_active_users` | int | Active users (bots only) |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `is_self` | Is the authenticated user |
| `contact` | Is in contacts |
| `mutual_contact` | Mutual contact |
| `deleted` | Account deleted |
| `bot` | Is a bot |
| `bot_chat_history` | Bot can read chat history |
| `bot_nochats` | Bot cannot be added to groups |
| `bot_inline_geo` | Bot requests geo for inline |
| `bot_attach_menu` | Bot has attach menu |
| `bot_can_edit` | Bot is editable |
| `bot_business` | Is a business bot |
| `bot_has_main_app` | Bot has a main mini app |
| `verified` | Officially verified |
| `restricted` | Content restricted |
| `scam` | Marked as scam |
| `fake` | Marked as fake |
| `premium` | **Has Telegram Premium** |
| `close_friend` | Marked as close friend |
| `stories_hidden` | Stories hidden from feed |
| `stories_unavailable` | No stories available |
| `contact_require_premium` | Requires premium to contact |
| `support` | Is Telegram support |
| `attach_menu_enabled` | Attach menu active |
| `bot_forum_view` | Bot uses forum view |

---

## 12. UserFull (Extended Info)

Retrieved via `client(GetFullUserRequest(user_id))`.

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | long | User ID |
| `about` | string | **Bio / about text** |
| `common_chats_count` | int | Mutual groups count |
| `personal_photo` | Photo | Personal photo (for you) |
| `profile_photo` | Photo | Public profile photo |
| `fallback_photo` | Photo | Fallback photo |
| `pinned_msg_id` | int | Pinned message in 1:1 chat |
| `folder_id` | int | Chat folder |
| `ttl_period` | int | Auto-delete timer |
| `theme` | ChatTheme | Chat theme |
| `private_forward_name` | string | Name shown when forwarding privately |
| `settings` | PeerSettings | Peer settings |
| `notify_settings` | PeerNotifySettings | Notification settings |
| `bot_info` | BotInfo | Bot description, commands, menu |
| `wallpaper` | WallPaper | Chat wallpaper |
| `stories` | PeerStories | User's stories |
| `birthday` | Birthday | Birthday info |
| `personal_channel_id` | long | Personal channel ID |
| `note` | TextWithEntities | Your note about this user |

### Business Fields (bots/business accounts)

| Field | Type | Description |
|-------|------|-------------|
| `business_work_hours` | BusinessWorkHours | Work hours |
| `business_location` | BusinessLocation | Business address |
| `business_greeting_message` | BusinessGreetingMessage | Auto-greeting |
| `business_away_message` | BusinessAwayMessage | Away message |
| `business_intro` | BusinessIntro | Business intro |
| `bot_group_admin_rights` | ChatAdminRights | Bot's default group perms |
| `bot_broadcast_admin_rights` | ChatAdminRights | Bot's default channel perms |

### Boolean Flags

| Flag | Description |
|------|-------------|
| `blocked` | User is blocked |
| `phone_calls_available` | Can make phone calls |
| `phone_calls_private` | Phone calls are private |
| `video_calls_available` | Can make video calls |
| `voice_messages_forbidden` | Voice messages blocked |
| `can_pin_message` | Can pin messages |
| `has_scheduled` | Has scheduled messages |
| `translations_disabled` | Translations disabled |
| `stories_pinned_available` | Has pinned stories |
| `blocked_my_stories_from` | Blocked from your stories |
| `wallpaper_overridden` | Custom wallpaper set |
| `contact_require_premium` | Premium required to contact |
| `read_dates_private` | Read receipts hidden |
| `sponsored_enabled` | Sponsored content enabled |

---

## 13. Participants & Permissions

### Participant Types

Retrieved via `client.get_participants()` / `client.iter_participants()`.

#### ChannelParticipant (Regular Member)

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | long | User ID |
| `date` | date | **Join date** |
| `subscription_until_date` | date | Subscription expiry |

#### ChannelParticipantAdmin

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | long | User ID |
| `date` | date | Promotion date |
| `promoted_by` | long | Who promoted them |
| `inviter_id` | long | Who invited them |
| `admin_rights` | ChatAdminRights | Permission set |
| `rank` | string | **Custom admin title** |
| `can_edit` | flag | Can be edited |
| `is_self` | flag | Is current user |

#### ChannelParticipantCreator (Owner)

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | long | User ID |
| `admin_rights` | ChatAdminRights | Permission set |
| `rank` | string | **Custom owner title** |

#### ChannelParticipantBanned

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | long | User ID |
| `date` | date | Ban date |
| `kicked_by` | long | Who banned them |
| `banned_rights` | ChatBannedRights | Restriction set |

#### ChannelParticipantLeft

| Field | Type | Description |
|-------|------|-------------|
| `peer` | Peer | The peer that left |

#### ChannelParticipantSelf

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | long | User ID |
| `date` | date | Join date |
| `inviter_id` | long | Who invited current user |
| `subscription_until_date` | date | Subscription expiry |
| `via_request` | flag | Joined via request |

### ChatAdminRights (16 Permissions)

| Permission | Description |
|------------|-------------|
| `change_info` | Change group info (title, photo, etc.) |
| `post_messages` | Post messages (channels) |
| `edit_messages` | Edit others' messages |
| `delete_messages` | Delete others' messages |
| `ban_users` | Ban/restrict users |
| `invite_users` | Invite users |
| `pin_messages` | Pin messages |
| `add_admins` | Add new admins |
| `anonymous` | Post anonymously |
| `manage_call` | Manage voice/video chats |
| `other` | Other admin actions |
| `manage_topics` | Manage forum topics |
| `post_stories` | Post stories |
| `edit_stories` | Edit stories |
| `delete_stories` | Delete stories |
| `manage_direct_messages` | Manage DMs |

### ChatBannedRights (21 Restrictions)

| Restriction | Description |
|-------------|-------------|
| `until_date` | Expiration timestamp |
| `view_messages` | Cannot view messages |
| `send_messages` | Cannot send text |
| `send_media` | Cannot send any media |
| `send_stickers` | Cannot send stickers |
| `send_gifs` | Cannot send GIFs |
| `send_games` | Cannot send games |
| `send_inline` | Cannot use inline bots |
| `embed_links` | Cannot embed link previews |
| `send_polls` | Cannot send polls |
| `change_info` | Cannot change group info |
| `invite_users` | Cannot invite users |
| `pin_messages` | Cannot pin messages |
| `manage_topics` | Cannot manage topics |
| `send_photos` | Cannot send photos |
| `send_videos` | Cannot send videos |
| `send_roundvideos` | Cannot send video messages |
| `send_audios` | Cannot send audio files |
| `send_voices` | Cannot send voice notes |
| `send_docs` | Cannot send documents |
| `send_plain` | Cannot send plain text |

---

## 14. Client API Methods

### Message Retrieval

#### `iter_messages()` / `get_messages()`

| Parameter | Type | Description |
|-----------|------|-------------|
| `entity` | EntityLike | Target chat |
| `limit` | int | Max messages to fetch |
| `offset_date` | DateLike | Start from this date |
| `offset_id` | int | Start from this message ID |
| `max_id` | int | Exclude messages above this ID |
| `min_id` | int | Exclude messages below this ID |
| `add_offset` | int | Additional pagination offset |
| `search` | str | **Full-text search query** |
| `filter` | MessagesFilter | Filter by type (photos, docs, URLs, etc.) |
| `from_user` | EntityLike | **Filter by sender** |
| `wait_time` | float | Delay between API requests |
| `reverse` | bool | Oldest-first iteration |

**MessagesFilter types** (for the `filter` parameter):
- `InputMessagesFilterPhotos` — only photos
- `InputMessagesFilterVideo` — only videos
- `InputMessagesFilterDocument` — only documents
- `InputMessagesFilterUrl` — only messages with URLs
- `InputMessagesFilterGeo` — only locations
- `InputMessagesFilterContacts` — only contacts
- `InputMessagesFilterPhoneCalls` — only calls
- `InputMessagesFilterVoice` — only voice notes
- `InputMessagesFilterMusic` — only music/audio
- `InputMessagesFilterRoundVoice` — round videos + voice notes
- `InputMessagesFilterRoundVideo` — round videos only
- `InputMessagesFilterPinned` — only pinned messages
- `InputMessagesFilterMyMentions` — messages mentioning current user
- `InputMessagesFilterPhotoVideo` — photos or videos
- `InputMessagesFilterGif` — GIFs
- `InputMessagesFilterChatPhotos` — chat photo change events
- `InputMessagesFilterEmpty` — no filter

**Special usage:** Pass `ids=[101, 202, 303]` to fetch specific message IDs directly.

### Participant Retrieval

#### `iter_participants()` / `get_participants()`

| Parameter | Type | Description |
|-----------|------|-------------|
| `entity` | EntityLike | Target chat |
| `limit` | int | Max participants |
| `search` | str | **Search by name/username** |
| `filter` | ChannelParticipantsFilter | Filter type |

**Filter types:**
- `ChannelParticipantsSearch` — search by query
- `ChannelParticipantsAdmins` — admins only
- `ChannelParticipantsBots` — bots only
- `ChannelParticipantsBanned` — banned users
- `ChannelParticipantsKicked` — kicked users
- `ChannelParticipantsRecent` — recently active
- `ChannelParticipantsContacts` — members who are your contacts
- `ChannelParticipantsMentions` — users matchable via @mention

**Note:** `get_participants` is limited to ~10,000 members via the Recent filter. The `aggressive=True` parameter uses repeated alphabetical search queries to work around this cap for large groups (slower, more API calls).

### Entity Resolution

#### `get_entity()`
Converts usernames, IDs, invite links, phone numbers → full `User`, `Chat`, or `Channel` objects.

### Other Data Retrieval

| Method | Returns | Description |
|--------|---------|-------------|
| `get_me()` | User | Current authenticated user |
| `get_dialogs()` | list of Dialog | All open conversations |
| `get_permissions(chat, user)` | Permissions | User's permissions in a chat |
| `get_profile_photos(entity)` | list of Photo | Profile photo history |
| `download_media(message)` | file path | Download any media attachment |
| `download_profile_photo(entity)` | file path | Download avatar |

### Raw API Calls (via `client(Request(...))`)

These provide data not exposed by the high-level client methods.

#### Thread/Reply Retrieval

| Request | Description |
|---------|-------------|
| `messages.GetRepliesRequest(peer, msg_id, ...)` | Fetch all replies within a message thread. `msg_id` is the top-level message. Returns messages + chats + users. |
| `messages.GetDiscussionMessageRequest(peer, msg_id)` | Get the discussion group message linked to a channel post. Returns `max_id`, `read_inbox_max_id`, `unread_count`. |

#### Forum Topics

| Request | Description |
|---------|-------------|
| `channels.GetForumTopicsRequest(channel, q, offset_date, offset_id, offset_topic, limit)` | Fetch forum topics. Returns `count`, `topics` (Vector\<ForumTopic\>), `messages`, `chats`, `users`, `pts`. |
| `channels.GetForumTopicsByIDRequest(channel, topics)` | Fetch specific topics by ID list. |

#### Reactions (Per-User Attribution)

| Request | Description |
|---------|-------------|
| `messages.GetMessageReactionsListRequest(peer, id, reaction, offset, limit)` | Get per-user reaction list — **who** reacted with **what**. Only works when `can_see_list` is True. |
| `messages.GetMessagesReactionsRequest(peer, id)` | Bulk-fetch reaction summaries for multiple message IDs. |

#### Views

| Request | Description |
|---------|-------------|
| `messages.GetMessagesViewsRequest(peer, id, increment)` | Get view counts and forward counts for specific message IDs. |

#### Search (Advanced)

| Request | Description |
|---------|-------------|
| `messages.SearchRequest(peer, q, filter, min_date, max_date, from_id, top_msg_id, ...)` | Advanced search with date range, sender filter, and thread scope (`top_msg_id`). |
| `messages.SearchGlobalRequest(q, filter, min_date, max_date, ...)` | Global search across all chats. Can filter `broadcasts_only`, `groups_only`, `users_only`. |

#### Bulk Export

| Request | Description |
|---------|-------------|
| `client.takeout()` | Opens a special export session with higher rate limits, intended for bulk data export. Useful for large-scale extraction. |

---

## 15. Admin Log Events

Retrieved via `client.iter_admin_log()`. Returns `AdminLogEvent` objects tracking **all administrative actions**.

### Filter Parameters

Can filter by event type: `join`, `leave`, `invite`, `restrict`, `unrestrict`, `ban`, `unban`, `promote`, `demote`, `info`, `settings`, `pinned`, `edit`, `delete`, `group_call`.

### Event Data Includes

- Who performed the action (`user_id`)
- When it happened (`date`)
- The specific action with before/after state:
  - Title/photo/description changes
  - Permission changes (with old and new rights)
  - Message edits and deletions (with content)
  - Pin/unpin events
  - User joins/leaves/kicks/bans
  - Invite link changes
  - Slowmode changes
  - Topic operations
  - Group call events

---

## 16. Statistics

Retrieved via `client.get_stats()`. Requires admin access and `can_view_stats == True`.

### MegagroupStats (for supergroups)

Available statistics include:
- **Growth**: member count over time, join/leave rates
- **Messages**: message count over time, per-hour distribution
- **Viewers**: view count trends
- **Posters**: who posts most
- **Top members by**:
  - Messages sent
  - Messages forwarded from the group
- **Language distribution** of members
- **Message action breakdown** (text, photo, video, etc.)
- **Top hours** for activity

### Per-Message Stats

Via `client.get_stats(entity, message=msg_id)`:
- View count over time
- Forward count over time
- Public share count

---

## Summary: Data We Can Extract

### Currently Captured by Our Pipeline
(Based on existing `extract.py` and `transform/`)

- Message text, ID, date, sender
- Reply-to relationships
- Forwards count
- Hashtags, @mentions, URLs (via entities + regex)
- Pinned status
- Basic user info (ID, name, username)
- Channel info (title, ID)

### Available but NOT Yet Captured

| Category | Data | Value |
|----------|------|-------|
2| **Engagement** | `views`, `reactions` (per-emoji counts), `forwards` | Measure content impact |
3| **Rich Replies** | `quote_text`, `quote_entities`, cross-chat replies | Better thread reconstruction |
1| **Forum Topics** | Full ForumTopic objects with titles, status, creator | Topic-level structure |
4| **Media** | Media type classification, poll questions/results, link previews (title, description, site_name) | Content type analysis |
5| **Users** | `premium`, `bot`, `verified`, `status`, `bio`, join date | Richer user profiles |
| **Participants** | Admin roles, custom titles, ban status, join dates | Community structure |
| **Service Events** | Topic create/edit, member add/remove, title changes, pin events | Group lifecycle history |
| **Admin Log** | All moderation actions with before/after state | Governance analysis |
| **Statistics** | Growth, activity patterns, top posters, language distribution | Community analytics |
6| **Edits** | `edit_date` — whether and when messages were edited | Content evolution |
7| **Albums** | `grouped_id` — messages that form a media album | Grouped content |
| **Scheduled** | `from_scheduled` flag | Content planning |
| **Auto-delete** | `ttl_period` | Ephemeral content tracking |
8| **Link Previews** | Full WebPage: site_name, title, description, author, type | Rich URL metadata for free |
9| **Inline Bots** | `via_bot_id` — messages sent through bots | Bot usage patterns |
| **Channel Settings** | slowmode, noforwards, default_banned_rights, available_reactions | Community configuration |

---

## Limitations & Practical Notes

- **Participant cap**: `get_participants` returns max ~10,000 via Recent filter. Use `aggressive=True` for larger groups (slow).
- **Reactions full list**: Per-user reaction attribution (`GetMessageReactionsListRequest`) only works when `can_see_list == True` on the message's `MessageReactions`.
- **View counts**: `GetMessagesViewsRequest` has rate limits — can only be called sparingly per account.
- **Admin log / Statistics**: Require admin privileges. Stats additionally require `can_view_stats == True`.
- **User status privacy**: Most users hide precise last-seen. Expect `UserStatusRecently` / `UserStatusLastWeek` / `UserStatusLastMonth` / `UserStatusEmpty` far more than exact timestamps.
- **Min users**: When `user.min == True`, `access_hash` is unusable for API calls. Full data only available when the user has posted in a channel you access.
- **Forum topic messages**: Filtered via `reply_to_top_id` matching the topic ID. Use `GetRepliesRequest` or `iter_messages` scoped to the thread.
- **Entity caching**: Entity resolution is cached in the `.session` SQLite file; `get_input_entity()` is cheaper than `get_entity()` for repeated lookups.
- **Takeout sessions**: `client.takeout()` provides higher rate limits for bulk export — useful for full history extraction.
- **Bot accounts**: Cannot use `messages.getHistory` (iter_messages) — must use Bot API endpoints instead. This pipeline uses a **user account** via Telethon.
