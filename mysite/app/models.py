from django.db import models


class AmountType(models.Model):
    """Represents the type of measurement for items (e.g., kg, litre, piece)."""
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.name)  # Explicit conversion to string


class ItemType(models.Model):
    """Represents a type of item with a unique barcode."""
    unique_barcode = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    amount_type = models.ForeignKey(AmountType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)  # Explicit conversion to string


class IndividualItem(models.Model):
    """Represents an individual item, such as a specific instance of a product."""
    id = models.AutoField(primary_key=True)
    expiration_date = models.DateField()
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)  # Renamed for clarity
    amount = models.FloatField()

    def __str__(self):
        return f"{str(self.item_type.name)} (ID: {str(self.id)})"  # Ensuring string conversion


class ShoppingList(models.Model):
    """Represents an item and its quantity in a shopping list."""
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, primary_key=True)  # Primary Key & FK
    amount = models.FloatField()

    def __str__(self):
        return f"{str(self.item_type.name)} - {str(self.amount)}"  # Ensuring string conversion
