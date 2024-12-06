class NDimensionTensor:
    def __init__(self, shape = [], fill=0):
        self.shape = shape
        if isinstance (fill, int):
            self.tensor = self._create_tensor(shape, fill)
        else:
            raise ValueError ("Please only use an integer for the creation of the tensor")

    def _create_tensor(self, shape, fill):
        if len(shape) <= 0:
            return None
        if len(shape) == 1:
            return [fill]*shape[0]
        else:
            return [self._create_tensor(shape[1:],fill) for _ in range(shape[0])]
    
    def __str__(self):
        if len(self.shape) == 2:
            line = ""
            for x,y in enumerate(self.tensor):
                line += ("[")
                for j in self.tensor[x][:-1]:
                    line += (str(j)+", ")
                line += (str(self.tensor[x][-1])+"]\n")
        else:
            line = str(self.tensor)
        return line
    
    def __getitem__(self, indexes):
        if isinstance(indexes, list):
            indexes = tuple(indexes)
        elif not isinstance(indexes, tuple):
            indexes = (indexes,)
        return self._get_element(indexes)
    
    def _get_element(self, indexes):
        data = self.tensor
        for _ in indexes:
            data = data[_]
        return data
    
    def __setitem__(self, indexes, value):
        if value != None:
            if isinstance(indexes, list):
                indexes = tuple(indexes)
            elif not isinstance(indexes, tuple):
                indexes = (indexes,)
            return self._set_element(indexes, value)
    
    def _set_element(self, indexes, value):
        data = self.tensor
        for _ in indexes[:-1]:
            data = data[_]
        data[indexes[-1]] = value

    def __add__(self, tensor):
        if self.shape != tensor.shape:
            raise ValueError("The two tensors are of different shapes")
        if not isinstance(tensor, NDimensionTensor):
            raise ValueError("You can only add a tensor to another")
        result = NDimensionTensor(self.shape)
        result.tensor = self._recursive_addition(self.tensor, tensor.tensor, 1)
        return result
    
    def __sub__(self, tensor):
        if self.shape != tensor.shape:
            raise ValueError("The two tensors are of different shapes")
        if not isinstance(tensor, NDimensionTensor):
            raise ValueError("You can only add a tensor to another")
        result = NDimensionTensor(self.shape)
        result.tensor = self._recursive_addition(self.tensor, tensor.tensor, -1)
        return result
    
    def __len__(tensor):
        if isinstance(tensor, NDimensionTensor):
            return tensor.shape[0]
    
    def _recursive_addition(self, data1, data2, sign):
        if isinstance (data1, list):
            return [self._recursive_addition(subdata1, subdata2, sign) for subdata1, subdata2 in zip(data1, data2)]    
        else:
            if sign > 0:
                return data1 + data2
            else:
                return data1 - data2  
    
    def _get_DLine(self, indexes):
        dline = []
        for n in indexes:
            if isinstance (n, list):
                for _ in range(n[0], n[-1]):
                    data = self.tensor
                    indexe = tuple(_ if x == n else x for x in indexes)
                    for i in indexe:
                        data = data[i]
                    dline.append(data)
        return dline
    
    def _lst_nbr(self, indexes):
        count = 0
        for n in indexes:
            if isinstance(n, list):
                count += 1
        return count
    
    def _get_combination(self,indexes, recursive_memory = []):
        if self._lst_nbr(indexes)< 1 and recursive_memory == [] :
            return indexes
        elif len(indexes) == 1:
            if isinstance (indexes[0], list):
                return [recursive_memory+[_] for _ in range(indexes[0][0], indexes[0][-1])]
            else:
                return [recursive_memory+indexes]
        else:
            if isinstance(indexes[0], list):
                return[item for sublist in [self._get_combination(indexes[1:], recursive_memory+[_]) for _ in range(indexes[0][0], indexes[0][-1])] for item in sublist]
            else:
                return self._get_combination(indexes[1:], recursive_memory+[indexes[0]])

    def extract_tensor(self, indexes):
        if self._lst_nbr(indexes) == 1:
            return self._get_DLine(indexes)
        else:
            extract = []
            for _ in indexes:
                if isinstance(_, list):
                    return [self.extract_tensor(tuple(i if x == _ else x for x in indexes)) for i in range(_[0], _[-1])]

    def partial_filing(self, indexes, filing):
        if isinstance (filing, int):
            if self._lst_nbr(indexes) < 1:
                data = self.tensor
                for _ in indexes[:-1]:
                    data = data[_]
                data[indexes[-1]] = filing
            else:
                indexes = self._get_combination(indexes)
                print(indexes)
                for i in indexes:
                    data = self.tensor
                    for _ in i[:-1]:
                        data = data[_]
                    data[i[-1]] = filing
        elif isinstance(filing, NDimensionTensor):
            if self._lst_nbr(indexes) < 1:
                data = self.tensor
                for _ in indexes[:-1]:
                    data = data[_]
                data[indexes[-1]] = filing[indexes[-1]]
            else:
                indexes_filing = self._get_combination([[0,i] for i in filing.shape])
                indexes = self._get_combination(indexes)
                for i,j in zip(indexes, indexes_filing):
                    data = self.tensor
                    data_filing = filing.tensor
                    for x,y in zip(i[:-1], j[:-1]):
                        data = data[x]
                        data_filing = data_filing[y]
                    data[i[-1]] = data_filing[j[-1]]
        else:
            raise ValueError("Please use only an integer or another tensor to partially fill your tensor")
    
    
    def concatenate(self, tensor, dimension, position):
        if self.shape[:dimension] != tensor.shape[:dimension]:
            raise ValueError ("The two tensors must have coherent shapes")
        if not isinstance (tensor, NDimensionTensor):
            raise ValueError ("You can only concatenante a tensor to another")
        if dimension >= len(self.shape):
            raise ValueError ("Please specify a valid dimension")
        if position != "front" and position != "back":
            raise ValueError ("Please indicate clearly the point of concatenation")
        new_shape = [self.shape[dimension]+tensor.shape[dimension] if x == dimension else y for x,y in enumerate(self.shape)]
        print(new_shape)
        result = NDimensionTensor(new_shape, 0)
        if position == "back":
            result.partial_filing([[0,x] for x in self.shape], self)
            result.partial_filing([[y,y+self.shape[dimension]] if x == dimension else [0,y] for x,y in enumerate(tensor.shape)], tensor)
        elif position == "front":
            result.partial_filing([[0,x] for x in tensor.shape], tensor)
            print(result)
            result.partial_filing([[y,y+self.shape[dimension]] if x == dimension else [0,y] for x,y in enumerate(tensor.shape)], self)
        return result

    @classmethod
    def ToTensor(cls, data):
        if isinstance(data, list):
            new_shape = []
            _ = data
            while not isinstance (_, int):
                new_shape.append(len(_))
                _ = _[0]
            new_tensor = NDimensionTensor(new_shape)
            indexes = new_tensor._get_combination([[0,i] for i in new_shape])
            for i in indexes:
                filing = data
                for j in i:
                    filing = filing[j]
                new_tensor.partial_filing(i,filing)
            return new_tensor
        else:
            raise ValueError ("You can only convert a list to a tensor")
        
    @classmethod
    def rank(cls, tensor):
        if isinstance(tensor, NDimensionTensor):
            return len(tensor.shape)

