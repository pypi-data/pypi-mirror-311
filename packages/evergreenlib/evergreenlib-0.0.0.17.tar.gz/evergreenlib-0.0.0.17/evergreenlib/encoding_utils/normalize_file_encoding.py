import chardet


def normalize_file_encoding(filepath, target_encoding='utf-8', errors='replace'):
    """
    Нормализует кодировку файла, перекодируя его в указанную целевую кодировку.

    :param filepath: str, путь к файлу
    :param target_encoding: str, кодировка, к которой нужно преобразовать файл (по умолчанию 'utf-8')
    :param errors: str, способ обработки ошибок ('replace', 'ignore' или 'strict')
    :return: str, путь к нормализованному файлу
    """
    try:
        # Определяем текущую кодировку файла
        with open(filepath, 'rb') as file:
            raw_data = file.read()
            detected = chardet.detect(raw_data)
            source_encoding = detected['encoding']

        if source_encoding is None:
            raise ValueError("Не удалось определить кодировку файла.")

        # Читаем файл в исходной кодировке и перекодируем в целевую
        with open(filepath, 'r', encoding=source_encoding, errors=errors) as file:
            content = file.read()

        # Перезаписываем файл в целевой кодировке
        with open(filepath, 'w', encoding=target_encoding, errors=errors) as file:
            file.write(content)

        return filepath
    except Exception as e:
        raise RuntimeError(f"Ошибка при нормализации кодировки файла: {e}")
