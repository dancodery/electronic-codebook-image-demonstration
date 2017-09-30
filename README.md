# Electronic Codebook Image Demonstration

This program converts a bitmap image into an AES (Advanced Encryption Standard) encrypted version.
Objects inside the image are still visible!! This demonstrates that AES is insecure if it is used with ECB Block Cipher Mode.

## Installation
1. Install Python 3 if you don't have it already
2. Go to your directory.
3. `git clone https://github.com/dancodery/electronic-codebook-image-demonstration.git`
4. `cd electronic-codebook-image-demonstration`
5. `pip install pycrypto`
6. `python encrypt_image.py` or `python encrypt_image.py myimage.bmp`

You can start 'encrypt_image' with arguments (it will use the default JavaDuke.bmp) or
you can feed in your own Bitmap file as an argument.


## Explanation
<img src='JavaDuke.bmp'><img src='ecb_enc.bmp'>

On the left image you see the Java Duke which we encrypt in this program. 
The duke is divided into a certain number of blocks. Each block is AES encrypted.
As you can see the blocks are encrypted the same way.
This enables us to see objects in the image even that it is AES encrypted.
So think twice the next time before using ECB.

Please give me a star if you like this repo ;=)

Copyright 2017 **© Daniel Gockel**
