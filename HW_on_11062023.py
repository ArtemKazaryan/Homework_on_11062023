
# !!!!!!  ДЛЯ ЗАПУСКА ОТДЕЛЬНЫХ ЗАДАНИЙ РАСКОММЕНТИРУЙТЕ ИХ РЕШЕНИЕ  !!!!!!


# Домашняя работа на 11.06.2023.

# Задание 1
# Реализуйте шаблон Factory Method, чтобы создать SocialMediaAccountFactory,
# который создает различные типы учетных записей социальных сетей (например, Facebook, Instagram, Twitter).
# Кроме того, реализуйте шаблон прокси, создав учетную запись ProxySocialMediaAccount,
# которая выступает в качестве прокси для фактической учетной записи в социальной сети,
# предоставляя дополнительные функции, такие как модерация контента и контроль доступа.

# Решение:
from abc import ABC, abstractmethod
# Абстрактный класс SocialMediaAccount
class SocialMediaAccount(ABC):
    @abstractmethod
    def create_post(self, content):
        pass
# Класс FacebookAccount, реализующий интерфейс SocialMediaAccount
class FacebookAccount(SocialMediaAccount):
    def create_post(self, content):
        print(f"Создан пост на Facebook: {content}")
# Класс InstagramAccount, реализующий интерфейс SocialMediaAccount
class InstagramAccount(SocialMediaAccount):
    def create_post(self, content):
        print(f"Создан пост на Instagram: {content}")
# Класс TwitterAccount, реализующий интерфейс SocialMediaAccount
class TwitterAccount(SocialMediaAccount):
    def create_post(self, content):
        print(f"Создан пост на Twitter: {content}")
# Фабрика SocialMediaAccountFactory
class SocialMediaAccountFactory:
    def create_account(self, account_type):
        if account_type == "Facebook":
            return FacebookAccount()
        elif account_type == "Instagram":
            return InstagramAccount()
        elif account_type == "Twitter":
            return TwitterAccount()
# Пример использования фабрики
factory = SocialMediaAccountFactory()
facebook_account = factory.create_account("Facebook")
facebook_account.create_post("Привет, Facebook!")
instagram_account = factory.create_account("Instagram")
instagram_account.create_post("Привет, Instagram!")
twitter_account = factory.create_account("Twitter")
twitter_account.create_post("Привет, Twitter!")

# Класс ProxySocialMediaAccount, реализующий интерфейс SocialMediaAccount
class ProxySocialMediaAccount(SocialMediaAccount):
    def __init__(self, real_account):
        self.real_account = real_account
    def create_post(self, content):
        # Реализация дополнительной функциональности (модерация контента, контроль доступа и т.д.)
        if "спам" in content.lower():
            print("Пост содержит запрещенный контент")
        else:
            self.real_account.create_post(content)
# Пример использования прокси-объекта
real_facebook_account = FacebookAccount()
proxy_facebook_account = ProxySocialMediaAccount(real_facebook_account)
proxy_facebook_account.create_post("Привет, Facebook!")
proxy_facebook_account.create_post("Реклама спама") # будет выведено сообщение о запрещенном контенте

print()

# Задание 2
# Создайте класс File, в котором опишите базовые методы для работы с файлами через функции,
# встроенные в python. Затем реализуйте шаблон Proxy, создав класс FileProxy,
# который действует как прокси для фактического класса File. FileProxy должен предоставлять дополнительные функции,
# такие как регистрация попыток чтения файлов, ограничение прав доступа и кэширование содержимого файла.

# Решение:
import os
class File:
    def __init__(self, filename):
        self.filename = filename
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()
    def write(self, content):
        with open(self.filename, 'w') as f:
            f.write(content)
    def delete(self):
        os.remove(self.filename)

