from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "-", "+", "%"]
        
        # मुख्य लेआउट (ऊपर से नीचे)
        main_layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        
        # मोबाइल डिस्प्ले बॉक्स
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55,
            background_color=(0.17, 0.24, 0.31, 1), foreground_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.solution)
        
        # बटनों का लेआउट (Android Safe Text "DEL" के साथ)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "%", "+"],
            ["DEL", "="]  # यहाँ ⌫ की जगह DEL कर दिया है ताकि मोबाइल में सही दिखे
        ]
        
        for row in buttons:
            h_layout = BoxLayout(spacing=5)
            for label in row:
                if label in self.operators:
                    bg_color = (0.83, 0.33, 0, 1) # ऑरेंज ऑपरेटर्स
                elif label == "C":
                    bg_color = (0.75, 0.22, 0.17, 1) # लाल क्लियर बटन
                elif label == "DEL":
                    bg_color = (0.5, 0.5, 0.5, 1) # ग्रे बैकस्पेस बटन
                elif label == "=":
                    bg_color = (0.15, 0.68, 0.38, 1) # हरा बराबर बटन
                else:
                    bg_color = (0.2, 0.29, 0.37, 1) # डार्क ग्रे नंबर बटन
                    
                button = Button(
                    text=label, pos_hint={"center_x": 0.5, "center_y": 0.5},
                    background_color=bg_color, background_normal='', font_size=30
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
            
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
            
        elif button_text == "DEL":
            if current and current != "Error":
                self.solution.text = current[:-1]
                
        elif button_text == "=":
            if current and current != "Error":
                try:
                    # % प्रतिशत को सही से संभालना
                    expr = current.replace('%', '/100')
                    # Zero (0) से डिवाइड करने पर क्रैश रोकना
                    if "/0" in expr:
                        self.solution.text = "Error"
                    else:
                        result = str(eval(expr))
                        # अगर रिजल्ट .0 पर खत्म हो तो दशमलव हटाना (जैसे 5.0 को 5 करना)
                        if result.endswith('.0'):
                            result = result[:-2]
                        self.solution.text = result
                except Exception:
                    self.solution.text = "Error"
                    
        else:
            if current == "Error":
                current = ""
                
            # अगर लगातार दो ऑपरेटर्स दबाए जाएं, तो पुराना ऑपरेटर बदलकर नया आ जाए
            if current and current[-1] in self.operators and button_text in self.operators:
                self.solution.text = current[:-1] + button_text
            # पहला कैरेक्टर ऑपरेटर नहीं हो सकता (सिर्फ माइनस '-' को छोड़कर)
            elif current == "" and button_text in self.operators and button_text != "-":
                return
            else:
                self.solution.text = current + button_text

if __name__ == "__main__":
    CalculatorApp().run()
