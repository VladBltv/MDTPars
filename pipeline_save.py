# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class DramthPipeline:
    def open_spider(self, spider):
        self.data = []
        self.first_item = True
        self.count_tickets = 0
        self.id = ""

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        line_form = json.loads(line)
        if line_form["row"] == '':
            pass
        else:
            line_form["row"] = int(line_form["row"])

        line_form["seat"] = int(line_form["seat"])
        line_form["price"] = int(line_form["price"])
        line_form["sector"] = line_form["sector"].replace('"','')
        line_form["sector"] = str(line_form["sector"])
        self.id = line_form["id"]
        del line_form['id']

        line = json.dumps(line_form, ensure_ascii=False)


        self.data.append(line)
        self.count_tickets+=1
        return item

    def close_spider(self, spider):
        self.file = open(f"{len(self.data)}_{self.id}.json", "w", encoding='utf-8')
        self.file.write("[")
        for el in self.data:
            if self.first_item:
                self.first_item = False
            else:
                self.file.write(",\n")
            self.file.write(el)
        self.file.write("]")
        self.file.close()


