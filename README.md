## `README.md`

```markdown
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/EidosSoft/tgs-lang)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-yellow.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Size](https://img.shields.io/github/repo-size/EidosSoft/tgs-lang)]()

# TGS - Terminal Generative Script

**TGS** — простой язык программирования для автоматизации задач и генерации данных.

## 🚀 Быстрый старт

```tgs
print "Hello, World!"
print "What is your name?"
input $name
print "Welcome, $name!"
```

## 📥 Установка

```bash
git clone https://github.com/EidosSoft/tgs-lang.git
cd tgs-lang
tgs --install
```

## 📖 Команды

| Команда | Описание | Пример |
|---------|----------|--------|
| `print` | Вывод | `print "Hello"` |
| `input` | Ввод | `input $name` |
| `set` | Переменная | `set $x 10` |
| `if` | Условие | `if $x == 10 label` |
| `goto` | Переход | `goto start` |
| `generate` | Генерация чисел | `generate 5 numbers from 1 to 100 into $list` |
| `list` | Показать список | `list $list` |
| `run` | Системная команда | `run "dir"` |
| `exit` | Выход | `exit` |

## 💡 Примеры

### Калькулятор
```tgs
set $a 10
set $b 5
set $sum $a + $b
print "$a + $b = $sum"
```

### Цикл
```tgs
set $i 1
loop:
    print "Count: $i"
    set $i $i + 1
    if $i == 5 end
    goto loop
end:
    print "Done!"
```

### Игра "Угадай число"
```tgs
generate 1 numbers from 1 to 10 into $secret
print "Guess the number:"
input $guess
if $guess == $secret win
print "Wrong! It was $secret"
goto end
win:
print "Correct!"
end:
```

## 🛠 Использование CLI

```bash
tgs script.tgs        # Запуск скрипта
tgs -v                # Версия
tgs -h                # Помощь
tgs -d                # Режим отладки
tgs -e "print \"Hi\"" # Выполнить строку
tgs --banner          # Показать баннер
```

## 📝 Особенности

- ✅ Простой синтаксис
- ✅ Переменные и арифметика
- ✅ Условные переходы
- ✅ Генерация случайных чисел
- ✅ Работа со списками
- ✅ Системные команды

## 📄 Лицензия

MIT License

## © Автор

**EidosSoft**

---
