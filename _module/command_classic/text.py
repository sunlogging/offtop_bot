
start= 'Bot is active.'
help = 'help message'

warning_user = lambda count: f'You have {count} warning.'
kick_user = lambda username_user, username_admin: f"{username_user} has been kicked. {username_admin}"
ban_user = lambda username_user, username_admin: f"{username_user} has been baned. {username_admin}"

not_reply = 'To give a warning to a user, reply to their message.'