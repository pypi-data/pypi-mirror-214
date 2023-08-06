import argparse
import threading
import sounddevice as sd
import soundfile as sf


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


class AudioPlayer:

    def __init__(self, filename, device=None):
        self.filename = filename
        self.device = device
        self.event = threading.Event()
        self.current_frame = 0
        self.paused = False
        self.thread = None

    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        if self.paused:
            outdata[:] = 0
        else:
            data, fs = self.data, self.fs
            chunksize = min(len(data) - self.current_frame, frames)
            outdata[:chunksize] = data[self.current_frame : self.current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                raise sd.CallbackStop()
            self.current_frame += chunksize

    def play(self):
        self.data, self.fs = sf.read(self.filename, always_2d=True)
        self.stream = sd.OutputStream(
            samplerate=self.fs,
            device=self.device,
            channels=self.data.shape[1],
            callback=self.callback,
            finished_callback=self.event.set,
        )

    def _playback_thread(self):
        try:
            with self.stream:
                while not self.event.is_set():
                    self.event.wait(0.1)  # Check event periodically
                    if self.event.is_set():
                        break
        except KeyboardInterrupt:
            raise SystemExit("\nInterrupted by user")
        except Exception as e:
            print(type(e).__name__ + ": " + str(e))

    def wait(self):
        self.thread = threading.Thread(target=self._playback_thread)
        self.thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.event.set()  # Request termination
    
        
class simpleplayer:
    def __init__(self, filename, device=None):
        self.AudioPlayer = AudioPlayer(filename, device=None)
    
    def start(self):
        if self.AudioPlayer.thread and self.AudioPlayer.thread.is_alive():
            return
        self.AudioPlayer.play()
        self.AudioPlayer.wait()
    
    def play(self):
        self.player = threading.Thread(target=self.start)
        self.player.start()
    
    def pause(self):
        self.AudioPlayer.pause()
    
    def resume(self):
        self.AudioPlayer.resume()
    
    def stop(self):
        self.AudioPlayer.stop()
    

def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Simple audio player",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-l",
        "--list-devices",
        action="store_true",
        help="show list of audio devices and exit",
    )
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        raise SystemExit(0)

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser],
    )
    parser.add_argument(
        "filename", metavar="FILENAME", help="audio file to be played back"
    )
    parser.add_argument(
        "-d",
        "--device",
        type=int_or_str,
        help="output device (numeric ID or substring)",
    )
    args = parser.parse_args(remaining)

    player = AudioPlayer(args.filename, device=args.device)
    player.play()
    player.wait()

if __name__ == "__main__":
    main()