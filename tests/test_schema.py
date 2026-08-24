"""The build must REJECT bad data, not merely accept good data.

CI already runs `npm run build`, which proves valid records compile. Nothing
proved the guards fire: delete assertIdsMatchFilenames, or loosen the Zod
schema, and CI stays green while the protection is gone. These tests falsify a
record on purpose and assert the build fails with the message a contributor
would need.

They are slow — each case is a real Astro build — so they are marked and can be
skipped locally with `-m "not slow"`. CI runs them.
"""
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

pytestmark = pytest.mark.slow

PAPERS = REPO_ROOT / "src" / "content" / "papers"
TAXONOMY = REPO_ROOT / "src" / "data" / "taxonomy.yml"
VICTIM = PAPERS / "react-2022.yml"


@pytest.fixture
def build(tmp_path):
    """Falsify a file, build, restore it, and hand back the output.

    Restoration happens in a finally so an interrupted run cannot leave the
    working tree modified.
    """
    backups = {}

    def run(edits):
        for path, (old, new) in edits.items():
            backups[path] = path.read_text(encoding="utf-8")
            assert old in backups[path], f"anchor not found in {path.name}: {old!r}"
            path.write_text(backups[path].replace(old, new, 1), encoding="utf-8")

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=600,
        )
        return result

    yield run

    for path, original in backups.items():
        path.write_text(original, encoding="utf-8")
    for extra in tmp_path.glob("*.yml"):
        target = PAPERS / extra.name
        if target.exists():
            target.unlink()


def failed(result, *expected):
    assert result.returncode != 0, "the build should have failed but succeeded"
    output = result.stdout + result.stderr
    for fragment in expected:
        assert fragment in output, f"missing {fragment!r} in:\n{output[-3000:]}"


# --- vocabulary ------------------------------------------------------------

def test_area_outside_the_taxonomy_fails(build):
    """The classic mistake: recording scale as if it were an area."""
    result = build({VICTIM: ("area: reasoning-planning", "area: multi-agent")})
    failed(result, '"multi-agent" is not part of areas')
    # The message lists the valid values, which is what makes it fixable.
    failed(result, "reasoning-planning")


def test_invented_topic_fails(build):
    result = build({VICTIM: ("topics: [react", "topics: [not-a-real-topic")})
    failed(result, '"not-a-real-topic" is not part of topics')


def test_invented_facet_value_fails(build):
    result = build({VICTIM: ("scale: [single-agent]", "scale: [solo-agent]")})
    failed(result, '"solo-agent" is not part of facets.scale')


# --- the three states ------------------------------------------------------

def test_read_without_tldr_fails(build):
    result = build({VICTIM: ('tldr: "Interleaves', 'x_tldr: "Interleaves')})
    failed(result, 'status: read requires "tldr"')
    # It has to say how to unblock, or the contributor is stuck.
    failed(result, "Drop it back to triaged")


def test_read_without_about_fails(build):
    result = build({VICTIM: ("about: [reasoning, tool-use]", "about: []")})
    failed(result, 'status: read requires "about"')


def test_triaged_without_area_fails(build):
    result = build({VICTIM: (
        "area: reasoning-planning\n", "")})
    failed(result, 'status: read requires "area"')


# --- structural guards -----------------------------------------------------

def test_id_not_matching_filename_fails(build):
    """Otherwise the paper is published at one URL and linked from another."""
    result = build({VICTIM: ("id: react-2022", "id: react-2O22")})
    failed(result, "the id field must equal the filename")


def test_empty_venue_fails(build):
    result = build({VICTIM: ('venue: "ICLR 2023"', 'venue: ""')})
    failed(result, "empty venue")


def test_non_date_added_fails(build):
    result = build({VICTIM: ("added: 2026-08-21", 'added: "sometime"')})
    failed(result, "added must be a YYYY-MM-DD date")


def test_dangling_relates_to_fails(build):
    """A reading path pointing at nothing is a silently broken link."""
    result = build({VICTIM: ("relates_to: []", "relates_to: [no-such-paper]")})
    failed(result, "References to papers that do not exist")
    failed(result, "no-such-paper")


# --- taxonomy integrity ----------------------------------------------------

def test_area_pointing_at_a_missing_group_fails(build):
    """A typo here would drop the area from the navigation with no error."""
    result = build({TAXONOMY: (
        "  memory:\n    group: capabilities",
        "  memory:\n    group: capabilties",
    )})
    failed(result, "points at a group that does not exist")


def test_domain_group_listing_an_unknown_domain_fails(build):
    result = build({TAXONOMY: (
        "    members: [web, gui, robotics]",
        "    members: [web, gui, robotics, telepathy]",
    )})
    failed(result, "not in facets.domain")


def test_facet_without_a_description_fails(build):
    """facet_blurbs feeds /taxonomy and the issue form."""
    result = build({TAXONOMY: (
        "  type: \"What kind of contribution it is.\"",
        "  x_type: \"What kind of contribution it is.\"",
    )})
    failed(result, "has no entry in facet_blurbs")


# --- the happy path --------------------------------------------------------

def test_the_committed_repository_builds():
    """Anchors the suite: every failure above is caused by the edit, not by a
    repository that was already broken."""
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=600,
    )
    assert result.returncode == 0, (result.stdout + result.stderr)[-3000:]
