# Auto generated from sioc.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-03-11T11:32:36
# Schema: sioc_min
#
# id: https://example.org/knowledge-graph-builder/sioc-min
# description: Minimal SIOC-aligned schema for Telegram-derived social data
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Datetime, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Namespaces
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SIOC = CurieNamespace('sioc', 'http://rdfs.org/sioc/ns#')
TG = CurieNamespace('tg', 'https://example.org/telegram/')
DEFAULT_ = TG


# Types

# Class references
class GraphDocumentId(extended_str):
    pass


class CommunityId(extended_str):
    pass


class ThreadId(extended_str):
    pass


class UserAccountId(extended_str):
    pass


class LinkId(extended_str):
    pass


class PostId(extended_str):
    pass


@dataclass(repr=False)
class GraphDocument(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TG["GraphDocument"]
    class_class_curie: ClassVar[str] = "tg:GraphDocument"
    class_name: ClassVar[str] = "GraphDocument"
    class_model_uri: ClassVar[URIRef] = TG.GraphDocument

    id: Union[str, GraphDocumentId] = None
    community: Optional[Union[dict, "Community"]] = None
    users: Optional[Union[dict[Union[str, UserAccountId], Union[dict, "UserAccount"]], list[Union[dict, "UserAccount"]]]] = empty_dict()
    links: Optional[Union[list[Union[str, LinkId]], dict[Union[str, LinkId], Union[dict, "Link"]]]] = empty_dict()
    posts: Optional[Union[dict[Union[str, PostId], Union[dict, "Post"]], list[Union[dict, "Post"]]]] = empty_dict()
    threads: Optional[Union[dict[Union[str, ThreadId], Union[dict, "Thread"]], list[Union[dict, "Thread"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GraphDocumentId):
            self.id = GraphDocumentId(self.id)

        if self.community is not None and not isinstance(self.community, Community):
            self.community = Community(**as_dict(self.community))

        self._normalize_inlined_as_dict(slot_name="users", slot_type=UserAccount, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="links", slot_type=Link, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="posts", slot_type=Post, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="threads", slot_type=Thread, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Community(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Community"]
    class_class_curie: ClassVar[str] = "sioc:Community"
    class_name: ClassVar[str] = "Community"
    class_model_uri: ClassVar[URIRef] = TG.Community

    id: Union[str, CommunityId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    member_count: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CommunityId):
            self.id = CommunityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.member_count is not None and not isinstance(self.member_count, int):
            self.member_count = int(self.member_count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Thread(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Thread"]
    class_class_curie: ClassVar[str] = "sioc:Thread"
    class_name: ClassVar[str] = "Thread"
    class_model_uri: ClassVar[URIRef] = TG.Thread

    id: Union[str, ThreadId] = None
    name: Optional[str] = None
    has_parent: Optional[Union[str, CommunityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThreadId):
            self.id = ThreadId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.has_parent is not None and not isinstance(self.has_parent, CommunityId):
            self.has_parent = CommunityId(self.has_parent)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UserAccount(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["UserAccount"]
    class_class_curie: ClassVar[str] = "sioc:UserAccount"
    class_name: ClassVar[str] = "UserAccount"
    class_model_uri: ClassVar[URIRef] = TG.UserAccount

    id: Union[str, UserAccountId] = None
    name: Optional[str] = None
    username: Optional[str] = None
    is_bot: Optional[Union[bool, Bool]] = None
    is_verified: Optional[Union[bool, Bool]] = None
    is_premium: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UserAccountId):
            self.id = UserAccountId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.username is not None and not isinstance(self.username, str):
            self.username = str(self.username)

        if self.is_bot is not None and not isinstance(self.is_bot, Bool):
            self.is_bot = Bool(self.is_bot)

        if self.is_verified is not None and not isinstance(self.is_verified, Bool):
            self.is_verified = Bool(self.is_verified)

        if self.is_premium is not None and not isinstance(self.is_premium, Bool):
            self.is_premium = Bool(self.is_premium)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Link(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["URL"]
    class_class_curie: ClassVar[str] = "schema:URL"
    class_name: ClassVar[str] = "Link"
    class_model_uri: ClassVar[URIRef] = TG.Link

    id: Union[str, LinkId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LinkId):
            self.id = LinkId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Post(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Post"]
    class_class_curie: ClassVar[str] = "sioc:Post"
    class_name: ClassVar[str] = "Post"
    class_model_uri: ClassVar[URIRef] = TG.Post

    id: Union[str, PostId] = None
    content: Optional[str] = None
    created: Optional[Union[str, XSDDateTime]] = None
    modified: Optional[Union[str, XSDDateTime]] = None
    has_creator: Optional[Union[str, UserAccountId]] = None
    has_container: Optional[Union[str, CommunityId]] = None
    has_thread: Optional[Union[str, ThreadId]] = None
    reply_to: Optional[Union[str, PostId]] = None
    links_to: Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]] = empty_list()
    forwards: Optional[int] = None
    pinned: Optional[Union[bool, Bool]] = None
    topics: Optional[Union[str, list[str]]] = empty_list()
    mentions: Optional[Union[str, list[str]]] = empty_list()
    entity_links: Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]] = empty_list()
    num_views: Optional[int] = None
    num_replies: Optional[int] = None
    reaction_count: Optional[int] = None
    reactions: Optional[Union[str, list[str]]] = empty_list()
    media_type: Optional[Union[str, "MediaType"]] = None
    forwarded_from: Optional[str] = None
    is_service: Optional[Union[bool, Bool]] = None
    service_action: Optional[Union[str, "ServiceActionType"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PostId):
            self.id = PostId(self.id)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        if self.modified is not None and not isinstance(self.modified, XSDDateTime):
            self.modified = XSDDateTime(self.modified)

        if self.has_creator is not None and not isinstance(self.has_creator, UserAccountId):
            self.has_creator = UserAccountId(self.has_creator)

        if self.has_container is not None and not isinstance(self.has_container, CommunityId):
            self.has_container = CommunityId(self.has_container)

        if self.has_thread is not None and not isinstance(self.has_thread, ThreadId):
            self.has_thread = ThreadId(self.has_thread)

        if self.reply_to is not None and not isinstance(self.reply_to, PostId):
            self.reply_to = PostId(self.reply_to)

        if not isinstance(self.links_to, list):
            self.links_to = [self.links_to] if self.links_to is not None else []
        self.links_to = [v if isinstance(v, LinkId) else LinkId(v) for v in self.links_to]

        if self.forwards is not None and not isinstance(self.forwards, int):
            self.forwards = int(self.forwards)

        if self.pinned is not None and not isinstance(self.pinned, Bool):
            self.pinned = Bool(self.pinned)

        if not isinstance(self.topics, list):
            self.topics = [self.topics] if self.topics is not None else []
        self.topics = [v if isinstance(v, str) else str(v) for v in self.topics]

        if not isinstance(self.mentions, list):
            self.mentions = [self.mentions] if self.mentions is not None else []
        self.mentions = [v if isinstance(v, str) else str(v) for v in self.mentions]

        if not isinstance(self.entity_links, list):
            self.entity_links = [self.entity_links] if self.entity_links is not None else []
        self.entity_links = [v if isinstance(v, LinkId) else LinkId(v) for v in self.entity_links]

        if self.num_views is not None and not isinstance(self.num_views, int):
            self.num_views = int(self.num_views)

        if self.num_replies is not None and not isinstance(self.num_replies, int):
            self.num_replies = int(self.num_replies)

        if self.reaction_count is not None and not isinstance(self.reaction_count, int):
            self.reaction_count = int(self.reaction_count)

        if not isinstance(self.reactions, list):
            self.reactions = [self.reactions] if self.reactions is not None else []
        self.reactions = [v if isinstance(v, str) else str(v) for v in self.reactions]

        if self.media_type is not None and not isinstance(self.media_type, MediaType):
            self.media_type = MediaType(self.media_type)

        if self.forwarded_from is not None and not isinstance(self.forwarded_from, str):
            self.forwarded_from = str(self.forwarded_from)

        if self.is_service is not None and not isinstance(self.is_service, Bool):
            self.is_service = Bool(self.is_service)

        if self.service_action is not None and not isinstance(self.service_action, ServiceActionType):
            self.service_action = ServiceActionType(self.service_action)

        super().__post_init__(**kwargs)


# Enumerations
class MediaType(EnumDefinitionImpl):

    photo = PermissibleValue(text="photo")
    video = PermissibleValue(text="video")
    document = PermissibleValue(text="document")
    webpage = PermissibleValue(text="webpage")
    audio = PermissibleValue(text="audio")
    sticker = PermissibleValue(text="sticker")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="MediaType",
    )

class ServiceActionType(EnumDefinitionImpl):

    join = PermissibleValue(text="join")
    leave = PermissibleValue(text="leave")
    pin = PermissibleValue(text="pin")
    title_change = PermissibleValue(text="title_change")
    photo_change = PermissibleValue(text="photo_change")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="ServiceActionType",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=DCTERMS.identifier, name="id", curie=DCTERMS.curie('identifier'),
                   model_uri=TG.id, domain=None, range=URIRef)

slots.name = Slot(uri=FOAF.name, name="name", curie=FOAF.curie('name'),
                   model_uri=TG.name, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=TG.description, domain=None, range=Optional[str])

slots.username = Slot(uri=FOAF.accountName, name="username", curie=FOAF.curie('accountName'),
                   model_uri=TG.username, domain=None, range=Optional[str])

slots.member_count = Slot(uri=TG.member_count, name="member_count", curie=TG.curie('member_count'),
                   model_uri=TG.member_count, domain=None, range=Optional[int])

slots.is_bot = Slot(uri=TG.is_bot, name="is_bot", curie=TG.curie('is_bot'),
                   model_uri=TG.is_bot, domain=None, range=Optional[Union[bool, Bool]])

slots.is_verified = Slot(uri=TG.is_verified, name="is_verified", curie=TG.curie('is_verified'),
                   model_uri=TG.is_verified, domain=None, range=Optional[Union[bool, Bool]])

slots.is_premium = Slot(uri=TG.is_premium, name="is_premium", curie=TG.curie('is_premium'),
                   model_uri=TG.is_premium, domain=None, range=Optional[Union[bool, Bool]])

slots.has_parent = Slot(uri=SIOC.has_parent, name="has_parent", curie=SIOC.curie('has_parent'),
                   model_uri=TG.has_parent, domain=None, range=Optional[Union[str, CommunityId]])

slots.content = Slot(uri=SIOC.content, name="content", curie=SIOC.curie('content'),
                   model_uri=TG.content, domain=None, range=Optional[str])

slots.created = Slot(uri=DCTERMS.created, name="created", curie=DCTERMS.curie('created'),
                   model_uri=TG.created, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.modified = Slot(uri=DCTERMS.modified, name="modified", curie=DCTERMS.curie('modified'),
                   model_uri=TG.modified, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.has_creator = Slot(uri=SIOC.has_creator, name="has_creator", curie=SIOC.curie('has_creator'),
                   model_uri=TG.has_creator, domain=None, range=Optional[Union[str, UserAccountId]])

slots.has_container = Slot(uri=SIOC.has_container, name="has_container", curie=SIOC.curie('has_container'),
                   model_uri=TG.has_container, domain=None, range=Optional[Union[str, CommunityId]])

slots.has_thread = Slot(uri=TG.has_thread, name="has_thread", curie=TG.curie('has_thread'),
                   model_uri=TG.has_thread, domain=None, range=Optional[Union[str, ThreadId]])

slots.reply_to = Slot(uri=SIOC.reply_of, name="reply_to", curie=SIOC.curie('reply_of'),
                   model_uri=TG.reply_to, domain=None, range=Optional[Union[str, PostId]])

slots.links_to = Slot(uri=SIOC.links_to, name="links_to", curie=SIOC.curie('links_to'),
                   model_uri=TG.links_to, domain=None, range=Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]])

slots.community = Slot(uri=TG.community, name="community", curie=TG.curie('community'),
                   model_uri=TG.community, domain=None, range=Optional[Union[dict, Community]])

slots.users = Slot(uri=TG.users, name="users", curie=TG.curie('users'),
                   model_uri=TG.users, domain=None, range=Optional[Union[dict[Union[str, UserAccountId], Union[dict, UserAccount]], list[Union[dict, UserAccount]]]])

slots.links = Slot(uri=TG.links, name="links", curie=TG.curie('links'),
                   model_uri=TG.links, domain=None, range=Optional[Union[list[Union[str, LinkId]], dict[Union[str, LinkId], Union[dict, Link]]]])

slots.posts = Slot(uri=TG.posts, name="posts", curie=TG.curie('posts'),
                   model_uri=TG.posts, domain=None, range=Optional[Union[dict[Union[str, PostId], Union[dict, Post]], list[Union[dict, Post]]]])

slots.threads = Slot(uri=TG.threads, name="threads", curie=TG.curie('threads'),
                   model_uri=TG.threads, domain=None, range=Optional[Union[dict[Union[str, ThreadId], Union[dict, Thread]], list[Union[dict, Thread]]]])

slots.forwards = Slot(uri=TG.forwards, name="forwards", curie=TG.curie('forwards'),
                   model_uri=TG.forwards, domain=None, range=Optional[int])

slots.pinned = Slot(uri=TG.pinned, name="pinned", curie=TG.curie('pinned'),
                   model_uri=TG.pinned, domain=None, range=Optional[Union[bool, Bool]])

slots.topics = Slot(uri=SIOC.topic, name="topics", curie=SIOC.curie('topic'),
                   model_uri=TG.topics, domain=None, range=Optional[Union[str, list[str]]])

slots.mentions = Slot(uri=TG.mentions, name="mentions", curie=TG.curie('mentions'),
                   model_uri=TG.mentions, domain=None, range=Optional[Union[str, list[str]]])

slots.entity_links = Slot(uri=SIOC.links_to, name="entity_links", curie=SIOC.curie('links_to'),
                   model_uri=TG.entity_links, domain=None, range=Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]])

slots.num_views = Slot(uri=SIOC.num_views, name="num_views", curie=SIOC.curie('num_views'),
                   model_uri=TG.num_views, domain=None, range=Optional[int])

slots.num_replies = Slot(uri=SIOC.num_replies, name="num_replies", curie=SIOC.curie('num_replies'),
                   model_uri=TG.num_replies, domain=None, range=Optional[int])

slots.reaction_count = Slot(uri=TG.reaction_count, name="reaction_count", curie=TG.curie('reaction_count'),
                   model_uri=TG.reaction_count, domain=None, range=Optional[int])

slots.reactions = Slot(uri=TG.reactions, name="reactions", curie=TG.curie('reactions'),
                   model_uri=TG.reactions, domain=None, range=Optional[Union[str, list[str]]])

slots.media_type = Slot(uri=TG.media_type, name="media_type", curie=TG.curie('media_type'),
                   model_uri=TG.media_type, domain=None, range=Optional[Union[str, "MediaType"]])

slots.forwarded_from = Slot(uri=TG.forwarded_from, name="forwarded_from", curie=TG.curie('forwarded_from'),
                   model_uri=TG.forwarded_from, domain=None, range=Optional[str])

slots.is_service = Slot(uri=TG.is_service, name="is_service", curie=TG.curie('is_service'),
                   model_uri=TG.is_service, domain=None, range=Optional[Union[bool, Bool]])

slots.service_action = Slot(uri=TG.service_action, name="service_action", curie=TG.curie('service_action'),
                   model_uri=TG.service_action, domain=None, range=Optional[Union[str, "ServiceActionType"]])

