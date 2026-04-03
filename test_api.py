#!/usr/bin/env python
"""
Quick test script for API endpoints
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from equipment.models import Equipment
from api.serializers import EquipmentListSerializer

print("=" * 60)
print("TESTING EQUIPMENT API SERIALIZER")
print("=" * 60)

# Get all equipment
equipment_qs = Equipment.objects.all()
print(f"\nTotal Equipment in DB: {equipment_qs.count()}")

if equipment_qs.exists():
    # Test with first equipment
    first_eq = equipment_qs.first()
    print(f"\nTesting with: {first_eq}")

    try:
        serializer = EquipmentListSerializer(first_eq)
        data = serializer.data
        print("\n✅ Serializer SUCCESS!")
        print("\nSerialized Data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"\n❌ Serializer FAILED!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Test with all equipment
    print("\n" + "=" * 60)
    print("Testing with ALL equipment")
    print("=" * 60)
    try:
        serializer = EquipmentListSerializer(equipment_qs, many=True)
        data = serializer.data
        print(f"\n✅ Bulk Serializer SUCCESS!")
        print(f"Serialized {len(data)} equipment items")
    except Exception as e:
        print(f"\n❌ Bulk Serializer FAILED!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n⚠️ No equipment in database!")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

