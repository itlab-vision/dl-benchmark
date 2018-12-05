# Скрипт тестирования производительности Inference Engine OPENVINO

## Метрики теста производительности

- Метрики синхронного режима
    - `Список времен работы всех запросов обрабатывается правилом трех сигм`
    - `Latency - Медиана обработанного времени`
    - `FPS (Frame Per Seconds) = 1000 / Latency`
- Метрики асинхронного режима
    - `Average time of single pass = Общее время / Количество итераций`
    - `FPS (Frame Per Seconds) = 1000 / Average time of single pass`