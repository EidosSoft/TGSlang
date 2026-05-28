# TGS (Terminal Generative Script)

**TGS** — простой язык программирования для автоматизации задач.

## Быстрый старт

```tgs
print "Hello, World!"
print "What's your name?"
input $name
print "Hello, $name!"
```

## Установка

```batch
git clone https://github.com/YOUR_USERNAME/tgs-lang.git
cd tgs-lang
tgs --install
```

## Команды

- `print` - вывод
- `input` - ввод
- `set` - переменная
- `if` - условие
- `goto` - переход
- `generate` - генерация чисел

## Пример

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
