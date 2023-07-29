from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client as xxx
from .api import *
db = xxx("data.sqlite", 'fuck')
def check_user(user_id):
    users = db.get(f"user_{user_id}_gift")
    now = time.time()    
    WAIT_TIME = 6
    if  db.exists(f"user_{user_id}_gift"):
        last_time = users['time']
        elapsed_time = now - last_time
        if elapsed_time < WAIT_TIME:
            remaining_time = WAIT_TIME - elapsed_time
            return int(remaining_time)
        else:
            
            users['time'] = now
            db.set(f'user_{user_id}_gift', users)
            return None
    else:
        users = {}
        users['time'] = now
        db.set(f'user_{user_id}_gift', users)
        return None

@app.on_callback_query(filters.regex("^userbot$"))
async def dailygiftt(app,query):
    user_id = query.from_user.id
    chats = db.get('force')
    force_msg = str(db.get("force_msg"))
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''{force_msg}\n\n• @{i}'''
        return await query.edit_message_text(k, reply_markup=mk([[btn(f'اضغط هنا للاشتراك 🧬', url=f't.me/{i}')]]))
    import datetime
    keys = mk(
        [
            [btn(text='رجوع', callback_data='back_invite')]
        ]
    )
    x = check_user(query.from_user.id)
    
    if x !=None:
        duration = datetime.timedelta(seconds=x)
        now = datetime.datetime.now()
        target_datetime = now + duration
        date_str = target_datetime.strftime('%Y/%m/%d')
        await query.answer('انتظر 3 ثواني قبل انت تضغط مره اخري ⏰', show_alert=True)
        return
    else:
        user_info = db.get(f'user_{user_id}')
        coin_msg = str(db.get("coin_msg"))
        await app.delete_messages(query.message.chat.id, query.message.id)
        users_bot = int(db.get("users_bot")) if db.exists("users_bot") else 10
        ask = await app.ask(user_id, f'•︙جيد ، الان ارسل عدد رشق المستخدمين التي ترريدها\n\n•︙سعر كل مستخدم = {users_bot} {coin_msg}\n',filters=filters.user(user_id))
        if ask.text:
            try:
                count = int(ask.text)
            except:
                await ask.reply("برجاء ارسال رقم فقط ، اعد المحاولة مره اخري")
                return
            
            ask1 = await app.ask(user_id, 'جيد جدا ، الان ارسل معرف البوت وليس الرابط ',filters=filters.user(user_id))
            if ask1.text and "@" in ask1.text:
                channel = ask1.text
                tex = "/start"
                try:
                    inf = await app.get_chat(channel)
                    if str(inf.type) == 'ChatType.BOT':
                        type = 'bot'
                        channel = ask1.text
                    else:
                        type = 'channel'
                        channel = ask1.text
                except:
                    await ask1.reply(f"رجاء تاكد من صحة معرف البوت")
                    return
            x = count * int(users_bot) / 2
            if int(x) > int(user_info['coins']):
                await ask1.reply(f" للاسف نقاطك غير كافية ، تحتاج الي : {x}")
                return
            ses = db.get("sessions")
            y = 0
            for i in range(count):
                try:
                    o = await sendbot(ses[i], str(channel), str(tex), str(type))
                except:
                    continue
                if o:
                    y+=1
            for i in range(y):
                user_info['coins'] = int(user_info['coins']) - int(users_bot) 
            idrec = db.get("id_requests") + 1
            db.set("id_requests", int(idrec))
            bef = db.get("requests") + 1
            db.set("requests", int(bef))
            db.set(f"user_{user_id}", user_info)
            await ask1.reply(f"•︙ تم إكتمال طلبك بنجاح ✅\n\n•︙تفاصيل عن طلبك  ⬇️\n\n•︙الطـIDـلـب : {idrec}\n•︙رقم الطلب : {bef}\n•︙العدد المطلوب : {count}\n•︙العدد المكتمل : {y}\n•︙رابط البوت المستخدم : {ask1.text}")
            return