class Container:
    """
    A container of integers that should support
    addition, removal, and search for the median integer
    """
    def __init__(self):
        pass
        

    def add(self, value: int) -> None:
        """
        Adds the specified value to the container

        :param value: int
        """
        # TODO: implement this method
        container = []
        container.append(value)
        print(container)

    def delete(self, value: int) -> bool:
        """
        Attempts to delete one item of the specified value from the container

        :param value: int
        :return: True, if the value has been deleted, or
                 False, otherwise.
        """
        # TODO: implement this method
        container.remove(value)
        
        
        if value in self._container:
            return False
        
        else:
            return True

    def get_median(self) -> int:
        """
        Finds the container's median integer value, which is
        the middle integer when the all integers are sorted in order.
        If the sorted array has an even length,
        the leftmost integer between the two middle 
        integers should be considered as the median.

        :return: The median if the array is not empty, or
        :raise:  a runtime exception, otherwise.
        """
        # TODO: implement this method
        lista = []
        for q in self._container:
            lista.append(q)
        
        lista.sort()
            
        quant = len(lista)
        
        if self._container[0] is None:
            raise RuntimeException
        
        elif quant%2 == 0:
            num = ((quant // 2)) - 1
            return self._container[num]
            
        else:
            num = ((quant // 2) - + 1) -1
            return self._container[num]
            
        
            
        
Container().add(1)
