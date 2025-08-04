#!/usr/bin/env python3
"""
Synthetic Generator Installation Verification Script

This script verifies that Synthetic Generator is properly installed and all
core functionality is working correctly.
"""

import sys
import traceback

def test_imports():
    """Test that all core modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from synthetic_generator import (
            generate_data, 
            infer_schema, 
            load_template, 
            validate_data,
            DataSchema,
            ColumnSchema,
            DataType,
            DistributionType
        )
        print("✅ All core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_basic_generation():
    """Test basic data generation."""
    print("\n🔍 Testing basic data generation...")
    
    try:
        from synthetic_generator import generate_data, DataSchema, ColumnSchema, DataType, DistributionType
        
        # Create a simple schema
        schema = DataSchema(
            columns=[
                ColumnSchema(
                    name="age",
                    data_type=DataType.INTEGER,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 30, "std": 10},
                    min_value=18,
                    max_value=80
                ),
                ColumnSchema(
                    name="income",
                    data_type=DataType.FLOAT,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 50000, "std": 20000},
                    min_value=20000,
                    max_value=200000
                )
            ]
        )
        
        # Generate data
        data = generate_data(schema, n_samples=100, seed=42)
        
        # Basic checks
        assert len(data) == 100
        assert "age" in data.columns
        assert "income" in data.columns
        assert data["age"].min() >= 18
        assert data["age"].max() <= 80
        
        print("✅ Basic data generation successful")
        print(f"   Generated {len(data)} samples")
        print(f"   Age range: {data['age'].min()} - {data['age'].max()}")
        print(f"   Income range: {data['income'].min():.0f} - {data['income'].max():.0f}")
        return True
        
    except Exception as e:
        print(f"❌ Basic generation failed: {e}")
        traceback.print_exc()
        return False

def test_templates():
    """Test template loading."""
    print("\n🔍 Testing templates...")
    
    try:
        from synthetic_generator import load_template, generate_data
        
        # Test all templates
        templates = ["customer_data", "ecommerce_data", "medical_data", "financial_data"]
        
        for template_name in templates:
            # Load a template
            schema = load_template(template_name)
            
            # Generate data
            data = generate_data(schema, n_samples=50, seed=123)
            
            print(f"✅ {template_name} template successful")
            print(f"   Columns: {list(data.columns)}")
            print(f"   Generated {len(data)} samples")
        
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        traceback.print_exc()
        return False

def test_schema_inference():
    """Test schema inference."""
    print("\n🔍 Testing schema inference...")
    
    try:
        import pandas as pd
        import numpy as np
        from synthetic_generator import infer_schema, generate_data
        
        # Create sample data with various types
        sample_data = pd.DataFrame({
            "user_id": range(1, 21),
            "age": np.random.normal(35, 10, 20).astype(int),
            "salary": np.random.normal(60000, 15000, 20),
            "department": np.random.choice(["IT", "HR", "Sales"], 20),
            "is_manager": np.random.choice([True, False], 20, p=[0.2, 0.8])
        })
        
        # Infer schema
        inferred_schema = infer_schema(sample_data)
        
        # Generate data from inferred schema
        new_data = generate_data(inferred_schema, n_samples=30, seed=456)
        
        print("✅ Schema inference successful")
        print(f"   Inferred {len(inferred_schema.columns)} columns")
        print(f"   Generated {len(new_data)} new samples")
        
        # Show inferred types
        for col in inferred_schema.columns:
            print(f"   {col.name}: {col.data_type.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema inference failed: {e}")
        traceback.print_exc()
        return False

def test_validation():
    """Test data validation."""
    print("\n🔍 Testing data validation...")
    
    try:
        from synthetic_generator import generate_data, validate_data, DataSchema, ColumnSchema, DataType, DistributionType
        
        # Create schema and data
        schema = DataSchema(
            columns=[
                ColumnSchema(
                    name="id",
                    data_type=DataType.INTEGER,
                    distribution=DistributionType.UNIFORM,
                    parameters={"low": 1, "high": 100},
                    unique=True
                ),
                ColumnSchema(
                    name="value",
                    data_type=DataType.FLOAT,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 0, "std": 1}
                )
            ]
        )
        
        data = generate_data(schema, n_samples=50, seed=789)
        
        # Validate data
        results = validate_data(data, schema)
        
        print("✅ Data validation successful")
        print(f"   Valid: {results['valid']}")
        print(f"   Errors: {len(results['errors'])}")
        print(f"   Warnings: {len(results['warnings'])}")
        return True
        
    except Exception as e:
        print(f"❌ Data validation failed: {e}")
        traceback.print_exc()
        return False

def test_export():
    """Test data export."""
    print("\n🔍 Testing data export...")
    
    try:
        from synthetic_generator import load_template, generate_data
        from synthetic_generator.export import export_data
        
        # Generate some data
        schema = load_template("customer_data")
        data = generate_data(schema, n_samples=10, seed=222)
        
        # Export to different formats
        export_data(data, 'csv', filepath='test_export.csv')
        export_data(data, 'json', filepath='test_export.json')
        
        print("✅ Data export successful")
        print("   Exported to CSV and JSON formats")
        return True
        
    except Exception as e:
        print(f"❌ Data export failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all verification tests."""
    print("🚀 Synthetic Generator Installation Verification")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_basic_generation,
        test_templates,
        test_schema_inference,
        test_validation,
        test_export
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Synthetic Generator is properly installed and working.")
        print("\n🎯 You can now:")
        print("   • Generate synthetic data for testing and development")
        print("   • Use pre-built templates for common use cases")
        print("   • Infer schemas from existing data")
        print("   • Export data to various formats")
        print("   • Apply correlations and constraints")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 