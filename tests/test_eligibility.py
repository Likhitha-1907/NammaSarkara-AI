
import sys
from pathlib import Path

# Allow Python to find the src folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from eligibility_checker import check_pm_kisan_eligibility


def create_valid_profile():
    return {
        "has_cultivable_land": True,
        "institutional_landholder": False,
        "constitutional_post": False,
        "political_position": False,
        "government_employee": False,
        "pension_10000_or_more": False,
        "income_tax_payer": False,
        "practising_professional": False,
        "nri_family": False,
        "land_acquired_after_cutoff": False,
        "land_transfer_due_to_death": False
    }


def test_no_post_cutoff_transfer():
    profile = create_valid_profile()

    result = check_pm_kisan_eligibility(profile)

    assert result["status"] == "POTENTIALLY ELIGIBLE"


def test_inherited_land_after_cutoff():
    profile = create_valid_profile()
    profile["land_acquired_after_cutoff"] = True
    profile["land_transfer_due_to_death"] = True

    result = check_pm_kisan_eligibility(profile)

    assert result["status"] == "POTENTIALLY ELIGIBLE"


def test_other_land_transfer_after_cutoff():
    profile = create_valid_profile()
    profile["land_acquired_after_cutoff"] = True
    profile["land_transfer_due_to_death"] = False

    result = check_pm_kisan_eligibility(profile)

    assert result["status"] == "NOT ELIGIBLE"


def test_income_tax_exclusion():
    profile = create_valid_profile()
    profile["income_tax_payer"] = True

    result = check_pm_kisan_eligibility(profile)

    assert result["status"] == "NOT ELIGIBLE"


def test_missing_land_information():
    profile = create_valid_profile()
    profile["has_cultivable_land"] = None

    result = check_pm_kisan_eligibility(profile)

    assert result["status"] == "NEED MORE INFORMATION"


if __name__ == "__main__":
    test_no_post_cutoff_transfer()
    test_inherited_land_after_cutoff()
    test_other_land_transfer_after_cutoff()
    test_income_tax_exclusion()
    test_missing_land_information()

    print("PASS: All 5 eligibility tests passed.")
