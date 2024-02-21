import asyncio
from datetime import datetime, timedelta
from data_recording import AsyncRecorder
from schemas import SuperUser, Urls
from config import (
    AUTHORIZATION_URL,
    GET_TOKENS_URL,
    POST_ASSET_URL,
    POST_OPERATION_URL,
    GET_INSTRUMENT_LIST,
    SUPER_USER_MAIL,
    SUPER_USER_PASSWORD,
)


async def main():
    urls = Urls(
        authorization_url=AUTHORIZATION_URL,
        get_tokens_url=GET_TOKENS_URL,
        post_asset_url=POST_ASSET_URL,
        post_operation_url=POST_OPERATION_URL,
        get_instrument_list=GET_INSTRUMENT_LIST,
    )
    super_user = SuperUser(email=SUPER_USER_MAIL, password=SUPER_USER_PASSWORD)
    recorder = AsyncRecorder(urls=urls, super_user=super_user)
    while True:
        await asyncio.sleep(0.33)
        if datetime.now().minute == 0 and datetime.now().second == 1:
            print(datetime.now())
            await asyncio.create_task(recorder.authorization())
            users = await asyncio.create_task(recorder.get_tokens())
            asset_reqs = [recorder.set_assets(i) for i in users]
            position_reqs = [recorder.set_operation(i) for i in users]
            results_asset_recording = await asyncio.gather(
                *asset_reqs, return_exceptions=True
            )
            results_position_recording = await asyncio.gather(
                *position_reqs, return_exceptions=True
            )
            exceptions_asset_recording = [
                res for res in results_asset_recording if isinstance(res, Exception)
            ]
            exceptions_position_recording = [
                res for res in results_position_recording if isinstance(res, Exception)
            ]
            successful_results_asset = [
                res for res in results_asset_recording if not isinstance(res, Exception)
            ]
            successful_results_position = [
                res
                for res in results_position_recording
                if not isinstance(res, Exception)
            ]
            print("Errors in asset recording: \n", exceptions_asset_recording)
            print("Successfully recorded assets: \n", successful_results_asset)
            print("Errors in recording positions: \n", exceptions_position_recording)
            print("Successfully recorded positions: \n", successful_results_position)


if __name__ == "__main__":
    asyncio.run(main=main())
