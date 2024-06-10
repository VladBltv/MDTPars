# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class DramthPipeline:
    def open_spider(self, spider):
        self.data_list = []
        self.data = []
        self.first_item = True
        self.ids = []

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        line_form = json.loads(line)

        if len(self.ids) == 0:
            self.ids.append(line_form['id'])

        if line_form['id'] in self.ids:
            if line_form["row"] == '':
                pass
            else:
                line_form["row"] = int(line_form["row"])

            line_form["seat"] = int(line_form["seat"])
            line_form["price"] = int(line_form["price"])
            line_form["sector"] = line_form["sector"].replace('"','')
            line_form["sector"] = str(line_form["sector"])
            del line_form['id']

            line = json.dumps(line_form, ensure_ascii=False)


            self.data.append(line)

            return item
        else:
            self.ids.append(line_form['id'])
            self.data_list.append(self.data)
            self.first_item = True
            self.data = []

            if line_form["row"] == '':
                pass
            else:
                line_form["row"] = int(line_form["row"])

            line_form["seat"] = int(line_form["seat"])
            line_form["price"] = int(line_form["price"])
            line_form["sector"] = line_form["sector"].replace('"', '')
            line_form["sector"] = str(line_form["sector"])
            self.id = line_form["id"]
            del line_form['id']

            line = json.dumps(line_form, ensure_ascii=False)

            self.data.append(line)

            return item

    def close_spider(self, spider):
        self.data_list.append(self.data)
        for id in self.ids:
            self.first_item = True
            ind = self.ids.index(id)
            data_len = len(self.data_list[ind])
            self.file = open(f"{data_len}_{id}.json", "w", encoding='utf-8')
            self.file.write("[")
            for el in self.data_list[ind]:
                if self.first_item:
                    self.first_item = False
                else:
                    self.file.write(",\n")
                self.file.write(el)
            self.file.write("]")
            self.file.close()




