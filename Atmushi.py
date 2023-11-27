from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
import random
import time  # For the simulated delay in verification

Window.clearcolor = (1, 1, 1, 1)  # Set background color

class ATM(App):
    def __init__(self):
        super().__init__()
        self.current_balance = 5000  # Sample initial balance
        self.login_layout = BoxLayout(orientation='vertical', padding=dp(20))
        self.services_layout = BoxLayout(orientation='vertical', padding=dp(20))
        self.mobile_verification_layout = BoxLayout(orientation='vertical', padding=dp(20))
        self.currency_layout = BoxLayout(orientation='vertical', padding=dp(20))
        self.init_ui()

        self.is_mobile_verified = False
        self.phone_number = ""
        self.verification_code = ""

    def build(self):
        return self.login_layout

    def init_ui(self):
        label = Label(text='Welcome to the ATM', font_size=dp(24), color=(0, 0, 0, 1))
        login_button = Button(text='Login', size_hint=(None, None), size=(dp(150), dp(50)),
                              background_color=(0.2, 0.6, 1, 1))
        login_button.bind(on_press=self.mobile_verification)
        
        self.login_layout.add_widget(label)
        self.login_layout.add_widget(login_button)

    def mobile_verification(self, instance):
        self.login_layout.clear_widgets()
        self.mobile_verification_layout.clear_widgets()

        label = Label(text="Enter your phone number:")
        self.phone_number_input = TextInput(hint_text="Phone Number")
        verify_button = Button(text="Send Code")
        verify_button.bind(on_press=self.send_verification_code)

        self.mobile_verification_layout.add_widget(label)
        self.mobile_verification_layout.add_widget(self.phone_number_input)
        self.mobile_verification_layout.add_widget(verify_button)

        self.root.add_widget(self.mobile_verification_layout)

    def send_verification_code(self, instance):
        self.phone_number = self.phone_number_input.text
        self.verification_code = str(random.randint(1000, 9999))

        # Simulating sending the code by displaying it in the console
        print(f"Verification code sent to {self.phone_number}: {self.verification_code}")

        # Simulating a delay for receiving the code (2 seconds)
        time.sleep(2)

        code_label = Label(text="Enter the verification code sent to your phone:")
        self.code_input = TextInput(hint_text="Verification Code")
        verify_code_button = Button(text="Verify Code")
        verify_code_button.bind(on_press=self.verify_code)

        self.mobile_verification_layout.clear_widgets()
        self.mobile_verification_layout.add_widget(code_label)
        self.mobile_verification_layout.add_widget(self.code_input)
        self.mobile_verification_layout.add_widget(verify_code_button)

    def verify_code(self, instance):
        entered_code = self.code_input.text
        if entered_code == self.verification_code:
            self.is_mobile_verified = True
            self.mobile_verification_layout.clear_widgets()
            self.show_verification_success_message()
            self.display_options()  # Function to display options after verification
        else:
            self.show_error_popup("Error", "Invalid verification code")

    def show_verification_success_message(self):
        verified_label = Label(text="Verified!", font_size=dp(20), color=(0, 0.7, 0, 1))
        self.mobile_verification_layout.add_widget(verified_label)

    def display_options(self):
        balance_button = Button(text='Check Balance', size_hint=(None, None), size=(dp(150), dp(50)),
                                background_color=(0.2, 0.6, 1, 1))
        balance_button.bind(on_press=self.check_balance)

        withdraw_button = Button(text='Withdraw', size_hint=(None, None), size=(dp(150), dp(50)),
                                 background_color=(0.2, 0.6, 1, 1))
        withdraw_button.bind(on_press=self.withdraw)

        deposit_button = Button(text='Deposit', size_hint=(None, None), size=(dp(150), dp(50)),
                                background_color=(0.2, 0.6, 1, 1))
        deposit_button.bind(on_press=self.deposit)

        currency_button = Button(text='Currency Exchange', size_hint=(None, None), size=(dp(150), dp(50)),
                                 background_color=(0.2, 0.6, 1, 1))
        currency_button.bind(on_press=self.currency_option)

        logout_button = Button(text='Logout', size_hint=(None, None), size=(dp(150), dp(50)),
                               background_color=(0.2, 0.6, 1, 1))
        logout_button.bind(on_press=self.logout)

        self.services_layout.add_widget(balance_button)
        self.services_layout.add_widget(withdraw_button)
        self.services_layout.add_widget(deposit_button)
        self.services_layout.add_widget(currency_button)
        self.services_layout.add_widget(logout_button)

        self.root.add_widget(self.services_layout)

    def logout(self, instance):
        self.root.clear_widgets()
        self.init_ui()

    def check_balance(self, instance):
        self.show_popup('Balance', f'Your balance is ${self.current_balance}')

    def withdraw(self, instance):
        if self.is_mobile_verified:
            self.show_withdraw_deposit_popup("Withdraw", self.withdraw_action)
        else:
            self.show_error_popup("Error", "Mobile verification required for withdrawal")

    def deposit(self, instance):
        if self.is_mobile_verified:
            self.show_withdraw_deposit_popup("Deposit", self.deposit_action)
        else:
            self.show_error_popup("Error", "Mobile verification required for deposit")

    def currency_option(self, instance):
        self.services_layout.clear_widgets()

        currencies = {
            "USD": "$ (Dollar) - 1.0",
            "INR": "₹ (Rupee) - 74.5",
            "GBP": "£ (Pound) - 0.72",
            "JPY": "¥ (Yen) - 113.05",
            # Add more currencies here
        }
        for code, details in currencies.items():
            currency_button = Button(text=details, size_hint=(None, None), size=(dp(200), dp(50)),
                                     background_color=(0.2, 0.6, 1, 1))
            currency_button.bind(on_press=lambda instance, code=code: self.convert_currency(code))
            self.services_layout.add_widget(currency_button)

        back_button = Button(text="Back", size_hint=(None, None), size=(dp(150), dp(50)),
                             background_color=(0.2, 0.6, 1, 1))
        back_button.bind(on_press=self.display_options)
        self.services_layout.add_widget(back_button)

    def convert_currency(self, target_currency):
        conversion_rates = {
            "USD": 1.0,
            "INR": 74.5,  # Sample conversion rates
            "GBP": 0.72,
            "JPY": 113.05,
            # Add more conversion rates here
        }
        target_symbol = {
            "USD": "$",
            "INR": "₹",
            "GBP": "£",
            "JPY": "¥",
            # Add more symbols here
        }
        target_rate = conversion_rates.get(target_currency, 1.0)
        converted_balance = self.current_balance / target_rate
        symbol = target_symbol.get(target_currency, "")
        self.current_balance = converted_balance  # Update current balance after currency conversion
        self.show_popup('Converted Balance', f'Your balance is {symbol}{converted_balance:.2f} in {target_currency}')

    # Other existing methods like show_error_popup, withdraw_action, deposit_action, update_balance, show_withdraw_deposit_popup, show_verification_success_message

if __name__ == "__main__":
    ATM().run()
