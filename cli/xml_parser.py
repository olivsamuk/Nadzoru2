import xml.etree.ElementTree as ET
from xml.dom import minidom

def ides_export(g, filename):
    model = ET.Element('model')
    model.set('version', '2.1')
    model.set('type', 'FSA')
    model.set('id', 'Untitled')
    data = ET.SubElement(model, 'data')

    for i in g.keys():
        for j in g[i]:
            item = ET.SubElement(data, str(i)[:-1])
            item.set('id', str(j['id']))
            if i != 'transitions':
                properties = ET.SubElement(item, "properties")
                for k in j.keys():
                    if k == 'controllable':
                        if j['controllable']:
                            ET.SubElement(properties, "controllable")
                    if k == 'observable':
                        if j['observable']:
                            ET.SubElement(properties, "observable")
                    if k == 'marked':
                        if j['marked']:
                            ET.SubElement(properties, "marked")
                    if k == 'initial':
                        if j['initial']:
                            ET.SubElement(properties, "initial")
                name = ET.SubElement(item, "name")
                name.text = str(j['label'])
            else:
                item.set('source', str(j['source']))
                item.set('event', str(j['event']))
                item.set('target', str(j['target']))
        xmlstr = minidom.parseString(ET.tostring(model)).toprettyxml(indent="   ")
        with open('USER/xml/'+str(filename)+'.xmd', "w") as f:
            f.write(xmlstr)