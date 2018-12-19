from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'game'
        ]
    )
except SystemExit:
    pass
