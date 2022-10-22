import os

import telebot
from telebot import types

from apps.recipes.models import Recipe
from apps.users.models import GenderChoices, Profile

API_KEY = os.environ.get("TELEGRAM_BOT_API_KEY")
bot = telebot.TeleBot(API_KEY)


def get_keyboard(keyboard_type: str = "main_menu"):
    recipes = Recipe.objects.all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if keyboard_type == "main_menu":
        markup.add(types.KeyboardButton("About me"))
        markup.add(types.KeyboardButton("Recipes"))
    elif keyboard_type == "recipes":
        for recipe in recipes:
            markup.add(types.KeyboardButton(recipe.title))
    return markup


def process_name_step(message):
    try:
        profile = Profile.objects.filter(external_id=message.from_user.id).first()

        if profile:  # Update the name if profile already exists
            profile.name = message.text
            profile.save(update_fields=["name"])
        else:
            Profile.objects.create(
                external_id=message.from_user.id,
                username=message.from_user.username,
                name=message.text,
            )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(*GenderChoices.names)

        msg = bot.reply_to(message, "Please, specify your gender", reply_markup=markup)
        bot.register_next_step_handler(msg, process_gender_step)
    except Exception as e:
        print(f"[ERROR] {e}")
        bot.reply_to(message, "Oops, something's went wrong with the name assignment")


def process_gender_step(message):
    try:
        gender = message.text
        if gender in GenderChoices.names:
            profile = Profile.objects.get(external_id=message.from_user.id)
            profile.gender = GenderChoices[gender]
            profile.save(update_fields=["gender"])
        else:
            raise ValueError(f'User {message.from_user.id} picked unknown gender: "{message.text}"')

        bot.send_message(
            message.chat.id,
            "Now you are able to navigate the main menu.",
            reply_markup=get_keyboard("main_menu"),
        )
    except Profile.DoesNotExist:
        bot.reply_to(message, "Seems like the profile does not exist yet, try '/start' command.")
    except Exception as e:
        print(f"[ERROR] {e}")
        bot.reply_to(message, "Oops, something's went wrong with the gender assignment")


@bot.message_handler(commands=["help"])
def send_greeting(message):
    bot.reply_to(
        message,
        "I'm CookBookBot and I store some interesting recipes for you\n\n"
        "You can control me by sending these commands:\n\n"
        "/start - introduce yourself (update profile info)\n"
        "/menu - enter the main menu",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(commands=["start"])
def send_greeting(message):
    msg = bot.reply_to(
        message,
        "Hey there, I'm CookBookBot. "
        "I'm here to help you cook some interesting and delicious recipes.\n\n"
        "But first, please enter your name.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    bot.register_next_step_handler(msg, process_name_step)


@bot.message_handler(commands=["menu"])
def enter_main_menu(message):
    bot.reply_to(message, "You are in the main menu", reply_markup=get_keyboard("main_menu"))


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id

    if message.text == "About me":
        try:
            profile = Profile.objects.get(external_id=message.from_user.id)
        except Profile.DoesNotExist:
            bot.reply_to(message, "You have not introduced yet, try '/start' command ")
            raise ValueError("Profile does not exist")

        bot.send_message(
            chat_id,
            f"Name: {profile.name}\nGender: {profile.get_gender_display()}",
            reply_markup=get_keyboard("main_menu"),
        )
    elif message.text == "Recipes":
        bot.send_message(
            chat_id,
            "Here are the available recipes",
            reply_markup=get_keyboard("recipes"),
        )
    elif message.text in Recipe.objects.values_list("title", flat=True):
        recipe = Recipe.objects.get(title=message.text)

        caption = f"<b>{recipe.title}</b>"
        description = recipe.description
        chunk_length = 4095

        if recipe.image:
            bot.send_photo(chat_id, recipe.image, caption, parse_mode="html")
        else:
            bot.send_message(chat_id, caption, parse_mode="html")

        # Send the recipe description in chunks if too long
        if len(description) > chunk_length:
            for x in range(0, len(description), chunk_length):
                bot.send_message(chat_id, description[x: x + chunk_length])  # fmt: skip
        else:
            bot.send_message(chat_id, description)


bot.infinity_polling()
