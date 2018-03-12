unicode = 'utf-8'
import scrapy
from test_item import Product
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def parse(self, response):
    loader = ItemLoader(item=Product(), response=response)
    loader.add_xpath('name', '//div[@class="product_name"]')
    loader.add_xpath('name', '//div[@class="product_title"]')
    loader.add_xpath('price', '//p[@id="price"]')
    loader.add_css('stock', 'p#stock]')
    loader.add_value('last_updated', 'today')
    loader.load_item()


# judge is a number or not
def filter_price(value):
    if value.isdigit():
        return value


def parse_length(text, loader_context):
    unit = loader_context.get('unit', 'm')
    return text + unit


class ProductLoader(ItemLoader):
    default_input_processor = TakeFirst()
    name_in = MapCompose(remove_tags)
    name_out = Join()
    price_in = MapCompose(remove_tags, filter_price)
    price_out = TakeFirst()
    length_in = MapCompose(parse_length)
    length_out = TakeFirst()


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    length = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class ItemProduct(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_price),
        output_processor=TakeFirst(),
    )
    length = scrapy.Field(
        input_processor=MapCompose(parse_length),
        output_processor=TakeFirst(),
    )

if __name__ == '__main__':
    productLoader = ProductLoader(item=Product())
    productLoader.add_value('name', [u'Welcome to my', u'<strong>website</strong>'])
    productLoader.add_value('price', [u'&euro;', u'<span>1000</span>'])
    productLoader.add_value('length', u'100')
    print productLoader.load_item()

    itemLoader = ItemLoader(item=ItemProduct())
    itemLoader.context['unit'] = 'cm'
    itemLoader.add_value('name', [u'Welcome to my', u'<strong>website</strong>'])
    itemLoader.add_value('price', [u'$;', u'<span>1000</span>'])
    itemLoader.add_value('length', u'100')
    print itemLoader.load_item()





