from faker import Faker
import random

class JukeboxInc():

    fake = Faker()
    Faker.seed(0)
    countries = ['KE', 'NG', 'UG']
    def __init__(self):
        pass 

    def get_name(self):
        return self.fake.name()

    def get_country(self):
        return random.choice(self.countries)

    def get_place(self, country):
        return self.fake.local_latlng(country_code=country)


