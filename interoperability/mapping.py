def map_revenue_data(data):
    return {
        "master_citizen_id": f"MHC-{data.get('citizen_code', 'UNKNOWN')}",
        "full_name": data.get("full_name"),
        "annual_income": data.get("income_value"),
        "residence": data.get("residence"),
        "source_department": "REVENUE",
        "verified": True,
    }


def map_education_data(data):
    return {
        "master_citizen_id": f"MHC-{data.get('student_id', 'UNKNOWN')}",
        "full_name": data.get("student_name"),
        "education_course": data.get("course"),
        "institution": data.get("institution"),
        "source_department": "EDUCATION",
        "verified": True,
    }


def map_health_data(data):
    return {
        "master_citizen_id": f"MHC-{data.get('patient_ref', 'UNKNOWN')}",
        "full_name": data.get("name"),
        "benefit_status": data.get("scheme_status"),
        "source_department": "HEALTH",
        "verified": True,
    }