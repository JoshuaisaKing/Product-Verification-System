import re
import sys
import cv2
import requests
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.uix.popup import Popup


class Qrcodedetector(MDApp):
    firebase_url = 'https://kivyproductverification-default-rtdb.firebaseio.com/.json'

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Yellow'
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.checkvalidity = (
            MDFillRoundFlatButton(text="Check Product Validity", pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                  size_hint=(None, None)))
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

    def show_alert_dialog(self):
         self.dialog = MDDialog(
            title="Valid Product",
            text="This product shows up as valid on our database",
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                ),
                MDRectangleFlatButton(
                    text="Yes It's Neat!", text_color=self.theme_cls.primary_color, on_release=self.neat_dialog
                ),
            ],
         )

         self.dialog.open()

    def check_validity(self, *args):
        valid = None
        # print("Button Clicked")
        # json_data = '{"Table":{"Product_Id":"Zra-1233-5242","Sold":"N"}}'
        # res = requests.post(url=self.firebase_url, json=json.loads(json_data))
        # print(res)
        res = requests.get(url=self.firebase_url)
        x = res.text.split('{')
        c = 0
        for i in x:
            if c != 1 and (c % 2) != 0:
                split = re.split(r'[:,}"]', i)
                # print(split)
                if split[4] == self.data and split[10] == 'N':
                    valid = True
                elif split[4] == self.data and split[10] == 'Y':
                    valid = False
                elif split[4] != self.data:
                    pass

            c += 1

        if valid == True:
            self.show_alert_dialog()
            print('Product Shows as Valid on our Database!')
            sys.exit()
        elif valid == False:
            print('Product Shows as Invalid on our Database!')
            sys.exit()
        else:
            print('Product does not exist on our database!')
            sys.exit()


'''     rows = []
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
'''

if __name__ == '__main__':
    Qrcodedetector().run()
