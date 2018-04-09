import os
import django
import time
from django.conf import settings

os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'sharehold.settings.dev')
django.setup()

LIST_FILE = os.path.join (settings.BASE_DIR, 'skk.games.xlsx')
print (LIST_FILE)

import xlrd
from catalogue.models import BoardGameItem, BoardGameCommodity


book = xlrd.open_workbook (LIST_FILE)
sheet = book.sheet_by_name ("Lista gier")

#skip headline row end go through listed games
if __name__ == '__main__':
    print (sheet.nrows)
    for r in range(1, sheet.nrows):
        game = None
        commodity = None
        try:
            time.sleep (.02)
            barcode = sheet.cell(r, 0).value
            title = sheet.cell (r, 3).value
            bgg_index = sheet.cell (r, 4).value
            bgg_url="http://www.boardgamegeek.com/boardgame/"
            if bgg_index:
                bgg_url += str(int(bgg_index))
            else:
                bgg_url = None
            q = BoardGameCommodity.get_commodity_by_code (BoardGameCommodity.BARCODE, barcode)
            if q.exists():
                commodity = q[0]
                game = commodity.catalogueEntry
                print ('{0}: {1} skipped - found as: {2}'.format(r+1, commodity.codeValue, game.itemLabel))
            else:
                print ('{0}: {1} - missing {2} to be added...'.format(r+1, barcode, title))
                game, isNew = BoardGameItem.objects.get_or_create (itemLabel=title, bggURL=bgg_url)
                if isNew:
                    game.save()
                else:
                    print ('{0}: {1} game retrieved'.format(r+1, game.itemLabel))
                commodity = BoardGameCommodity (codeType=BoardGameCommodity.BARCODE,
                    codeValue = barcode, catalogueEntry = game)
                commodity.save()
                print ('{0}: commodity {3} added to {1} @bgg: {2}'.format(r+1,
                    game.itemLabel, game.bggURL, commodity.codeValue))
        except OSError as e:
            pass
