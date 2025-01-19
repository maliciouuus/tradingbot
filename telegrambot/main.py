import csv
from datetime import date, timedelta
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import json


# Configuration du bot Telegram
telegram_token = ''


free = [
    "Raph1300",
    "Sweldoz",
    "maevaapeang",
    "AntoineDelhay",
    "stelladle",
    "marielaure974",
    "bdargent",
    "Jderem",
    "halainachanzy",
    "Julecar",
    "Hierrymichael",
    "Jderem",
    "Novaofficiel",
    "areyouseriousdude",
    "Zzkathleen",
    "Jerem62137",
    "mar_tine_J",
    "Laeticejoy",
    "Stephaniebarry",
    "Leti_sln",
    "celinegloriaumonf",
    "Gozerta",
    "Evanoskahoff",
    "aos_denis",
    "MelanieRoulinMeloun",
    "Reunionnaise_3",
    "marionnas1",
    "dorha5",
    "Deborah271122",
    "padolusprecilia",
    "Vanessandco",
    "ChristelBorne",
    "Tauheretan",
    "eliottcse",
    "Elise86",
    "Momtrading1991",
    "Ninie_smiles",
    "christophechican",
    "angiesav63",
    "maxencee511",
    "meli1908",
    "MelissaJauquet",
    "Lucie_mlx",
    "hinata0206",
    "piccoloang08",
    "Sandrinedzs",
    "Virginie2710",
    "Fabio_NuJo",
    "Dylou",
    "Giulietta1204",
    "Fabio_NuJo",
    "Fabio_Nujo",
    "Yvesvervaeke",
    "sophiebergier",
    "venus0194",
    "IngridMB",
    "manonv06",
    "Boulle_Depoil",
    "Charlotte1810",
    "Giulietta1204",
    "tina_girsboss",
    "Alex17310",
    "laetitia_moneyboost",
    "NadeigeLef",
    "boyer_laetitia",
    "cam2244",
    "Cam2244",
    "mathilde_isa",
    "gonrhier",
    "Falk_13",
    "Caroline_poupa",
    "Cindyber"
]

updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher



