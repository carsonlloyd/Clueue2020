import time, os, random
# import json

# debug_flag true/false to allow for command-line printing (intend to have this be a program-wide global? can re-configure if needed)
# ARGUMENT FORMAT: TO, [data], debug_flag
# message itself will be a Python dict (can translate easily to JSON if needed)

# TODO: include data sanitization per message

def send_message(send_to_id, message, debug_flag=False):
	assert type(debug_flag) == bool
	if debug_flag:
		print(message)
	# TODO: IMPLEMENT SENDING MESSAGE ONCE SOCKETS ARE CONFIGURED


def send_success_connect(send_to_id, connected_client, failed_to_connect, is_game_full=False, debug_flag=False):
	message = {	"message_type": "success_connect",
				"connected_client": connected_client,
				"failed_to_connect": failed_to_connect,
				"is_game_full": is_game_full
				}

	send_message(send_to_id, message, debug_flag)

def send_player_connected(send_to_id, connected_client, debug_flag=False):
	message = {	"message_type": "player_connected",
				"connected_client": connected_client
				}
	send_message(send_to_id, message, debug_flag)

def send_character_unavail(send_to_id, debug_flag=False):
	message = {	"message_type": "character_unavail"}
	send_message(send_to_id, message, debug_flag)

def send_choose_character(send_to_id, characters_available, debug_flag=False):
	message = {	"message_type": "choose_character",
				"characters_available": characters_available
				}
	send_message(send_to_id, message, debug_flag)

# TODO: Carson continue here
def send_character_choice(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_start_game(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_card_set(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_ready_for_turns(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_take_turn(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_end_turn(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_player_move(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_move(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_player_move_broadcast(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_make_suggestion(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_suggestion(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_suggest(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_make_accusation(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_accusation(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_accusation_made(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_game_win_accusation(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_make_disprove(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_disprove(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_disprove_made(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)

def send_disprove_done(send_to_id, data, debug_flag=False):
	message = {	"message_type": "",
				}
	send_message(send_to_id, message, debug_flag)
