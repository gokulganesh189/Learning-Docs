class Dog:
    def sound(self):
        print("Bark")


class Cat:
    def sound(self):
        print("Meow")

class Bird:
    def sound(self):
        print("Chirp")

def animal_sound(animal):
    animal.sound()


dog = Dog()
cat = Cat()
bird = Bird()

animal_sound(dog)
animal_sound(cat)
animal_sound(bird)