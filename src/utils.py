from slugify import slugify


def generate_slug_by_name(name: str):
    """ Генерировать слаг имя по значению колонки"""
    return slugify(name)

