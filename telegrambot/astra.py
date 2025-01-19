from telethon.sync import TelegramClient, events
from telethon.tl import types
import asyncio

api_id = '9040052'
api_hash = '99d26ac62559b43d4b8835063f67e763'
source_invite_link_1 = "https://t.me/+RwruW3POM2FmYjQ5"
destination_invite_link_1 = "https://t.me/+A8mswUv1lKthM2Nk"
source_invite_link_2 = "https://t.me/joinchat/AAAAAEp-9Wy82vc3BXhLTA"
destination_invite_link_2 = 'https://t.me/+PICj7ZXjcJhmM2Y8'

source_invite_link_3 = "https://t.me/+Uws81NYVI1gwMGYx" #delta
destination_invite_link_3 = 'https://t.me/+Ij4JwFhgKMRiNjE0'





excluded_keywords = ['igenius', 'lds', 'fxpro', 'Fx', "FX", "Iota", "IGENIUS", "LDS", "FXPRO", "Resistance", "live"]

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        source_channel_1 = await client.get_entity(source_invite_link_1)
        destination_channel_1 = await client.get_entity(destination_invite_link_1)
        
        source_channel_2 = await client.get_entity(source_invite_link_2)
        destination_channel_2 = await client.get_entity(destination_invite_link_2)

        source_channel_3 = await client.get_entity(source_invite_link_3)
        destination_channel_3 = await client.get_entity(destination_invite_link_3)

        
        @client.on(events.NewMessage(chats=[source_channel_1]))
        async def handle_new_message(event):
            message = event.message
            should_forward = True
            
            if message.text:
                if any(keyword in message.text for keyword in excluded_keywords):
                    should_forward = False
                elif any(url in message.text for url in ["http://", "https://", ".com", ".fr", ".de", ".biz", ".eu"]):
                    should_forward = False
                
            if should_forward:
                if message.media and not message.text:  # Vérifier si c'est seulement une image
                    await client.forward_messages(destination_channel_1, message)
                elif message.text:
                    await client.send_message(destination_channel_1, message.text)

        @client.on(events.NewMessage(chats=[source_channel_2]))
        async def handle_new_message(event):
            message = event.message
            should_forward = True
            
            if message.text:
                if any(keyword in message.text for keyword in excluded_keywords):
                    should_forward = False
                elif any(url in message.text for url in ["http://", "https://", ".com", ".fr", ".de", ".biz", ".eu"]):
                    should_forward = False
                
            if should_forward:
                if message.media and not message.text:  # Vérifier si c'est seulement une image
                    await client.forward_messages(destination_channel_2, message)
                elif message.text:
                    await client.send_message(destination_channel_2, message.text)


        @client.on(events.NewMessage(chats=[source_channel_3]))
        async def handle_new_message(event):
            message = event.message
            should_forward = True
            
            if message.text:
                if any(keyword in message.text for keyword in excluded_keywords):
                    should_forward = False
                elif any(url in message.text for url in ["http://", "https://", ".com", ".fr", ".de", ".biz", ".eu"]):
                    should_forward = False
                
            if should_forward:
                if message.media and not message.text:  # Vérifier si c'est seulement une image
                    await client.forward_messages(destination_channel_3, message)
                elif message.text:
                    await client.send_message(destination_channel_3, message.text)


        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())