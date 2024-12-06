"""
MIT License

Copyright (c) 2024-PRESENT Maki (https://maki.gg)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import (
    Any,
    Awaitable,
    Callable,
    Final,
    List,
    Literal,
    NotRequired,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

from discord_webhooks.enums import (
    DiscordGuildDefaultMessageNotificationsLevelEnumLiterals,
    DiscordGuildExplicitContentFilterLevelEnumLiterals,
    DiscordGuildMFALevelEnumLiterals,
    DiscordGuildNSFWLevelEnumLiterals,
    DiscordGuildPremiumTierEnumLiterals,
    DiscordGuildVerificationLevelEnumLiterals,
    DiscordStickerFormatTypeEnumLiterals,
    DiscordStickerTypeEnumLiterals,
    EntitlementTypeEnumLiterals,
    IntegrationTypeEnum,
    WebhookEventTypeEnum,
    WebhookTypeEnum,
)


__all__: Final[Tuple[str, ...]] = (
    "JSONResponseError",
    "WebhookPayload",
    "WebhookHandler",
    "WebhookPayloadEventApplicationAuthorized",
    "WebhookPayloadEventEntitlementCreate",
    "WebhookPayloadEventQuestUserEnrollment",
)


class JSONResponseError(TypedDict):
    error: str


AppInstallScopes = Union[
    Literal["applications.commands"],
    Literal["bot"],
]


class DiscordUserAvatarDecorationData(TypedDict):
    asset: str
    sku_id: str


class DiscordUser(TypedDict):
    id: str
    username: str
    discriminator: Literal['0']
    global_name: Optional[str]
    avatar: Optional[str]
    bot: NotRequired[bool]
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    banner: NotRequired[Optional[str]]
    accent_color: NotRequired[Optional[int]]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[Optional[str]]
    flags: NotRequired[int]
    premium_type: NotRequired[int]
    public_flags: NotRequired[int]
    avatar_decoration_data: NotRequired[Optional[DiscordUserAvatarDecorationData]]



# I really wish I was joking when I mean these are literally documented as an optional type null
# https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
class DiscordRoleTags(TypedDict):
    bot_id: NotRequired[str]
    intergration_id: NotRequired[str]
    premium_subscriber: NotRequired[Literal[None]]
    subscription_listing_id: NotRequired[str]
    available_for_purchase: NotRequired[Literal[None]]
    guild_connections: NotRequired[Literal[None]]


class DiscordRole(TypedDict):
    id: str
    name: str
    color: int
    hoist: bool
    icon: NotRequired[Optional[str]]
    unicode_emoji: NotRequired[Optional[str]]
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: NotRequired[DiscordRoleTags]
    flags: int


# Why yes, that *is* a critial OPTIONAL field.
# https://discord.com/developers/docs/resources/emoji#emoji-object
class DiscordEmoji(TypedDict):
    id: Optional[str]
    name: Optional[str]
    roles: NotRequired[List[str]]
    user: DiscordUser
    require_colons: NotRequired[bool]
    managed: NotRequired[bool]
    animated: NotRequired[bool]
    available: NotRequired[bool]


class DiscordSticker(TypedDict):
    id: str
    pack_id: NotRequired[str]
    name: str
    description: Optional[str]
    tags: NotRequired[str]
    type: DiscordStickerTypeEnumLiterals
    format_type: DiscordStickerFormatTypeEnumLiterals
    available: NotRequired[bool]
    guild_id: NotRequired[bool]
    user: NotRequired[DiscordUser]
    soft_value: int


class DiscordWelcomeScreenChannel(TypedDict):
    channel_id: str
    description: str
    emoji_id: Optional[str]
    emoji_name: Optional[str]


class DiscordWelcomeScreen(TypedDict):
    description: str
    welcome_channels: list[DiscordWelcomeScreenChannel]


class DiscordGuild(TypedDict):
    id: str
    name: str
    icon: str
    splash: Optional[str]
    discovery_splash: Optional[str]
    owner: NotRequired[bool]
    owner_id: str
    permissions: NotRequired[str]
    afk_channel_id: Optional[str]
    afk_timeout: int
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[Optional[str]]
    verification_level: DiscordGuildVerificationLevelEnumLiterals
    default_message_notifications: DiscordGuildDefaultMessageNotificationsLevelEnumLiterals
    explicit_content_filter: DiscordGuildExplicitContentFilterLevelEnumLiterals
    roles: list[DiscordRole]
    emojis: list[DiscordEmoji]
    features: list[str]
    mfa_level: DiscordGuildMFALevelEnumLiterals
    application_id: Optional[str]
    system_channel_id: Optional[str]
    system_channel_flags: int
    rules_channel_id: Optional[str]
    max_presences: NotRequired[Optional[str]]
    max_members: NotRequired[int]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    premium_tier: DiscordGuildPremiumTierEnumLiterals
    premium_subscription_count: NotRequired[int]
    preferred_locale: str
    public_updates_channel_id: Optional[str]
    max_video_channel_users: NotRequired[int]
    max_stage_video_channel_users: NotRequired[int]
    approximate_member_count: NotRequired[int]
    approximate_presence_count: NotRequired[int]
    welcome_screen: DiscordWelcomeScreen
    nsfw_level: DiscordGuildNSFWLevelEnumLiterals
    stickers: NotRequired[List[DiscordSticker]]
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: Optional[str]



class WebhookPayloadEventBase(TypedDict):
    timestamp: str


class WebhookPayloadEventApplicationAuthorizedData(TypedDict):
    integration_type: Literal[IntegrationTypeEnum.GUILD_INSTALL]
    user: DiscordUser
    scopes: list[AppInstallScopes]
    guild: DiscordGuild


class WebhookPayloadEventEntitlementCreateData(TypedDict):
    id: str
    sku_id: str
    application_id: str
    user_id: Optional[str]
    promotion_id: Optional[str]
    type: EntitlementTypeEnumLiterals
    deleted: bool
    gift_code_flags: int
    consumed: Optional[bool]
    starts_at: Optional[str]
    ends_at: Optional[str]
    guild_id: Optional[str]
    subscriptioon_id: Optional[str]


class WebhookPayloadEventApplicationAuthorized(WebhookPayloadEventBase):
    type: Literal[WebhookEventTypeEnum.APPLICATION_AUTHORIZED]
    data: WebhookPayloadEventApplicationAuthorizedData


class WebhookPayloadEventEntitlementCreate(WebhookPayloadEventBase):
    type: Literal[WebhookEventTypeEnum.ENTITLEMENT_CREATE]
    data: WebhookPayloadEventEntitlementCreateData


class WebhookPayloadEventQuestUserEnrollment(WebhookPayloadEventBase):
    type: Literal[WebhookEventTypeEnum.QUEST_USER_ENROLLMENT]
    data: dict[str, Any]  # Undocumented.


WebhookPayloadEvent = Union[
    WebhookPayloadEventApplicationAuthorized,
    WebhookPayloadEventEntitlementCreate,
    WebhookPayloadEventQuestUserEnrollment,
]



class WebhookPayload_Ping(TypedDict):
    version: Literal[1]
    application_id: str
    type: Literal[WebhookTypeEnum.PING]


class WebhookPayload_Event(TypedDict):
    version: Literal[1]
    application_id: str
    type: Literal[WebhookTypeEnum.EVENT]
    event: WebhookPayloadEvent


WebhookPayload = Union[
    WebhookPayload_Ping,
    WebhookPayload_Event,
]


WebhookHandler = Union[
    Callable[[WebhookPayloadEventApplicationAuthorized], Awaitable[None]],
    Callable[[WebhookPayloadEventEntitlementCreate], Awaitable[None]],
    Callable[[WebhookPayloadEventQuestUserEnrollment], Awaitable[None]],
]
