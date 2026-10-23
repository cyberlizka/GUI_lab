Структура проекта:

.
├── main.py               # Точка входа: создает QApplication, собирает "шину сигналов" (build_signal_bus) и запускает окно
├── usd_signals.py        # Класс UsdSignals с сигналом usd_changed (float)
├── eur_signals.py        # Класс EurSignals с сигналом eur_changed (float)
├── rub_signals.py        # Класс RubSignals с сигналом rub_changed (float)
├── common_signals.py     # Класс CommonSignals с сигналами clear_all и rates_updated (dict)
├── currency_converter.py # Интерфейс, логика пересчета (_apply), таблица курсов и сетевой запрос (API)
├── requirements.txt     # Список зависимостей (PyQt5)        
└── screenshots_2.md      # Описание проекта


Исходное окно при запуске приложения

<img width="378" height="209" alt="image" src="https://github.com/user-attachments/assets/4b162e6c-f987-47a4-bf38-c7003d6ad7b3" />

Обновление в строке USD

<img width="379" height="212" alt="image" src="https://github.com/user-attachments/assets/5566dd17-4c4f-418d-bf45-7e2681bca2f5" />

Обновление в строке EUR

<img width="380" height="208" alt="image" src="https://github.com/user-attachments/assets/4ceff0f6-4bf3-4249-8f65-3537d8ba9867" />

Обновление в строке RUB

<img width="381" height="208" alt="image" src="https://github.com/user-attachments/assets/b454cab1-5e4b-4807-bce4-c8a6c7b4b867" />

После нажатия Очистить все поля

<img width="376" height="210" alt="image" src="https://github.com/user-attachments/assets/3cfde8c5-c0eb-41ef-94a1-ece7708f6015" />



  

