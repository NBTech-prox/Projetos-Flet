import os
import flet
from flet import *
from openai import OpenAI

client = OpenAI(api_key=os.getenv('API_KEY'))
import urllib.request
from dotenv import load_dotenv

load_dotenv()

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
          if int(self.app_counter_text.value) != 0:
               count=int(self.app_counter_text.value) - 1
               self.app_counter_text.value=str(count)
               self.app_counter_text.update()
          else:
               pass


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

class AppSizeMenu(UserControl):
     def __init__(self):
          super().__init__()

     def change_size_box(self, e):
          for check in self.controls[0].content.controls[:]:
               check.controls[1].content.value = False
               check.controls[1].content.update()

               e.control.value = True
               e.control.update()


     def app_size_container(self):
          return Container(
               border_radius=25,
               width=25,
               height=25,
               border=border.all(2, 'black'),
               alignment=alignment.center,
               content=Checkbox(
                    fill_color='transparent',
                    check_color='black',
                    on_change=lambda e:self.change_size_box(e),


               ),
          )

     def app_size_main_builder(self, size:str):
          return Column(
               horizontal_alignment=CrossAxisAlignment.CENTER,
               spacing=4,
               controls=[
                    Text(
                         value=size,
                         size=9,
                         color='black',
                         weight='bold',
                    ),
                    self.app_size_container()
               ]
          )

     def build(self):
          return Container(
               height=50,
               border_radius=5,
               bgcolor='#ebebeb',
               content=Row(
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                         self.app_size_main_builder('256x256'),
                         self.app_size_main_builder('512x512'),
                         self.app_size_main_builder('1024x1024'),
                    ]
               )
          )

class AppButton(UserControl):
     def __init__(self, function):
          self.function=function
          super().__init__()


     def build(self):
          return Container(
               alignment=alignment.center,
               content=ElevatedButton(
                    on_click=self.function,
                    bgcolor='black',
                    color='white',
                    height=45,
                    content=Row(
                         alignment=MainAxisAlignment.CENTER,
                         controls=[
                              Text('Generate A.I. Images!', size=11, weight='bold'),
                         ],
                    ),
                     style=ButtonStyle(
                         shape={'':RoundedRectangleBorder(radius=5)},
                     )    
               ),
          )

def main(page: Page):
     page.horizontal_alignment='center'
     page.vertical_alignment='center'
     page.bgcolor='#ebebeb'

     def generate_ai_imagen(e):
          data_list=[]
          img_list=[]
          for data in  main_instance:
               if not isinstance(data, Text):
                    if not isinstance(data, Divider):
                         if not isinstance(data, AppButton):
                              data_list.append(data.controls[0].content)
          for data in data_list:
               for item in data.controls[:]:
                    if isinstance(item, TextField):
                         img_list.append(item.value)

                    if isinstance(item, Text):
                         img_list.append(item.value)

                    if isinstance(item, Column):
                         for checks in item.controls[:]:
                              if isinstance(checks, Container):
                                   if checks.content.value == True:
                                        filesize = str(item.controls[0].value)
                                        img_list.append(filesize)


          response = client.images.generate(prompt=img_list[0],
          n=int(img_list[1]),
          size=img_list[2])
          counter = 0 
          for i in range(int(img_list[1])):
               image_url=response.data[counter].url
               img=f'./images/{img_list[3]}{i}.png'
               urllib.request.urlretrieve(image_url, img)
               counter += 1

               main_image_instance.controls.append(
                    Container(
                         width=400,
                         height=400,
                         image_src=img,
                         image_fit='cover',
                         border_radius=10,
                    ),
               )
               main_image_instance.update()
          print(img_list)


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
                                             Text('Select Image Size', size=10),
                                             AppSizeMenu(),
                                             Text('Filename', size=10),
                                             AppForm('./imagen/', None),
                                             Divider(height=10, color='transparent'),
                                             AppButton(
                                                  lambda e:generate_ai_imagen(e)
                                             ),
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
     main_instance = page.controls[0].content.content.controls[0].content.controls[:]
     main_image_instance = page.controls[0].content.content.controls[2].content

if __name__=='__main__':
     flet.app(target=main, assets_dir='imagen')