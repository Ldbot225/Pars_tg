from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import pandas as pd
import asyncio

# Подставьте сюда ваш API ID и API Hash, полученные от Telegram
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=lambda: phone)
    print("Клиент авторизован.")
    
    # Получение списка диалогов
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=100,
        hash=0
    ))

    groups = [g for g in result.chats if getattr(g, 'megagroup', False)]

    print('[+] Выберите группу для парсинга участников:')
    for i, g in enumerate(groups):
        print(f'[{i}] - {g.title}')
    
    g_index = int(input("[+] Введите номер группы: "))
    target_group = groups[g_index]

    all_participants = []
    async for user in client.iter_participants(target_group.id):
        if user.phone:
            phone_number = user.phone
        else:
            phone_number = 'Номер не указан или скрыт'
        all_participants.append({
            'id': user.id,
            'username': '@' + user.username if user.username else 'None',
            'phone': phone_number
        })
        print(user.id, user.username, phone_number)

    # Сохранение данных в CSV файл
    df = pd.DataFrame(all_participants)
    df.to_csv('Users.csv', index=False)
    print('Участники сохранены в файл "Users.csv"')

    # Запись логов в текстовый файл
    with open('logs.txt', 'a') as file:
        for participant in all_participants:
            file.write(f"{participant['id']} {participant['username']} {participant['phone']}\n")
    print('Логи сохранены в файл "logs.txt"')

# Для исполнения в Jupyter Notebook или других средах, где используется уже запущенный цикл событий
import nest_asyncio
nest_asyncio.apply()
await main()  # Используем await напрямую без вызова get_event_loop()
