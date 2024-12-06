# -*- coding: utf-8 -*-
"""Unit tests for transcript endpoints"""

import pytest
import json
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import RevAiApiDeploymentConfigMap, RevAiApiDeployment
from src.rev_ai.models.asynchronous import Transcript, Monologue, Element
from src.rev_ai.models.asynchronous.group_channels_type import GroupChannelsType

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
TOKEN = "token"
SPEECH_TO_TEXT_URL = f"{RevAiApiDeploymentConfigMap[RevAiApiDeployment.US]['base_url']}/speechtotext/v1/"
URL = urljoin(SPEECH_TO_TEXT_URL, 'jobs/{}/transcript'.format(JOB_ID))


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestTranscriptEndpoints():
    @pytest.mark.parametrize(
        'group_channels_by, group_channels_threshold_ms',
        [(None, None), (GroupChannelsType.SENTENCE, 5000), (GroupChannelsType.WORD, 2000)]
    )
    def test_get_transcript_text(
        self,
        mock_session,
        make_mock_response,
        group_channels_by,
        group_channels_threshold_ms
    ):
        data = 'Test'
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'text/plain'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response
        expected_url = URL
        if group_channels_by and group_channels_threshold_ms:
            expected_url += f"?group_channels_by={group_channels_by}&group_channels_threshold_ms={group_channels_threshold_ms}"

        res = client.get_transcript_text(JOB_ID, group_channels_by=group_channels_by, group_channels_threshold_ms=group_channels_threshold_ms)

        assert res == data
        mock_session.request.assert_called_once_with("GET",
                                                     expected_url,
                                                     headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_text(id)

    @pytest.mark.parametrize(
        'group_channels_by, group_channels_threshold_ms',
        [(None, None), (GroupChannelsType.SENTENCE, 5000), (GroupChannelsType.WORD, 2000)]
    )
    def test_get_transcript_text_as_stream(
        self,
        mock_session,
        make_mock_response,
        group_channels_by,
        group_channels_threshold_ms
    ):
        data = 'Test'
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'text/plain'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response
        expected_url = URL
        if group_channels_by and group_channels_threshold_ms:
            expected_url += f"?group_channels_by={group_channels_by}&group_channels_threshold_ms={group_channels_threshold_ms}"

        res = client.get_transcript_text_as_stream(JOB_ID, group_channels_by=group_channels_by, group_channels_threshold_ms=group_channels_threshold_ms)

        assert res.content == data
        mock_session.request.assert_called_once_with("GET",
                                                     expected_url,
                                                     headers=expected_headers,
                                                     stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_as_stream_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_text_as_stream(id)

    @pytest.mark.parametrize(
        'group_channels_by, group_channels_threshold_ms',
        [(None, None), (GroupChannelsType.SENTENCE, 5000), (GroupChannelsType.WORD, 2000)]
    )
    def test_get_transcript_json(
        self,
        mock_session,
        make_mock_response,
        group_channels_by,
        group_channels_threshold_ms
    ):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = json.loads(json.dumps(data))
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response
        expected_url = URL
        if group_channels_by and group_channels_threshold_ms:
            expected_url += f"?group_channels_by={group_channels_by}&group_channels_threshold_ms={group_channels_threshold_ms}"

        res = client.get_transcript_json(JOB_ID, group_channels_by=group_channels_by, group_channels_threshold_ms=group_channels_threshold_ms)

        assert res == expected
        mock_session.request.assert_called_once_with(
            "GET", expected_url, headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_json(id)

    @pytest.mark.parametrize(
        'group_channels_by, group_channels_threshold_ms',
        [(None, None), (GroupChannelsType.SENTENCE, 5000), (GroupChannelsType.WORD, 2000)]
    )
    def test_get_transcript_json_as_stream(
        self,
        mock_session,
        make_mock_response,
        group_channels_by,
        group_channels_threshold_ms
    ):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = json.loads(json.dumps(data))
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response
        expected_url = URL
        if group_channels_by and group_channels_threshold_ms:
            expected_url += f"?group_channels_by={group_channels_by}&group_channels_threshold_ms={group_channels_threshold_ms}"

        res = client.get_transcript_json_as_stream(JOB_ID, group_channels_by=group_channels_by, group_channels_threshold_ms=group_channels_threshold_ms)

        assert json.loads(res.content.decode('utf-8').replace("\'", "\"")) == expected
        mock_session.request.assert_called_once_with(
            "GET", expected_url, headers=expected_headers, stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_as_stream_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_json_as_stream(id)

    @pytest.mark.parametrize(
        'group_channels_by, group_channels_threshold_ms',
        [(None, None), (GroupChannelsType.SENTENCE, 5000), (GroupChannelsType.WORD, 2000)]
    )
    def test_get_transcript_object_with_success(
        self,
        mock_session,
        make_mock_response,
        group_channels_by,
        group_channels_threshold_ms
    ):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = Transcript([Monologue(1, [Element('text', 'Hello', 0.75, 1.25, 0.85)])])
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response
        expected_url = URL
        if group_channels_by and group_channels_threshold_ms:
            expected_url += f"?group_channels_by={group_channels_by}&group_channels_threshold_ms={group_channels_threshold_ms}"

        res = client.get_transcript_object(JOB_ID, group_channels_by=group_channels_by, group_channels_threshold_ms=group_channels_threshold_ms)

        assert res == expected
        mock_session.request.assert_called_once_with(
            "GET", expected_url, headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_object_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_object(id)
