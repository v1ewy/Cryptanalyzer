import copy
from collections import Counter

# Частотный порядок
RUSSIAN_FREQ_ORDER = [
    'о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л',
    'к', 'м', 'д', 'п', 'у', 'я', 'ы', 'ь', 'г', 'з',
    'б', 'ч', 'й', 'х', 'ж', 'ш', 'ю', 'ц', 'щ', 'э', 
    'ф', 'ъ', 'ё'
]

# Русский алфавит
RUSSIAN_ALPHABET = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

# Класс для криптоаналитики
class Cryptanalyzer:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext          # исходная строка шифротекста
        self.mapping = {}                      # текущий словарь замен: символ -> буква
        self.history = []                       # стек предыдущих состояний mapping

    def _save_state(self):
        """Сохраняет текущее состояние mapping в историю""" # ?
        self.history.append(copy.deepcopy(self.mapping))

    def compute_frequencies(self):
        """Возвращает список символов, отсортированных по убыванию частоты""" #
        freq = Counter(char for char in self.ciphertext if char != ' ')
        sorted_chars = [item[0] for item in freq.most_common()]
        return sorted_chars

    def group_words_by_length(self):
        """Возвращает словарь {длина: список слов} для всех слов криптограммы"""
        words = self.ciphertext.split()
        groups = {}
        for word in words:
            length = len(word)
            groups.setdefault(length, []).append(word)
        return groups

    def group_words_by_unknown(self):
        """
        Группирует слова по количеству нерасшифрованных символов
        Возвращает словарь {чиcлo_нeизвecтныx: список слов}
        """
        words = self.ciphertext.split()
        groups = {}
        for word in words:
            unknown = sum(1 for ch in word if ch not in self.mapping)
            groups.setdefault(unknown, []).append(word)
        return groups

    def current_text(self):
        """Возвращает строку c текущим состоянием дешифровки"""
        result = []
        for ch in self.ciphertext:
            if ch == ' ':
                result.append(' ')
            elif ch in self.mapping:
                result.append(self.mapping[ch])
            else:
                result.append(ch)
        return ''.join(result)

    def substitute(self, symbol, letter):
        """Задаёт или изменяет замену для символа"""
        if len(symbol) != 1 or len(letter) != 1:
            print("Ошибка: вводите по одному символу")
            return False
        if not (symbol.isalpha() and symbol.isupper()):
            print("Ошибка: символ криптограммы должен быть заглавной буквой")
            return False
        if letter not in RUSSIAN_ALPHABET:
            print("Ошибка: буква должна быть строчной русской буквой")
            return False

        self._save_state()
        self.mapping[symbol] = letter
        print(f"Замена {symbol} -> {letter} выполнена")
        return True

    def undo(self):
        """Откатывает последнее изменение mapping""" # ?
        if not self.history:
            print("Нет сохранённых состояний для отката")
            return False
        self.mapping = self.history.pop()
        print("Последнее изменение отменено")
        return True

    def auto_substitute(self):
        """Автоматическая замена на основе частотного анализа."""
        cipher_order = self.compute_frequencies()
        unmapped = [ch for ch in cipher_order if ch not in self.mapping]

        if not unmapped:
            print("Все символы уже имеют замены")
            return 0

        letters_to_use = RUSSIAN_FREQ_ORDER[:len(unmapped)]

        self._save_state()

        count = 0
        for ch, letter in zip(unmapped, letters_to_use):
            self.mapping[ch] = letter
            count += 1

        print(f"Автоматически заменено {count} символов")
        return count

# Загрузка шифротекста из файла
def load_ciphertext(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None

# Вывод меню
def print_help():
    print("\n--- МЕНЮ ---")
    print("1. Показать частоты символов")
    print("2. Показать слова по длине")
    print("3. Показать слова по количеству нерасшифрованных букв")
    print("4. Показать текущий текст")
    print("5. Заменить символ")
    print("6. Откатить последнюю замену")
    print("7. Автоматическая замена по частотам")
    print("8. Сохранить результат в файл")
    print("9. Выход")
    print("------------")

# Основная функция
def main():
    filename = input("Введите имя файла с криптограммой (например, cipher.txt): ").strip()
    if not filename:
        print("Ошибка ввода")
        return
    
    # Загрузка файла
    ciphertext = load_ciphertext(filename)
    if ciphertext is None:
        print("Ошибка загрузки файла")
        return

    # Инициализация анализатора
    analyzer = Cryptanalyzer(ciphertext)

    while True:
        print_help()
        choice = input("Выберите пункт меню: ").strip()

        if choice == '1':
            freq_order = analyzer.compute_frequencies()
            if not freq_order:
                print("Ошибка. В криптограмме нет букв")
            else:
                print("Символы в порядке убывания частоты:")
                for ch in freq_order:
                    print(f"{ch}: {analyzer.ciphertext.count(ch)}")

        elif choice == '2':
            groups = analyzer.group_words_by_length()
            if not groups:
                print("Ошибка. Нет слов")
            else:
                for length, words in sorted(groups.items()):
                    print(f"\nДлина {length}:")
                    for w in words:
                        print(f" {w}")

        elif choice == '3':
            groups = analyzer.group_words_by_unknown()
            if not groups:
                print("Ошибка. Нет слов")
            else:
                for unknown, words in sorted(groups.items()):
                    print(f"\nНеизвестных букв: {unknown} —")
                    for w in words:
                        print(f" {w}")

        elif choice == '4':
            print("\nТекущее состояние дешифровки:")
            print(analyzer.current_text())

        elif choice == '5':
            symbol = input("Введите символ криптограммы (заглавная буква): ").strip().upper()
            if not symbol:
                continue
            letter = input("Введите предполагаемую русскую букву (строчная буква): ").strip().lower()
            analyzer.substitute(symbol, letter)

        elif choice == '6':
            analyzer.undo()

        elif choice == '7':
            analyzer.auto_substitute()
            print("Результат авто-замены:")
            print(analyzer.current_text())

        elif choice == '8':
            out_filename = input("Имя файла для сохранения (по умолчанию result.txt): ").strip()
            if not out_filename:
                out_filename = "result.txt"
            try:
                with open(out_filename, 'w', encoding='utf-8') as f:
                    f.write(analyzer.current_text())
                print(f"Результат сохранён в {out_filename}")
            except Exception as e:
                print(f"Ошибка записи: {e}")

        elif choice == '9':
            print("Выход из программы.")
            break

        else:
            print("Неверный пункт меню. Попробуйте снова.")

if __name__ == "__main__":
    main()