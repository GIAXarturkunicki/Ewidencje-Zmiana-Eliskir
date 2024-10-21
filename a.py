import xml.etree.ElementTree as ET
import uuid


def remove_namespace_prefixes(element):
    if element.tag.startswith('{'):
        element.tag = element.tag.split('}', 1)[1] 

    for subelement in element:
        remove_namespace_prefixes(subelement)

  
    for attr in list(element.attrib.keys()):
        value = element.attrib[attr]
        if attr.startswith('{'):
            new_attr = attr.split('}', 1)[1]  
            element.attrib[new_attr] = value
            del element.attrib[attr]


def modyfikuj_ewidencje_esp_eliskir(plik_xml_2):
    try:
       
        with open(plik_xml_2, 'r', encoding='utf-8', errors='replace') as file:
            xml_content = file.read()

      
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()
        namespace = {'ns': 'http://www.soneta.pl/schema/business'}


        nowy_guid = str(uuid.uuid4())

       
        nowy_format = ET.Element('FormatWymianyElektronicznej', {
            'id': nowy_guid,
            'class': 'Soneta.Kasa.FormatEksportuPrzelewów,Soneta.Kasa'
        })
        
        typ = ET.SubElement(nowy_format, 'Typ')
        typ.text = 'EksportPrzelewów'
        
        nazwa = ET.SubElement(nowy_format, 'Nazwa')
        nazwa.text = 'Elixir-O'
        
        nazwa_serializera = ET.SubElement(nowy_format, 'NazwaSerializera')
        nazwa_serializera.text = 'Elixir-O'
        
        parametry_serializera = ET.SubElement(nowy_format, 'ParametrySerializera')
        
        runtime_info = ET.SubElement(nowy_format, 'RuntimeInfo')
        project = ET.SubElement(runtime_info, 'Project')
        identifier = ET.SubElement(runtime_info, 'Identifier')
        file_name = ET.SubElement(runtime_info, 'FileName')

        root.append(nowy_format)

        for ewidencja in root.findall(".//ns:EwidencjaSP", namespace):
            pole1 = ewidencja.find(".//ns:RodzajRaportow", namespace)
            if pole1 is not None:
                pole1.text = "DziennyMulti"
            
            pole2 = ewidencja.find(".//ns:OkresRaportow", namespace)
            if pole2 is not None:
                pole2.text = "Dzienny"
            
            pole3 = ewidencja.find(".//ns:FiltrImportu", namespace)
            if pole3 is not None:
                pole3.text = "BGK24 masowe (XML)"
            
            eksport_przelewow = ewidencja.find(".//ns:EksportPrzelewow", namespace)
            if eksport_przelewow is not None:
                eksport_przelewow.text = "00000000-0003-0005-0001-000000000000"

        remove_namespace_prefixes(root)

        tree.write("22.xml", encoding="utf-8", xml_declaration=True)
    
    except ET.ParseError as e:
        print(f"Error parsing the XML file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def modyfikuj_ewidencje_esp(plik_xml):
    try:
        tree = ET.parse(plik_xml)
        root = tree.getroot()
        namespace = {'ns': 'http://www.soneta.pl/schema/business'}

        for ewidencja in root.findall(".//ns:EwidencjaSP", namespace):
            pole1 = ewidencja.find(".//ns:RodzajRaportow", namespace)
            if pole1 is not None:
                pole1.text = "DziennyMulti"
            
            pole2 = ewidencja.find(".//ns:OkresRaportow", namespace)
            if pole2 is not None:
                pole2.text = "Dzienny"

            pole3 = ewidencja.find(".//ns:FiltrImportu", namespace)
            if pole3 is not None:
                pole3.text = "BGK24 masowe (XML)"
            
            eksport_przelewow = ewidencja.find(".//ns:EksportPrzelewow", namespace)
            if eksport_przelewow is not None:
                eksport_przelewow.text = "00000000-0003-0005-0001-000000000000"

        remove_namespace_prefixes(root)

        tree.write("2.xml", encoding="utf-8", xml_declaration=True)

    except ET.ParseError as e:
        print(f"Error parsing the XML file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

plik_xml = "1.xml"
plik_xml_2 = "11.xml"

modyfikuj_ewidencje_esp(plik_xml)
modyfikuj_ewidencje_esp_eliskir(plik_xml_2)
