"""Test to verify AMC enum is in sync with AMFI website."""

import json
import re

import httpx
import pytest

from data.amc import AMC

AMFI_NAV_URL = "https://www.amfiindia.com/net-asset-value/nav-download"


def fetch_amfi_amc_list() -> list[dict[str, str]]:
    """Fetch the list of AMCs from AMFI website."""
    response = httpx.get(AMFI_NAV_URL, timeout=30)
    response.raise_for_status()

    html = response.text

    # Find the JavaScript array containing AMC data
    # Pattern matches: var mfData = [...] or similar structures
    pattern = r"\[\s*\{[^]]*tableId[^]]*\}\s*\]"
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        pytest.fail("Could not find AMC data in AMFI website response")

    # Parse the JSON array
    json_str = match.group(0)
    # Remove escaped backslashes from the JSON string
    json_str = json_str.replace('\\"', '"')
    # Fix JavaScript object notation to valid JSON (unquoted keys)
    json_str = re.sub(r"([{,])\s*(\w+)\s*:", r'\1"\2":', json_str)
    # Remove trailing commas
    json_str = re.sub(r",\s*([}\]])", r"\1", json_str)

    amc_list: list[dict[str, str]] = json.loads(json_str)
    return amc_list


def normalize_name(name: str) -> str:
    """Normalize AMC name for comparison."""
    # Convert to uppercase, replace special chars with underscores
    normalized = name.upper()
    normalized = re.sub(r"[^A-Z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    normalized = normalized.strip("_")
    # Handle special case: names starting with numbers need underscore prefix
    if normalized and normalized[0].isdigit():
        normalized = "_" + normalized
    return normalized


@pytest.mark.network
def test_all_amfi_amcs_present_in_enum() -> None:
    """Test that all AMCs from AMFI website are present in our enum."""
    amfi_amcs = fetch_amfi_amc_list()

    # Build a mapping of mfId -> mfName from AMFI
    amfi_by_id: dict[int, str] = {}
    for amc in amfi_amcs:
        mf_id = int(amc["mfId"])
        mf_name = amc["mfName"]
        amfi_by_id[mf_id] = mf_name

    # Build a mapping of value -> name from our enum
    enum_by_id: dict[int, str] = {member.value: member.name for member in AMC}

    # Check that all AMFI AMCs are in our enum
    missing_in_enum: list[str] = []
    for mf_id, mf_name in amfi_by_id.items():
        if mf_id not in enum_by_id:
            missing_in_enum.append(f"{mf_name} (ID: {mf_id})")

    if missing_in_enum:
        pytest.fail(
            "AMCs present in AMFI but missing in enum:\n"
            + "\n".join(f"  - {name}" for name in missing_in_enum)
        )


@pytest.mark.network
def test_enum_ids_match_amfi() -> None:
    """Test that enum IDs match AMFI IDs."""
    amfi_amcs = fetch_amfi_amc_list()

    amfi_ids = {int(amc["mfId"]) for amc in amfi_amcs}
    enum_ids = {member.value for member in AMC}

    # IDs in enum but not in AMFI (possibly defunct AMCs)
    extra_in_enum = enum_ids - amfi_ids
    if extra_in_enum:
        extra_names = [
            f"{member.name} (ID: {member.value})"
            for member in AMC
            if member.value in extra_in_enum
        ]
        print("Note: AMCs in enum but not in AMFI (possibly defunct):")
        for name in extra_names:
            print(f"  - {name}")


@pytest.mark.network
def test_amfi_endpoint_accessible() -> None:
    """Test that AMFI endpoint is accessible."""
    response = httpx.get(AMFI_NAV_URL, timeout=30)
    assert response.status_code == 200
