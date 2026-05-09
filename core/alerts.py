import os
import platform
import subprocess
from plyer import notification

class Notifier:
    def __init__(self):
        self.system = platform.system()

    def notify(self, title: str, message: str, timeout: int = 5):
        if self.system == "Darwin":
            # macOS: use osascript for reliability
            try:
                # Clean up quotes for AppleScript
                title = title.replace('"', '\\"')
                message = message.replace('"', '\\"')
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(["osascript", "-e", script], check=True)
            except Exception as e:
                print(f"Failed to send macOS notification: {e}")
        else:
            # Other platforms: use plyer
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name="WatchDog",
                    timeout=timeout
                )
            except Exception as e:
                print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    notifier = Notifier()
    notifier.notify("WatchDog", "System Started")