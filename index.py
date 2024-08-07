import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import random
import os

kivy.require('2.0.0')

class MemoryGame(App):
    def build(self):
        self.title = "Pexeso"
        
        self.layout = BoxLayout(orientation='vertical')
        
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid = GridLayout(cols=8, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_view.add_widget(self.grid)
        
        self.pairs = 32
        
        # VLASTNÉ OBRÁZKY
        self.images = [
            'obr1.jpg', 'obr2.jpg', 'obr3.jpg', 'obr4.jpg', 'obr5.jpg', 'obr6.jpg', 
            'obr7.jpg', 'obr8.jpg', 'obr9.jpg', 'obr10.jpg', 'obr11.jpg', 'obr12.jpg', 
            'obr13.jpg', 'obr14.jpg', 'obr15.jpg', 'obr16.jpg', 'obr17.jpg', 'obr18.jpg', 
            'obr19.jpg', 'obr20.jpg', 'obr21.jpg', 'obr22.jpg', 'obr23.jpg', 'obr24.jpg', 
            'obr25.jpg', 'obr26.jpg', 'obr27.jpg', 'obr28.jpg', 'obr29.jpg', 'obr30.jpg', 
            'obr31.jpg', 'obr32.jpg'
        ] * 2
        self.check_images()
        self.buttons = []
        self.first = None
        self.second = None
        self.matched_pairs = 0
        
        self.shuffle_and_create_buttons()
        
        shuffle_button = Button(text="Zamiešať kartičky", size_hint=(1, 0.1))
        shuffle_button.bind(on_release=self.shuffle_and_create_buttons)
        
        self.layout.add_widget(shuffle_button)
        self.layout.add_widget(self.scroll_view)
        
        return self.layout
    
    def check_images(self):
        for image in set(self.images + ['backside.jpg']):
            if not os.path.exists(image):
                print(f"Error: {image} not found in the directory.")
    
    def shuffle_and_create_buttons(self, *args):
        random.shuffle(self.images)
        self.grid.clear_widgets()
        self.buttons = []
        for image in self.images:
            btn = Button(on_release=self.on_button_press)
            btn.image_source = image
            btn.background_normal = 'backside.jpg'
            btn.background_down = 'backside.jpg'
            btn.size_hint = (None, None)
            btn.size = (120, 120)  # Nastavenie menšej veľkosti tlačidiel
            self.buttons.append(btn)
            self.grid.add_widget(btn)
        self.first = None
        self.second = None
        self.matched_pairs = 0
    
    def on_button_press(self, instance):
        if instance == self.first or instance == self.second:
            return
        
        # Show the image fullscreen for 0.5 seconds
        self.show_fullscreen_image(instance.image_source)
        
        if not self.first:
            self.first = instance
            Clock.schedule_once(lambda dt: self.set_button_image(instance, instance.image_source), 0.5)
        elif not self.second:
            self.second = instance
            Clock.schedule_once(lambda dt: self.set_button_image(instance, instance.image_source), 0.5)
            if self.first.image_source == self.second.image_source:
                self.matched_pairs += 1
                self.first, self.second = None, None
                if self.matched_pairs == self.pairs:
                    self.show_winner_popup()
            else:
                Clock.schedule_once(self.hide_mismatch, 1.5)  # Increase time to account for the 0.5 second delay
    
    def set_button_image(self, instance, image_source):
        instance.background_normal = image_source
    
    def hide_mismatch(self, dt):
        self.first.background_normal = 'backside.jpg'
        self.second.background_normal = 'backside.jpg'
        self.first, self.second = None, None
    
    def show_fullscreen_image(self, image_source):
        content = BoxLayout()
        img = Image(source=image_source, allow_stretch=True, keep_ratio=True)
        content.add_widget(img)
        
        popup = Popup(content=content, size_hint=(1, 1), auto_dismiss=True)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 0.5)
    
    def show_winner_popup(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Vyhrali ste!'))
        close_button = Button(text='Znova')
        content.add_widget(close_button)
        
        popup = Popup(title='Víťazstvo!', content=content, size_hint=(0.5, 0.5))
        close_button.bind(on_release=popup.dismiss)
        close_button.bind(on_release=self.shuffle_and_create_buttons)
        
        popup.open()

if __name__ == '__main__':
    MemoryGame().run()

