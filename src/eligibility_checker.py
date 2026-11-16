
def check_pm_kisan_eligibility(profile):
    """
    Preliminary PM-KISAN eligibility assessment.
    True = Yes, False = No, None = Unknown.
    """

    # Check basic landholding requirement
    land_owned = profile.get("has_cultivable_land")

    if land_owned is False:
        return {
            "status": "NOT ELIGIBLE",
            "reason": "The farmer family does not have cultivable land recorded in its name."
        }

    if land_owned is None:
        return {
            "status": "NEED MORE INFORMATION",
            "reason": "We need to know whether the farmer family has cultivable land recorded in its name."
        }

    # Official exclusion categories
    exclusions = {
        "institutional_landholder": "The land is held by an institution.",
        "constitutional_post": "A family member holds or has held a constitutional post.",
        "political_position": "A family member belongs to an excluded political category.",
        "government_employee": "A family member belongs to an excluded government employment category.",
        "pension_10000_or_more": "A family member receives an excluded government pension of ₹10,000 or more per month.",
        "income_tax_payer": "A family member paid income tax in the last assessment year.",
        "practising_professional": "A family member is an excluded practising registered professional.",
        "nri_family": "The farmer family falls under the NRI exclusion."
    }

    # Check exclusion answers
    for field, reason in exclusions.items():
        answer = profile.get(field)

        if answer is True:
            return {
                "status": "NOT ELIGIBLE",
                "reason": reason
            }

    # Check for missing exclusion answers
    missing = [
        field for field in exclusions
        if profile.get(field) is None
    ]

    if missing:
        return {
            "status": "NEED MORE INFORMATION",
            "reason": "Some exclusion-related information is missing.",
            "missing_fields": missing
        }

    # Check land acquisition information
    land_acquisition = profile.get("land_acquired_after_cutoff")

    if land_acquisition is None:
        return {
            "status": "NEED MORE INFORMATION",
            "reason": "We need to know whether the land was acquired after 1 February 2019."
        }

    if land_acquisition is True:
        return {
            "status": "NEED MORE INFORMATION",
            "reason": "This land acquisition case requires official verification. Please check the PM-KISAN portal."
        }

    return {
        "status": "ELIGIBLE",
        "reason": (
            "No exclusion was identified from the information provided. "
            "Final eligibility is subject to government verification."
        )
    }



def get_yes_no_answer(question):
    while True:
        answer = input(question + " (yes/no/not sure): ").strip().lower()

        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        elif answer in ["not sure", "unsure", ""]:
            return None
        else:
            print("Please enter yes, no, or not sure.")


def collect_user_profile():
    print("\nPM-KISAN Eligibility Questions")
    print("--------------------------------")

    profile = {}

    profile["has_cultivable_land"] = get_yes_no_answer(
        "Does your farmer family have cultivable land recorded in its name?"
    )

    questions = {
        "institutional_landholder": "Is the land held by an institution?",
        "constitutional_post": "Does a family member fall under the excluded constitutional post category?",
        "political_position": "Does a family member fall under an excluded political category?",
        "government_employee": "Does a family member fall under an excluded government employment category?",
        "pension_10000_or_more": "Does a family member receive an excluded government pension of ₹10,000 or more per month?",
        "income_tax_payer": "Did a family member pay income tax in the last assessment year?",
        "practising_professional": "Is a family member an excluded practising registered professional?",
        "nri_family": "Does the farmer family fall under the NRI exclusion?"
    }

    for field, question in questions.items():
        profile[field] = get_yes_no_answer(question)

    profile["land_acquired_after_cutoff"] = get_yes_no_answer(
        "Was the land acquired after 1 February 2019?"
    )

    return profile


if __name__ == "__main__":

    print("NammaSarkara AI")
    print("PM-KISAN Eligibility Assessment")

    user_profile = collect_user_profile()

    result = check_pm_kisan_eligibility(user_profile)

    print("\nEligibility Assessment Result")
    print("--------------------------------")
    print("Status:", result["status"])
    print("Reason:", result["reason"])

    if "missing_fields" in result:
        print("Missing information:", result["missing_fields"])



   