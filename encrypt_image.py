'''
Daniel Gockel's unsecure advanced encryption standard electronic codebook bitmap image encryptor (AES & ECB) 
	based on Chaos Computer Club

This program converts a bitmap image into an AES Encrypted version.
Objects in the image are still visible!! This demonstrates that AES is unsecure if it is used with ECB Block Cipher Mode.

Example:
	python encrypt_image.py
	python encrypt_image.py yourimage.bmp

!!!read README.md for description!!!

@author Daniel Gockel
@website daniel.gockel.co
'''
from Crypto.Cipher import AES
import sys

def read_file(filename):
	"""
	Read a file binary and fill message
	Args:
		filename(string): a string with the name of the file.
	Returns:
		A string containing the content of the file.
	"""
	input_file = open(filename, "rb")
	print("Reading...")
	message = input_file.read()
	print("Read file from " + filename)
	print("Read " + str(len(message)) + " Bytes (or characters)")  # 1 Byte ^= 1 Character
	input_file.close()
	return message

def apply_padding(message, blocksize):
	"""
	Applies padding to a given message to fill a whole block
	Args:
		message(string): a string with content of image
		blocksize(int): number of bytes the message needs to be divided into
	Returns:
		The message with appended zeros
	"""
	counter = 0
	while (len(message) % (blocksize) != 0):  # blocksize is in Bytes
		message += b"\x00"
		counter += 1
	print("Length of Plaintext: " + str(len(message)) + " Bytes")
	print("Append " + str(counter) + " Bytes to Plaintext for Padding (now " + str(len(message)) + " Bytes long)")
	return message

def split_into_blocks(text, blocksize):
	"""
	Splits a given String into blocks of blocksize and returns a list of blocks.
	Throws an Error if text is not a multiple of blocksize
	(note: Do not mess with this function)
	Args:
		text(string): a string with content of image (multiple of block size)
		blocksize(int): number of bytes the message needs to be divided into
	Returns:
		A list of divided content blocks
	"""
	if len(text) % blocksize != 0:
		raise ValueError("Text needs to be a multiple of blocksize - call apply_padding(message, blocksize) first")
	# iter iterates over the bytes of a given text
	# [] creates a list out of the iteration over text
	# which will be unpacked *[a,b] ==> a,b than repacked zip( * blocksize)
	# and a list will be returned list()
	print("Text chopped into " + str(len(text)/blocksize) + " "  + str(blocksize) + "-Byte-Blocks")
	return list(map("".join, zip( *[iter(text)] * blocksize )))

def encrypt_ecb(plaintext_blocks, cipher_obj):
	"""
	Encrypt Plaintext with cipher_obj and key

	Args:
		plaintext_blocks(list): list of content blocks
		cipher_obj(AES): AES object. Able to encrypt
	Returns:
		string containing all encrypted blocks
	"""
	ciphertext = ""
	for plain_block in plaintext_blocks:
		ciphertext += cipher_obj.encrypt(plain_block)
	print("Encrypted all Plaintext-Blocks")
	return ciphertext

def restore_header(plaintext, ciphertext, skip):
	"""
	copy back the first 'skip' Bytes from Plaintext

	Args:
		plaintext(string): plain text
		ciphertext(string): encrypted text
	Returns:
		encrypted string with header from plain text
	"""
	# Phyton Strings are immutable - therefore this will not work:
	# for byte in range(0, skip):
		# ciphertext[byte] = plaintext[byte]
	# but this will work:
	result = plaintext[0:skip+1]  # written as interval: [0,skip+1)
	result += ciphertext[skip+1:]  # copy from byte skip+1 to end: [skip+1,EOF)
	return result

def write_file(filename, ciphertext):
	"""
	saves encrypted text to a file

	Args:
		filename(string): output filename
		ciphertext(string): encrypted text
	Returns:
		encrypted string with header from plain text
	"""
	output_file = open(filename, "wb")  # write binary (w over-writes); file will be created
	print("Writing...")
	output_file.write(ciphertext)
	output_file.close()
	print("Written to " + filename)

if __name__ == '__main__':
	# path to your image
	in_filename = "JavaDuke.bmp"

	for arg in sys.argv:
		if '.bmp' in arg: # if bmp in arguments -> take filename from there
			in_filename = arg

	# output filename --> AES ECB Encrypted
	out_filename = "ecb_enc.bmp"

	# for AES-128 a 128bit key ^= 16 Bytes is needed
	key = b"Sixteen Byte KeySixteen Byte Key" # 32 characters
	#print(sys.getsizeof(key))
	skip = 68  # Number of Bytes not to encrypt
	cipher_obj = AES.new(key) # AES object with key

	##### MAIN FUNCTION CALLS
	# save content as a string in message
	message = read_file(in_filename) 
	# concatenates zeros to message 
	# until message can be divided into blocks with given block_size
	# block_size is equal to 16 bytes
	plaintext = apply_padding(message, cipher_obj.block_size) 
	# split content into blocks
	plaintext_blocks = split_into_blocks(plaintext, cipher_obj.block_size)
	# encrypt content blocks
	ciphertext = encrypt_ecb(plaintext_blocks, cipher_obj)
	# fix bmp header in encrypted text
	result = restore_header(plaintext, ciphertext, skip)
	# save content as file
	write_file(out_filename, result)

	print("Done")