import factory
import phonenumbers
from faker import Faker
from faker.providers.phone_number.en_US import Provider
from phonenumbers.phonenumberutil import NumberParseException

from accounts.models import User

class CustomPhoneProvider(Provider):
    def phone_number(self):
        while True:
            try:
                phone_number = self.numerify(self.random_element(self.msisdn_formats))
                parsed_number = phonenumbers.parse(phone_number, 'US')
                if phonenumbers.is_valid_number(parsed_number):
                    return phonenumbers.format_number(
                        parsed_number,
                        phonenumbers.PhoneNumberFormat.E164
                    )
            except NumberParseException:
                pass

fake = Faker()
fake.add_provider(CustomPhoneProvider)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    nickname = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    address = factory.Faker('address')
    role = '회원'
