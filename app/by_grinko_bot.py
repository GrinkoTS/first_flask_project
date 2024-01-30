import telebot
import app.models as m
import config
from app import app

# импортируем токен tg-бота
TOKEN = config.API_token
bot = telebot.TeleBot(TOKEN)

def notification(product):
    bot.send_message(chat_id=config.tg_id, text=f'Внимание! У нас новый заказ на {product}')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message)
    bot.reply_to(message,f'Привет! Я помогу тебе сделать заказ волшебного изделия и ' 
                         f'получить максимум привилегий в нашей Программе лояльности!\n\n'
                         f'Нажмите /email для поиска тебя в базе клиентов')

@bot.message_handler(commands=['email'])
def check_email(message):
    bot.send_message(message.chat.id, f'Напиши свой email')

@bot.message_handler(commands=['product'])
def check_email(message):
    bot.send_message(message.chat.id, f'Опиши жедаемое изделие \n'
                     f'Например: разноцветная шапка, цветочный жилет и тд')

n_flag=False
@bot.message_handler(content_types=["text"])
def sleep_text(message):
    global n_flag
    if '@' in message.text or n_flag==False:
        email_user = message.text
        with app.app_context():
            user = m.db.session.query(m.Users).filter(m.Users.email == f'{email_user}').first()
        if user:
            n_flag = True
            bot.reply_to(message, 'Нажми /product и расскажи, какое изделие ты хотел бы заказать')
            try:
                with app.app_context():
                    User_pr = m.Products(user_tg_id=message.from_user.id, user_id=user.id)
                    m.db.session.add(User_pr)
                    m.db.session.commit()
            except:
                with app.app_context():
                    m.db.session.rollback()
        else:
            bot.reply_to(message, 'Не нашли твой email в базе данных, попробуй еще раз /email')

    elif n_flag == True:
        product = message.text
        user_tg_id = message.from_user.id
        try:
            with app.app_context():
                user_pr = m.db.session.query(m.Products).filter(m.Products.user_tg_id == f'{user_tg_id}').first()
                user_pr.products = product
                m.db.session.add(user_pr)
                m.db.session.commit()
        except:
            with app.app_context():
                m.db.session.rollback()

        bot.reply_to(message,
                     f'Спасибо! Данные о твоем заказе успешно записаны и я направил оповещение хазяйке медной горы')
        notification(product)





bot.polling()




