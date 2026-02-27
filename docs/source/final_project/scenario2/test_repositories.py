"""
Test suite for repository classes.

These tests verify that your repositories correctly interact with the
PostgreSQL database. Each test should use a real database connection
(not mocks) so you are testing actual SQL execution.

SETUP:
    1. Create a test database:
       createdb healthcare_management_test

    2. Load your schema and data:
       psql -d healthcare_management_test -f postgresql/schema.sql
       psql -d healthcare_management_test -f postgresql/data.sql

    3. Set your .env to point to the test database:
       DB_NAME=healthcare_management_test

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
#   from repositories.patient_repo import PatientRepository
#   from repositories.prescription_repo import PrescriptionRepository
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
def patient_repo():
    """Provide a fresh PatientRepository instance for each test."""
    # return PatientRepository()
    pass


@pytest.fixture
def prescription_repo():
    """Provide a fresh PrescriptionRepository instance for each test."""
    # return PrescriptionRepository()
    pass


# ----------------------------------------------------------------
# PatientRepository Tests
# ----------------------------------------------------------------

class TestPatientRepository:
    """Tests for PatientRepository CRUD operations."""

    def test_find_by_id_returns_entity(self, patient_repo):
        """find_by_id() should return a Patient for a known ID."""
        # Arrange: use an ID that exists in your data.sql
        known_id = 1

        # Act
        result = patient_repo.find_by_id(known_id)

        # Assert
        assert result is not None
        assert result.patient_id == known_id
        assert result.mrn is not None

    def test_find_by_id_returns_none_for_missing(self, patient_repo):
        """find_by_id() should return None for a non-existent ID."""
        result = patient_repo.find_by_id(99999)
        assert result is None

    def test_find_all_returns_list(self, patient_repo):
        """find_all() should return a list of Patient objects."""
        results = patient_repo.find_all(limit=5, offset=0)

        assert isinstance(results, list)
        assert len(results) <= 5
        assert len(results) > 0  # data.sql should have patients

    def test_find_all_respects_limit(self, patient_repo):
        """find_all() should not return more rows than the limit."""
        results = patient_repo.find_all(limit=3, offset=0)
        assert len(results) <= 3

    def test_find_all_respects_offset(self, patient_repo):
        """find_all() with offset should skip the first N rows."""
        page1 = patient_repo.find_all(limit=5, offset=0)
        page2 = patient_repo.find_all(limit=5, offset=5)

        # Pages should not overlap (assuming 10+ patients exist)
        if len(page1) > 0 and len(page2) > 0:
            page1_ids = {p.patient_id for p in page1}
            page2_ids = {p.patient_id for p in page2}
            assert page1_ids.isdisjoint(page2_ids)

    def test_create_and_retrieve(self, patient_repo):
        """create() should insert a record that can then be retrieved."""
        # Arrange: build a new patient (adjust fields to your schema)
        # new_patient = Patient(
        #     patient_id=None,  # auto-generated
        #     mrn="9999999999",
        #     first_name="Test",
        #     last_name="Patient",
        #     date_of_birth="1990-01-01",
        #     ...
        # )

        # Act
        # created = patient_repo.create(new_patient)

        # Assert
        # assert created.patient_id is not None
        # retrieved = patient_repo.find_by_id(created.patient_id)
        # assert retrieved is not None
        # assert retrieved.mrn == "9999999999"

        # Cleanup
        # patient_repo.delete(created.patient_id)
        pass

    def test_update_persists_changes(self, patient_repo):
        """update() should modify a record so changes persist."""
        # Arrange: create a record, then update it
        # original = patient_repo.find_by_id(1)
        # original.phone = "555-000-0000"

        # Act
        # patient_repo.update(original)
        # updated = patient_repo.find_by_id(1)

        # Assert
        # assert updated.phone == "555-000-0000"

        # Cleanup: restore original value
        # original.phone = <original_value>
        # patient_repo.update(original)
        pass

    def test_delete_removes_record(self, patient_repo):
        """delete() should remove a record so it can no longer be found."""
        # Arrange: create a temporary record
        # temp = patient_repo.create(...)

        # Act
        # patient_repo.delete(temp.patient_id)

        # Assert
        # assert patient_repo.find_by_id(temp.patient_id) is None
        pass

    def test_create_duplicate_mrn_raises_error(self, patient_repo):
        """Inserting a duplicate MRN should raise an exception."""
        # existing = patient_repo.find_by_id(1)
        # with pytest.raises(Exception):
        #     patient_repo.create(Patient(mrn=existing.mrn, ...))
        pass

    def test_create_invalid_fk_raises_error(self, patient_repo):
        """Inserting a record with a non-existent FK should raise an error."""
        # Example: creating an appointment that references patient_id=99999
        # with pytest.raises(Exception):
        #     appointment_repo.create(Appointment(patient_id=99999, ...))
        pass


# ----------------------------------------------------------------
# PrescriptionRepository Tests
# ----------------------------------------------------------------

class TestPrescriptionRepository:
    """Tests for PrescriptionRepository operations."""

    def test_find_by_id_returns_entity(self, prescription_repo):
        """find_by_id() should return a Prescription for a known ID."""
        result = prescription_repo.find_by_id(1)
        assert result is not None
        assert result.prescription_id == 1

    def test_find_by_id_returns_none_for_missing(self, prescription_repo):
        """find_by_id() should return None for a non-existent ID."""
        result = prescription_repo.find_by_id(99999)
        assert result is None

    # ----------------------------------------------------------
    # Add tests for your custom query methods here.
    # Examples:
    # ----------------------------------------------------------

    # def test_find_active_by_patient(self, prescription_repo):
    #     """find_active_prescriptions() should return only active ones."""
    #     results = prescription_repo.find_active_prescriptions(patient_id=1)
    #     assert all(p.status == "active" for p in results)

    # def test_find_controlled_substances(self, prescription_repo):
    #     """find_controlled_substances() should return scheduled meds."""
    #     results = prescription_repo.find_controlled_substances()
    #     assert all(p.controlled_substance_schedule is not None
    #                for p in results)


# ----------------------------------------------------------------
# Add more test classes for your other repositories:
#   TestAppointmentRepository
#   TestLabOrderRepository
#   TestInsuranceClaimRepository
#   etc.
# ----------------------------------------------------------------
