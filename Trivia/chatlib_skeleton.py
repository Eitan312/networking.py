# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	"""

	full_msg = ""

	if cmd not in PROTOCOL_CLIENT.values():
		return None

	if len(data) > 9999:
		return None

	full_msg += cmd + '|'
	data_length = len(data)
	full_msg += '0' * (4 - data_length) + str(data_length) + '|'
	full_msg += data

	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	"""
	cmd, msg = "", ""

	fields = data.split('|')
	index = 0
	while not fields[0][index] == ' ':
		cmd += fields[0][index]
		index += 1

	if not cmd in PROTOCOL_CLIENT.values():
		cmd = None

	if not int(fields[1]) == len(fields[2]):
		msg = None
		return cmd,msg

	msg = fields[2]

	# The function should return 2 values
	return cmd, msg


def split_data(msg, expected_fields) -> list:
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occurred, returns None
	"""

	fields = msg.split('#')

	if not len(fields) - 1 == expected_fields:
		return [None]

	return fields


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""

	data = ""
	for field in msg_fields:
		data +=  field + '#'

	data -= '#' # removes extra hashtag
	return data