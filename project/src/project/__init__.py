import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import praw
from dotenv import load_dotenv
import os
from prawcore.exceptions import ResponseException

load_dotenv()

class ApiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple API App")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.info_label = QLabel("Press the button to get data from API.")
        self.layout.addWidget(self.info_label)

        self.button = QPushButton("Get Info")
        self.button.clicked.connect(self.callRedditApi)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def callRedditApi(self):
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )

        # Get subreddit
        subreddit = reddit.subreddit("developer")

        try:
            response = subreddit.hot(limit=10)

            posts_text = ""
            for post in response:
                posts_text += f"• {post.title} (↑ {post.score})\n"

            self.info_label.setText(f"Latest Posts:\n\n{posts_text}")
        except ResponseException as e:
            self.info_label.setText("Status Code:" + str(e.response.status_code) + "\nResponse Body:" + e.response.text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApiApp()
    window.show()
    sys.exit(app.exec_())
