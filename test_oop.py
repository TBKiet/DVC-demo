class Animal:
    def __init__(self, name, age=0):
        self.name = name
        self.age = age

    def speak(self):
        raise NotImplementedError("Subclass must implement this!")


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, age=1)

    def speak(self):
        return f"{self.name} GauGau"


dog = Dog("Khoa")
print(dog.speak())
Dog.age = 1
print(dog.age)
