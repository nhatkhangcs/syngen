"""
API endpoints for Synthetic Generator Web UI.
"""

import os
import tempfile
import json
import pandas as pd
import numpy as np
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
# Import these functions directly to avoid circular imports
from ..schemas import DataSchema, ColumnSchema, DataType, DistributionType

api_bp = Blueprint('api', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx', 'parquet'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.7'
    })


@api_bp.route('/generate', methods=['POST'])
def generate_synthetic_data():
    """Generate synthetic data based on schema."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        schema_dict = data.get('schema')
        n_samples = data.get('n_samples', 1000)
        seed = data.get('seed')
        privacy_level = data.get('privacy_level')
        
        if not schema_dict:
            return jsonify({'error': 'Schema is required'}), 400
        
        # Convert schema dict to DataSchema object
        schema = DataSchema.from_dict(schema_dict)
        
        # Import and generate data (avoid circular import)
        from ..generators.base import DataGenerator
        generator = DataGenerator(schema)
        result = generator.generate(n_samples, seed)
        
        # Convert to JSON-serializable format
        data_json = result.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': data_json,
            'shape': result.shape,
            'columns': list(result.columns),
            'sample_size': len(result)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/infer-schema', methods=['POST'])
def infer_data_schema():
    """Infer schema from uploaded data."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.rsplit('.', 1)[1].lower()}") as tmp_file:
            file.save(tmp_file.name)
            
            # Read data based on file type
            if file.filename.endswith('.csv'):
                data = pd.read_csv(tmp_file.name)
            elif file.filename.endswith('.json'):
                data = pd.read_json(tmp_file.name)
            elif file.filename.endswith('.xlsx'):
                data = pd.read_excel(tmp_file.name)
            elif file.filename.endswith('.parquet'):
                data = pd.read_parquet(tmp_file.name)
            
            # Clean up temporary file
            os.unlink(tmp_file.name)
        
        # Infer schema (avoid circular import)
        sample_size = request.form.get('sample_size', type=int)
        from ..schemas.inference import infer_schema_from_data
        schema = infer_schema_from_data(data, sample_size)
        
        # Convert schema to dict
        schema_dict = schema.to_dict()
        
        return jsonify({
            'success': True,
            'schema': schema_dict,
            'original_shape': data.shape,
            'columns': list(data.columns)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get available templates."""
    try:
        templates = [
            {
                'name': 'customer_data',
                'display_name': 'Customer Data',
                'description': 'Customer information with demographics and contact details',
                'category': 'Business'
            },
            {
                'name': 'medical_data',
                'display_name': 'Medical Data',
                'description': 'Patient data with health metrics and medical conditions',
                'category': 'Healthcare'
            },
            {
                'name': 'financial_data',
                'display_name': 'Financial Data',
                'description': 'Transaction data with amounts, categories, and temporal patterns',
                'category': 'Finance'
            },
            {
                'name': 'ecommerce_data',
                'display_name': 'E-commerce Data',
                'description': 'Order and product data with realistic business relationships',
                'category': 'E-commerce'
            }
        ]
        
        return jsonify({
            'success': True,
            'templates': templates
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/templates/<template_name>', methods=['GET'])
def get_template(template_name):
    """Get specific template schema."""
    try:
        # Load template (avoid circular import)
        from ..schemas.templates import load_template_schema
        schema = load_template_schema(template_name)
        schema_dict = schema.to_dict()
        
        return jsonify({
            'success': True,
            'template_name': template_name,
            'schema': schema_dict
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/validate', methods=['POST'])
def validate_synthetic_data():
    """Validate generated data against schema."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data_df = pd.DataFrame(data.get('data', []))
        schema_dict = data.get('schema')
        
        if not schema_dict:
            return jsonify({'error': 'Schema is required'}), 400
        
        schema = DataSchema.from_dict(schema_dict)
        
        # Validate data (avoid circular import)
        validation_results = schema.validate_data(data_df)
        
        return jsonify({
            'success': True,
            'validation': validation_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/export', methods=['POST'])
def export_generated_data():
    """Export generated data to various formats."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data_df = pd.DataFrame(data.get('data', []))
        export_format = data.get('format', 'csv')
        filename = data.get('filename', f'synthetic_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{export_format}') as tmp_file:
            # Export data (avoid circular import)
            if export_format == 'csv':
                data_df.to_csv(tmp_file.name, index=False)
            elif export_format == 'json':
                data_df.to_json(tmp_file.name, orient='records', indent=2)
            elif export_format == 'excel':
                data_df.to_excel(tmp_file.name, index=False)
            elif export_format == 'parquet':
                data_df.to_parquet(tmp_file.name, index=False)
            
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=f'{filename}.{export_format}',
                mimetype='application/octet-stream'
            )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/statistics', methods=['POST'])
def get_data_statistics():
    """Get statistical analysis of generated data."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data_df = pd.DataFrame(data.get('data', []))
        
        # Calculate basic statistics
        stats = {
            'shape': data_df.shape,
            'columns': list(data_df.columns),
            'dtypes': data_df.dtypes.astype(str).to_dict(),
            'missing_values': data_df.isnull().sum().to_dict(),
            'numeric_stats': {},
            'categorical_stats': {}
        }
        
        # Numeric statistics
        numeric_cols = data_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats['numeric_stats'] = data_df[numeric_cols].describe().to_dict()
        
        # Categorical statistics
        categorical_cols = data_df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            stats['categorical_stats'][col] = {
                'unique_count': data_df[col].nunique(),
                'top_values': data_df[col].value_counts().head(5).to_dict()
            }
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/data-types', methods=['GET'])
def get_data_types():
    """Get available data types."""
    try:
        data_types = [
            {'value': 'INTEGER', 'label': 'Integer', 'category': 'Numeric'},
            {'value': 'FLOAT', 'label': 'Float', 'category': 'Numeric'},
            {'value': 'STRING', 'label': 'String', 'category': 'Text'},
            {'value': 'EMAIL', 'label': 'Email', 'category': 'Text'},
            {'value': 'PHONE', 'label': 'Phone', 'category': 'Text'},
            {'value': 'ADDRESS', 'label': 'Address', 'category': 'Text'},
            {'value': 'NAME', 'label': 'Name', 'category': 'Text'},
            {'value': 'CATEGORICAL', 'label': 'Categorical', 'category': 'Categorical'},
            {'value': 'BOOLEAN', 'label': 'Boolean', 'category': 'Categorical'},
            {'value': 'DATE', 'label': 'Date', 'category': 'Temporal'},
            {'value': 'DATETIME', 'label': 'DateTime', 'category': 'Temporal'}
        ]
        
        return jsonify({
            'success': True,
            'data_types': data_types
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/distributions', methods=['GET'])
def get_distributions():
    """Get available distributions."""
    try:
        distributions = [
            {'value': 'NORMAL', 'label': 'Normal', 'category': 'Continuous'},
            {'value': 'UNIFORM', 'label': 'Uniform', 'category': 'Continuous'},
            {'value': 'EXPONENTIAL', 'label': 'Exponential', 'category': 'Continuous'},
            {'value': 'GAMMA', 'label': 'Gamma', 'category': 'Continuous'},
            {'value': 'BETA', 'label': 'Beta', 'category': 'Continuous'},
            {'value': 'WEIBULL', 'label': 'Weibull', 'category': 'Continuous'},
            {'value': 'POISSON', 'label': 'Poisson', 'category': 'Discrete'},
            {'value': 'BINOMIAL', 'label': 'Binomial', 'category': 'Discrete'},
            {'value': 'GEOMETRIC', 'label': 'Geometric', 'category': 'Discrete'},
            {'value': 'CATEGORICAL', 'label': 'Categorical', 'category': 'Categorical'},
            {'value': 'CONSTANT', 'label': 'Constant', 'category': 'Special'}
        ]
        
        return jsonify({
            'success': True,
            'distributions': distributions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
