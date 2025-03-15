import streamlit as st
import json

# Функция загрузки данных пользователей
try:
    with open("../decision_weights.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {"users": {}}

# Страница с вводом ID
st.title("Весовые коэффициенты для принятия решений")

# Ввод ID пользователя
user_id = st.text_input("Введите ваш ID")

if user_id:
    if user_id not in user_data["users"]:
        user_data["users"][user_id] = {
            "weights": {
                "Мили": 0,
                "Рубли": 0,
                "Льготный период": 0,
                "Лимит кредита": 0
            }
        }

    st.subheader("Заполните значения по важности")

    # Ввод значений пользователем
    user_data["users"][user_id]["weights"]["Мили"] = st.number_input("Мили", min_value=0, max_value=100, value=user_data["users"][user_id]["weights"].get("Мили", 0))
    user_data["users"][user_id]["weights"]["Рубли"] = st.number_input("Рубли", min_value=0, max_value=100, value=user_data["users"][user_id]["weights"].get("Рубли", 0))
    user_data["users"][user_id]["weights"]["Льготный период"] = st.number_input("Льготный период", min_value=0, max_value=100, value=user_data["users"][user_id]["weights"].get("Льготный период", 0))
    user_data["users"][user_id]["weights"]["Лимит кредита"] = st.number_input("Лимит кредита", min_value=0, max_value=100, value=user_data["users"][user_id]["weights"].get("Лимит кредита", 0))

    # Сохранение данных
    if st.button("Сохранить данные"):
        with open("../decision_weights.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)
        st.success(f"Данные для пользователя {user_id} сохранены!")

    # Отображение данных пользователя
    st.subheader("Ваши данные")
    st.json(user_data["users"][user_id])