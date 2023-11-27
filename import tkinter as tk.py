from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random


class ATM(App):
    def __init__(self):
        super().__init__()
        self.current_balance = 5000  # Sample initial balance
        self.login_layout = BoxLayout(orientation='vertical')
        self.services_layout = BoxLayout(orientation='vertical')
        self.mobile_verification_layout = BoxLayout(orientation='vertical')
        self.init_ui()

    def build(self):
        return self.login_layout

    def init_ui(self):
        # Login Page
        login_label = Label(text="Login Details")
        self.username_entry = TextInput(hint_text='Username')
        self.password_entry = TextInput(hint_text='Password', password=True)
        login_button = Button(text="Login")
        login_button.bind(on_press=self.login)
        self.login_layout.add_widget(login_label)
        self.login_layout.add_widget(self.username_entry)
        self.login_layout.add_widget(self.password_entry)
        self.login_layout.add_widget(login_button)

        # Services Page
        self.services_label = Label(text="Services Available")
        balance_button = Button(text="Balance Enquiry")
        balance_button.bind(on_press=self.check_balance)
        change_details_button = Button(text="Change Login Details")
        currency_button = Button(text="Currency Option")
        currency_button.bind(on_press=self.currency_option)
        mobile_verification_button = Button(text="Mobile Verification")
        mobile_verification_button.bind(on_press=self.mobile_verification)
        logout_button = Button(text="Logout")
        logout_button.bind(on_press=self.logout)
        self.services_layout.add_widget(self.services_label)
        self.services_layout.add_widget(balance_button)
        self.services_layout.add_widget(change_details_button)
        self.services_layout.add_widget(currency_button)
        self.services_layout.add_widget(mobile_verification_button)
        self.services_layout.add_widget(logout_button)

    def login(self, instance):
        # Sample validation (replace with actual logic)
        username = self.username_entry.text
        password = self.password_entry.text

        if username == "user" and password == "password":
            self.login_layout.clear_widgets()
            self.login_layout.add_widget(self.services_layout)
        else:
            self.show_error_popup("Error", "Invalid username or password")

    def check_balance(self, instance):
        popup = Popup(title='Balance', content=Label(text=f"Your balance is ${self.current_balance}"), size_hint=(None, None), size=(300, 200))
        popup.open()

    def logout(self, instance):
        self.username_entry.text = ''
        self.password_entry.text = ''
        self.login_layout.clear_widgets()
        self.init_ui()

    def show_error_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

    def mobile_verification(self, instance):
        self.login_layout.clear_widgets()
        mobile_label = Label(text="Enter Mobile Number")
        self.mobile_number_entry = TextInput(hint_text='Mobile Number')
        send_code_button = Button(text="Send Verification Code")
        send_code_button.bind(on_press=self.send_verification_code)
        self.mobile_verification_layout.add_widget(mobile_label)
        self.mobile_verification_layout.add_widget(self.mobile_number_entry)
        self.mobile_verification_layout.add_widget(send_code_button)
        back_button = Button(text="Back")
        back_button.bind(on_press=self.back_to_services)
        self.mobile_verification_layout.add_widget(back_button)
        self.login_layout.add_widget(self.mobile_verification_layout)

    def send_verification_code(self, instance):
        mobile_number = self.mobile_number_entry.text
        # Here, you can implement the code to send the verification code to the provided mobile number
        verification_code = random.randint(1000, 9999)
        message = f"Your verification code is: {verification_code}"  # Replace with actual message sending logic
        self.show_popup("Verification Code Sent", message)

    def back_to_services(self, instance):
        self.mobile_verification_layout.clear_widgets()
        self.login_layout.clear_widgets()
        self.login_layout.add_widget(self.services_layout)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

    def currency_option(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        currencies = {
            "USD": "$ (Dollar)",
            "INR": "₹ (Rupee)",
            "GBP": "£ (Pound)",
            "JPY": "¥ (Yen)",
            # Add more currencies here
        }
        for code, symbol in currencies.items():
            currency_label = Label(text=f"{code} - {symbol}")
            popup_content.add_widget(currency_label)

        back_button = Button(text="Back")
        back_button.bind(on_press=self.back_to_services)
        popup_content.add_widget(back_button)

        currency_popup = Popup(title="Currency Options", content=popup_content, size_hint=(None, None), size=(400, 300))
        currency_popup.open()


if __name__ == "__main__":
    ATM().run()
