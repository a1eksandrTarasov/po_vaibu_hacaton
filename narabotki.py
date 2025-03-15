# Список всех существующих карт
ALL_CARDS = {}
# Список доступных на рынке карт (у них нет владельца)
AVIABLE_CARDS = []
# Словарь пользователей вида {id: User}
ALL_USERS = {}


def transaction_handler(transaction: dict, seller_id: int):
    """
    Обработчик транзакции

    Аргументы:
    - transaction (dict): Данные о транзакции, словарь вида:
    {
    "category": str - категория магазина,
    "shop": str - название магазина,
    "amount": int - сумма покупки,
    }
    - seller_id (int): ID пользователя

    Возвращает:
    - list: Список карт, отсортированный по выгодности
    """
    # Список карт, которые будем рассматривать
    cards_list = ALL_USERS[seller_id].cards + AVIABLE_CARDS
    cards_top = []
    for card in cards_list:
        result_sum = 0
        for pref in ALL_USERS[seller_id]['preferences']:
            result_sum += ALL_USERS[seller_id]['preferences'][pref] * \
                  card.get_benefit(transaction, pref)
        cards_top.append((card, result_sum))
    return sorted(cards_top, key=lambda x: x[1])


class User:
    """
    Класс, описывающий

    Аттрибуты:
        id (int): ID пользователя
        cards (list[Card]): Список карт пользователя
        preferences (dict): Ранжированный словарь предпочтений
    """
    def __init__(self, id, cards, preferences):
        self.id = id
        self.cards = self.__load_cards()
        self.preferences = preferences
    
    def __load_cards(self):
        """
        Возвращает список карт пользователя по его ID
        """
        pass
                


class Card:
    """
    Класс, описывающий карту

    Аттрибуты:
        id (int): ID карты
        cashbacks (dict): Словарь кэшбэков вида {"типа кэшбэка": %}
        additional (dict): Дополнительные аттрибуты карты вида {"название": int}, например:
        {"льготный период": 30, "стоимость обслуживания": 290}
    """
    def __init__(self, id, cashbacks, additional):
        self.id = id
        self.cashbacks = cashbacks
        self.additional = additional
    
    def get_benefit(self, transaction, param):
        """
        Тут обработка запроса на получение выгоды для данной транзакции transaction и параметра param
        """
        pass

