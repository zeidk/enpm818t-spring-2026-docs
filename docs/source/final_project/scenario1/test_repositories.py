"""
Test suite for repository classes.

These tests verify that your repositories correctly interact with the
PostgreSQL database. Each test should use a real database connection
(not mocks) so you are testing actual SQL execution.

SETUP:
    1. Create a test database:
       createdb traffic_management_test

    2. Load your schema and data:
       psql -d traffic_management_test -f postgresql/schema.sql
       psql -d traffic_management_test -f postgresql/data.sql

    3. Set your .env to point to the test database:
       DB_NAME=traffic_management_test

    4. Run tests from the project root:
       pytest tests/ --cov=src --cov-report=html

NOTE: These are starter tests. You should add more tests to reach
      50% coverage across your repositories and services.
"""

import pytest
from config.database import DatabaseConfig

# ----------------------------------------------------------------
# Import your repositories here. Adjust paths to match your project.
# Example:
#   from repositories.intersection_repo import IntersectionRepository
#   from repositories.incident_repo import IncidentRepository
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    """Initialize the connection pool once for the entire test session."""
    DatabaseConfig.initialize()
    yield
    DatabaseConfig.close_all()


@pytest.fixture
def intersection_repo():
    """Provide a fresh IntersectionRepository instance for each test."""
    # return IntersectionRepository()
    pass


@pytest.fixture
def incident_repo():
    """Provide a fresh IncidentRepository instance for each test."""
    # return IncidentRepository()
    pass


# ----------------------------------------------------------------
# IntersectionRepository Tests
# ----------------------------------------------------------------

class TestIntersectionRepository:
    """Tests for IntersectionRepository CRUD operations."""

    def test_find_by_id_returns_entity(self, intersection_repo):
        """find_by_id() should return an Intersection for a known ID."""
        # Arrange: use an ID that exists in your data.sql
        known_id = 1

        # Act
        result = intersection_repo.find_by_id(known_id)

        # Assert
        assert result is not None
        assert result.intersection_id == known_id
        assert result.intersection_name is not None

    def test_find_by_id_returns_none_for_missing(self, intersection_repo):
        """find_by_id() should return None for a non-existent ID."""
        result = intersection_repo.find_by_id(99999)
        assert result is None

    def test_find_all_returns_list(self, intersection_repo):
        """find_all() should return a list of Intersection objects."""
        results = intersection_repo.find_all(limit=5, offset=0)

        assert isinstance(results, list)
        assert len(results) <= 5
        assert len(results) > 0  # data.sql should have intersections

    def test_find_all_respects_limit(self, intersection_repo):
        """find_all() should not return more rows than the limit."""
        results = intersection_repo.find_all(limit=3, offset=0)
        assert len(results) <= 3

    def test_find_all_respects_offset(self, intersection_repo):
        """find_all() with offset should skip the first N rows."""
        page1 = intersection_repo.find_all(limit=5, offset=0)
        page2 = intersection_repo.find_all(limit=5, offset=5)

        # Pages should not overlap (assuming 10+ intersections exist)
        if len(page1) > 0 and len(page2) > 0:
            page1_ids = {i.intersection_id for i in page1}
            page2_ids = {i.intersection_id for i in page2}
            assert page1_ids.isdisjoint(page2_ids)

    def test_create_and_retrieve(self, intersection_repo):
        """create() should insert a record that can then be retrieved."""
        # Arrange: build a new intersection (adjust fields to your schema)
        # new_intersection = Intersection(
        #     intersection_id=None,  # auto-generated
        #     intersection_name="Test St & Pytest Ave",
        #     latitude=38.9000,
        #     longitude=-77.0400,
        #     intersection_type="4-way",
        #     traffic_capacity=1000,
        #     ...
        # )

        # Act
        # created = intersection_repo.create(new_intersection)

        # Assert
        # assert created.intersection_id is not None
        # retrieved = intersection_repo.find_by_id(created.intersection_id)
        # assert retrieved is not None
        # assert retrieved.intersection_name == "Test St & Pytest Ave"

        # Cleanup
        # intersection_repo.delete(created.intersection_id)
        pass

    def test_update_persists_changes(self, intersection_repo):
        """update() should modify a record so changes persist."""
        # Arrange: create a record, then update it
        # original = intersection_repo.find_by_id(1)
        # original.traffic_capacity = 9999

        # Act
        # intersection_repo.update(original)
        # updated = intersection_repo.find_by_id(1)

        # Assert
        # assert updated.traffic_capacity == 9999

        # Cleanup: restore original value
        # original.traffic_capacity = <original_value>
        # intersection_repo.update(original)
        pass

    def test_delete_removes_record(self, intersection_repo):
        """delete() should remove a record so it can no longer be found."""
        # Arrange: create a temporary record
        # temp = intersection_repo.create(...)

        # Act
        # intersection_repo.delete(temp.intersection_id)

        # Assert
        # assert intersection_repo.find_by_id(temp.intersection_id) is None
        pass

    def test_create_duplicate_pk_raises_error(self, intersection_repo):
        """Inserting a duplicate primary key should raise an exception."""
        # existing = intersection_repo.find_by_id(1)
        # with pytest.raises(Exception):
        #     intersection_repo.create(existing)  # same PK
        pass

    def test_create_invalid_fk_raises_error(self, intersection_repo):
        """Inserting a record with a non-existent FK should raise an error."""
        # Example: creating a signal that references intersection_id=99999
        # with pytest.raises(Exception):
        #     signal_repo.create(Signal(intersection_id=99999, ...))
        pass


# ----------------------------------------------------------------
# IncidentRepository Tests
# ----------------------------------------------------------------

class TestIncidentRepository:
    """Tests for IncidentRepository operations."""

    def test_find_by_id_returns_entity(self, incident_repo):
        """find_by_id() should return an Incident for a known ID."""
        result = incident_repo.find_by_id(1)
        assert result is not None
        assert result.incident_id == 1

    def test_find_by_id_returns_none_for_missing(self, incident_repo):
        """find_by_id() should return None for a non-existent ID."""
        result = incident_repo.find_by_id(99999)
        assert result is None

    # ----------------------------------------------------------
    # Add tests for your custom query methods here.
    # Examples:
    # ----------------------------------------------------------

    # def test_find_by_severity(self, incident_repo):
    #     """find_by_severity() should return only matching incidents."""
    #     results = incident_repo.find_by_severity("critical")
    #     assert all(i.severity_level == "critical" for i in results)

    # def test_find_by_intersection(self, incident_repo):
    #     """find_by_intersection() should return incidents at a location."""
    #     results = incident_repo.find_by_intersection(1)
    #     assert all(i.intersection_id == 1 for i in results)


# ----------------------------------------------------------------
# Add more test classes for your other repositories:
#   TestTrafficSignalRepository
#   TestSensorRepository
#   TestMaintenanceScheduleRepository
#   etc.
# ----------------------------------------------------------------
