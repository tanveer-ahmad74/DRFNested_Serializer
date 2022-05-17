from django.test import TestCase
from model_bakery import baker
from datetime import datetime
from api.models import Profile, Hobby, Job


class TestProfile(TestCase):

    def test_case_of_models(self):
        profile = baker.make('Profile')
        hobby = baker.make('Hobby')
        job = baker.make('Job')
        assert profile
        assert hobby
        assert job

    def test_profile_models_fields(self):
        person = baker.make(
            Profile,
            name='ali',
            email='ali@gmail.com',
            mobile_number='03047478515',
            status=True
        )
        assert person.name=='ali'
        assert person.email== 'ali@gmail.com'
        assert person.status
        assert isinstance(person.created_at, datetime)

    def test_Hobby_models_fields(self):
        person = baker.make(Profile, name='ali', email='ali@gmail.com', mobile_number='03047478515', status=True)
        hobby = baker.make(Hobby, user=person, name='Reading')
        assert person.name == 'ali'
        assert hobby.name == 'Reading'
        assert isinstance(hobby.created_at, datetime)
        assert isinstance(hobby.updated_at, datetime)

    def test_Job_models_fields(self):
        person = baker.make(Profile, name='ali', email='ali@gmail.com', mobile_number='03047478515', status=True)
        job = baker.make(Job, user=person, name='Teaching')
        assert person.name == 'ali'
        assert job.name == 'Teaching'
        assert isinstance(job.created_at, datetime)
        assert isinstance(job.updated_at, datetime)


