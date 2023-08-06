import logging
import sys

logger = logging.getLogger('server')


class DescriptPort:
    '''
    Класс - дескриптор. Проверяет корректность подключаемого порта
    '''

    def __set__(self, instance, port):
        try:
            if port < 1024 or port > 65535:
                raise ValueError
            instance.__dict__[self.name] = port
        except IndexError:
            logger.critical(f'Не верно указан порт сервера')
            sys.exit(1)
        except ValueError:
            logger.critical(f'Порт не может быть меньше "1024" или больше "65535"')
            sys.exit(1)

    def __set_name__(self, my_class, my_port):
        self.name = my_port
