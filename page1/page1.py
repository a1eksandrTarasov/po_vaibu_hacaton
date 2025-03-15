import streamlit as st
import json

# Пример данных о картах
cards_data = [
    {"card_id": 1, "name_card": "Tinkoff Platinum", "КЭШБЭК": True, "МИЛИ": True, "БАЛЛЫ БАНКА": False},
    {"card_id": 2, "name_card": "Tinkoff Server", "КЭШБЭК": True, "МИЛИ": False, "БАЛЛЫ БАНКА": True},
    {"card_id": 3, "name_card": "Alfa Travel", "КЭШБЭК": False, "МИЛИ": True, "БАЛЛЫ БАНКА": True},
]

# Пример данных с готовыми категориями и процентами
preset_cashback_data = {
    "Tinkoff Platinum": {"Продукты": 5, "Транспорт": 3},
    "Tinkoff Server": {"Одежда": 2, "Развлечения": 4},
}

# Пример категорий
categories = ["Продукты", "Транспорт", "Одежда", "Развлечения", "Другое"]

st.title("Пользователь вводит инфу")

# Хранение данных о введенных картах
try:
    with open("../user_data.json", "r") as file:
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
    if cashback_info:
        st.write("Автоматически подставленные категории (можно изменить):")
        for category, percent in cashback_info.items():
            cashback_info[category] = st.number_input(f"% (Кэшбек - {category})", min_value=0, max_value=100, value=percent)
    remaining_categories = [cat for cat in categories if cat not in cashback_info]
    cashback_count = st.number_input("Сколько категорий хотите добавить для кэшбэка?", min_value=0, max_value=10, value=0)
    user_added_cashback = []
    for i in range(cashback_count):
        category = st.selectbox(f"Категория {i + 1} (Кэшбек)", remaining_categories, key=f"cashback_cat{i}")
        cashback_percent = st.number_input(f"% (Кэшбек - {category})", min_value=0, max_value=100, key=f"cashback_perc{i}")
        cashback_info[category] = cashback_percent
        user_added_cashback.append(category)
        remaining_categories.remove(category)

if miles_enabled:
    st.subheader("Мили")
    miles_count = st.number_input("Сколько категорий хотите добавить для миль?", min_value=0, max_value=10, value=0)
    user_added_miles = []
    for i in range(miles_count):
        category = st.selectbox(f"Категория {i + 1} (Мили)", [cat for cat in categories if cat not in user_added_miles], key=f"miles_cat{i}")
        miles_percent = st.number_input(f"% (Мили - {category})", min_value=0, max_value=100, key=f"miles_perc{i}")
        miles_info[category] = miles_percent
        user_added_miles.append(category)

if bank_points_enabled:
    st.subheader("Баллы банка")
    points_count = st.number_input("Сколько категорий хотите добавить для баллов банка?", min_value=0, max_value=10, value=0)
    user_added_points = []
    for i in range(points_count):
        category = st.selectbox(f"Категория {i + 1} (Баллы банка)", [cat for cat in categories if cat not in user_added_points], key=f"points_cat{i}")
        points_percent = st.number_input(f"% (Баллы банка - {category})", min_value=0, max_value=100, key=f"points_perc{i}")
        bank_points_info[category] = points_percent
        user_added_points.append(category)

if st.button("Добавить карту"):
    user_data["users"]["id"]["cards"].append({
        "card_id": selected_card["card_id"],
        "categories": {
            "Кэшбек": cashback_info,
            "Мили": miles_info,
            "Баллы банка": bank_points_info
        }
    })

    with open("../user_data.json", "w", encoding="UTF-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

    st.success(f"Карта {selected_card_name} добавлена!")

# Показ всех карт
if user_data["users"]["id"]["cards"]:
    st.subheader("Ваши карты (JSON)")
    st.json(user_data)
