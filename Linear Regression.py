class LinearRegression():
    def __init__(self):
        self.x = [20, 30, 40, 36, 38, 32]
        self.y = [29,25,42,40,32,30]

    def fit(self):
        n = len(self.x)


        x_bar = sum(self.x) / n
        y_bar = sum(self.y) / n


        num = sum([(x - x_bar) * (y - y_bar) for x, y in zip(self.x, self.y)])
        den = sum([(x - x_bar)**2 for x in self.x])

        self.m = num / den
        self.b = y_bar - self.m * x_bar

    def predict(self, x):

        return self.m * x + self.b
lr = LinearRegression()
lr.fit()
print(lr.predict(35))
