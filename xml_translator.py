import os
from lxml import etree
from openai import OpenAI
from langdetect import detect

class XMLTranslator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.target_language = "English"  # La lingua di destinazione verrà aggiornata nella chiamata a translate_xml_file

    def translate(self, text):
        if not text.strip():
            return text
        lang = detect(text)
        lang_map = {"English": "en", "French": "fr", "Spanish": "es", "Russian": "ru", "Italian": "it"}
        if lang == lang_map.get(self.target_language, self.target_language.lower()):
            return text

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Translate into {self.target_language}. Only return the translated text."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        translated = response.choices[0].message.content.strip()
        print("\n🔹 Original:  ", text)
        print("🔸 Translated:", translated)
        print("-" * 50)
        return translated

    def translate_xml_file(self, input_path, output_path, target_language):
        self.target_language = target_language

        parser = etree.XMLParser(strip_cdata=False, remove_blank_text=False)
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        NAMESPACES = {
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'wp': 'http://wordpress.org/export/1.2/',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }

        for item in root.xpath("//item"):
            # <title>
            title = item.find("title")
            if title is not None and title.text:
                original = title.text
                title.text = etree.CDATA(self.translate(original))

            # <content:encoded>
            content = item.find("content:encoded", namespaces=NAMESPACES)
            if content is not None and content.text:
                original = content.text
                content.text = etree.CDATA(self.translate(original))

            # <excerpt:encoded>
            excerpt = item.find("excerpt:encoded", namespaces=NAMESPACES)
            if excerpt is not None and excerpt.text:
                original = excerpt.text
                excerpt.text = etree.CDATA(self.translate(original))

            # wp:meta_value associato a _wp_attachment_image_alt
            metas = item.findall("wp:postmeta", namespaces=NAMESPACES)
            for meta in metas:
                key = meta.find("wp:meta_key", namespaces=NAMESPACES)
                val = meta.find("wp:meta_value", namespaces=NAMESPACES)
                if key is not None and val is not None and key.text == "_wp_attachment_image_alt" and val.text:
                    val.text = etree.CDATA(self.translate(val.text))

        tree.write(output_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)