import asyncio

import aiohttp

from schemas.workers import WorkerOnFireDTO
from secret import SendEmailDTO, token


def getFireText(worker: WorkerOnFireDTO) -> str:
    return (
        f"Здравствуйте, {worker.surname} {worker.name} ({worker.username}).\n"
        f"К сожалению, мы вынужденые сообщить, что вы уволены из нашей компании по причине: {worker.fire_reason}."
    )


async def send_email(worker: WorkerOnFireDTO) -> None:
    send_email_dto = SendEmailDTO(text=getFireText(worker))

    async with aiohttp.ClientSession() as session:
        send_dict = send_email_dto.model_dump()
        response = await session.post(
            url="https://api.mailopost.ru/v1/email/messages",
            json=send_dict,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            })
        print(await response.json())
