from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from utilis import main_keyboard
from telegram.ext import ConversationHandler

def anketa_start(update, context):
    update.message.reply_text(
        'Привет как вас зовут?',
        reply_markup = ReplyKeyboardRemove()
    )
    return 'name'

def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text(
            'Введите Имя и Фамилию'
        ) 
        return 'name'
    else:
        context.user_data['anketa'] = {'name' : user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Оцените приложение от 1 до 5', 
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'

def anketa_rating(update, context):
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text(
        'Оставьте комментарий или нажмите /skip, чтобы пропустить'
    )
    return 'comment'

def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup = main_keyboard() ,parse_mode = ParseMode.HTML )
    return ConversationHandler.END
    
def anketa_skip(update, context):
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup = main_keyboard() ,parse_mode = ParseMode.HTML )
    return ConversationHandler.END

def format_anketa(anketa):
    user_text = f'''<b>Имя и Фамилия</b>: {anketa['name']}
<b>Оценка</b> : {anketa['rating']}
'''
    if 'comment' in anketa:
        user_text += f"<b>Комментарий</b>: {anketa['comment']}"
    return user_text

def anketa_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю. Следуйте интсрукции!')