def get_user_language(user_id):
    with open('database/langues.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == str(user_id):
                return row[1]  # The second column contains the language
    return None

# Fonction pour extraire la variable du fichier JSON en fonction de la langue
def get_json_variable(user_id, variable_name):
    # Récupérer la langue de l'utilisateur
    user_language = get_user_language(user_id)
    
    if user_language:
        file_path = f'messages/{user_language}.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data.get(variable_name, None)  # Retourner la variable si elle existe, sinon None
    else:
        return None


def save_user_language(user_id, language):
    with open('database/langues.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([user_id, language])

def is_user_registered_with_language(user_id):
    with open('database/langues.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) > 0 and row[0] == str(user_id):
                return True
    return False

def change_user_language(user_id, new_language):
    with open('database/langues.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open('database/langues.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 2 and parts[0] == str(user_id):
                parts[1] = new_language
                writer.writerow(parts)
            else:
                writer.writerow(parts)  # Write the line as is


def save_verification_status(user_id):
    # Charger les statuts de vérification depuis le fichier CSV
    verification_statuses = {}
    try:
        with open('database/verification_status.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                verification_statuses[row[0]] = row[1]
    except FileNotFoundError:
        pass

    # Mettre à jour le statut de vérification de l'utilisateur
    verification_statuses[str(user_id)] = 'True'

    # Écrire les nouveaux statuts dans le fichier CSV
    with open('database/verification_status.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for user_id, status in verification_statuses.items():
            writer.writerow([user_id, status])



# Fonction pour sauvegarder l'affiliation dans la base de données affiliation.csv
def save_affiliation(user_id, affiliate_name):
    with open('database/affiliation.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, affiliate_name])

def get_affiliate_name(user_id):
    with open('database/affiliation.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(user_id):
                return row[1]
    return None

def get_affiliate_link_from_name(affiliate_name):
    affiliate_link = None

    with open('database/partner.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].strip().lower() == affiliate_name.lower():
                affiliate_link = row[1].strip()
                break

    if not affiliate_link:
        affiliate_link = affiliate_link_default

    return affiliate_link

def compare_string_with_list(string, string_list):
    for item in string_list:
        if string in item:
            return True
    return False




def start(update, context):
    user_id = update.effective_user.id
    user = update.effective_user
    if is_user_registered_with_language(user_id) == False:
        keyboard = [
        [InlineKeyboardButton("🇫🇷 Français", callback_data='fr')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='en')],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data='de')],
        [InlineKeyboardButton("🇪🇸 Español", callback_data='es')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='ru')]
    ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Choose your language / Choisissez votre langue / Wählen Sie Ihre Sprache / Выберите ваш язык :", reply_markup=reply_markup)
    if get_affiliate_name(user_id) == None and check_subscription_payment(user_id) != True and compare_string_with_list(str(user['username']), free) == False and is_user_registered_with_language(user_id) != False:
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_json_variable(user_id, "saisir_code"))

    if get_affiliate_name(user_id) != None and check_subscription_payment(user_id) != True and compare_string_with_list(str(user['username']), free) == False and is_user_registered_with_language(user_id) != False:
        # Récupérer le nom du parrain de l'utilisateur
        affiliate_name = get_affiliate_name(user_id)

        gif_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2x2eGdsYzI2enBiaGhubzl4b2ZtbHJkOHRwY3poeGN5YXJtZTA2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ndHsDj7XZJu9zAn4lw/giphy.gif"
        

        reply_text = get_json_variable(user_id, "reply_text")
        affiliate_link = get_affiliate_link_from_name(affiliate_name)
        robot_button = InlineKeyboardButton("🤖", url=affiliate_link)
        verify_button = InlineKeyboardButton("✅", callback_data='verify')
        keyboard = InlineKeyboardMarkup([[robot_button], [verify_button]])
        context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_url)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_markup=keyboard)
        
    if check_subscription_payment(user_id) == True or compare_string_with_list(str(user['username']), free) == True:
        reply_text = get_json_variable(user_id, "novagroup")
        group_button = InlineKeyboardButton(get_json_variable(user_id, "groups_button"), callback_data='groupes')
        settings_button = InlineKeyboardButton(get_json_variable(user_id, "para_button"), callback_data='settings')
        automate_button = InlineKeyboardButton(get_json_variable(user_id, "auto_button"), callback_data='automate')  # Nouveau bouton "Automate"
        keyboard = InlineKeyboardMarkup([[group_button], [automate_button], [settings_button]])  # Ajoutez le bouton "Automate" à la liste

        update.message.reply_text(reply_text, reply_markup=keyboard)


def language_selection_callback(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    selected_language = query.data
    if is_user_registered_with_language(user_id) == False:
        save_user_language(user_id, selected_language)
        start(update, context)
    else:
        change_user_language(user_id, selected_language)
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_json_variable(user_id, "change"))

        





def button_click(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    if query.data == 'automate':
        automate_text = get_json_variable(user_id, "automate")
        automate_text += get_json_variable(user_id, "video")

        # Ajouter le bouton de retour
        back_button = InlineKeyboardButton(get_json_variable(user_id, "return"), callback_data='back')
        keyboard = InlineKeyboardMarkup([[back_button]])
        query.message.reply_text(automate_text, parse_mode='Markdown', reply_markup=keyboard)

def settings_button(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    query.answer()

    if query.data == 'contact':
        # Message de contact
        contact_message = get_json_variable(user_id, "contact_message")

        # Créer un bouton "Retour"
        back_button = InlineKeyboardButton(get_json_variable(user_id, "return"), callback_data='back')

        # Créer le clavier avec le bouton de retour
        keyboard = InlineKeyboardMarkup([[back_button]])

        # Modifier le message existant avec le message de contact et le clavier
        query.message.edit_text(contact_message, reply_markup=keyboard)
    else:
        # Afficher les boutons "Contact", "Désabonnement" et "Retour"
        contact_button = InlineKeyboardButton(get_json_variable(user_id, "contact_button"), callback_data='contact')
        language_button = InlineKeyboardButton(get_json_variable(user_id, "langue_button"), callback_data='language')
        back_button = InlineKeyboardButton(get_json_variable(user_id, "return"), callback_data='back')

        reply_markup = InlineKeyboardMarkup([[contact_button], [language_button], [back_button]])

        # Modifier le message existant avec les nouveaux boutons
        query.message.edit_reply_markup(reply_markup)



# Fonction pour demander la nouvelle langue à l'utilisateur
def ask_language(update, context):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("🇫🇷 Français", callback_data='fr')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='en')],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data='de')],
        [InlineKeyboardButton("🇪🇸 Español", callback_data='es')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='ru')],
        [InlineKeyboardButton(get_json_variable(user_id, "return"), callback_data='back')]  # Ajouter un bouton de retour
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Utiliser query.message pour éditer le message existant
    query = update.callback_query
    query.message.edit_text(get_json_variable(user_id, "choisirlangue"), reply_markup=reply_markup)


