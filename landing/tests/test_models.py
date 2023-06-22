from typing import Callable

import pytest

from account.models import User
from conftest import BIRTHDAY
from landing.models import TeamMember

TEAM_MEMBER_NAME = 'Guy Beckenstein'


@pytest.mark.django_db
class TestTeamMemberModel:
    def test_add_team_member(self, create_user, create_team_member: Callable[[str], TeamMember]):
        user: User = create_user(
            phone_number='972541234',
            password='123456',
            email='john1@doe.com',
            date_of_birth=BIRTHDAY,
            user_type=User.UserType.CLIENT,

            first_name='John',
            last_name='Doe',
            country='United Kingdom',
            city='London',
            address='Address'
        )
        name = f'{user.first_name} {user.last_name}'
        team_member = create_team_member(name)
        team_member.save()
        assert team_member in TeamMember.objects.all()

    def test_remove_team_member(self):
        assert TeamMember.get_member(name=TEAM_MEMBER_NAME).delete() not in TeamMember.objects.all()

    def test_str_method(self, create_user, create_team_member: Callable[[str], TeamMember]):
        user: User = create_user(
            phone_number='972541234',
            password='123456',
            email='john1@doe.com',
            date_of_birth=BIRTHDAY,
            user_type=User.UserType.CLIENT,

            first_name='John',
            last_name='Doe',
            country='United Kingdom',
            city='London',
            address='Address'
        )
        name = f'{user.first_name} {user.last_name}'
        team_member = create_team_member(name)
        assert name == str(team_member)
