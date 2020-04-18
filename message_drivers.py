import time, os, random, json
from main import addMessage

# debug_flag true/false to allow for command-line printing (intend to have this be a program-wide global? can re-configure if needed)
# ARGUMENT FORMAT: TO, [data], debug_flag
# message itself will be a Python dict (can translate easily to JSON if needed)

# TODO: include data sanitization per message

def send_message(send_to_id, message, debug_flag=False):
	assert type(debug_flag) == bool
	if debug_flag:
		print(message)
	# TODO: IMPLEMENT SENDING MESSAGE ONCE SOCKETS ARE CONFIGURED

	#turn message into bytes to be sent and then pad it out to 1024 bytes
	#WARNING: all messages must be 1024 bytes
	messageBytes = json.dumps(message).encode()
	messageBytes += b' ' * (256-len(messageBytes))

	if send_to_id == 'ALL_CLIENTS':
		for i,m in enumerate(main.messages):
			addMessage(messageBytes, i)
	else:
		addMessage(messageBytes, send_to_id)


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
	message = {	"message_type": "character_unavail" }
	send_message(send_to_id, message, debug_flag)

def send_choose_character(send_to_id, characters_available, debug_flag=False):
	message = {	"message_type": "choose_character",
				"characters_available": characters_available
				}
	send_message(send_to_id, message, debug_flag)

def send_character_choice(send_to_id, character_choice, client_id, debug_flag=False):
	message = {	"message_type": "character_choice",
				"character_choice": character_choice,
				"client_id": client_id
				}
	send_message(send_to_id, message, debug_flag)

def send_start_game(send_to_id, debug_flag=False):
	message = {	"message_type": "start_game" }
	send_message(send_to_id, message, debug_flag)

def send_card_set(send_to_id, cards, debug_flag=False):
	message = {	"message_type": "card_set",
				"cards": cards
				}
	send_message(send_to_id, message, debug_flag)

def send_ready_for_turns(send_to_id, client_id, debug_flag=False):
	message = {	"message_type": "ready_for_turns",
				"client_id": client_id
				}
	send_message(send_to_id, message, debug_flag)

def send_take_turn(send_to_id, debug_flag=False):
	message = {	"message_type": "take_turn" }
	send_message(send_to_id, message, debug_flag)

def send_end_turn(send_to_id, client_id, debug_flag=False):
	message = {	"message_type": "end_turn",
				"client_id": client_id
				}
	send_message(send_to_id, message, debug_flag)

def send_player_move(send_to_id, client_id, direction, debug_flag=False):
	message = {	"message_type": "player_move",
				"client_id": client_id,
				"direction": direction
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_move(send_to_id, error_message, debug_flag=False):
	message = {	"message_type": "cannot_move",
				"error_message": error_message
				}
	send_message(send_to_id, message, debug_flag)

def send_player_move_broadcast(send_to_id, client_id, direction, debug_flag=False):
	message = {	"message_type": "player_move_broadcast",
				"client_id": client_id,
				"direction": direction
				}
	send_message(send_to_id, message, debug_flag)

def send_make_suggestion(send_to_id, suspects, weapons, debug_flag=False):
	message = {	"message_type": "make_suggestion",
				"suspects": suspects,
				"weapons": weapons
				}
	send_message(send_to_id, message, debug_flag)

def send_suggestion(send_to_id, client_id, suspect, weapon, debug_flag=False):
	message = {	"message_type": "suggestion",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_suggest(send_to_id, error_message, debug_flag=False):
	message = {	"message_type": "cannot_suggest",
				"error_message": error_message
				}
	send_message(send_to_id, message, debug_flag)

def send_make_accusation(send_to_id, suspects, weapons, rooms, debug_flag=False):
	message = {	"message_type": "make_accusation",
				"suspects": suspects,
				"weapons": weapons,
				"rooms": rooms
				}
	send_message(send_to_id, message, debug_flag)

def send_accusation(send_to_id, client_id, suspect, weapon, room, debug_flag=False):
	message = {	"message_type": "accusation",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon,
				"room": room
				}
	send_message(send_to_id, message, debug_flag)

def send_accusation_made(send_to_id, client_id, suspect, weapon, room, debug_flag=False):
	message = {	"message_type": "accusation_made",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon,
				"room": room
				}
	send_message(send_to_id, message, debug_flag)

def send_game_win_accusation(send_to_id, client_id, suspect, weapon, room, debug_flag=False):
	message = {	"message_type": "game_win_accusation",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon,
				"room": room
				}
	send_message(send_to_id, message, debug_flag)

def send_make_disprove(send_to_id, client_id, suspect, weapon, room, suspects, weapons, rooms, debug_flag=False):
	message = {	"message_type": "make_disprove",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon,
				"room": room,
				"suspects": suspects,
				"weapons": weapons,
				"rooms": rooms
				}
	send_message(send_to_id, message, debug_flag)

def send_cannot_disprove(send_to_id, debug_flag=False):
	message = {	"message_type": "cannot_disprove" }
	send_message(send_to_id, message, debug_flag)

def send_disprove_made(send_to_id, client_id, suspect, weapon, room, debug_flag=False):
	message = {	"message_type": "disprove_made",
				"client_id": client_id,
				"suspect": suspect,
				"weapon": weapon,
				"room": room
				}
	send_message(send_to_id, message, debug_flag)

def send_disprove_done(send_to_id, client_id_accuse, client_id_disprove, suspect, weapon, room, debug_flag=False):
	message = {	"message_type": "disprove_done",
				"client_id_accuse": client_id_accuse,
				"client_id_disprove": client_id_disprove,
				"suspect": suspect,
				"weapon": weapon,
				"room": room
				}
	send_message(send_to_id, message, debug_flag)
