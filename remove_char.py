class Remove:
    def remove(self, string):
        data = string
        for i in range(len(string)):
            if string[i]  == '(':
                data = string[0:i]
        return data
