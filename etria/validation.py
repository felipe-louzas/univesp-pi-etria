def required(value: str, field_name):
    if value is None or value.strip() == '':
        raise ValueError(f'{field_name} é obrigatório')

    return value


def valid_option(value: str, options: list, field_name):
    if value not in options:
        raise ValueError(f'{field_name} inválido')

    return value


def is_positive_int(value: str, field_name):
    try:
        value = int(value)
        if value <= 0:
            raise ValueError(f'{field_name} inválido')
    except:
        raise ValueError(f'{field_name} inválido')

    return value


def cpf(value: str, field_name):
    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in value if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        raise ValueError(f'{field_name} inválido')

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValueError(f'{field_name} inválido')

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValueError(f'{field_name} inválido')

    return ''.join([str(num) for num in numbers])

def rg(value: str, field_name):
    # Obtém apenas os números do RG, ignorando pontuações
    numbers = [digit for digit in value if digit.isdigit() or digit == 'X']

    # Verifica se o RG possui 9 números ou se todos são iguais:
    if (len(numbers) != 9 and len(numbers) != 8) or len(set(numbers)) == 1:
        raise ValueError(f'{field_name} inválido')

    return ''.join([str(num) for num in numbers])


def numeric(value: str, field_name, length=None, min_length=None, max_length=None):
    if value is None or value.strip() == '':
        return None

    numbers = [digit for digit in value if digit.isdigit()]

    if length is not None and len(numbers) != length:
        raise ValueError(f'{field_name} deve conter {length} dígitos')

    if min_length is not None and len(numbers) < min_length:
        raise ValueError(f'{field_name} deve conter no mínimo {min_length} dígitos')

    if max_length is not None and len(numbers) > max_length:
        raise ValueError(f'{field_name} deve conter no máximo {max_length} dígitos')

    return ''.join([str(num) for num in numbers])