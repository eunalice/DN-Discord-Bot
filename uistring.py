import xml.etree.ElementTree as ET

xml_file = 'uistring.xml'


def getCdata(mid):
  tree = ET.parse(xml_file)
  root = tree.getroot()
  xpath = f"./message[@mid='{mid}']"
  message = root.find(xpath)
  if message is None:
    return ("似乎找不到您所要查詢的文本")
  return message.text.strip()