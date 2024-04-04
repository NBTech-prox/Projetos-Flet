import os
import flet
from flet import *
import openai # necesario instalar pelo pip
import urllib.request
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('API_KEY')

class AppForm(UserControl):
     def __init__(self, name:str, end_name:str):
          self.name=name
          self.end_name=end_name
          super().__init__()
     
     def build(self):
          return Container(
               height=45,
               bgcolor='#ebebeb',
               border_radius=5,
               padding=8,
               alignment=alignment.center_left,
               content=Column(
                    spacing=1,
                    controls=[
                         TextField(
                              border_color='transparent',
                              height=19,
                              text_size=13,
                              content_padding=5,
                              cursor_color='black',
                              cursor_height=18,
                              cursor_width=1,
                              color='black',
                              suffix_text=self.end_name,
                              suffix_style=TextStyle(color='black'),
                              prefix_text=self.name,
                              prefix_style=TextStyle(color='black'),
                         ),
                    ],
               ),
          )

class AppCounter(UserControl):
     def __init__(self):
          super().__init__()

     def app_counter_addition(self, e):
          count=int(self.app_counter_text.value) + 1
          self.app_counter_text.value=str(count)
          self.app_counter_text.update()

     def app_counter_subtraction(self, e):
          count=int(self.app_counter_text.value) - 1
          self.app_counter_text.value=str(count)
          self.app_counter_text.update()


     def build(self):
          self.app_counter_text=Text('0', size=12, color='black')
          return Container(
               height=45,
               border_radius=5,
               bgcolor='#ebebeb',
               content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                         IconButton(icon=icons.ADD_ROUNDED, icon_color='black', icon_size=15, on_click= lambda e:self.app_counter_addition(e)),
                         self.app_counter_text,
                         IconButton(icon=icons.REMOVE_ROUNDED, icon_color='black', icon_size=15,  on_click= lambda e:self.app_counter_subtraction(e)),
                    ],
               ),
          )

def main(page: Page):
     page.horizontal_alignment='center'
     page.vertical_alignment='center'
     page.bgcolor='#ebebeb'

     page.add(
          Card(
               width=750,
               height=450,
               elevation=20,
               content=Container(
                    padding=15,
                    content=Row(
                         controls=[
                              Container(
                                   width=280,
                                   height=400,
                                   content=Column(
                                        controls=[
                                             Text('Image Promot', size=10),
                                             AppForm(None, None),
                                             Text('No. of Images Generate', size=10),
                                             AppCounter(),
                                             Text('Filename', size=10),
                                             AppForm('./imagen/', None),
                                        ]
                                   )
                              ),
                              VerticalDivider(width=5, color='white'),
                              Container(
                                   width=400,
                                   height=400,
                                   padding=5,
                                   content=Column(
                                        scroll='auto',
                                        expand=True,
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[

                                        ]

                                   )
                              ),
                         ]
                    )
               )

          )
     )

     page.update()








if __name__=='__main__':
     flet.app(target=main, assets_dir='imagen')