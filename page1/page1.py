import streamlit as st
import json

# Загрузка данных MCC-кодов
try:
    with open("mcc_code.json", "r", encoding="utf-8") as file:
        mcc_data = json.load(file)
except FileNotFoundError:
    mcc_data = {}

# Пример данных о картах
cards_data = [
    {"card_id": 1, "name_card": "Tinkoff Platinum", "КЭШБЭК": True, "МИЛИ": True, "БАЛЛЫ БАНКА": False},
    {"card_id": 2, "name_card": "Tinkoff Server", "КЭШБЭК": True, "МИЛИ": False, "БАЛЛЫ БАНКА": True},
    {"card_id": 3, "name_card": "Alfa Travel", "КЭШБЭК": False, "МИЛИ": True, "БАЛЛЫ БАНКА": True},
]

# Пример данных с готовыми категориями и процентами
preset_cashback_data = {
    "Tinkoff Platinum": {"Продуктовые магазины, супермаркеты": 5, "АЗС (с дополнительными услугами)": 3},
    "Tinkoff Server": {"Магазины мужской обуви": 2, "Рестораны и кафе": 4},
}
# Использование категорий из mcc_code.json
categories = list(mcc_data.values())

st.title("Пользователь вводит инфу")

# Хранение данных о введенных картах
try:
    with open("../user_data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {"users": {"id": {"cards": []}}}

st.subheader("Похожие карты:")
selected_card_name = st.selectbox("Выберите карту", [card["name_card"] for card in cards_data])
selected_card = next(card for card in cards_data if card["name_card"] == selected_card_name)

cashback_enabled = selected_card["КЭШБЭК"]
miles_enabled = selected_card["МИЛИ"]
bank_points_enabled = selected_card["БАЛЛЫ БАНКА"]

st.subheader(f"Настройки для карты: {selected_card_name}")

cashback_info = preset_cashback_data.get(selected_card_name, {}).copy()
miles_info = {}
bank_points_info = {}

if cashback_enabled:
    st.subheader("Кэшбек")
    for category, percent in cashback_info.items():
        cashback_info[category] = st.number_input(f"% (Кэшбек - {category})", min_value=0, max_value=100, value=percent)

if miles_enabled:
    st.subheader("Мили")
    remaining_categories = list(categories)
    miles_count = st.number_input("Сколько категорий хотите добавить для миль?", min_value=0, max_value=10, value=0)
    for i in range(miles_count):
        category = st.selectbox(f"Категория {i + 1} (Мили)", remaining_categories, key=f"miles_cat{i}")
        miles_percent = st.number_input(f"% (Мили - {category})", min_value=0, max_value=100, key=f"miles_perc{i}")
        miles_info[category] = miles_percent
        if category in remaining_categories:
            remaining_categories.remove(category)

if bank_points_enabled:
    st.subheader("Баллы банка")
    remaining_categories = list(categories)
    points_count = st.number_input("Сколько категорий хотите добавить для баллов банка?", min_value=0, max_value=10, value=0)
    for i in range(points_count):
        category = st.selectbox(f"Категория {i + 1} (Баллы банка)", remaining_categories, key=f"points_cat{i}")
        points_percent = st.number_input(f"% (Баллы банка - {category})", min_value=0, max_value=100, key=f"points_perc{i}")
        bank_points_info[category] = points_percent
        if category in remaining_categories:
            remaining_categories.remove(category)

if st.button("Добавить карту"):
    user_data["users"]["id"]["cards"].append({
        "card_id": selected_card["card_id"],
        "categories": {
            "Кэшбек": cashback_info,
            "Мили": miles_info,
            "Баллы банка": bank_points_info
        }
    })

    with open("../user_data.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

    st.success(f"Карта {selected_card_name} добавлена!")

# Показ всех карт
if user_data["users"]["id"]["cards"]:
    st.subheader("Ваши карты (JSON)")
    st.json(user_data)
