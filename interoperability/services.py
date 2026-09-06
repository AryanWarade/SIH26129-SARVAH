from .adapters import DepartmentAPIAdapter


class InteroperabilityService:

    @staticmethod
    def fetch_revenue_data(citizen_code="MH1001"):
        return DepartmentAPIAdapter.get_revenue_data(
            citizen_code
        )

    @staticmethod
    def fetch_education_data(student_id="EDU5501"):
        return DepartmentAPIAdapter.get_education_data(
            student_id
        )

    @staticmethod
    def fetch_health_data(patient_ref="HLT8801"):
        return DepartmentAPIAdapter.get_health_data(
            patient_ref
        )

    @staticmethod
    def fetch_all_demo_data():

        revenue = InteroperabilityService.fetch_revenue_data()
        education = InteroperabilityService.fetch_education_data()
        health = InteroperabilityService.fetch_health_data()

        return {
            "revenue": revenue,
            "education": education,
            "health": health,
        }