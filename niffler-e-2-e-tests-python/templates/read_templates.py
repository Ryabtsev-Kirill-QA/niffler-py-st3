import os

import xmlschema
from jinja2 import Environment, select_autoescape, FileSystemLoader
from xmlschema import XMLSchema11

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def current_user_xml(username: str) -> str:
    template = env.get_template('/templates/xml/current_user.xml')
    return template.render({'username': username})


def xsd_response(operation: str) -> XMLSchema11:
    envelope_xsd = env.get_template('./templates/xsd/envelope.xsd')
    render_xsd_response = envelope_xsd.render(
        {'operation_xsd': f'{operation}.xsd', 'operation': operation})

    temp_path = './templates/xsd/temp.xsd'
    with open(f'{temp_path}', 'w') as f:
        f.write(render_xsd_response)

    try:
        return xmlschema.XMLSchema11('./templates/xsd/temp.xsd')
    finally:
        os.remove(temp_path)