def back_button(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query
    query.answer()

    # Afficher les boutons "Groupes", "Paramètres" et "Automate"
    group_button = InlineKeyboardButton(get_json_variable(user_id, "groups_button"), callback_data='groupes')
    settings_button = InlineKeyboardButton(get_json_variable(user_id, "para_button"), callback_data='settings')
    automate_button = InlineKeyboardButton(get_json_variable(user_id, "auto_button"), callback_data='automate')
    keyboard = InlineKeyboardMarkup([[group_button], [automate_button], [settings_button]])

    # Modifier le message existant avec les nouveaux boutons
    query.message.edit_text(get_json_variable(user_id, "novagroup"), reply_markup=keyboard)




# Ajouter un gestionnaire de rappels pour le bouton "Paramètres"
def settings_handler(update, context):
    settings_button(update, context)

# Ajouter un gestionnaire de rappels pour le bouton "Retour"
def back_handler(update, context):
    back_button(update, context)



# Gestion de la réponse de l'utilisateur pour le code de promo
def process_promo_code(update, context):
    user_id = update.effective_user.id
    user_code = update.message.text.strip().lower()

    # Charger les codes partenaires depuis le fichier CSV
    with open('database/partner.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].strip().lower() == user_code:
                affiliate_name = row[0]
                save_affiliation(user_id, affiliate_name)
                return start(update, context)

    # Si le code n'est pas valide, envoyer le message d'erreur uniquement dans cette fonction
    update.message.reply_text(get_json_variable(user_id, "code_error"))


def check_subscription_payment(user_id):
    with open('database/verification_status.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(user_id):
                return row[1] == 'True'
        return False


def groupes(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = update.effective_user

    if check_subscription_payment(user_id) or compare_string_with_list(str(user['username']), free):
        query = update.callback_query
        query.answer()

        # Créer une liste de groupes d'alertes accessibles
        groupes_list = [
            {
                'nom': '🔹 Nova',
                'lien': 'https://t.me/+gnqdx71Pv4Y0Zjdk'
            },
            {
                'nom': '🛡️ Astra ',
                'lien': 'https://t.me/+A8mswUv1lKthM2Nk'
            },
            {
                'nom': '🔥 Sayan ',
                'lien': 'https://t.me/+Ij4JwFhgKMRiNjE0'
            },
            {
                'nom': '💸 Univers',
                'lien': 'https://t.me/+PICj7ZXjcJhmM2Y8'
            },
            {
                'nom': '🎁 Airdrops Crypto',
                'lien': 'https://t.me/airdrops_io'
            },
            {
                'nom': '📰 Crypto News',
                'lien': 'https://t.me/CryptoPanicNotifications'
            }
        ]
        # Créer une liste de boutons pour les groupes
        buttons = []
        for groupe in groupes_list:
            button = InlineKeyboardButton(groupe['nom'], url=groupe['lien'])
            buttons.append([button])

        # Ajouter un bouton "Retour"
        retour_button = InlineKeyboardButton(get_json_variable(user_id, "return"), callback_data='back')
        buttons.append([retour_button])

        # Créer le clavier avec les boutons
        keyboard = InlineKeyboardMarkup(buttons)

        # Créer le message avec la liste des groupes et le clavier
        message_text = get_json_variable(user_id, "groups_text")

        # Ajouter le clavier au message
        message_text += get_json_variable(user_id, "groups_text2")

        # Modifier le message existant avec le nouveau message et le clavier
        query.message.edit_text(message_text, reply_markup=keyboard)

    else:
        # Si l'utilisateur n'a pas accès, afficher un message d'erreur
        query = update.callback_query
        query.answer(get_json_variable(user_id, "error_groups"))


def verify_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    # Enregistrez la vérification de l'utilisateur
    save_verification_status(user_id)
    # Message de bienvenue avec des emojis
    welcome_message = get_json_variable(user_id, "welcome")

    # Envoi du message de bienvenue sans clavier inline
    context.bot.send_message(chat_id=user_id, text=welcome_message, parse_mode=ParseMode.MARKDOWN)

    # Envoi de l'animation GIF
    gif_url = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTJncjBzN2ExYnBhaGVzZW9pdW1rNmRiNXE0b2NsMGd6dnE1OXRmMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qSsgcG8tCpsUxxHZKE/giphy.gif"
    context.bot.send_animation(chat_id=user_id, animation=gif_url)

"""                  
admin

"""

def process_free_command(update, context):
    user_id = update.message.from_user.id
    command = update.message.text

    if user_id == 6109590415:
        if command.startswith("/free "):
            username = command.split("/free ")[1]  # Extraire le username de la commande
            free.append(str(username))  # Ajouter le username à la liste
            message = f"Username ajouté avec succès : {username}"
            update.message.reply_text(message)
        elif command.startswith("/unfree "):
            username = command.split("/unfree ")[1]  # Extraire le username de la commande
            if username in free:
                free.remove(str(username))  # Retirer le username de la liste
                message = f"Username retiré avec succès : {username}"
                update.message.reply_text(message)
            else:
                message = f"Username non trouvé : {username}"
                update.message.reply_text(message)

def remove_partner(update, context):
    user_id = update.message.from_user.id
    command = update.message.text

    if user_id == 6109590415 and command.startswith("/remove "):
        codepromo = command.split("/remove ")[1]
        with open('database/partner.csv', 'r') as csvfile:
            partners = list(csv.reader(csvfile))
        with open('database/partner.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            removed = False
            for partner in partners:
                if partner[0] == codepromo:
                    removed = True
                    continue
                writer.writerow(partner)
            if removed:
                message = f"Partenaire '{codepromo}' supprimé avec succès."
                update.message.reply_text(message)
            else:
                message = f"Partenaire '{codepromo}' non trouvé."
                update.message.reply_text(message)




def add_partner(update, context):
    user_id = update.message.from_user.id
    command = update.message.text

    if user_id == 6109590415 and command.startswith("/partner "):
        partner_info = command.split("/partner ")[1]
        partner_data = partner_info.split(" ", 1)
        
        if len(partner_data) == 2:
            codepromo = partner_data[0].strip()
            lien = partner_data[1].strip()
            
            with open('database/partner.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([codepromo, lien])
                
            message = "Partenaire ajouté avec succès."
        else:
            message = "Format invalide. Utilisez /partner nom url"
        
        update.message.reply_text(message)
    else:
        update.message.reply_text("Vous n'avez pas les autorisations pour accéder à cette commande.")


def see_partners(update, context):
    with open('database/partner.csv', 'r') as csvfile:
        partners = list(csv.reader(csvfile))
    
    if partners:
        message = "Liste des partenaires :\n"
        for partner in partners:
            message += f"Code promo : {partner[0]}, Lien d'affiliation : {partner[1]}\n"
    else:
        message = "Aucun partenaire trouvé dans la base de données."
    
    update.message.reply_text(message)


def admin_commands(update, context):
    user_id = update.message.from_user.id
    if user_id == 6109590415:
        message = "Commandes administratives :\n"
        message += "/partner codepromo lien - Ajouter un partenaire\n"
        message += "/remove codepromo - Supprimer un partenaire\n"
        message += "/see_partners - Voir tous les partenaires\n"
        message += "/free user - Ajouter un abonnement gratuit\n"
        message += "/unfree user - Retirer un abonnement gratuit\n"
        message += "/see_free user - Voir liste des abonnements gratuit\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("Vous n'avez pas les autorisations pour accéder aux commandes administratives.")

def see_free_command(update, context):
    user_id = update.message.from_user.id
    
    if user_id == 6109590415:
        if free:
            message = "Liste des usernames dans free :\n"
            message += "\n".join(free)
        else:
            message = "La liste free est vide."
        update.message.reply_text(message)
    else:
        update.message.reply_text("Vous n'avez pas les autorisations pour accéder à cette commande.")

# Ajouter le gestionnaire de commande
dispatcher.add_handler(CommandHandler('see_free', see_free_command))
dispatcher.add_handler(CommandHandler("free", process_free_command))
dispatcher.add_handler(CommandHandler("partner", add_partner))
dispatcher.add_handler(CommandHandler("remove", remove_partner))
dispatcher.add_handler(CommandHandler("see_partners", see_partners))
dispatcher.add_handler(CommandHandler("admin", admin_commands))
dispatcher.add_handler(CommandHandler('unfree', process_free_command))


# Gestionnaire de commande pour /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='^automate$'))

#parametres langues 
dispatcher.add_handler(CallbackQueryHandler(ask_language, pattern='language'))

# Gestionnaire pour le bouton de vérification
verify_button_handler = CallbackQueryHandler(verify_button, pattern='verify')
dispatcher.add_handler(verify_button_handler)

# Gestionnaire de message pour le code de promo
promo_code_handler = MessageHandler(Filters.text & (~Filters.command), process_promo_code)
dispatcher.add_handler(promo_code_handler)


# Ajouter les gestionnaires de rappels au gestionnaire de dispatcher
dispatcher.add_handler(CallbackQueryHandler(settings_handler, pattern='settings'))

# Ajouter les gestionnaires de rappels à l'updater
updater.dispatcher.add_handler(CallbackQueryHandler(settings_handler, pattern='settings'))
updater.dispatcher.add_handler(CallbackQueryHandler(back_handler, pattern='back'))

# Ajouter le gestionnaire de rappel pour le bouton "Contact"
dispatcher.add_handler(CallbackQueryHandler(settings_button, pattern='contact'))



groupes_handler = CommandHandler('groupes', groupes)
dispatcher.add_handler(groupes_handler)


dispatcher.add_handler(CallbackQueryHandler(language_selection_callback, pattern='^(fr|es|en|de|ru)$'))


# Obtenir le gestionnaire de dispatcher
dispatcher = updater.dispatcher

#groupes 

dispatcher.add_handler(CallbackQueryHandler(groupes, pattern='^groupes$'))


# Démarrer le bot
updater.start_polling()
