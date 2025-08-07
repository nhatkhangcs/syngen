# Synthetic Generator Web UI Guide

## 🚀 Quick Start

### Starting the Web Interface

```bash
# Method 1: Using the launcher script
python run_web_ui.py

# Method 2: Using the CLI
synthetic-generator web

# Method 3: With custom settings
synthetic-generator web --port 8080 --host 0.0.0.0
```

### Accessing the Interface

- **Main URL**: http://localhost:5000
- **API Endpoints**: http://localhost:5000/api
- **Documentation**: http://localhost:5000/about

## 📊 Dashboard

The dashboard provides an overview of the Synthetic Generator with:
- Quick statistics about available features
- Recent activity tracking
- System status information
- Quick access to main features

## 🔧 Data Generator

### Creating Custom Schemas

1. **Navigate to Generator**: Click "Generator" in the navigation
2. **Configure Settings**:
   - Set number of samples (1-100,000)
   - Choose random seed (optional)
   - Select privacy level
3. **Add Columns**:
   - Click "Add Column" to create new columns
   - Configure each column:
     - **Name**: Column identifier
     - **Data Type**: Integer, Float, String, Email, etc.
     - **Distribution**: Normal, Uniform, Exponential, etc.
     - **Parameters**: Distribution-specific settings
     - **Constraints**: Min/max values, uniqueness
4. **Generate Data**: Click "Generate Data" to create synthetic data

### Using Templates

1. **Load Template**: Select from dropdown menu
2. **Available Templates**:
   - **Customer Data**: Demographics and contact information
   - **Medical Data**: Patient health metrics
   - **Financial Data**: Transaction data
   - **E-commerce Data**: Order and product data
3. **Customize**: Modify template parameters as needed
4. **Generate**: Create data based on template

## 🧠 Schema Inference

### Uploading Data

1. **Navigate to Inference**: Click "Inference" in navigation
2. **Upload File**: Drag & drop or click to browse
   - **Supported Formats**: CSV, JSON, Excel (.xlsx), Parquet
   - **File Size Limit**: 16MB maximum
3. **Configure Settings**:
   - Set sample size for inference (100-10,000 rows)
4. **Infer Schema**: Click "Infer Schema" to analyze data
5. **Review Results**: Examine inferred data types and distributions
6. **Take Action**:
   - Use schema for generation
   - Download schema as JSON
   - Generate sample data

## ✅ Data Validation

### Validating Generated Data

1. **Navigate to Validation**: Click "Validation" in navigation
2. **Upload Data**: Upload your generated data file
3. **Upload Schema** (Optional): Provide schema for validation
4. **Choose Validation Type**:
   - **Basic**: Standard data quality checks
   - **Strict**: Comprehensive validation
   - **Custom**: User-defined rules
5. **Validate**: Click "Validate Data" to run checks
6. **Review Results**: Check validation status and issues

## 📤 Data Export

### Exporting Generated Data

1. **Navigate to Export**: Click "Export" in navigation
2. **Configure Export Settings**:
   - **Format**: CSV, JSON, Excel, Parquet
   - **Filename**: Custom filename
   - **Timestamp**: Include date/time in filename
   - **Compression**: Gzip, ZIP, or none
3. **Export**: Click "Export Data" to download
4. **Quick Export**: Use quick export buttons for common formats

### Export History

- View recent exports with timestamps
- Track file sizes and row counts
- Access export statistics

## 🔌 API Endpoints

### Available Endpoints

- `GET /api/health` - Health check
- `POST /api/generate` - Generate synthetic data
- `POST /api/infer-schema` - Infer schema from data
- `GET /api/templates` - List available templates
- `GET /api/templates/{name}` - Get specific template
- `POST /api/validate` - Validate data against schema
- `POST /api/export` - Export data in various formats
- `POST /api/statistics` - Get data statistics
- `GET /api/data-types` - List available data types
- `GET /api/distributions` - List available distributions

### Example API Usage

```bash
# Generate data
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"schema": {...}, "n_samples": 1000}'

# Get templates
curl http://localhost:8000/api/templates

# Health check
curl http://localhost:8000/api/health
```

## 🎨 Features

### Interactive Interface
- **Drag & Drop**: Easy file uploads
- **Real-time Preview**: See generated data instantly
- **Live Statistics**: Dynamic data analysis
- **Responsive Design**: Works on desktop and mobile

### Data Types Supported
- **Numeric**: Integer, Float
- **Text**: String, Email, Phone, Address, Name
- **Categorical**: Categorical, Boolean
- **Temporal**: Date, DateTime

### Distributions Available
- **Continuous**: Normal, Uniform, Exponential, Gamma, Beta, Weibull
- **Discrete**: Poisson, Binomial, Geometric
- **Categorical**: Categorical, Constant

### Export Formats
- **CSV**: Comma-separated values
- **JSON**: JavaScript Object Notation
- **Excel**: Microsoft Excel (.xlsx)
- **Parquet**: Columnar format

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Try different port
   synthetic-generator web --port 5001
   ```

2. **File Upload Errors**
   - Check file size (max 16MB)
   - Verify file format (CSV, JSON, Excel, Parquet)
   - Ensure file is not corrupted

3. **Generation Errors**
   - Check schema configuration
   - Verify parameter values
   - Review error messages in console

4. **Browser Issues**
   - Clear browser cache
   - Try different browser
   - Check JavaScript console for errors

### Performance Tips

- Use smaller sample sizes for testing
- Close unnecessary browser tabs
- Restart the server if performance degrades
- Use appropriate data types for your use case

## 📚 Additional Resources

- **Documentation**: Visit `/about` page for detailed information
- **Examples**: Check the `examples/` directory for code samples
- **GitHub**: Visit the project repository for source code
- **PyPI**: Install via `pip install synthetic-generator`

## 🤝 Support

For issues and questions:
- Check the troubleshooting section above
- Review error messages in the browser console
- Visit the project GitHub repository
- Contact the maintainer via email

---

**Happy generating! 🚀**
