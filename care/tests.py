from datetime import date
from unittest.mock import patch

import care.services
import pytest
from rest_framework.exceptions import ValidationError

from care.models import CareTaskLog
from care.services import mark_task_as_done, send_daily_care


@pytest.mark.django_db
def test_mark_task_as_done_success(care_task, mocker):
    mock_update = mocker.patch.object(care_task, 'update_next_due')

    assert care_task.last_done is None

    updated_task = mark_task_as_done(care_task, notes='Обильный тестовый полив')

    assert updated_task.last_done == date.today()

    assert CareTaskLog.objects.filter(care_task=care_task).count() == 1

    mock_update.assert_called_once_with()


@pytest.mark.django_db
def test_mark_task_is_inactive(care_task):
    care_task.is_active = False
    care_task.save()

    with pytest.raises(ValidationError) as exc:
        mark_task_as_done(care_task)

    assert "неактивн" in str(exc.value).lower()


@pytest.mark.django_db
def test_mark_task_already_done(care_task):
    care_task.last_done = date.today()
    care_task.save()

    with pytest.raises(ValidationError) as exc:
        mark_task_as_done(care_task)

    assert "уже выполнен" in str(exc.value).lower()

@pytest.mark.django_db
def test_send_daily_care_empty_return_false(user):
    result =  send_daily_care(user, due_tasks=[])
    assert result is False

@pytest.mark.django_db
@patch('care.services.send_mail')
def test_send_daily_care_success(mock_send_mail, user, care_task):
    mock_send_mail.return_value = 1

    result = send_daily_care(user, due_tasks=[care_task])

    assert result is True
    assert mock_send_mail.call_count == 1

    args, kwargs = mock_send_mail.call_args
    assert user.email in kwargs['recipient_list']
    assert "напоминание" in kwargs['subject']


@pytest.mark.django_db
@patch('care.services.send_mail')
def test_send_daily_care_fail(mock_send_mail, user, care_task):
    mock_send_mail.side_effect = Exception('SMTP error')

    result = send_daily_care(user, due_tasks=[care_task])

    assert result is False
