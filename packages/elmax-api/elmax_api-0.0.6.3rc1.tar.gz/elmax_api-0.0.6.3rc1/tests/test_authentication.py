"""Test the authentication process."""

import pytest
import asyncio
from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import ElmaxLocal, Elmax
from tests import client, LOCAL_TEST, LOCAL_API_URL, PANEL_PIN

BAD_USERNAME = "thisIsWrong@gmail.com"
BAD_PASSWORD = "fakePassword"


@pytest.mark.asyncio
async def test_wrong_credentials():
    client = Elmax(username=BAD_USERNAME, password=BAD_PASSWORD) if LOCAL_TEST != "true" else ElmaxLocal(
        panel_api_url=LOCAL_API_URL, panel_code=PANEL_PIN)
    with pytest.raises(ElmaxBadLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_good_credentials():
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)

    username = client.get_authenticated_username()
    # TODO: parametrize the following control
    #assert username == USERNAME


@pytest.mark.asyncio
async def test_token_renew():
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)
    old_expiration = client.token_expiration_time

    await asyncio.sleep(60)

    new_jwt_data = await client.renew_token()
    assert isinstance(new_jwt_data, dict)
    new_expiration = client.token_expiration_time

    assert new_expiration >= old_expiration + 60

