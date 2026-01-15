from enum import Enum

from data.amc import AMC


def test_amc_is_enum() -> None:
    """Test that AMC is an Enum."""
    assert issubclass(AMC, Enum)


def test_amc_has_members() -> None:
    """Test that AMC enum has members."""
    assert len(AMC) > 0


def test_amc_hdfc_value() -> None:
    """Test specific AMC value."""
    assert AMC.HDFC_MUTUAL_FUND.value == 9


def test_amc_sbi_value() -> None:
    """Test specific AMC value."""
    assert AMC.SBI_MUTUAL_FUND.value == 22


def test_amc_member_access_by_name() -> None:
    """Test that AMC members can be accessed by name."""
    assert AMC["AXIS_MUTUAL_FUND"] == AMC.AXIS_MUTUAL_FUND


def test_amc_member_access_by_value() -> None:
    """Test that AMC members can be accessed by value."""
    assert AMC(53) == AMC.AXIS_MUTUAL_FUND


def test_amc_all_values_are_integers() -> None:
    """Test that all AMC values are integers."""
    for member in AMC:
        assert isinstance(member.value, int)


def test_amc_all_values_are_unique() -> None:
    """Test that all AMC values are unique."""
    values = [member.value for member in AMC]
    assert len(values) == len(set(values))
