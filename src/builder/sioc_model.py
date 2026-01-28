# Auto generated from sioc_min.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-01-27T17:26:06
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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
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
    community: Optional[Union[str, CommunityId]] = None
    users: Optional[Union[list[Union[str, UserAccountId]], dict[Union[str, UserAccountId], Union[dict, "UserAccount"]]]] = empty_dict()
    links: Optional[Union[list[Union[str, LinkId]], dict[Union[str, LinkId], Union[dict, "Link"]]]] = empty_dict()
    posts: Optional[Union[dict[Union[str, PostId], Union[dict, "Post"]], list[Union[dict, "Post"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GraphDocumentId):
            self.id = GraphDocumentId(self.id)

        if self.community is not None and not isinstance(self.community, CommunityId):
            self.community = CommunityId(self.community)

        self._normalize_inlined_as_dict(slot_name="users", slot_type=UserAccount, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="links", slot_type=Link, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="posts", slot_type=Post, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Community(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Community"]
    class_class_curie: ClassVar[str] = "sioc:Community"
    class_name: ClassVar[str] = "Community"
    class_model_uri: ClassVar[URIRef] = TG.Community

    id: Union[str, CommunityId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CommunityId):
            self.id = CommunityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UserAccount(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["UserAccount"]
    class_class_curie: ClassVar[str] = "sioc:UserAccount"
    class_name: ClassVar[str] = "UserAccount"
    class_model_uri: ClassVar[URIRef] = TG.UserAccount

    id: Union[str, UserAccountId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UserAccountId):
            self.id = UserAccountId(self.id)

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
    has_creator: Optional[Union[str, UserAccountId]] = None
    has_container: Optional[Union[str, CommunityId]] = None
    reply_to: Optional[Union[str, PostId]] = None
    links_to: Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]] = empty_list()
    forwards: Optional[int] = None
    pinned: Optional[Union[bool, Bool]] = None
    topics: Optional[Union[str, list[str]]] = empty_list()
    mentions: Optional[Union[str, list[str]]] = empty_list()
    entity_links: Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PostId):
            self.id = PostId(self.id)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        if self.has_creator is not None and not isinstance(self.has_creator, UserAccountId):
            self.has_creator = UserAccountId(self.has_creator)

        if self.has_container is not None and not isinstance(self.has_container, CommunityId):
            self.has_container = CommunityId(self.has_container)

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

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DCTERMS.identifier, name="id", curie=DCTERMS.curie('identifier'),
                   model_uri=TG.id, domain=None, range=URIRef)

slots.content = Slot(uri=SIOC.content, name="content", curie=SIOC.curie('content'),
                   model_uri=TG.content, domain=None, range=Optional[str])

slots.created = Slot(uri=DCTERMS.created, name="created", curie=DCTERMS.curie('created'),
                   model_uri=TG.created, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.has_creator = Slot(uri=SIOC.has_creator, name="has_creator", curie=SIOC.curie('has_creator'),
                   model_uri=TG.has_creator, domain=None, range=Optional[Union[str, UserAccountId]])

slots.has_container = Slot(uri=SIOC.has_container, name="has_container", curie=SIOC.curie('has_container'),
                   model_uri=TG.has_container, domain=None, range=Optional[Union[str, CommunityId]])

slots.reply_to = Slot(uri=SIOC.reply_of, name="reply_to", curie=SIOC.curie('reply_of'),
                   model_uri=TG.reply_to, domain=None, range=Optional[Union[str, PostId]])

slots.links_to = Slot(uri=SIOC.links_to, name="links_to", curie=SIOC.curie('links_to'),
                   model_uri=TG.links_to, domain=None, range=Optional[Union[Union[str, LinkId], list[Union[str, LinkId]]]])

slots.community = Slot(uri=TG.community, name="community", curie=TG.curie('community'),
                   model_uri=TG.community, domain=None, range=Optional[Union[str, CommunityId]])

slots.users = Slot(uri=TG.users, name="users", curie=TG.curie('users'),
                   model_uri=TG.users, domain=None, range=Optional[Union[list[Union[str, UserAccountId]], dict[Union[str, UserAccountId], Union[dict, UserAccount]]]])

slots.links = Slot(uri=TG.links, name="links", curie=TG.curie('links'),
                   model_uri=TG.links, domain=None, range=Optional[Union[list[Union[str, LinkId]], dict[Union[str, LinkId], Union[dict, Link]]]])

slots.posts = Slot(uri=TG.posts, name="posts", curie=TG.curie('posts'),
                   model_uri=TG.posts, domain=None, range=Optional[Union[dict[Union[str, PostId], Union[dict, Post]], list[Union[dict, Post]]]])

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

