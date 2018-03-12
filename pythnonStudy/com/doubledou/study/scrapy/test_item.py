import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    length = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


if __name__ == '__main__':
     print(Product.fields)
     product = Product(name='Desktop PC', price=1000)
     print (product)
     print (product['name'])
     print (product.get('name'))
     #print (product['last_updated'])
     print (product.get('stock'))
     print (product.get('stock', 'not set'))
     print ('name' in product)
     print ('stock' in product)
     print ('stock' in product.fields)
     print (product.get('stock'))
     product['last_updated'] = 'today'
     print (product['last_updated'])