class FileProxy:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.reads = 0 # количество попыток чтения файла
        self.content_cache = None # кэш содержимого файла
    def read(self):
        self.reads += 1
        if self.file is None:
            self.file = File(self.filename)
        if self.content_cache is None:
            self.content_cache = self.file.read()
        return self.content_cache
    def write(self, content):
        if self.file is None:
            self.file = File(self.filename)
        self.content_cache = content
        self.file.write(content)
    def delete(self):
        if self.file is None:
            self.file = File(self.filename)
        self.file.delete()
    # Реализация дополнительной функциональности (ограничение прав доступа и т.д.)
    def set_access_rights(self, rights):
        os.chmod(self.filename, rights)

file_proxy = FileProxy('test.txt')
file_proxy.write('Привет, мир!')
content = file_proxy.read()
print(content)
print(file_proxy.reads) # будет выведено 1, так как файл был прочитан 1 раз
file_proxy.set_access_rights(0o777) # установим права доступа 777
file_proxy.delete() # удалим файл

print()

# Задание 3
# Напишите программу дистанционного управления электронными устройствами
# (например, телевизором, DVD-плеером), используя шаблон Command. Реализуйте набор команд
# (например, PowerOnCommand, PowerOffCommand, VolumeUpCommand, VolumeDownCommand),
# которые инкапсулируют действия, выполняемые на устройствах. На пульте дистанционного
# управления должны быть кнопки для выполнения этих команд, и он должен иметь возможность
# отменить или повторить выполненные команды. Пример использования такого кода:
#   remote_control = RemoteControl()
# 	power_on_command = PowerOnCommand(tv)
# 	volume_up_command = VolumeUpCommand(tv)
#
# 	remote_control.set_command(0, power_on_command)  # Кнопка 0 будет включать ТВ
# 	remote_control.set_command(1, volume_up_command)  # Кнопка 1 будет увеличивать громкость
#
# 	remote_control.press_button(0)  # Включает ТВ
# 	remote_control.press_button(1)  # Поднимает уровень громкости

# Решение:
class ElectronicDevice:
    def on(self):
        pass
    def off(self):
        pass
    def volume_up(self):
        pass
    def volume_down(self):
        pass

class TV(ElectronicDevice):
    def on(self):
        print("TV is on")
    def off(self):
        print("TV is off")
    def volume_up(self):
        print("TV volume up")
    def volume_down(self):
        print("TV volume down")

class Command:
    def execute(self):
        pass
    def undo(self):
        pass

class PowerOnCommand(Command):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.on()
    def undo(self):
        self.device.off()

class PowerOffCommand(Command):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.off()
    def undo(self):
        self.device.on()

class VolumeUpCommand(Command):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.volume_up()
    def undo(self):
        self.device.volume_down()

class VolumeDownCommand(Command):
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.volume_down()
    def undo(self):
        self.device.volume_up()

class RemoteControl:
    def __init__(self):
        self.commands = {}
        self.undo_command = None
    def set_command(self, button, command):
        self.commands[button] = command
    def press_button(self, button):
        if button in self.commands:
            self.commands[button].execute()
            self.undo_command = self.commands[button]
    def undo_button(self):
        if self.undo_command:
            self.undo_command.undo()
            self.undo_command = None

# Пример использования
tv = TV()
remote_control = RemoteControl()
power_on_command = PowerOnCommand(tv)
power_off_command = PowerOffCommand(tv)
volume_up_command = VolumeUpCommand(tv)
volume_down_command = VolumeDownCommand(tv)
remote_control.set_command(0, power_on_command)
remote_control.set_command(1, power_off_command)
remote_control.set_command(2, volume_up_command)
remote_control.set_command(3, volume_down_command)
remote_control.press_button(0)  # Включает ТВ
remote_control.press_button(2)  # Поднимает уровень громкости
remote_control.press_button(2)  # Поднимает уровень громкости
remote_control.press_button(3)  # Опускает уровень громкости
remote_control.undo_button()  # Отмена последней команды (опускание громкости)
remote_control.press_button(1)  # Выключает ТВ
remote_control.undo_button()  # Отмена последней команды (включение ТВ)