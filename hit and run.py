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
        self.users = {
            "user1": User(user_id="user1", password="pass1", balance=5000),
            # Add more users here
        }
        self.admin = Admin(admin_id="admin", password="admin123", total_balance=500000)
        self.current_user = None
        self.failed_login_attempts = {}
        self.locked_accounts = {}

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

        if user_id in self.locked_accounts:
            self.show_error_popup("Account Locked", "Account is locked. Contact admin.")
            return

        if user_id in self.users and self.users[user_id].password == password:
            if user_id in self.failed_login_attempts:
                del self.failed_login_attempts[user_id]
            self.current_user = self.users[user_id]
            self.show_user_menu()
        elif user_id == self.admin.admin_id and password == self.admin.password:
            if self.admin.admin_id in self.failed_login_attempts:
                del self.failed_login_attempts[self.admin.admin_id]
            self.show_admin_menu()
        else:
            if user_id not in self.failed_login_attempts:
                self.failed_login_attempts[user_id] = 1
            else:
                self.failed_login_attempts[user_id] += 1

            if self.failed_login_attempts[user_id] >= 3:
                self.locked_accounts[user_id] = True
                self.show_error_popup("Account Locked", "Too many failed attempts. Account locked.")
            else:
                self.show_error_popup("Login Error", "Invalid credentials")

    def handle_denominations(self, amount):
        denominations = {2000: 0, 500: 0, 200: 0, 100: 0}
        remaining_amount = amount

        for denomination in denominations.keys():
            if remaining_amount >= denomination:
                denominations[denomination] = remaining_amount // denomination
                remaining_amount %= denomination

        return denominations

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            self.current_user.balance += amount
            denominations = self.handle_denominations(amount)
            self.show_success_popup("Deposit", f"Successfully deposited ${amount}\nDenominations: {denominations}")
        except ValueError:
            self.show_error_popup("Error", "Invalid amount")

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            if amount > self.current_user.balance:
                self.show_error_popup("Error", "Insufficient balance")
            else:
                self.current_user.balance -= amount
                denominations = self.handle_denominations(amount)
                self.show_success_popup("Withdrawal", f"Withdrew ${amount}\nDenominations: {denominations}")
        except ValueError:
            self.show_error_popup("Error", "Invalid amount")

    def check_balance(self, instance):
        if self.current_user.balance < 5000:
            self.show_error_popup("Low Balance", "Your balance is below the minimum required.")
        self.show_success_popup("Balance", f"Your balance is ${self.current_user.balance}")

    def change_password(self, current_password, new_password):
        if current_password == self.current_user.password:
            self.current_user.password = new_password
            self.show_success_popup("Password Changed", "Password has been updated")
        else:
            self.show_error_popup("Error", "Incorrect current password")

    def admin_total_balance(self, instance):
        denominations = self.handle_denominations(self.admin.total_balance)
        balance_msg = f"Total balance: ${self.admin.total_balance}\nDenominations: {denominations}"
        self.show_success_popup("Admin Balance", balance_msg)

    def show_admin_deposit_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        amount_input = TextInput(hint_text='Enter Amount')
        confirm_button = Button(text='Deposit', on_press=lambda x: self.admin_cash_deposit(amount_input.text))

        popup_layout.add_widget(Label(text='Cash Deposit'))
        popup_layout.add_widget(amount_input)
        popup_layout.add_widget(confirm_button)

        popup = Popup(title='Cash Deposit', content=popup_layout, size_hint=(None, None), size=(300, 200))
        popup.open()

    def admin_cash_deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            self.admin.total_balance += amount
            self.show_success_popup("Admin Deposit", f"Successfully deposited ${amount}")
        except ValueError:
            self.show_error_popup("Error", "Invalid amount")

    def admin_notification(self, instance):
        low_balance_users = [user.user_id for user in self.users.values() if user.balance < 75000]
        if low_balance_users:
            self.show_error_popup("Low Balance Users", f"Users with low balance: {', '.join(low_balance_users)}")

    def show_user_menu(self):
        self.layout.clear_widgets()

        deposit_button = Button(text='Deposit', on_press=self.show_deposit_popup)
        withdraw_button = Button(text='Withdraw', on_press=self.show_withdraw_popup)
        check_balance_button = Button(text='Check Balance', on_press=self.check_balance)
        change_password_button = Button(text='Change Password', on_press=self.show_change_password_popup)

        self.layout.add_widget(deposit_button)
        self.layout.add_widget(withdraw_button)
        self.layout.add_widget(check_balance_button)
        self.layout.add_widget(change_password_button)

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
        confirm_button = Button(text='Change', on_press=lambda x: self.change_password(
            current_password_input.text, new_password_input.text))

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


if __name__ == "__main__":
    ATM().run()
