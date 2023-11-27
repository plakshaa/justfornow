from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class User:
    def __init__(self, user_id, password, balance):
        self.user_id = user_id
        self.password = password
        self.balance = balance


class Admin:
    def __init__(self, admin_id, password, total_balance):
        self.admin_id = admin_id
        self.password = password
        self.total_balance = total_balance


class ATM(App):
    def __init__(self):
        super().__init__()

        # Initialize users and admin
        self.users = {
            "user1": User(user_id="user1", password="pass1", balance=5000),
            # Add more users here
        }
        self.admin = Admin(admin_id="admin", password="admin123", total_balance=500000)
        self.current_user = None
        self.failed_login_attempts = {}
        self.locked_accounts = {}

        # Currency symbols and conversion rates
        self.currency_symbols = {
            "USD": "$",  # Dollar
            "JPY": "¥",  # Yen
            "GBP": "£",  # Pound
            "EUR": "€",  # Euro
            "INR": "₹",  # Rupee
        }
        self.conversion_rates = {
            "USD": 1.0,
            "JPY": 113.05,
            "GBP": 0.72,
            "EUR": 0.84,
            "INR": 74.5,
        }

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.user_id_input = TextInput(hint_text='User ID')
        self.password_input = TextInput(hint_text='Password', password=True)
        login_button = Button(text='Login', on_press=self.login)

        self.layout.add_widget(Label(text='Welcome to the ATM'))
        self.layout.add_widget(self.user_id_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(login_button)

        return self.layout

    def login(self, instance):
        user_id = self.user_id_input.text
        password = self.password_input.text

        if user_id in self.users:
            user = self.users[user_id]
            if user.password == password:
                self.current_user = user
                self.show_user_menu()
            else:
                self.show_error_popup('Error', 'Incorrect password')
        elif user_id == self.admin.admin_id and password == self.admin.password:
            self.current_user = self.admin
            self.show_admin_menu()
        else:
            self.show_error_popup('Error', 'User not found')

    def deposit(self, amount):
        try:
            amount = int(amount)
            if amount > 0:
                self.current_user.balance += amount
                self.show_success_popup('Success', f'Deposited {amount} successfully!')
            else:
                self.show_error_popup('Error', 'Enter a valid amount')
        except ValueError:
            self.show_error_popup('Error', 'Enter a valid amount')

    def withdraw(self, amount):
        try:
            amount = int(amount)
            if amount > 0 and amount <= self.current_user.balance:
                self.current_user.balance -= amount
                self.show_success_popup('Success', f'Withdrawn {amount} successfully!')
            else:
                self.show_error_popup('Error', 'Invalid amount or insufficient balance')
        except ValueError:
            self.show_error_popup('Error', 'Enter a valid amount')

    def check_balance(self, instance):
        if self.current_user:
            self.show_success_popup('Balance', f'Your balance is {self.current_user.balance}')
        else:
            self.show_error_popup('Error', 'Login to check balance')

    def change_password(self, current_password, new_password):
        if self.current_user:
            if current_password == self.current_user.password:
                self.current_user.password = new_password
                self.show_success_popup('Success', 'Password changed successfully!')
            else:
                self.show_error_popup('Error', 'Incorrect current password')
        else:
            self.show_error_popup('Error', 'Login to change password')

    def convert_currency(self, target_currency):
        if self.current_user:
            target_rate = self.conversion_rates.get(target_currency, 1.0)
            converted_balance = self.current_user.balance / target_rate
            symbol = self.currency_symbols.get(target_currency, "")
            self.show_success_popup('Converted Balance', f'Your balance is {symbol}{converted_balance:.2f} in {target_currency}')
        else:
            self.show_error_popup('Error', 'Login to convert currency')

    def show_currency_options(self, instance):
        currencies = ["USD", "JPY", "GBP", "EUR", "INR"]

        for currency in currencies:
            currency_button = Button(text=f"Convert to {currency}", on_press=lambda x, currency=currency: self.convert_currency(currency))
            self.layout.add_widget(currency_button)

        back_button = Button(text="Back", on_press=self.show_user_menu)
        self.layout.add_widget(back_button)

    def show_user_menu(self):
        self.layout.clear_widgets()

        deposit_button = Button(text='Deposit', on_press=self.show_deposit_popup)
        withdraw_button = Button(text='Withdraw', on_press=self.show_withdraw_popup)
        check_balance_button = Button(text='Check Balance', on_press=self.check_balance)
        change_password_button = Button(text='Change Password', on_press=self.show_change_password_popup)
        convert_currency_button = Button(text='Currency Conversion', on_press=self.show_currency_options)

        self.layout.add_widget(deposit_button)
        self.layout.add_widget(withdraw_button)
        self.layout.add_widget(check_balance_button)
        self.layout.add_widget(change_password_button)
        self.layout.add_widget(convert_currency_button)

    def show_admin_menu(self):
        self.layout.clear_widgets()

        total_balance_button = Button(text='Total Balance', on_press=self.admin_total_balance)
        deposit_button = Button(text='Admin Deposit', on_press=self.show_admin_deposit_popup)
        notification_button = Button(text='Notification', on_press=self.admin_notification)

        self.layout.add_widget(total_balance_button)
        self.layout.add_widget(deposit_button)
        self.layout.add_widget(notification_button)

    def show_deposit_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        amount_input = TextInput(hint_text='Enter Amount')
        confirm_button = Button(text='Deposit', on_press=lambda x: self.deposit(amount_input.text))

        popup_layout.add_widget(Label(text='Cash Deposit'))
        popup_layout.add_widget(amount_input)
        popup_layout.add_widget(confirm_button)

        popup = Popup(title='Cash Deposit', content=popup_layout, size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_withdraw_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        amount_input = TextInput(hint_text='Enter Amount')
        confirm_button = Button(text='Withdraw', on_press=lambda x: self.withdraw(amount_input.text))

        popup_layout.add_widget(Label(text='Cash Withdrawal'))
        popup_layout.add_widget(amount_input)
        popup_layout.add_widget(confirm_button)

        popup = Popup(title='Cash Withdrawal', content=popup_layout, size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_change_password_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        current_password_input = TextInput(hint_text='Current Password', password=True)
        new_password_input = TextInput(hint_text='New Password', password=True)
        confirm_button = Button(text='Change', on_press=lambda x: self.change_password(current_password_input.text, new_password_input.text))

        popup_layout.add_widget(Label(text='Change Password'))
        popup_layout.add_widget(current_password_input)
        popup_layout.add_widget(new_password_input)
        popup_layout.add_widget(confirm_button)

        popup = Popup(title='Change Password', content=popup_layout, size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_error_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_success_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

    # Other methods and the main block remain
