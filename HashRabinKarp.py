class HashString:
    numberHash = set()
    modulous = 10**9 + 7
    hash_constant = 33 # http://stackoverflow.com/questions/11546791/what-is-the-best-hash-function-for-rabin-karp-algorithm
    def ComputeHash(self, value):
        hashValue = 0
        for ch in value:
            hashValue = self.hash_constant * hashValue + ord(ch)
            if hashValue > self.modulous:
                hashValue = hashValue%self.modulous
        return hashValue

    def add(self,value):
        if not isinstance(value, str):
            raise TypeError("Cannot call with non-string type")
        self.numberHash.add(self.ComputeHash(value))
    def query(self,value):
        if not isinstance(value, str):
            raise TypeError("Cannot call with non-string type")
        return self.ComputeHash(value) in self.numberHash

         
