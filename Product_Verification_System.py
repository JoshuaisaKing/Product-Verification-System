import sys

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
import csv
import cv2
import psycopg2


class Qrcodedetector(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Yellow'
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.checkvalidity = (MDFillRoundFlatButton(text="Check Product Validity", pos_hint={'center_x': 0.5, 'center_y': 0.3}, size_hint=(None, None)))
        self.checkvalidity.bind(on_press=self.check_validity)
        layout.add_widget(self.checkvalidity)
        self.capture = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        data, bbox, _ = self.detector.detectAndDecode(self.image_frame)
        self.data = data
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def check_validity(self, *args):
        conn = psycopg2.connect(
            host="18.133.244.120",
            user="square_youthful_estimate",
            password="swift_male_king")

        # Automatically commit transactions
        conn.set_session(autocommit=True)
        print(self.data)
        rows = []
        with open('data.csv', 'r+') as file:
            reader = csv.reader(file)
            writer = csv.writer(file)
            lc = 0
            for i in reader:
                if lc == 0:
                    pass
                lc += 1
                if (i[0] == self.data) and (i[3] == 'N'):
                    print('Valid Product!')
                    sys.exit()
                elif (i[0] == self.data) and (i[3] == 'Y'):
                    print('Invalid Product! Your Product is a fake as a previous one was recorded sold by the manufacturer!')
                    sys.exit()
                elif i[0] != self.data:
                    pass
                else:
                    print("Product does not exist in our database!")
                    sys.exit()


if __name__ == '__main__':
    Qrcodedetector().run()
