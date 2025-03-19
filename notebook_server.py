import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import threading
from datetime import datetime

class NotebookServer:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.lock = threading.Lock()
        self._init_xml()

    def _init_xml(self):
        try:
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()
            if self.root is None:
                raise FileNotFoundError
        except (FileNotFoundError, ET.ParseError):
            self.root = ET.Element("data")
            self.tree = ET.ElementTree(self.root)
            self._save_xml()

    def _save_xml(self):
        with open(self.xml_file, "wb") as f:
            self.tree.write(f, encoding="utf-8", xml_declaration=True)

    def add_note(self, topic, note_name, text):
        with self.lock:
            try:
                self.tree = ET.parse(self.xml_file)
                self.root = self.tree.getroot()
                
                # check if topic exists, if not create it
                topic_elem = next(
                    (t for t in self.root.findall("topic") if t.get("name") == topic),
                    None
                )
                if not topic_elem:
                    topic_elem = ET.SubElement(self.root, "topic", name=topic)
                
                # check if note name already exists
                if any(note.get("name") == note_name for note in topic_elem.findall("note")):
                    return "Name already exists"
                
                # create note
                note_elem = ET.SubElement(topic_elem, "note", name=note_name)
                ET.SubElement(note_elem, "text").text = text.strip()
                timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
                ET.SubElement(note_elem, "timestamp").text = timestamp
                
                self._save_xml()
                return True
            except Exception as e:
                print(f"Error: {str(e)}")
                return False

    def get_notes(self, topic):
        with self.lock:
            try:
                self.tree = ET.parse(self.xml_file)
                self.root = self.tree.getroot()
                
                topic_elem = next(
                    (t for t in self.root.findall("topic") if t.get("name") == topic),
                    None
                )
                
                if not topic_elem:
                    return []
                
                return [
                    {
                        "name": note.get("name"),
                        "text": note.find("text").text,
                        "timestamp": note.find("timestamp").text
                    }
                    for note in topic_elem.findall("note")
                ]
            except Exception as e:
                print(f"Error: {str(e)}")
                return []

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_instance(NotebookServer("notebook.xml"))
    print("Server running on port 8000...")
    server.serve_forever()