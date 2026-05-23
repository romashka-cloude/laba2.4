class XMLNode:
    def __init__(self, tag, text='', attributes=None):
        self.tag = tag
        self.text = text
        if attributes is not None:
            self.attributes = attributes
        else:
            self.attributes = {}
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def serialize(node):
    attrs = ''.join(f' {key}="{value}"' for key, value in node.attributes.items())
    children_serialized = ''.join(serialize(child) for child in node.children)
    return f'<{node.tag}{attrs}>{node.text}{children_serialized}</{node.tag}>'


def deserialize(xml_string):
    def parse_node(xml, start):
        end_tag = find_closing_tag(xml, start)
        if end_tag == -1:
            raise ValueError(f'Непревзойденный открывающий тег в позиции {start}')

        tag_content = xml[start:end_tag]
        tag_name = tag_content.split()[0][1:]

        attributes = {}
        parts = tag_content.split()
        for part in parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                attributes[key] = value.strip('"')

        text_start = end_tag + len(tag_name) + 2
        text_end = xml.find(f'</{tag_name}>', text_start)
        if text_end == -1:
            raise ValueError(f'Отсутствует закрывающий тег для {tag_name}, начинающийся с позиции {text_start}')

        text_content = xml[text_start:text_end].strip()

        node = XMLNode(tag_name, text_content, attributes)


        child_start = text_end + len(tag_name) + 3
        while child_start < len(xml):
            next_start = xml.find('<', child_start)
            if next_start == -1:
                break
            if xml[next_start + 1] == '/':
                break
            child_node, child_end = parse_node(xml, next_start)
            node.add_child(child_node)
            child_start = child_end

        return node, text_end + len(tag_name) + 3

    def find_closing_tag(xml, start):
        depth = 0
        for i in range(start, len(xml)):
            if xml[i] == '<':
                if i + 1 < len(xml) and xml[i + 1] != '/':
                    depth += 1
                elif i + 1 < len(xml) and xml[i + 1] == '/':
                    depth -= 1
                    if depth == 0:
                        return i
        return -1

    root_node, _ = parse_node(xml_string, xml_string.find('<'))
    return root_node


def validate(xml_string):
    try:
        deserialize(xml_string)
        return True, "Корректный XML"
    except ValueError as e:
        return False, str(e)


def load_xml_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


if __name__ == "__main__":
    file_path = 'resourse/data.xml'

    try:
        xml_content = load_xml_from_file(file_path)

        print("Тестируем XML:")
        print(xml_content)

        # Валидация
        valid, message = validate(xml_content)
        print(f"Валидация: {message}")

        if valid:
            # Десериализация
            node = deserialize(xml_content)
            print("Десериализованный узел:")
            print(serialize(node))

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
