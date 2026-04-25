# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=too-few-public-methods

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from service.models import Product, Category


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)

    # Use FuzzyChoice for random product names
    name = FuzzyChoice(choices=[
        "Hat", "Pants", "Shirt", "Apple", "Banana",
        "Pots", "Towels", "Ford", "Chevy", "Hammer", "Wrench"
    ])

    # Use Faker for description text
    description = factory.Faker("text")

    # Use FuzzyDecimal for price range
    price = FuzzyDecimal(0.5, 2000.0, 2)

    # Use FuzzyChoice for availability
    available = FuzzyChoice(choices=[True, False])

    # Use FuzzyChoice for categories
    category = FuzzyChoice(choices=[
        Category.UNKNOWN,
        Category.CLOTHS,
        Category.FOOD,
        Category.HOUSEWARES,
        Category.AUTOMOTIVE,
        Category.TOOLS,
    ])

   ## Add code to create Fake Products 
