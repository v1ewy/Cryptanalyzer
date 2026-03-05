import copy
from collections import Counter

# Частотный порядок букв русского языка (по убыванию)
RUSSIAN_FREQ_ORDER = [
    'о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л',
    'к', 'м', 'д', 'п', 'у', 'я', 'ы', 'ь', 'г', 'з',
    'б', 'ч', 'й', 'х', 'ж', 'ш', 'ю', 'ц', 'щ', 'э', 
    'ф', 'ъ', 'ё'
]

# Множество допустимых русских букв (строчных)
RUSSIAN_ALPHABET = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

class Cryptanalyzer:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext          # исходный шифротекст
        self.mapping = {}                      # словарь замен: символ -> буква
        self.history = []                       # стек для отката

    def _save_state(self):
        """Сохраняет текущее состояние mapping в историю"""
        self.history.append(copy.deepcopy(self.mapping))

    def compute_frequencies(self):
        """Возвращает список символов отсортированных по убыванию частоты"""
        freq = Counter(char for char in self.ciphertext if char.isalpha())
        sorted_chars = [item[0] for item in freq.most_common()]
        return sorted_chars

    def group_words_by_length(self):
        """Группирует слова по длине"""
        words = self.ciphertext.split()
        groups = {}
        for word in words:
            clean_word = ''.join(ch for ch in word if ch.isalpha())
            length = len(clean_word)
            if length > 0:                   
                groups.setdefault(length, []).append(word)
        return groups

    def group_words_by_unknown(self):
        """Группирует слова по количеству нерасшифрованных букв"""
        words = self.ciphertext.split()
        groups = {}
        for word in words:
            unknown = sum(1 for ch in word if ch.isalpha() and ch not in self.mapping)
            groups.setdefault(unknown, []).append(word)
        return groups

    def current_text(self):
        """Возвращает текущее состояние дешифровки"""
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
        """Откатывает последнее изменение"""
        if not self.history:
            print("Нет сохранённых состояний для отката")
            return False
        self.mapping = self.history.pop()
        print("Последнее изменение отменено")
        return True

    def auto_substitute(self):
        """
        Автоматическая замена на основе частотного анализа
        Сопоставляет самые частые буквы шифротекста с самыми частыми буквами
        русского языка, ещё не использованными в заменах
        """
        cipher_order = self.compute_frequencies()
        unmapped = [ch for ch in cipher_order if ch not in self.mapping]

        if not unmapped:
            print("Все символы уже имеют замены")
            return 0
        
        letters_to_use = []
        for letter in RUSSIAN_FREQ_ORDER:
            if letter not in self.mapping.values():
                letters_to_use.append(letter)
                if len(letters_to_use) == len(unmapped):
                    break

        self._save_state()
        count = min(len(unmapped), len(letters_to_use))
        for i in range(count):
            self.mapping[unmapped[i]] = letters_to_use[i]

        print(f"Автоматически заменено {count} символов")
        if count < len(unmapped):
            print("Предупреждение: не хватило свободных букв")
        return count


def load_ciphertext(filename):
    """Загружает шифротекст из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None


def print_help():
    """Вывод меню"""
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


def main():
    filename = input("Введите имя файла с криптограммой (по умолчанию cipher.txt): ").strip()
    if not filename:
        filename = "cipher.txt"
        return

    ciphertext = load_ciphertext(filename)
    if ciphertext is None:
        return

    analyzer = Cryptanalyzer(ciphertext)

    while True:
        print_help()
        choice = input("Выберите пункт меню: ").strip()

        if choice == '1':
            freq_order = analyzer.compute_frequencies()
            if not freq_order:
                print("В криптограмме нет букв")
            else:
                print("Символы в порядке убывания частоты:")
                for ch in freq_order:
                    print(f"{ch}: {analyzer.ciphertext.count(ch)}")

        elif choice == '2':
            groups = analyzer.group_words_by_length()
            if not groups:
                print("Нет слов для анализа")
            else:
                for length, words in sorted(groups.items()):
                    print(f"\nДлина {length}:")
                    for w in words:
                        print(f"  {w}")

        elif choice == '3':
            groups = analyzer.group_words_by_unknown()
            if not groups:
                print("Нет слов для анализа")
            else:
                for unknown, words in sorted(groups.items()):
                    print(f"\nНеизвестных букв: {unknown} —")
                    for w in words:
                        print(f"  {w}")

        elif choice == '4':
            print("\nТекущее состояние дешифровки:")
            print(analyzer.current_text())

        elif choice == '5':
            symbol = input("Введите символ криптограммы (заглавная буква): ").strip().upper()
            if not symbol:
                continue
            letter = input("Введите предполагаемую русскую букву (строчную): ").strip().lower()
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
            print("Выход из программы")
            break

        else:
            print("Неверный пункт меню. Попробуйте снова")

if __name__ == "__main__":
    main()