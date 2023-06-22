from account.models import User
from account.models.professional import Professional
from conftest import USER_INFORMATION
from reservation.models import PriceList
import pytest

JOB_NAME = "Hair cut"
JOB_PRICE = 100


def save_job(new_job: PriceList):
    new_job.professional.save()
    new_job.save()


@pytest.fixture
def create_and_save_single_job(create_professional_job):
    def _factory(professional, job_name, price):
        job: PriceList = create_professional_job(professional=professional, job_name=job_name, price=price)
        save_job(job)
        return job
    return _factory


@pytest.fixture
def create_and_save_jobs(create_professional, create_and_save_single_job):
    professional: Professional = create_professional(
        phone_number=USER_INFORMATION.get('phone_number')[2],
        password=USER_INFORMATION.get('password')[2],
        email=USER_INFORMATION.get('email')[2],
        user_type=User.UserType.PROFESSIONAL
    )
    job1 = create_and_save_single_job(professional=professional, job_name="Gel nail polish", price=90)
    job2 = create_and_save_single_job(professional=professional, job_name="Nail polish", price=50)
    return {'job1': job1, 'job2': job2}


@pytest.mark.django_db()
class TestTypeOfJobModel:
    def test_create_job(self, create_professional, create_professional_job):
        professional: Professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],
            user_type=User.UserType.PROFESSIONAL
        )
        job = create_professional_job(professional=professional, job_name=JOB_NAME, price=JOB_PRICE)
        assert job.professional == professional
        assert job.job_name == JOB_NAME
        assert job.price == JOB_PRICE

    def test_save_job(self, create_professional, create_professional_job):
        professional: Professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],
            user_type=User.UserType.PROFESSIONAL
        )
        job = create_professional_job(professional=professional, job_name=JOB_NAME, price=JOB_PRICE)
        assert job in PriceList.objects.all()

    def test_delete_job(self, create_professional, create_professional_job):
        professional: Professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],
            user_type=User.UserType.PROFESSIONAL
        )
        job = create_professional_job(professional=professional, job_name=JOB_NAME, price=JOB_PRICE)
        job.delete()
        assert job not in PriceList.objects.all()

    def test_delete_professional(self, create_professional, create_professional_job):
        professional: Professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],
            user_type=User.UserType.PROFESSIONAL
        )
        job = create_professional_job(professional=professional, job_name=JOB_NAME, price=JOB_PRICE)
        job.professional.delete()
        assert job not in PriceList.objects.all()

    def test_get_all_jobs_attributes_by_professional(self, create_and_save_jobs):
        jobs: dict = create_and_save_jobs
        professional = jobs['job1'].professional
        expected_result = []
        for job in jobs.values():
            expected_result.append((job.job_name, job.price))
        assert expected_result == list(PriceList.get_type_of_jobs_name_and_price_list(professional=professional))
