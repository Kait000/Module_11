from inspect import getmodule


class TV:
    """
    ========================================================
    Класс для работы с телевизором LG с диагональю 56 дюймов
    ========================================================
    Доступные методы:
        >> tv_on()              - включить телевизор
        >> tv_off()             - выключить телевизор
        >> set_channel()        - выбрать канал
        >> set_volume()         - установить громкость
        >> get_channel()        - получить номер канала
        >> get_volume()         - получить значение громкости
    """
    BRAND = 'LG'
    DIAGONAL = '56`'
    _MAX_CHANNEL, _MAX_VOLUME = 100, 100
    _MIN_CHANNEL, _MIN_VOLUME = 0, 0

    def __init__(self):
        self.__channel = 0
        self.__volume = 0
        self.__power = 'OFF'

    def tv_on(self):
        """Включает телевизор"""
        self.__power = 'ON'

    def tv_off(self):
        """Выключает телевизор"""
        self.__power = 'OFF'

    def set_channel(self, channel=0):
        """Устанавливает программу, принимает один параметр
        channel в диапазоне от 0 до 100, по умолчанию 0"""
        self.__power = 'ON'
        if self._MIN_CHANNEL <= channel <= self._MAX_CHANNEL:
            self.__channel = channel

    def set_volume(self, volume=0):
        """Устанавливает громкость, принимает один параметр
        volume в диапазоне от 0 до 100, по умолчанию 0"""
        if self.__power == 'OFF':
            pass
        if volume < self._MIN_VOLUME:
            self.__volume = 0
        elif volume > self._MAX_VOLUME:
            self.__volume = 100
        else:
            self.__volume = volume

    def get_channel(self):
        """Возвращает номер включенного канала"""
        if self.__power == 'OFF':
            pass
        return self.__channel

    def get_volume(self):
        """Возвращает текущую громкость"""
        if self.__power == 'OFF':
            pass
        return self.__volume


def introspection_info(obj):
    attributes = []
    methods = []
    for _ in dir(obj):
        if callable(getattr(obj, _)):
            methods.append(_)
        else:
            attributes.append(_)

    return (f'\033[31mТип объекта\033[0m \033[33m{type(obj)}\033[0m\n'
            f'\033[31mАтрибуты объекта\033[0m \033[33m{attributes}\033[0m\n'
            f'\033[31mМетоды объекта\033[0m \033[33m{methods}\033[0m\n'
            f'\033[31mПринадлежность объекта к модулю\033[0m \033[33m{getmodule(obj)}\033[0m\n\n'
            f'\033[31mСправка {type(obj).__name__}:\033[0m \033[33m{obj.__doc__}')


myTV = TV()
myTV.set_channel(channel=10)
myTV.set_volume(volume=60)

obj_info = introspection_info(myTV)
print(obj_info)
