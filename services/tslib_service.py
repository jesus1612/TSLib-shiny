# Service layer for TSLib integration
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import matplotlib.pyplot as plt
import io
import base64

# Import TSLib components
from tslib import ARModel, MAModel, ARMAModel, ARIMAModel
from tslib.preprocessing.validation import DataValidator


class TSLibService:
    """Service class to encapsulate TSLib functionality for Shiny app"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def validate_data(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Validate time series data using TSLib DataValidator
        
        Args:
            df: DataFrame containing the data
            column: Name of the column to validate
            
        Returns:
            Dictionary with validation results and messages
        """
        try:
            # Extract the series and convert to numeric if needed
            if pd.api.types.is_numeric_dtype(df[column]):
                data = df[column].values
            else:
                # Try to convert from string format (currency, etc.)
                data = self.convert_to_numeric(df, column).values
            
            # Validate using TSLib
            is_valid = self.validator.validate(data)
            
            messages = []
            warnings = []
            
            # Basic checks
            if np.any(np.isnan(data)):
                missing_count = np.sum(np.isnan(data))
                missing_pct = (missing_count / len(data)) * 100
                warnings.append(f"Datos faltantes: {missing_count} ({missing_pct:.2f}%)")
            
            if len(data) < 30:
                warnings.append("Serie temporal corta (< 30 observaciones). Resultados pueden no ser confiables.")
            
            if np.any(np.isinf(data)):
                warnings.append("Valores infinitos detectados")
            
            # Check for outliers using IQR method
            q1 = np.percentile(data[~np.isnan(data)], 25)
            q3 = np.percentile(data[~np.isnan(data)], 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = np.sum((data < lower_bound) | (data > upper_bound))
            if outliers > 0:
                warnings.append(f"Outliers detectados: {outliers}")
            
            if is_valid:
                messages.append("✓ Datos válidos para análisis")
            else:
                messages.append("✗ Los datos requieren preprocesamiento")
            
            return {
                'valid': is_valid or len(warnings) == 0,  # Consider valid if no critical warnings
                'messages': messages,
                'warnings': warnings,
                'quality_report': {},
                'length': len(data),
                'has_issues': len(warnings) > 0
            }
            
        except Exception as e:
            return {
                'valid': False,
                'messages': [f"Error en validación: {str(e)}"],
                'warnings': [],
                'quality_report': {},
                'length': 0,
                'has_issues': True
            }
    
    def detect_datetime_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Detect datetime column in DataFrame
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Name of detected datetime column or None
        """
        # Common datetime column names
        datetime_keywords = ['date', 'time', 'timestamp', 'fecha', 'tiempo', 'datetime']
        
        for col in df.columns:
            # Check by name
            if any(keyword in col.lower() for keyword in datetime_keywords):
                return col
            
            # Check by dtype
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                return col
            
            # Try to parse as datetime
            try:
                pd.to_datetime(df[col].head(10))
                return col
            except:
                continue
        
        return None
    
    def get_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of numeric columns from DataFrame
        Includes columns that can be converted to numeric (e.g., currency format)
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            List of numeric column names
        """
        numeric_cols = []
        
        # First, add columns that are already numeric
        numeric_cols.extend(df.select_dtypes(include=[np.number]).columns.tolist())
        
        # Then, check string columns that might contain numeric data
        string_cols = df.select_dtypes(include=['object']).columns
        
        for col in string_cols:
            # Skip if already identified as numeric
            if col in numeric_cols:
                continue
            
            # Try to convert to numeric (handles currency, percentages, etc.)
            try:
                # Take a sample to test conversion
                sample = df[col].dropna().head(10)
                if len(sample) == 0:
                    continue
                
                # Try to convert removing common non-numeric characters
                test_values = sample.astype(str).str.replace('$', '', regex=False)
                test_values = test_values.str.replace(',', '', regex=False)
                test_values = test_values.str.replace('%', '', regex=False)
                test_values = test_values.str.strip()
                
                # Try conversion
                pd.to_numeric(test_values, errors='raise')
                
                # If successful, add to numeric columns
                numeric_cols.append(col)
            except (ValueError, TypeError, AttributeError):
                # Not convertible to numeric
                continue
        
        return numeric_cols
    
    def convert_to_numeric(self, df: pd.DataFrame, column: str) -> pd.Series:
        """
        Convert a column to numeric, handling currency and percentage formats
        
        Args:
            df: DataFrame containing the column
            column: Name of column to convert
            
        Returns:
            Series with numeric values
        """
        if pd.api.types.is_numeric_dtype(df[column]):
            return df[column]
        
        # Convert to string and clean
        series = df[column].astype(str)
        series = series.str.replace('$', '', regex=False)
        series = series.str.replace(',', '', regex=False)
        series = series.str.replace('%', '', regex=False)
        series = series.str.strip()
        
        # Convert to numeric
        return pd.to_numeric(series, errors='coerce')
    
    def fit_model(
        self,
        data: np.ndarray,
        model_type: str,
        order: Tuple[int, ...],
        auto_select: bool = False,
        **kwargs
    ) -> Any:
        """
        Fit a TSLib model
        
        Args:
            data: Time series data
            model_type: Type of model ('AR', 'MA', 'ARMA', 'ARIMA')
            order: Model order (p), (q), (p,q), or (p,d,q)
            auto_select: Whether to use automatic order selection
            **kwargs: Additional model parameters
            
        Returns:
            Fitted model instance
        """
        try:
            if model_type == 'AR':
                model = ARModel(
                    order=order[0] if not auto_select else None,
                    auto_select=auto_select,
                    validation=True,
                    **kwargs
                )
            elif model_type == 'MA':
                model = MAModel(
                    order=order[0] if not auto_select else None,
                    auto_select=auto_select,
                    validation=True,
                    **kwargs
                )
            elif model_type == 'ARMA':
                model = ARMAModel(
                    order=order if not auto_select else None,
                    auto_select=auto_select,
                    validation=True,
                    **kwargs
                )
            elif model_type == 'ARIMA':
                model = ARIMAModel(
                    order=order if not auto_select else None,
                    auto_select=auto_select,
                    validation=True,
                    **kwargs
                )
            else:
                raise ValueError(f"Modelo no soportado: {model_type}")
            
            # Fit the model
            model.fit(data)
            
            return model
            
        except Exception as e:
            raise RuntimeError(f"Error al ajustar modelo {model_type}: {str(e)}")
    
    def get_forecast(
        self,
        model: Any,
        steps: int = 10,
        return_conf_int: bool = True
    ) -> Dict[str, Any]:
        """
        Generate forecast from fitted model
        
        Args:
            model: Fitted TSLib model
            steps: Number of steps to forecast
            return_conf_int: Whether to return confidence intervals
            
        Returns:
            Dictionary with forecast results
        """
        try:
            if return_conf_int:
                forecast, conf_int = model.predict(steps=steps, return_conf_int=True)
                return {
                    'forecast': forecast,
                    'lower_bound': conf_int[0],
                    'upper_bound': conf_int[1],
                    'steps': steps
                }
            else:
                forecast = model.predict(steps=steps, return_conf_int=False)
                return {
                    'forecast': forecast,
                    'lower_bound': None,
                    'upper_bound': None,
                    'steps': steps
                }
        except Exception as e:
            raise RuntimeError(f"Error al generar forecast: {str(e)}")
    
    def get_model_metrics(self, model: Any) -> Dict[str, float]:
        """
        Extract metrics from fitted model
        
        Args:
            model: Fitted TSLib model
            
        Returns:
            Dictionary with model metrics
        """
        try:
            metrics = {}
            
            # Get fitted parameters if available
            if hasattr(model, '_fitted_params'):
                params = model._fitted_params
                metrics['aic'] = params.get('aic', None)
                metrics['bic'] = params.get('bic', None)
            
            # Get model order
            if hasattr(model, 'order'):
                order = model.order
                if isinstance(order, tuple):
                    if len(order) == 1:
                        metrics['order'] = f"({order[0]})"
                    elif len(order) == 2:
                        metrics['order'] = f"({order[0]}, {order[1]})"
                    elif len(order) == 3:
                        metrics['order'] = f"({order[0]}, {order[1]}, {order[2]})"
                else:
                    metrics['order'] = f"({order})"
            
            return metrics
            
        except Exception as e:
            print(f"Error extracting metrics: {e}")
            return {}
    
    def get_exploratory_analysis(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Get exploratory analysis including ACF/PACF
        
        Args:
            data: Time series data
            
        Returns:
            Dictionary with analysis results
        """
        try:
            from tslib.core.acf_pacf import ACFCalculator, PACFCalculator
            
            # Calculate ACF and PACF
            acf_calc = ACFCalculator()
            pacf_calc = PACFCalculator()
            
            # Try with nlags parameter first, fallback to default if not supported
            try:
                acf_values = acf_calc.calculate(data, nlags=min(20, len(data) // 2))
            except TypeError:
                # nlags not supported, use default
                acf_values = acf_calc.calculate(data)
                # Truncate to reasonable length
                if isinstance(acf_values, (list, np.ndarray)) and len(acf_values) > 20:
                    acf_values = acf_values[:20]
            
            try:
                pacf_values = pacf_calc.calculate(data, nlags=min(20, len(data) // 2))
            except TypeError:
                # nlags not supported, use default
                pacf_values = pacf_calc.calculate(data)
                # Truncate to reasonable length
                if isinstance(pacf_values, (list, np.ndarray)) and len(pacf_values) > 20:
                    pacf_values = pacf_values[:20]
            
            # Basic statistics
            stats = {
                'mean': float(np.mean(data)),
                'std': float(np.std(data)),
                'min': float(np.min(data)),
                'max': float(np.max(data)),
                'median': float(np.median(data)),
                'length': len(data)
            }
            
            return {
                'acf': acf_values.tolist() if isinstance(acf_values, np.ndarray) else acf_values if isinstance(acf_values, list) else [],
                'pacf': pacf_values.tolist() if isinstance(pacf_values, np.ndarray) else pacf_values if isinstance(pacf_values, list) else [],
                'statistics': stats
            }
            
        except Exception as e:
            print(f"Error in exploratory analysis: {e}")
            return {
                'acf': [],
                'pacf': [],
                'statistics': {
                    'mean': float(np.mean(data)),
                    'std': float(np.std(data)),
                    'min': float(np.min(data)),
                    'max': float(np.max(data)),
                    'median': float(np.median(data)),
                    'length': len(data)
                }
            }
    
    def get_residual_diagnostics(self, model: Any) -> Dict[str, Any]:
        """
        Get residual diagnostics from fitted model
        
        Args:
            model: Fitted TSLib model
            
        Returns:
            Dictionary with diagnostic results
        """
        try:
            diagnostics = {}
            
            # Get residuals
            if hasattr(model, 'get_residuals'):
                residuals = model.get_residuals()
                diagnostics['residuals'] = residuals.tolist() if isinstance(residuals, np.ndarray) else residuals
                
                # Basic residual statistics
                diagnostics['residual_mean'] = float(np.mean(residuals))
                diagnostics['residual_std'] = float(np.std(residuals))
            
            # Get residual diagnostics if available
            if hasattr(model, 'get_residual_diagnostics'):
                diag = model.get_residual_diagnostics()
                diagnostics.update(diag)
            
            return diagnostics
            
        except Exception as e:
            print(f"Error in residual diagnostics: {e}")
            return {}
    
    def calculate_basic_stats(self, data: np.ndarray) -> Dict[str, float]:
        """
        Calculate basic statistics for time series
        
        Args:
            data: Time series data
            
        Returns:
            Dictionary with statistics
        """
        return {
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'median': float(np.median(data)),
            'q25': float(np.percentile(data, 25)),
            'q75': float(np.percentile(data, 75)),
            'length': len(data)
        }

