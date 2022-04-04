class Painting:

    museum = "Louvre"

    def __init__(self, title, painter, year):

        self.title = title
        self.painter = painter
        self.year = year

        self.output()

    def get_details(self):

        self.title = input()
        self.painter = input()
        self.year = input()

    def output(self):

        print('"{}" by {} ({}) hangs in the {}.'.format(self.title, self.painter, self.year, Painting.museum))


x = input()
y = input()
z = input()

painting = Painting(x, y, z)