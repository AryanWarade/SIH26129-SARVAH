import requests

from .mapping import (
    map_revenue_data,
    map_education_data,
    map_health_data,
)


class DepartmentAPIAdapter:

    BASE_URL = "http://127.0.0.1:8000/api/interoperability/"

    @classmethod
    def get_revenue_data(cls, citizen_code="MH1001"):

        url = cls.BASE_URL + "revenue/citizen/"

        response = requests.get(
            url,
            params={"citizen_code": citizen_code},
            timeout=5,
        )

        response.raise_for_status()

        return map_revenue_data(response.json())

    @classmethod
    def get_education_data(cls, student_id="EDU5501"):

        url = cls.BASE_URL + "education/citizen/"

        response = requests.get(
            url,
            params={"student_id": student_id},
            timeout=5,
        )

        response.raise_for_status()

        return map_education_data(response.json())

    @classmethod
    def get_health_data(cls, patient_ref="HLT8801"):

        url = cls.BASE_URL + "health/citizen/"

        response = requests.get(
            url,
            params={"patient_ref": patient_ref},
            timeout=5,
        )

        response.raise_for_status()

        return map_health_data(response.json())