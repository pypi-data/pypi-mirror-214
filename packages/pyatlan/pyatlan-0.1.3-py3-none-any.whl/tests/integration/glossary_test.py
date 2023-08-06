# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest
from pydantic import StrictStr

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("GLS")

TERM_NAME1 = f"{MODULE_NAME}1"
TERM_NAME2 = f"{MODULE_NAME}2"


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.upsert(g)
    return r.assets_created(AtlasGlossary)[0]


def create_term(
    client: AtlanClient, name: str, glossary_guid: str
) -> AtlasGlossaryTerm:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(name), glossary_guid=StrictStr(glossary_guid)
    )
    r = client.upsert(t)
    return r.assets_created(AtlasGlossaryTerm)[0]


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, MODULE_NAME)
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


def test_glossary(
    glossary: AtlasGlossary,
):
    assert glossary.guid
    assert glossary.name == MODULE_NAME
    assert glossary.qualified_name
    assert glossary.qualified_name != MODULE_NAME


@pytest.fixture(scope="module")
def term1(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME1, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term1(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1.guid
    assert term1.name == TERM_NAME1
    assert term1.qualified_name
    assert term1.qualified_name != TERM_NAME1
    t = client.get_asset_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term1.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term2(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term2(
    client: AtlanClient,
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term2.guid
    assert term2.name == TERM_NAME2
    assert term2.qualified_name
    assert term2.qualified_name != TERM_NAME2
    t = client.get_asset_by_guid(term2.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term2.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


def test_read_glossary(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    g = client.get_asset_by_guid(glossary.guid, asset_type=AtlasGlossary)
    assert g
    assert isinstance(g, AtlasGlossary)
    assert g.guid == glossary.guid
    assert g.qualified_name == glossary.qualified_name
    assert g.name == glossary.name
    terms = g.terms
    assert terms
    assert len(terms) == 2


@pytest.mark.order(after="test_read_glossary")
def test_trim_to_required_glossary(
    client: AtlanClient,
    glossary: AtlasGlossary,
):
    glossary = glossary.trim_to_required()
    response = client.upsert(glossary)
    assert response.mutated_entities is None


@pytest.mark.order(after="test_term1")
def test_term_trim_to_required(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
):
    term1 = client.get_asset_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
    term1 = term1.trim_to_required()
    response = client.upsert(term1)
    assert response.mutated_entities is None
