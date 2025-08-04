# Synthetic Generator

A comprehensive Python library for generating synthetic data with various distributions, correlations, and constraints for machine learning and data science applications.

## 🌟 Features

### Core Data Generation
- **Multiple Distributions**: Normal, Uniform, Exponential, Gamma, Beta, Weibull, Poisson, Binomial, Geometric, Categorical
- **Data Types**: Integer, Float, String, Boolean, Date, DateTime, Email, Phone, Address, Name
- **Correlations**: Define relationships between variables with correlation matrices
- **Constraints**: Value ranges, uniqueness, null probabilities, pattern matching
- **Dependencies**: Generate data based on other columns with conditional rules

### Advanced Features
- **Schema Inference**: Automatically detect data types and distributions from existing data
- **Templates**: Pre-built schemas for common use cases (customer data, medical data, e-commerce, financial)
- **Privacy**: Basic anonymization and differential privacy support
- **Validation**: Comprehensive data validation against schemas
- **Export**: Multiple format support (CSV, JSON, Parquet, Excel)

### User Experience
- **Easy-to-Use API**: Simple, intuitive interface for data generation
- **Flexible Configuration**: Support for both programmatic and configuration-based setup
- **Reproducibility**: Seed-based random generation for consistent results
- **Performance**: Optimized for large-scale data generation

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install synthetic-generator

# Install from GitHub
git clone https://github.com/nguyenpanda/synthetic-generator.git
cd synthetic-generator
pip install -e .
```

### Basic Usage

```python
import pandas as pd
from synthetic_generator import generate_data, DataSchema, ColumnSchema, DataType, DistributionType

# Define a simple schema
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
        ),
        ColumnSchema(
            name="city",
            data_type=DataType.CATEGORICAL,
            distribution=DistributionType.CATEGORICAL,
            parameters={
                "categories": ["New York", "Los Angeles", "Chicago", "Houston"],
                "probabilities": [0.3, 0.25, 0.25, 0.2]
            }
        )
    ]
)

# Generate data
data = generate_data(schema, n_samples=1000, seed=42)
print(data.head())
```

### Using Templates

```python
from synthetic_generator import load_template, generate_data

# Load a pre-built template
schema = load_template("customer_data")

# Generate data
data = generate_data(schema, n_samples=500, seed=123)
print(data.head())
```

### Schema Inference

```python
import pandas as pd
from synthetic_generator import infer_schema, generate_data

# Load existing data
existing_data = pd.read_csv("your_data.csv")

# Infer schema
schema = infer_schema(existing_data)

# Generate new data based on inferred schema
new_data = generate_data(schema, n_samples=1000, seed=456)
```

## 📚 Detailed Documentation

### Data Types

Synthetic Generator supports various data types:

- **Numeric**: `INTEGER`, `FLOAT`
- **Text**: `STRING`, `EMAIL`, `PHONE`, `ADDRESS`, `NAME`
- **Categorical**: `CATEGORICAL`, `BOOLEAN`
- **Temporal**: `DATE`, `DATETIME`

### Distributions

Available statistical distributions:

- **Continuous**: `NORMAL`, `UNIFORM`, `EXPONENTIAL`, `GAMMA`, `BETA`, `WEIBULL`
- **Discrete**: `POISSON`, `BINOMIAL`, `GEOMETRIC`
- **Categorical**: `CATEGORICAL`, `CONSTANT`

### Correlations

Define relationships between variables:

```python
schema = DataSchema(
    columns=[...],
    correlations={
        "height": {"weight": 0.7},  # Height and weight correlation
        "age": {"income": 0.4}      # Age and income correlation
    }
)
```

### Constraints

Apply various constraints to your data:

```python
ColumnSchema(
    name="salary",
    data_type=DataType.FLOAT,
    distribution=DistributionType.NORMAL,
    parameters={"mean": 50000, "std": 15000},
    min_value=30000,        # Minimum value
    max_value=100000,       # Maximum value
    unique=True,            # Unique values
    nullable=True,          # Allow null values
    null_probability=0.05   # 5% null probability
)
```

### Dependencies

Generate data based on other columns:

```python
ColumnSchema(
    name="bonus",
    data_type=DataType.FLOAT,
    distribution=DistributionType.UNIFORM,
    parameters={"low": 0, "high": 10000},
    depends_on=["salary"],
    conditional_rules={
        "rules": [
            {
                "condition": {"salary": {"operator": ">", "value": 70000}},
                "value": 5000
            }
        ],
        "default": 1000
    }
)
```

## 🎯 Use Cases

### Customer Data
Generate realistic customer profiles with demographics, contact information, and preferences.

### Medical Data
Create synthetic patient data with health metrics, demographics, and medical conditions while preserving privacy.

### Financial Data
Generate transaction data with realistic amounts, categories, and temporal patterns.

### E-commerce Data
Create order and product data with realistic relationships and business rules.

## 🔧 Advanced Features

### Privacy Settings

```python
# Generate data with privacy protection
data = generate_data(
    schema, 
    n_samples=1000, 
    privacy_level="basic"  # or "differential"
)
```

### Data Validation

```python
from synthetic_generator import validate_data

# Validate generated data
results = validate_data(data, schema)
print(f"Valid: {results['valid']}")
print(f"Errors: {results['errors']}")
print(f"Warnings: {results['warnings']}")
```

### Data Export

```python
from synthetic_generator.export import export_data

# Export to various formats
export_data(data, 'csv', filepath='data.csv')
export_data(data, 'json', filepath='data.json')
export_data(data, 'excel', filepath='data.xlsx')
export_data(data, 'parquet', filepath='data.parquet')
```

## 📊 Available Templates

- `customer_data`: Customer information with demographics
- `ecommerce_data`: E-commerce transaction data
- `medical_data`: Medical patient data with health metrics
- `financial_data`: Financial transaction data

## 🛠️ Development

### Installation for Development

```bash
git clone https://github.com/nguyenpanda/synthetic-generator.git
cd synthetic-generator
make install_dev
```

### Running Tests

```bash
make test
```

### Running Examples

```bash
python examples/basic_usage.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/nguyenpanda/synthetic-generator.git
cd synthetic-generator
make install_dev
```

## 📄 License

Synthetic Generator is released under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## 📞 Contact

**Hà Tường Nguyên (Mr.)**  
**Computer Science**  
<small>Office for International Study Programs | HCMC University of Technology</small>

**Contact via:**
- **Gmail:** nguyen.hatuong0107@hcmut.edu.vn
- **Gmail:** hatuongnguyen0107@gmail.com

## 🙏 Acknowledgments

Thanks to all contributors and the open-source community for making this project possible.

---

Happy coding with Synthetic Generator! 🚀
