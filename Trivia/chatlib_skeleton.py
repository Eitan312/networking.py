# Protocol Constants

__CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
__LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
__MAX_DATA_LENGTH = 10**__LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
__MSG_HEADER_LENGTH = __CMD_FIELD_LENGTH + 1 + __LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
__MAX_MSG_LENGTH = __MSG_HEADER_LENGTH + __MAX_DATA_LENGTH  # Max size of total message
__DELIMITER = "|"  # Delimiter character in protocol
__DATA_DELIMITER = "#"  # Delimiter in the data part of the message

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

__ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	"""

	full_msg = ""

	if cmd not in PROTOCOL_CLIENT.values():
		return None

	if len(data) > __MAX_DATA_LENGTH:
		return None

	full_msg += cmd + (16 - len(cmd)) * " " + __DELIMITER
	data_length = len(data)
	full_msg += (__LENGTH_FIELD_LENGTH - len(str(data_length))) * "0" + str(data_length) + __DELIMITER
	full_msg += data

	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	"""
	cmd, msg = None, None

	try:
		fields = data.split(__DELIMITER)

		if not len(fields) == 3:
			return cmd, msg

		if not len(fields[0]) == __CMD_FIELD_LENGTH:
			raise Exception("Input was not in expected format")

		if len(fields[1]) > __LENGTH_FIELD_LENGTH:
			raise Exception("Input was not in expected format")

		if not int(fields[1]) == len(fields[2]) or len(fields[2]) > __MAX_DATA_LENGTH:
			raise Exception("Input was not in expected format")

		cmd = ""
		index = 0
		while index < __CMD_FIELD_LENGTH and fields[0][index] == ' ':
			index += 1

		while index < __CMD_FIELD_LENGTH and not fields[0][index] == ' ':
			cmd += fields[0][index]
			index += 1

		if cmd is not None and not cmd in PROTOCOL_CLIENT.values():
			cmd = None
			raise Exception("Input was not in expected format")

		msg = fields[2]

		# The function should return 2 values
		return cmd, msg
	except Exception:
		return cmd, msg


def split_data(msg, expected_fields) -> list:
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occurred, returns None
	"""

	fields = msg.split(__DATA_DELIMITER)

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
		data +=  field + __DATA_DELIMITER

	data -= __DATA_DELIMITER # removes extra hashtag
	return data