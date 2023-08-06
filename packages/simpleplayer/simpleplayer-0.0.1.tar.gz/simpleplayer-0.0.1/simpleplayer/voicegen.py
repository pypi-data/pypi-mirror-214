import sys
import socket
import argparse
from gtts import gTTS


class voicegen:
    def __init__(self, text, filename, lang='en'):
        if not self.check_internet_connection():
            print('You are not connected to the internet!')
            return
        filename = filename + '.mp3'

        # Render teks ke dalam file MP3
        tts = gTTS(text, lang=lang)
        tts.save(filename)

    def check_internet_connection(self):
        try:
            # Mencoba membuat koneksi ke DNS Google pada port 53, timeout 3 detik
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except socket.error:
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Voice Generator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "text",
        metavar="TEXT",
        help="text to convert to speech"
    )
    parser.add_argument(
        "filename",
        metavar="FILENAME",
        help="name of the speech file"
    )
    parser.add_argument(
        "--lang",
        metavar="LANG",
        default="en",
        help="language for the speech (default: en)"
    )

    args = parser.parse_args()

    try:
        voicegen(args.text, args.filename, args.lang)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
