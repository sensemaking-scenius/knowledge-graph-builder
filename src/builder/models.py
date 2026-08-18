# Auto generated from sioc.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-08-18T03:43:32
# Schema: sioc
#
# id: https://example.org/knowledge-graph-builder/sioc
# description: SIOC-aligned schema for Telegram-derived social knowledge graphs
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

from linkml_runtime.linkml_model.types import Boolean, Datetime, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Namespaces
DC = CurieNamespace('dc', 'http://purl.org/dc/elements/1.1/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SIOC = CurieNamespace('sioc', 'http://rdfs.org/sioc/ns#')
SIOC_TYPES = CurieNamespace('sioc_types', 'http://rdfs.org/sioc/types#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TG = CurieNamespace('tg', 'https://example.org/telegram/')
DEFAULT_ = TG


# Types

# Class references
class GraphDocumentId(extended_str):
    pass


class CommunityId(extended_str):
    pass


class SiteId(extended_str):
    pass


class ForumId(extended_str):
    pass


class ThreadId(extended_str):
    pass


class UserId(extended_str):
    pass


class PersonId(extended_str):
    pass


class PostId(extended_str):
    pass


class PollId(extended_str):
    pass


class AttachmentId(extended_str):
    pass


class LinkedDocumentId(extended_str):
    pass


class ConceptId(extended_str):
    pass


class AnnotationId(extended_str):
    pass


class AnnotationSessionId(extended_str):
    pass


class ReactionId(extended_str):
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
    site: Optional[Union[dict, "Site"]] = None
    forums: Optional[Union[dict[Union[str, ForumId], Union[dict, "Forum"]], list[Union[dict, "Forum"]]]] = empty_dict()
    users: Optional[Union[dict[Union[str, UserId], Union[dict, "User"]], list[Union[dict, "User"]]]] = empty_dict()
    persons: Optional[Union[dict[Union[str, PersonId], Union[dict, "Person"]], list[Union[dict, "Person"]]]] = empty_dict()
    posts: Optional[Union[dict[Union[str, PostId], Union[dict, "Post"]], list[Union[dict, "Post"]]]] = empty_dict()
    threads: Optional[Union[dict[Union[str, ThreadId], Union[dict, "Thread"]], list[Union[dict, "Thread"]]]] = empty_dict()
    concepts: Optional[Union[dict[Union[str, ConceptId], Union[dict, "Concept"]], list[Union[dict, "Concept"]]]] = empty_dict()
    attachments: Optional[Union[dict[Union[str, AttachmentId], Union[dict, "Attachment"]], list[Union[dict, "Attachment"]]]] = empty_dict()
    linked_documents: Optional[Union[dict[Union[str, LinkedDocumentId], Union[dict, "LinkedDocument"]], list[Union[dict, "LinkedDocument"]]]] = empty_dict()
    polls: Optional[Union[dict[Union[str, PollId], Union[dict, "Poll"]], list[Union[dict, "Poll"]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationId], Union[dict, "Annotation"]], list[Union[dict, "Annotation"]]]] = empty_dict()
    annotation_sessions: Optional[Union[dict[Union[str, AnnotationSessionId], Union[dict, "AnnotationSession"]], list[Union[dict, "AnnotationSession"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GraphDocumentId):
            self.id = GraphDocumentId(self.id)

        if self.community is not None and not isinstance(self.community, Community):
            self.community = Community(**as_dict(self.community))

        if self.site is not None and not isinstance(self.site, Site):
            self.site = Site(**as_dict(self.site))

        self._normalize_inlined_as_dict(slot_name="forums", slot_type=Forum, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="users", slot_type=User, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="posts", slot_type=Post, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="threads", slot_type=Thread, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="concepts", slot_type=Concept, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="attachments", slot_type=Attachment, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="linked_documents", slot_type=LinkedDocument, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="polls", slot_type=Poll, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotation_sessions", slot_type=AnnotationSession, key_name="id", keyed=True)

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
    has_part: Optional[Union[str, SiteId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CommunityId):
            self.id = CommunityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.has_part is not None and not isinstance(self.has_part, SiteId):
            self.has_part = SiteId(self.has_part)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Site(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Site"]
    class_class_curie: ClassVar[str] = "sioc:Site"
    class_name: ClassVar[str] = "Site"
    class_model_uri: ClassVar[URIRef] = TG.Site

    id: Union[str, SiteId] = None
    name: Optional[str] = None
    host_of: Optional[Union[Union[str, ForumId], list[Union[str, ForumId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SiteId):
            self.id = SiteId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.host_of, list):
            self.host_of = [self.host_of] if self.host_of is not None else []
        self.host_of = [v if isinstance(v, ForumId) else ForumId(v) for v in self.host_of]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Forum(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["Forum"]
    class_class_curie: ClassVar[str] = "sioc:Forum"
    class_name: ClassVar[str] = "Forum"
    class_model_uri: ClassVar[URIRef] = TG.Forum

    id: Union[str, ForumId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    has_host: Optional[Union[str, SiteId]] = None
    has_parent_forum: Optional[Union[str, ForumId]] = None
    parent_of: Optional[Union[Union[str, ForumId], list[Union[str, ForumId]]]] = empty_list()
    container_of: Optional[Union[Union[str, PostId], list[Union[str, PostId]]]] = empty_list()
    closed: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ForumId):
            self.id = ForumId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.has_host is not None and not isinstance(self.has_host, SiteId):
            self.has_host = SiteId(self.has_host)

        if self.has_parent_forum is not None and not isinstance(self.has_parent_forum, ForumId):
            self.has_parent_forum = ForumId(self.has_parent_forum)

        if not isinstance(self.parent_of, list):
            self.parent_of = [self.parent_of] if self.parent_of is not None else []
        self.parent_of = [v if isinstance(v, ForumId) else ForumId(v) for v in self.parent_of]

        if not isinstance(self.container_of, list):
            self.container_of = [self.container_of] if self.container_of is not None else []
        self.container_of = [v if isinstance(v, PostId) else PostId(v) for v in self.container_of]

        if self.closed is not None and not isinstance(self.closed, Bool):
            self.closed = Bool(self.closed)

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
    has_parent_forum: Optional[Union[str, ForumId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThreadId):
            self.id = ThreadId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.has_parent_forum is not None and not isinstance(self.has_parent_forum, ForumId):
            self.has_parent_forum = ForumId(self.has_parent_forum)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class User(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC["User"]
    class_class_curie: ClassVar[str] = "sioc:User"
    class_name: ClassVar[str] = "User"
    class_model_uri: ClassVar[URIRef] = TG.User

    id: Union[str, UserId] = None
    sioc_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: Optional[Union[bool, Bool]] = None
    account_of: Optional[Union[str, PersonId]] = None
    avatar: Optional[str] = None
    user_description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UserId):
            self.id = UserId(self.id)

        if self.sioc_name is not None and not isinstance(self.sioc_name, str):
            self.sioc_name = str(self.sioc_name)

        if self.username is not None and not isinstance(self.username, str):
            self.username = str(self.username)

        if self.is_bot is not None and not isinstance(self.is_bot, Bool):
            self.is_bot = Bool(self.is_bot)

        if self.account_of is not None and not isinstance(self.account_of, PersonId):
            self.account_of = PersonId(self.account_of)

        if self.avatar is not None and not isinstance(self.avatar, str):
            self.avatar = str(self.avatar)

        if self.user_description is not None and not isinstance(self.user_description, str):
            self.user_description = str(self.user_description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Person"]
    class_class_curie: ClassVar[str] = "foaf:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = TG.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    holds_account: Optional[Union[Union[str, UserId], list[Union[str, UserId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.holds_account, list):
            self.holds_account = [self.holds_account] if self.holds_account is not None else []
        self.holds_account = [v if isinstance(v, UserId) else UserId(v) for v in self.holds_account]

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
    has_creator: Optional[Union[str, UserId]] = None
    has_container: Optional[Union[str, ForumId]] = None
    reply_of: Optional[Union[str, PostId]] = None
    has_reply: Optional[Union[Union[str, PostId], list[Union[str, PostId]]]] = empty_list()
    sibling: Optional[Union[str, PostId]] = None
    links_to: Optional[Union[Union[str, LinkedDocumentId], list[Union[str, LinkedDocumentId]]]] = empty_list()
    attachment: Optional[Union[Union[str, AttachmentId], list[Union[str, AttachmentId]]]] = empty_list()
    has_poll: Optional[Union[str, PollId]] = None
    topics: Optional[Union[Union[str, ConceptId], list[Union[str, ConceptId]]]] = empty_list()
    forwards: Optional[int] = None
    pinned: Optional[Union[bool, Bool]] = None
    quote_text: Optional[str] = None
    grouped_id: Optional[str] = None
    via_bot: Optional[Union[str, UserId]] = None

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

        if self.has_creator is not None and not isinstance(self.has_creator, UserId):
            self.has_creator = UserId(self.has_creator)

        if self.has_container is not None and not isinstance(self.has_container, ForumId):
            self.has_container = ForumId(self.has_container)

        if self.reply_of is not None and not isinstance(self.reply_of, PostId):
            self.reply_of = PostId(self.reply_of)

        if not isinstance(self.has_reply, list):
            self.has_reply = [self.has_reply] if self.has_reply is not None else []
        self.has_reply = [v if isinstance(v, PostId) else PostId(v) for v in self.has_reply]

        if self.sibling is not None and not isinstance(self.sibling, PostId):
            self.sibling = PostId(self.sibling)

        if not isinstance(self.links_to, list):
            self.links_to = [self.links_to] if self.links_to is not None else []
        self.links_to = [v if isinstance(v, LinkedDocumentId) else LinkedDocumentId(v) for v in self.links_to]

        if not isinstance(self.attachment, list):
            self.attachment = [self.attachment] if self.attachment is not None else []
        self.attachment = [v if isinstance(v, AttachmentId) else AttachmentId(v) for v in self.attachment]

        if self.has_poll is not None and not isinstance(self.has_poll, PollId):
            self.has_poll = PollId(self.has_poll)

        if not isinstance(self.topics, list):
            self.topics = [self.topics] if self.topics is not None else []
        self.topics = [v if isinstance(v, ConceptId) else ConceptId(v) for v in self.topics]

        if self.forwards is not None and not isinstance(self.forwards, int):
            self.forwards = int(self.forwards)

        if self.pinned is not None and not isinstance(self.pinned, Bool):
            self.pinned = Bool(self.pinned)

        if self.quote_text is not None and not isinstance(self.quote_text, str):
            self.quote_text = str(self.quote_text)

        if self.grouped_id is not None and not isinstance(self.grouped_id, str):
            self.grouped_id = str(self.grouped_id)

        if self.via_bot is not None and not isinstance(self.via_bot, UserId):
            self.via_bot = UserId(self.via_bot)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Poll(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIOC_TYPES["Poll"]
    class_class_curie: ClassVar[str] = "sioc_types:Poll"
    class_name: ClassVar[str] = "Poll"
    class_model_uri: ClassVar[URIRef] = TG.Poll

    id: Union[str, PollId] = None
    question: Optional[str] = None
    answers: Optional[Union[str, list[str]]] = empty_list()
    total_voters: Optional[int] = None
    quiz: Optional[Union[bool, Bool]] = None
    poll_closed: Optional[Union[bool, Bool]] = None
    public_voters: Optional[Union[bool, Bool]] = None
    multiple_choice: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PollId):
            self.id = PollId(self.id)

        if self.question is not None and not isinstance(self.question, str):
            self.question = str(self.question)

        if not isinstance(self.answers, list):
            self.answers = [self.answers] if self.answers is not None else []
        self.answers = [v if isinstance(v, str) else str(v) for v in self.answers]

        if self.total_voters is not None and not isinstance(self.total_voters, int):
            self.total_voters = int(self.total_voters)

        if self.quiz is not None and not isinstance(self.quiz, Bool):
            self.quiz = Bool(self.quiz)

        if self.poll_closed is not None and not isinstance(self.poll_closed, Bool):
            self.poll_closed = Bool(self.poll_closed)

        if self.public_voters is not None and not isinstance(self.public_voters, Bool):
            self.public_voters = Bool(self.public_voters)

        if self.multiple_choice is not None and not isinstance(self.multiple_choice, Bool):
            self.multiple_choice = Bool(self.multiple_choice)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Attachment(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Document"]
    class_class_curie: ClassVar[str] = "foaf:Document"
    class_name: ClassVar[str] = "Attachment"
    class_model_uri: ClassVar[URIRef] = TG.Attachment

    id: Union[str, AttachmentId] = None
    format: Optional[str] = None
    extent: Optional[int] = None
    media_type: Optional[Union[str, "MediaType"]] = None
    duration: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AttachmentId):
            self.id = AttachmentId(self.id)

        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        if self.extent is not None and not isinstance(self.extent, int):
            self.extent = int(self.extent)

        if self.media_type is not None and not isinstance(self.media_type, MediaType):
            self.media_type = MediaType(self.media_type)

        if self.duration is not None and not isinstance(self.duration, int):
            self.duration = int(self.duration)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LinkedDocument(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Document"]
    class_class_curie: ClassVar[str] = "foaf:Document"
    class_name: ClassVar[str] = "LinkedDocument"
    class_model_uri: ClassVar[URIRef] = TG.LinkedDocument

    id: Union[str, LinkedDocumentId] = None
    title: Optional[str] = None
    doc_description: Optional[str] = None
    doc_creator: Optional[str] = None
    site_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LinkedDocumentId):
            self.id = LinkedDocumentId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.doc_description is not None and not isinstance(self.doc_description, str):
            self.doc_description = str(self.doc_description)

        if self.doc_creator is not None and not isinstance(self.doc_creator, str):
            self.doc_creator = str(self.doc_creator)

        if self.site_name is not None and not isinstance(self.site_name, str):
            self.site_name = str(self.site_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Concept(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = TG.Concept

    id: Union[str, ConceptId] = None
    pref_label: Optional[str] = None
    concept_type: Optional[Union[str, "EntityType"]] = None
    concept_description: Optional[str] = None
    confidence: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConceptId):
            self.id = ConceptId(self.id)

        if self.pref_label is not None and not isinstance(self.pref_label, str):
            self.pref_label = str(self.pref_label)

        if self.concept_type is not None and not isinstance(self.concept_type, EntityType):
            self.concept_type = EntityType(self.concept_type)

        if self.concept_description is not None and not isinstance(self.concept_description, str):
            self.concept_description = str(self.concept_description)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Annotation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TG["Annotation"]
    class_class_curie: ClassVar[str] = "tg:Annotation"
    class_name: ClassVar[str] = "Annotation"
    class_model_uri: ClassVar[URIRef] = TG.Annotation

    id: Union[str, AnnotationId] = None
    annotation_body: Optional[str] = None
    annotation_target: Optional[Union[str, PostId]] = None
    entity_type: Optional[Union[str, "EntityType"]] = None
    confidence: Optional[float] = None
    discovered_by: Optional[Union[str, UserId]] = None
    session_ref: Optional[Union[str, AnnotationSessionId]] = None
    created: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnnotationId):
            self.id = AnnotationId(self.id)

        if self.annotation_body is not None and not isinstance(self.annotation_body, str):
            self.annotation_body = str(self.annotation_body)

        if self.annotation_target is not None and not isinstance(self.annotation_target, PostId):
            self.annotation_target = PostId(self.annotation_target)

        if self.entity_type is not None and not isinstance(self.entity_type, EntityType):
            self.entity_type = EntityType(self.entity_type)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        if self.discovered_by is not None and not isinstance(self.discovered_by, UserId):
            self.discovered_by = UserId(self.discovered_by)

        if self.session_ref is not None and not isinstance(self.session_ref, AnnotationSessionId):
            self.session_ref = AnnotationSessionId(self.session_ref)

        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnnotationSession(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TG["AnnotationSession"]
    class_class_curie: ClassVar[str] = "tg:AnnotationSession"
    class_name: ClassVar[str] = "AnnotationSession"
    class_model_uri: ClassVar[URIRef] = TG.AnnotationSession

    id: Union[str, AnnotationSessionId] = None
    harmonica_session_id: Optional[str] = None
    theme: Optional[Union[str, "SessionTheme"]] = None
    messages_annotated: Optional[Union[Union[str, PostId], list[Union[str, PostId]]]] = empty_list()
    participant_count: Optional[int] = None
    created: Optional[Union[str, XSDDateTime]] = None
    session_status: Optional[Union[str, "SessionStatus"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnnotationSessionId):
            self.id = AnnotationSessionId(self.id)

        if self.harmonica_session_id is not None and not isinstance(self.harmonica_session_id, str):
            self.harmonica_session_id = str(self.harmonica_session_id)

        if self.theme is not None and not isinstance(self.theme, SessionTheme):
            self.theme = SessionTheme(self.theme)

        if not isinstance(self.messages_annotated, list):
            self.messages_annotated = [self.messages_annotated] if self.messages_annotated is not None else []
        self.messages_annotated = [v if isinstance(v, PostId) else PostId(v) for v in self.messages_annotated]

        if self.participant_count is not None and not isinstance(self.participant_count, int):
            self.participant_count = int(self.participant_count)

        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        if self.session_status is not None and not isinstance(self.session_status, SessionStatus):
            self.session_status = SessionStatus(self.session_status)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reaction(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TG["Reaction"]
    class_class_curie: ClassVar[str] = "tg:Reaction"
    class_name: ClassVar[str] = "Reaction"
    class_model_uri: ClassVar[URIRef] = TG.Reaction

    id: Union[str, ReactionId] = None
    reactor: Optional[Union[str, UserId]] = None
    emoji: Optional[str] = None
    target: Optional[Union[str, PostId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReactionId):
            self.id = ReactionId(self.id)

        if self.reactor is not None and not isinstance(self.reactor, UserId):
            self.reactor = UserId(self.reactor)

        if self.emoji is not None and not isinstance(self.emoji, str):
            self.emoji = str(self.emoji)

        if self.target is not None and not isinstance(self.target, PostId):
            self.target = PostId(self.target)

        super().__post_init__(**kwargs)


# Enumerations
class MediaType(EnumDefinitionImpl):

    photo = PermissibleValue(text="photo")
    video = PermissibleValue(text="video")
    document = PermissibleValue(text="document")
    audio = PermissibleValue(text="audio")
    voice = PermissibleValue(text="voice")
    sticker = PermissibleValue(text="sticker")
    animation = PermissibleValue(text="animation")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="MediaType",
    )

class EntityType(EnumDefinitionImpl):

    person = PermissibleValue(text="person")
    tool = PermissibleValue(text="tool")
    project = PermissibleValue(text="project")
    concept = PermissibleValue(text="concept")
    organization = PermissibleValue(text="organization")

    _defn = EnumDefinition(
        name="EntityType",
    )

class SessionTheme(EnumDefinitionImpl):

    free_hunt = PermissibleValue(text="free_hunt")
    whos_who = PermissibleValue(text="whos_who")
    tool_chest = PermissibleValue(text="tool_chest")
    project_radar = PermissibleValue(text="project_radar")
    idea_map = PermissibleValue(text="idea_map")
    link_dive = PermissibleValue(text="link_dive")
    relationships = PermissibleValue(text="relationships")
    verification = PermissibleValue(text="verification")

    _defn = EnumDefinition(
        name="SessionTheme",
    )

class SessionStatus(EnumDefinitionImpl):

    active = PermissibleValue(text="active")
    synthesized = PermissibleValue(text="synthesized")
    imported = PermissibleValue(text="imported")

    _defn = EnumDefinition(
        name="SessionStatus",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SIOC.id, name="id", curie=SIOC.curie('id'),
                   model_uri=TG.id, domain=None, range=URIRef)

slots.name = Slot(uri=FOAF.name, name="name", curie=FOAF.curie('name'),
                   model_uri=TG.name, domain=None, range=Optional[str])

slots.sioc_name = Slot(uri=SIOC.name, name="sioc_name", curie=SIOC.curie('name'),
                   model_uri=TG.sioc_name, domain=None, range=Optional[str])

slots.username = Slot(uri=FOAF.accountName, name="username", curie=FOAF.curie('accountName'),
                   model_uri=TG.username, domain=None, range=Optional[str])

slots.pref_label = Slot(uri=SKOS.prefLabel, name="pref_label", curie=SKOS.curie('prefLabel'),
                   model_uri=TG.pref_label, domain=None, range=Optional[str])

slots.title = Slot(uri=DC.title, name="title", curie=DC.curie('title'),
                   model_uri=TG.title, domain=None, range=Optional[str])

slots.question = Slot(uri=TG.question, name="question", curie=TG.curie('question'),
                   model_uri=TG.question, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=TG.description, domain=None, range=Optional[str])

slots.doc_description = Slot(uri=DCTERMS.description, name="doc_description", curie=DCTERMS.curie('description'),
                   model_uri=TG.doc_description, domain=None, range=Optional[str])

slots.user_description = Slot(uri=DCTERMS.description, name="user_description", curie=DCTERMS.curie('description'),
                   model_uri=TG.user_description, domain=None, range=Optional[str])

slots.has_part = Slot(uri=DCTERMS.hasPart, name="has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=TG.has_part, domain=None, range=Optional[Union[str, SiteId]])

slots.has_host = Slot(uri=SIOC.has_host, name="has_host", curie=SIOC.curie('has_host'),
                   model_uri=TG.has_host, domain=None, range=Optional[Union[str, SiteId]])

slots.has_parent_forum = Slot(uri=SIOC.has_parent, name="has_parent_forum", curie=SIOC.curie('has_parent'),
                   model_uri=TG.has_parent_forum, domain=None, range=Optional[Union[str, ForumId]])

slots.parent_of = Slot(uri=SIOC.parent_of, name="parent_of", curie=SIOC.curie('parent_of'),
                   model_uri=TG.parent_of, domain=None, range=Optional[Union[Union[str, ForumId], list[Union[str, ForumId]]]])

slots.host_of = Slot(uri=SIOC.host_of, name="host_of", curie=SIOC.curie('host_of'),
                   model_uri=TG.host_of, domain=None, range=Optional[Union[Union[str, ForumId], list[Union[str, ForumId]]]])

slots.container_of = Slot(uri=SIOC.container_of, name="container_of", curie=SIOC.curie('container_of'),
                   model_uri=TG.container_of, domain=None, range=Optional[Union[Union[str, PostId], list[Union[str, PostId]]]])

slots.has_container = Slot(uri=SIOC.has_container, name="has_container", curie=SIOC.curie('has_container'),
                   model_uri=TG.has_container, domain=None, range=Optional[Union[str, ForumId]])

slots.account_of = Slot(uri=SIOC.account_of, name="account_of", curie=SIOC.curie('account_of'),
                   model_uri=TG.account_of, domain=None, range=Optional[Union[str, PersonId]])

slots.holds_account = Slot(uri=FOAF.holdsAccount, name="holds_account", curie=FOAF.curie('holdsAccount'),
                   model_uri=TG.holds_account, domain=None, range=Optional[Union[Union[str, UserId], list[Union[str, UserId]]]])

slots.has_creator = Slot(uri=SIOC.has_creator, name="has_creator", curie=SIOC.curie('has_creator'),
                   model_uri=TG.has_creator, domain=None, range=Optional[Union[str, UserId]])

slots.via_bot = Slot(uri=TG.via_bot, name="via_bot", curie=TG.curie('via_bot'),
                   model_uri=TG.via_bot, domain=None, range=Optional[Union[str, UserId]])

slots.content = Slot(uri=SIOC.content, name="content", curie=SIOC.curie('content'),
                   model_uri=TG.content, domain=None, range=Optional[str])

slots.created = Slot(uri=DCTERMS.created, name="created", curie=DCTERMS.curie('created'),
                   model_uri=TG.created, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.modified = Slot(uri=DCTERMS.modified, name="modified", curie=DCTERMS.curie('modified'),
                   model_uri=TG.modified, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.reply_of = Slot(uri=SIOC.reply_of, name="reply_of", curie=SIOC.curie('reply_of'),
                   model_uri=TG.reply_of, domain=None, range=Optional[Union[str, PostId]])

slots.has_reply = Slot(uri=SIOC.has_reply, name="has_reply", curie=SIOC.curie('has_reply'),
                   model_uri=TG.has_reply, domain=None, range=Optional[Union[Union[str, PostId], list[Union[str, PostId]]]])

slots.sibling = Slot(uri=SIOC.sibling, name="sibling", curie=SIOC.curie('sibling'),
                   model_uri=TG.sibling, domain=None, range=Optional[Union[str, PostId]])

slots.links_to = Slot(uri=SIOC.links_to, name="links_to", curie=SIOC.curie('links_to'),
                   model_uri=TG.links_to, domain=None, range=Optional[Union[Union[str, LinkedDocumentId], list[Union[str, LinkedDocumentId]]]])

slots.attachment = Slot(uri=SIOC.attachment, name="attachment", curie=SIOC.curie('attachment'),
                   model_uri=TG.attachment, domain=None, range=Optional[Union[Union[str, AttachmentId], list[Union[str, AttachmentId]]]])

slots.has_poll = Slot(uri=TG.has_poll, name="has_poll", curie=TG.curie('has_poll'),
                   model_uri=TG.has_poll, domain=None, range=Optional[Union[str, PollId]])

slots.topics = Slot(uri=SIOC.topic, name="topics", curie=SIOC.curie('topic'),
                   model_uri=TG.topics, domain=None, range=Optional[Union[Union[str, ConceptId], list[Union[str, ConceptId]]]])

slots.forwards = Slot(uri=TG.forwards, name="forwards", curie=TG.curie('forwards'),
                   model_uri=TG.forwards, domain=None, range=Optional[int])

slots.pinned = Slot(uri=TG.pinned, name="pinned", curie=TG.curie('pinned'),
                   model_uri=TG.pinned, domain=None, range=Optional[Union[bool, Bool]])

slots.closed = Slot(uri=TG.closed, name="closed", curie=TG.curie('closed'),
                   model_uri=TG.closed, domain=None, range=Optional[Union[bool, Bool]])

slots.is_bot = Slot(uri=TG.is_bot, name="is_bot", curie=TG.curie('is_bot'),
                   model_uri=TG.is_bot, domain=None, range=Optional[Union[bool, Bool]])

slots.avatar = Slot(uri=TG.avatar, name="avatar", curie=TG.curie('avatar'),
                   model_uri=TG.avatar, domain=None, range=Optional[str])

slots.quote_text = Slot(uri=TG.quote_text, name="quote_text", curie=TG.curie('quote_text'),
                   model_uri=TG.quote_text, domain=None, range=Optional[str])

slots.grouped_id = Slot(uri=TG.grouped_id, name="grouped_id", curie=TG.curie('grouped_id'),
                   model_uri=TG.grouped_id, domain=None, range=Optional[str])

slots.format = Slot(uri=DCTERMS.format, name="format", curie=DCTERMS.curie('format'),
                   model_uri=TG.format, domain=None, range=Optional[str])

slots.extent = Slot(uri=DCTERMS.extent, name="extent", curie=DCTERMS.curie('extent'),
                   model_uri=TG.extent, domain=None, range=Optional[int])

slots.media_type = Slot(uri=TG.media_type, name="media_type", curie=TG.curie('media_type'),
                   model_uri=TG.media_type, domain=None, range=Optional[Union[str, "MediaType"]])

slots.duration = Slot(uri=TG.duration, name="duration", curie=TG.curie('duration'),
                   model_uri=TG.duration, domain=None, range=Optional[int])

slots.doc_creator = Slot(uri=DCTERMS.creator, name="doc_creator", curie=DCTERMS.curie('creator'),
                   model_uri=TG.doc_creator, domain=None, range=Optional[str])

slots.site_name = Slot(uri=TG.site_name, name="site_name", curie=TG.curie('site_name'),
                   model_uri=TG.site_name, domain=None, range=Optional[str])

slots.answers = Slot(uri=TG.answers, name="answers", curie=TG.curie('answers'),
                   model_uri=TG.answers, domain=None, range=Optional[Union[str, list[str]]])

slots.total_voters = Slot(uri=TG.total_voters, name="total_voters", curie=TG.curie('total_voters'),
                   model_uri=TG.total_voters, domain=None, range=Optional[int])

slots.quiz = Slot(uri=TG.quiz, name="quiz", curie=TG.curie('quiz'),
                   model_uri=TG.quiz, domain=None, range=Optional[Union[bool, Bool]])

slots.poll_closed = Slot(uri=TG.poll_closed, name="poll_closed", curie=TG.curie('poll_closed'),
                   model_uri=TG.poll_closed, domain=None, range=Optional[Union[bool, Bool]])

slots.public_voters = Slot(uri=TG.public_voters, name="public_voters", curie=TG.curie('public_voters'),
                   model_uri=TG.public_voters, domain=None, range=Optional[Union[bool, Bool]])

slots.multiple_choice = Slot(uri=TG.multiple_choice, name="multiple_choice", curie=TG.curie('multiple_choice'),
                   model_uri=TG.multiple_choice, domain=None, range=Optional[Union[bool, Bool]])

slots.reactor = Slot(uri=TG.reactor, name="reactor", curie=TG.curie('reactor'),
                   model_uri=TG.reactor, domain=None, range=Optional[Union[str, UserId]])

slots.emoji = Slot(uri=TG.emoji, name="emoji", curie=TG.curie('emoji'),
                   model_uri=TG.emoji, domain=None, range=Optional[str])

slots.target = Slot(uri=TG.target, name="target", curie=TG.curie('target'),
                   model_uri=TG.target, domain=None, range=Optional[Union[str, PostId]])

slots.concept_type = Slot(uri=TG.concept_type, name="concept_type", curie=TG.curie('concept_type'),
                   model_uri=TG.concept_type, domain=None, range=Optional[Union[str, "EntityType"]])

slots.concept_description = Slot(uri=TG.concept_description, name="concept_description", curie=TG.curie('concept_description'),
                   model_uri=TG.concept_description, domain=None, range=Optional[str])

slots.confidence = Slot(uri=TG.confidence, name="confidence", curie=TG.curie('confidence'),
                   model_uri=TG.confidence, domain=None, range=Optional[float])

slots.annotation_body = Slot(uri=TG.annotation_body, name="annotation_body", curie=TG.curie('annotation_body'),
                   model_uri=TG.annotation_body, domain=None, range=Optional[str])

slots.annotation_target = Slot(uri=TG.annotation_target, name="annotation_target", curie=TG.curie('annotation_target'),
                   model_uri=TG.annotation_target, domain=None, range=Optional[Union[str, PostId]])

slots.entity_type = Slot(uri=TG.entity_type, name="entity_type", curie=TG.curie('entity_type'),
                   model_uri=TG.entity_type, domain=None, range=Optional[Union[str, "EntityType"]])

slots.discovered_by = Slot(uri=TG.discovered_by, name="discovered_by", curie=TG.curie('discovered_by'),
                   model_uri=TG.discovered_by, domain=None, range=Optional[Union[str, UserId]])

slots.session_ref = Slot(uri=TG.session_ref, name="session_ref", curie=TG.curie('session_ref'),
                   model_uri=TG.session_ref, domain=None, range=Optional[Union[str, AnnotationSessionId]])

slots.harmonica_session_id = Slot(uri=TG.harmonica_session_id, name="harmonica_session_id", curie=TG.curie('harmonica_session_id'),
                   model_uri=TG.harmonica_session_id, domain=None, range=Optional[str])

slots.theme = Slot(uri=TG.theme, name="theme", curie=TG.curie('theme'),
                   model_uri=TG.theme, domain=None, range=Optional[Union[str, "SessionTheme"]])

slots.messages_annotated = Slot(uri=TG.messages_annotated, name="messages_annotated", curie=TG.curie('messages_annotated'),
                   model_uri=TG.messages_annotated, domain=None, range=Optional[Union[Union[str, PostId], list[Union[str, PostId]]]])

slots.participant_count = Slot(uri=TG.participant_count, name="participant_count", curie=TG.curie('participant_count'),
                   model_uri=TG.participant_count, domain=None, range=Optional[int])

slots.session_status = Slot(uri=TG.session_status, name="session_status", curie=TG.curie('session_status'),
                   model_uri=TG.session_status, domain=None, range=Optional[Union[str, "SessionStatus"]])

slots.community = Slot(uri=TG.community, name="community", curie=TG.curie('community'),
                   model_uri=TG.community, domain=None, range=Optional[Union[dict, Community]])

slots.site = Slot(uri=TG.site, name="site", curie=TG.curie('site'),
                   model_uri=TG.site, domain=None, range=Optional[Union[dict, Site]])

slots.forums = Slot(uri=TG.forums, name="forums", curie=TG.curie('forums'),
                   model_uri=TG.forums, domain=None, range=Optional[Union[dict[Union[str, ForumId], Union[dict, Forum]], list[Union[dict, Forum]]]])

slots.users = Slot(uri=TG.users, name="users", curie=TG.curie('users'),
                   model_uri=TG.users, domain=None, range=Optional[Union[dict[Union[str, UserId], Union[dict, User]], list[Union[dict, User]]]])

slots.persons = Slot(uri=TG.persons, name="persons", curie=TG.curie('persons'),
                   model_uri=TG.persons, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

slots.posts = Slot(uri=TG.posts, name="posts", curie=TG.curie('posts'),
                   model_uri=TG.posts, domain=None, range=Optional[Union[dict[Union[str, PostId], Union[dict, Post]], list[Union[dict, Post]]]])

slots.threads = Slot(uri=TG.threads, name="threads", curie=TG.curie('threads'),
                   model_uri=TG.threads, domain=None, range=Optional[Union[dict[Union[str, ThreadId], Union[dict, Thread]], list[Union[dict, Thread]]]])

slots.concepts = Slot(uri=TG.concepts, name="concepts", curie=TG.curie('concepts'),
                   model_uri=TG.concepts, domain=None, range=Optional[Union[dict[Union[str, ConceptId], Union[dict, Concept]], list[Union[dict, Concept]]]])

slots.attachments = Slot(uri=TG.attachments, name="attachments", curie=TG.curie('attachments'),
                   model_uri=TG.attachments, domain=None, range=Optional[Union[dict[Union[str, AttachmentId], Union[dict, Attachment]], list[Union[dict, Attachment]]]])

slots.linked_documents = Slot(uri=TG.linked_documents, name="linked_documents", curie=TG.curie('linked_documents'),
                   model_uri=TG.linked_documents, domain=None, range=Optional[Union[dict[Union[str, LinkedDocumentId], Union[dict, LinkedDocument]], list[Union[dict, LinkedDocument]]]])

slots.polls = Slot(uri=TG.polls, name="polls", curie=TG.curie('polls'),
                   model_uri=TG.polls, domain=None, range=Optional[Union[dict[Union[str, PollId], Union[dict, Poll]], list[Union[dict, Poll]]]])

slots.annotations = Slot(uri=TG.annotations, name="annotations", curie=TG.curie('annotations'),
                   model_uri=TG.annotations, domain=None, range=Optional[Union[dict[Union[str, AnnotationId], Union[dict, Annotation]], list[Union[dict, Annotation]]]])

slots.annotation_sessions = Slot(uri=TG.annotation_sessions, name="annotation_sessions", curie=TG.curie('annotation_sessions'),
                   model_uri=TG.annotation_sessions, domain=None, range=Optional[Union[dict[Union[str, AnnotationSessionId], Union[dict, AnnotationSession]], list[Union[dict, AnnotationSession]]]])

