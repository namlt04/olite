from PySide6.QtWidgets import QApplication
import qasync
import asyncio
from modules.MainWindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()
