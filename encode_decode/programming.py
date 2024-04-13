def encode_commands(commands):
    abbreviations = {'вверх': 'U', 'вниз': 'D', 'вправо': 'R', 'влево': 'L'}
    result = []
    previous_command = ''
    count = 1

    for command in commands.split():
        abbreviation = abbreviations.get(command)
        if abbreviation == previous_command:
            count += 1
        else:
            if previous_command:
                result.append(previous_command + (str(count) if count > 1 else ''))
            previous_command = abbreviation
            count = 1
    if previous_command:
        result.append(previous_command + (str(count) if count > 1 else ''))

    return ''.join(result)


def decode_commands(encoded):
    decode_map = {'U': 'вверх', 'D': 'вниз', 'R': 'вправо', 'L': 'влево'}
    result = ''
    prev = ''

    for char in encoded:
        if char.isdigit():
            result += (prev + ' ')*(int(char) - 1)
        else:
            result += decode_map[char] + ' '
            prev = decode_map[char]

    return result[:-1]


if __name__ == '__main__':
    test_str = input('Введите строку для кодирования: ')
    encode_result = encode_commands(test_str)
    print(f'Ваша закодированная строка: {encode_result}')
    decode_result = decode_commands(encode_result)
    print(f'А теперь раскодируем только что закодированную строку: {decode_result}')