"""Test the gator.api.client module."""
from types import SimpleNamespace

import pytest
from gator.schemas.timetable import CourseSchema, OrganisationSchema
from pytest_httpserver import HTTPServer

from gator.api.client import GatorClient
from tests.helpers import load_json_fixture

###############################################################################
# Setup fixtures for mocking Gator API calls.
###############################################################################


@pytest.fixture
def gator_client(httpserver: HTTPServer) -> None:
    """Fixture that configures a GatorClient for testing."""
    return GatorClient(httpserver.url_for('/'))


###############################################################################
# Tests for the GatorClient class.
###############################################################################


def test_get_courses_all(gator_client: GatorClient, httpserver: HTTPServer) -> None:
    """Test the get_courses API method with no ids parameter."""
    courses_fixture = load_json_fixture('courses_all.json')
    httpserver.expect_request('/courses', method='GET').respond_with_json(
        courses_fixture)

    expected = SimpleNamespace(
        courses=CourseSchema(many=True).load(courses_fixture['courses']),
        last_id=courses_fixture['last_id'],
    )

    assert gator_client.get_courses() == expected


def test_get_courses_some(gator_client: GatorClient, httpserver: HTTPServer) -> None:
    """Test the get_courses API method with ids parameter."""
    courses_fixture = load_json_fixture('courses_some.json')
    course_ids = [c['id'] for c in courses_fixture['courses']]

    httpserver.expect_request(
        '/courses',
        query_string=dict(ids=','.join(course_ids)),
        method='GET'
    ).respond_with_json(courses_fixture)

    expected = SimpleNamespace(
        courses=CourseSchema(many=True).load(courses_fixture['courses']),
        last_id=courses_fixture['last_id'],
    )

    # Test comma-separated input
    assert gator_client.get_courses(ids=','.join(course_ids)) == expected
    # Test list input
    assert gator_client.get_courses(ids=course_ids) == expected


def test_get_course(gator_client: GatorClient, httpserver: HTTPServer) -> None:
    """Test the get_course API method."""
    course_fixture = load_json_fixture('course_ACT350.json')
    course_id = course_fixture['id']

    httpserver.expect_request(f'/courses/{course_id}', method='GET')\
        .respond_with_json(course_fixture)

    expected = CourseSchema().load(course_fixture)

    assert gator_client.get_course('ACT350H1-F-20229') == expected


def test_get_organisations(gator_client: GatorClient, httpserver: HTTPServer) -> None:
    """Test the get_organisations API method."""
    organisations_fixture = load_json_fixture('organisations.json')
    httpserver.expect_request('/organisations', method='GET').respond_with_json(
        organisations_fixture)

    expected = SimpleNamespace(
        organisations=OrganisationSchema(many=True).load(
            organisations_fixture['organisations']),
        last_id=organisations_fixture['last_id'],
    )

    assert gator_client.get_organisations() == expected


def test_get_organisation(gator_client: GatorClient, httpserver: HTTPServer) -> None:
    """Test the get_organisation API method."""
    organisation_fixture = load_json_fixture('organisation_MAT.json')
    organisation_code = organisation_fixture['code']

    httpserver.expect_request(f'/organisations/{organisation_code}', method='GET')\
        .respond_with_json(organisation_fixture)

    expected = OrganisationSchema().load(organisation_fixture)

    assert gator_client.get_organisation('MAT') == expected
