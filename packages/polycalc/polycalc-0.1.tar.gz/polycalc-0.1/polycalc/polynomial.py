class Polynomial(object):
    
    def __init__(self, coefficients):
        self.co = coefficients
        
    def evaluate(self, x):
        if any(isinstance(i, list) for i in self.co):
            if x == 0:
                return sum([(x**i)*co for i, co in enumerate(self.co[1:])]) 
            else:
                return sum([self.co[0]/x]) + sum([(x**i)*co for i, co in enumerate(self.co[1:])])    
        if not any(isinstance(i, list) for i in self.co):
            return sum([(x**i)*co for i, co in enumerate(self.co)])

    def derive(self): 
        return Polynomial([self.co[i] * i for i in range(1, len(self.co))])
    
    def antiderive(self): 
        return Polynomial([0] + [self.co[i]/(i+1) for i in range(0, len(self.co))])

    def multiply(self, multiplier):
        ax = [0 for i in range( len(self.co) + len(multiplier.co)  - 1)]
        for i, co in enumerate(self.co):
            for u, coe in enumerate(multiplier.co):
                for index in range(len(ax)):
                    if (i+u)  == index:
                        ax[index] += co*coe   
        return Polynomial(ax)

    def subtract(self, subtractor):
        if (len(self.co) >= len(subtractor.co)):
            return Polynomial([self.co[i] - subtractor.co[i] for i in range(0,len(subtractor.co))] + [i for i in self.co[len(subtractor.co):]])
        if (len(self.co) < len(subtractor.co)):
            return Polynomial([self.co[i] - subtractor.co[i] 
                               for i in range(0,len(self.co))] + [-1*subtractor.co[i] for i in range(len(self.co), len(subtractor.co))])
        
    def add(self, adder):
        if (len(self.co) >= len(adder.co)):
            return Polynomial([self.co[i] + adder.co[i] for i in range(0,len(adder.co))] + [i for i in self.co[len(adder.co):]])

        if (len(self.co) < len(adder)):
            return Polynomial([self.co[i] + adder.co[i] for i in range(0,len(self.co))] + [adder.co[i] for i in range(len(self.co), len(adder.co))])

    def scalar_divide(self, divisor):
        return Polynomial([self.co[i]/divisor for i in range(len(self.co))])

    def x_divide(self):
        assert self.co[0] == 0
        return Polynomial([self.co[0], self.co[1:]])
    
    def integrate_x_axis(self, a, b):
        return self.antiderive().evaluate(b) - self.antiderive().evaluate(a)