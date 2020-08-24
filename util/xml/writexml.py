import xml.etree.ElementTree as ET


class WriteXml:
    def __init__(self, file):
        self.file = file

    def create_object(self, minX, minY, maxX, maxY):
        data = ET.Element('data')
        items = ET.SubElement(data, 'items')
        item = ET.SubElement(items, 'item')
        item.set('name', 'item')
        point1 = ET.SubElement(item, "point")
        point2 = ET.SubElement(item, "point")

        point1.set('name', 'point1')
        x1 = ET.SubElement(point1, 'x')
        y1 = ET.SubElement(point1, 'y')
        x1.text = str(minX)
        y1.text = str(minY)

        point2.set('name', 'point2')
        x2 = ET.SubElement(point2, 'x')
        y2 = ET.SubElement(point2, 'y')
        x2.text = str(maxX)
        y2.text = str(maxY)

        mydata = ET.tostring(data).decode('utf-8')
        myfile = open('xml/' + str(self.file) + '.xml', "w")
        myfile.write(mydata)