# Service layer for TSLib integration
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import matplotlib.pyplot as plt
import io
import base64
import logging

# Import TSLib components
from tslib import ARModel, MAModel, ARMAModel, ARIMAModel
from tslib.preprocessing.validation import DataValidator

# Setup logger
logger = logging.getLogger(__name__)

# Try to import ParallelARIMAWorkflow and check Spark availability
PARALLEL_ARIMA_AVAILABLE = False
SPARK_CHECKED = False
SPARK_AVAILABLE = False
ParallelARIMAWorkflow = None

try:
    from tslib.spark import ParallelARIMAWorkflow
    from tslib.utils.checks import check_spark_availability
    
    # Check if Spark is actually available (not just imported)
    SPARK_AVAILABLE = check_spark_availability()
    PARALLEL_ARIMA_AVAILABLE = SPARK_AVAILABLE
    SPARK_CHECKED = True
    
    if PARALLEL_ARIMA_AVAILABLE:
        logger.info("ParallelARIMAWorkflow imported and Spark is available")
    else:
        logger.warning("ParallelARIMAWorkflow imported but Spark is not available")
        logger.warning("Java gateway may not be running. Check Java installation and JAVA_HOME.")
except ImportError as e:
    logger.warning(f"ParallelARIMAWorkflow not available: {str(e)}")
    logger.warning("Parallel ARIMA model will not be available. Make sure Spark is configured.")
except Exception as e:
    logger.warning(f"Error checking Spark availability: {str(e)}")
    PARALLEL_ARIMA_AVAILABLE = False


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
        Fit a TSLib model (handles missing values)
        
        Args:
            data: Time series data (may contain NaN values)
            model_type: Type of model ('AR', 'MA', 'ARMA', 'ARIMA')
            order: Model order (p), (q), (p,q), or (p,d,q)
            auto_select: Whether to use automatic order selection
            **kwargs: Additional model parameters
            
        Returns:
            Fitted model instance
        """
        try:
            # Handle missing values: forward fill for model fitting
            data_clean = data.copy()
            if np.any(np.isnan(data_clean)):
                # Forward fill missing values
                mask = np.isnan(data_clean)
                indices = np.arange(len(data_clean))
                if np.any(~mask):  # If there are any non-NaN values
                    data_clean[mask] = np.interp(indices[mask], indices[~mask], data_clean[~mask])
                else:
                    # All values are NaN, use zeros
                    data_clean = np.zeros_like(data_clean)
            
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
            
            # Fit the model with cleaned data
            model.fit(data_clean)
            
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
        Get exploratory analysis including ACF/PACF (handles missing values)
        
        Args:
            data: Time series data (may contain NaN values)
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Check minimum data requirement for ACF/PACF
            MIN_DATA_FOR_ACF = 10  # Minimum observations needed for ACF/PACF
            
            # Handle missing values: forward fill for analysis
            data_clean = data.copy()
            if np.any(np.isnan(data_clean)):
                # Forward fill missing values
                mask = np.isnan(data_clean)
                indices = np.arange(len(data_clean))
                if np.any(~mask):  # If there are any non-NaN values
                    data_clean[mask] = np.interp(indices[mask], indices[~mask], data_clean[~mask])
                else:
                    # All values are NaN, use zeros
                    data_clean = np.zeros_like(data_clean)
            
            # Basic statistics (using cleaned data but noting missing values)
            valid_data = data[~np.isnan(data)] if np.any(np.isnan(data)) else data
            stats = {
                'mean': float(np.mean(valid_data)) if len(valid_data) > 0 else 0.0,
                'std': float(np.std(valid_data)) if len(valid_data) > 0 else 0.0,
                'min': float(np.min(valid_data)) if len(valid_data) > 0 else 0.0,
                'max': float(np.max(valid_data)) if len(valid_data) > 0 else 0.0,
                'median': float(np.median(valid_data)) if len(valid_data) > 0 else 0.0,
                'length': len(data),
                'missing_count': int(np.sum(np.isnan(data))) if np.any(np.isnan(data)) else 0
            }
            
            # Check if we have enough data for ACF/PACF
            if len(data_clean) < MIN_DATA_FOR_ACF:
                logger.warning(f"Insufficient data for ACF/PACF: {len(data_clean)} < {MIN_DATA_FOR_ACF}")
                return {
                    'acf': [],
                    'pacf': [],
                    'statistics': stats
                }
            
            # Try to import and calculate ACF/PACF
            try:
                from tslib.core.acf_pacf import ACFCalculator, PACFCalculator
                
                # Calculate ACF and PACF
                acf_calc = ACFCalculator()
                pacf_calc = PACFCalculator()
                
                # Calculate ACF
                # NOTE: ACFCalculator.calculate() returns a tuple (lags, values), not just values
                # It does NOT accept nlags as a parameter
                acf_values = None
                try:
                    logger.info(f"Calculating ACF, data_length={len(data_clean)}")
                    acf_result = acf_calc.calculate(data_clean)
                    logger.info(f"ACF calculation result type: {type(acf_result)}")
                    
                    # Handle tuple return: (lags, values)
                    if isinstance(acf_result, tuple) and len(acf_result) == 2:
                        lags, acf_values = acf_result
                        logger.info(f"ACF lags type: {type(lags)}, length: {len(lags) if hasattr(lags, '__len__') else 'N/A'}")
                        logger.info(f"ACF values type: {type(acf_values)}, length: {len(acf_values) if hasattr(acf_values, '__len__') else 'N/A'}")
                    else:
                        # Fallback: assume it's the values directly
                        acf_values = acf_result
                        logger.warning(f"ACF returned unexpected format: {type(acf_result)}")
                except Exception as e:
                    logger.error(f"Error calculating ACF: {type(e).__name__}: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    acf_values = None
                
                # Calculate PACF
                # NOTE: PACFCalculator.calculate() returns a tuple (lags, values), not just values
                # It does NOT accept nlags as a parameter
                pacf_values = None
                try:
                    logger.info(f"Calculating PACF, data_length={len(data_clean)}")
                    pacf_result = pacf_calc.calculate(data_clean)
                    logger.info(f"PACF calculation result type: {type(pacf_result)}")
                    
                    # Handle tuple return: (lags, values)
                    if isinstance(pacf_result, tuple) and len(pacf_result) == 2:
                        lags, pacf_values = pacf_result
                        logger.info(f"PACF lags type: {type(lags)}, length: {len(lags) if hasattr(lags, '__len__') else 'N/A'}")
                        logger.info(f"PACF values type: {type(pacf_values)}, length: {len(pacf_values) if hasattr(pacf_values, '__len__') else 'N/A'}")
                    else:
                        # Fallback: assume it's the values directly
                        pacf_values = pacf_result
                        logger.warning(f"PACF returned unexpected format: {type(pacf_result)}")
                except Exception as e:
                    logger.error(f"Error calculating PACF: {type(e).__name__}: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    pacf_values = None
                
                # Convert to list and validate
                acf_list = []
                if acf_values is not None:
                    if isinstance(acf_values, np.ndarray):
                        acf_list = acf_values.tolist()
                    elif isinstance(acf_values, list):
                        acf_list = acf_values
                    elif hasattr(acf_values, '__iter__'):
                        acf_list = list(acf_values)
                    else:
                        logger.warning(f"ACF values unexpected type: {type(acf_values)}")
                        acf_list = []
                    
                    # Truncate to reasonable length (max 20 lags)
                    if len(acf_list) > 20:
                        acf_list = acf_list[:20]
                
                pacf_list = []
                if pacf_values is not None:
                    if isinstance(pacf_values, np.ndarray):
                        pacf_list = pacf_values.tolist()
                    elif isinstance(pacf_values, list):
                        pacf_list = pacf_values
                    elif hasattr(pacf_values, '__iter__'):
                        pacf_list = list(pacf_values)
                    else:
                        logger.warning(f"PACF values unexpected type: {type(pacf_values)}")
                        pacf_list = []
                    
                    # Truncate to reasonable length (max 20 lags)
                    if len(pacf_list) > 20:
                        pacf_list = pacf_list[:20]
                
                logger.info(f"Final ACF length: {len(acf_list)}, PACF length: {len(pacf_list)}")
                
                return {
                    'acf': acf_list,
                    'pacf': pacf_list,
                    'statistics': stats
                }
                
            except ImportError as e:
                logger.error(f"Failed to import ACF/PACF calculators: {e}")
                return {
                    'acf': [],
                    'pacf': [],
                    'statistics': stats
                }
            
        except Exception as e:
            logger.error(f"Error in exploratory analysis: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Fallback: use cleaned data for statistics
            valid_data = data[~np.isnan(data)] if np.any(np.isnan(data)) else data
            return {
                'acf': [],
                'pacf': [],
                'statistics': {
                    'mean': float(np.mean(valid_data)) if len(valid_data) > 0 else 0.0,
                    'std': float(np.std(valid_data)) if len(valid_data) > 0 else 0.0,
                    'min': float(np.min(valid_data)) if len(valid_data) > 0 else 0.0,
                    'max': float(np.max(valid_data)) if len(valid_data) > 0 else 0.0,
                    'median': float(np.median(valid_data)) if len(valid_data) > 0 else 0.0,
                    'length': len(data),
                    'missing_count': int(np.sum(np.isnan(data))) if np.any(np.isnan(data)) else 0
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
        Calculate basic statistics for time series (handles missing values)
        
        Args:
            data: Time series data (may contain NaN values)
            
        Returns:
            Dictionary with statistics
        """
        # Handle missing values: use only valid data for statistics
        valid_data = data[~np.isnan(data)] if np.any(np.isnan(data)) else data
        
        if len(valid_data) == 0:
            # All values are NaN, return zeros
            return {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'median': 0.0,
                'q25': 0.0,
                'q75': 0.0,
                'length': len(data)
            }
        
        return {
            'mean': float(np.mean(valid_data)),
            'std': float(np.std(valid_data)),
            'min': float(np.min(valid_data)),
            'max': float(np.max(valid_data)),
            'median': float(np.median(valid_data)),
            'q25': float(np.percentile(valid_data, 25)),
            'q75': float(np.percentile(valid_data, 75)),
            'length': len(data)
        }
    
    def fit_parallel_arima(
        self,
        data: np.ndarray,
        verbose: bool = True
    ) -> Any:
        """
        DUMMY: Fit parallel ARIMA model using Spark (COMMENTED OUT - using linear dummy instead)
        
        Args:
            data: Time series data
            verbose: Whether to show verbose output
            
        Returns:
            Dummy workflow object with simple linear results
        """
        # DUMMY MODE: Commented out parallel processing, using simple linear calculations
        # Original parallel code commented below:
        """
        if not PARALLEL_ARIMA_AVAILABLE:
            error_msg = "ParallelARIMAWorkflow no está disponible. Verifica que Spark esté configurado correctamente."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        logger.info("Starting parallel ARIMA model fitting")
        logger.info(f"Data shape: {data.shape if hasattr(data, 'shape') else len(data)}")
        logger.info(f"Data type: {type(data)}")
        logger.info(f"Data sample (first 5): {data[:5] if len(data) >= 5 else data}")
        
        try:
            logger.info("Creating ParallelARIMAWorkflow instance...")
            workflow = ParallelARIMAWorkflow(verbose=verbose)
            logger.info("ParallelARIMAWorkflow instance created successfully")
            
            logger.info("Fitting parallel ARIMA model (this may take a while)...")
            workflow.fit(data)
            logger.info("Parallel ARIMA model fitted successfully")
            
            # Log model order if available
            if hasattr(workflow, 'order_'):
                logger.info(f"Model order: {workflow.order_}")
            
            return workflow
            
        except ImportError as e:
            error_str = str(e)
            logger.error(f"Import error: {error_str}")
            
            # Check for specific missing dependencies
            if "PyArrow" in error_str or "pyarrow" in error_str.lower():
                error_msg = (
                    "PyArrow >= 11.0.0 es requerido para el modelo ARIMA paralelo. "
                    "Instálalo con: pip install 'pyarrow>=11.0.0'"
                )
            elif "pyspark" in error_str.lower():
                error_msg = (
                    "PySpark no está instalado. Instálalo con: pip install pyspark"
                )
            else:
                error_msg = f"Error de importación: {error_str}. Verifica que todas las dependencias estén instaladas."
            
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        except IndexError as e:
            # Handle case where data is too small for parallel workflow
            error_str = str(e)
            if "list index out of range" in error_str:
                logger.warning(f"Dataset too small for parallel workflow: {len(data)} observations")
                error_msg = (
                    f"El modelo ARIMA paralelo requiere más datos. "
                    f"Tienes {len(data)} observaciones, pero se recomiendan al menos 50-100 observaciones. "
                    f"Usa el modelo ARIMA lineal para datasets pequeños."
                )
            else:
                error_msg = f"Error en el procesamiento de datos: {error_str}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            logger.error(f"Error fitting parallel ARIMA model: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise RuntimeError(f"Error al ajustar modelo ARIMA paralelo: {str(e)}")
        """
        
        # DUMMY: Return a simple object that mimics the parallel workflow
        logger.info("DUMMY MODE: Using linear calculations instead of parallel processing")
        
        # Handle missing values by filling with forward fill
        data_clean = data.copy()
        if np.any(np.isnan(data_clean)):
            # Forward fill missing values
            mask = np.isnan(data_clean)
            indices = np.arange(len(data_clean))
            data_clean[mask] = np.interp(indices[mask], indices[~mask], data_clean[~mask])
        
        # Create a dummy workflow object
        class DummyParallelWorkflow:
            def __init__(self, data, order=(1, 1, 1)):
                self.data = data
                self.order_ = order
                self.parameters_ = {'ar': [0.5], 'ma': [0.3], 'diff': 1}
            
            def predict(self, steps=10, return_conf_int=True):
                # Simple linear forecast: use last value + trend
                last_value = self.data[-1] if len(self.data) > 0 else 0
                mean_diff = np.mean(np.diff(self.data[-min(20, len(self.data)):])) if len(self.data) > 1 else 0
                
                forecast = []
                for i in range(steps):
                    forecast.append(last_value + mean_diff * (i + 1))
                
                forecast = np.array(forecast)
                
                if return_conf_int:
                    # Simple confidence intervals
                    std_val = np.std(self.data) if len(self.data) > 0 else 1.0
                    lower = forecast - 1.96 * std_val
                    upper = forecast + 1.96 * std_val
                    return forecast, (lower, upper)
                else:
                    return forecast
        
        # Use simple ARIMA order (1,1,1) for dummy
        dummy_workflow = DummyParallelWorkflow(data_clean, order=(1, 1, 1))
        logger.info(f"DUMMY: Created dummy parallel workflow with order {dummy_workflow.order_}")
        
        return dummy_workflow
    
    def get_parallel_arima_forecast(
        self,
        workflow: Any,
        steps: int = 10,
        return_conf_int: bool = True
    ) -> Dict[str, Any]:
        """
        DUMMY: Generate forecast from parallel ARIMA workflow (using linear calculations)
        
        Args:
            workflow: Fitted ParallelARIMAWorkflow instance (or dummy)
            steps: Number of steps to forecast
            return_conf_int: Whether to return confidence intervals
            
        Returns:
            Dictionary with forecast results
        """
        logger.info(f"DUMMY MODE: Generating parallel ARIMA forecast: steps={steps}, return_conf_int={return_conf_int}")
        try:
            # DUMMY: Use simple linear forecast
            if hasattr(workflow, 'predict'):
                if return_conf_int:
                    logger.info("DUMMY: Calling workflow.predict with confidence intervals...")
                    forecast, conf_int = workflow.predict(steps=steps, return_conf_int=True)
                    logger.info(f"DUMMY: Forecast generated: {len(forecast)} values")
                    logger.info(f"DUMMY: Confidence intervals: lower={len(conf_int[0]) if conf_int else 0}, upper={len(conf_int[1]) if conf_int else 0}")
                    return {
                        'forecast': forecast.tolist() if isinstance(forecast, np.ndarray) else forecast,
                        'lower_bound': conf_int[0].tolist() if isinstance(conf_int[0], np.ndarray) else conf_int[0],
                        'upper_bound': conf_int[1].tolist() if isinstance(conf_int[1], np.ndarray) else conf_int[1],
                        'steps': steps
                    }
                else:
                    logger.info("DUMMY: Calling workflow.predict without confidence intervals...")
                    forecast = workflow.predict(steps=steps, return_conf_int=False)
                    logger.info(f"DUMMY: Forecast generated: {len(forecast)} values")
                    return {
                        'forecast': forecast.tolist() if isinstance(forecast, np.ndarray) else forecast,
                        'lower_bound': None,
                        'upper_bound': None,
                        'steps': steps
                    }
            else:
                # Fallback: simple linear forecast
                logger.warning("DUMMY: Workflow doesn't have predict method, using fallback")
                last_val = workflow.data[-1] if hasattr(workflow, 'data') and len(workflow.data) > 0 else 0
                mean_diff = np.mean(np.diff(workflow.data[-20:])) if hasattr(workflow, 'data') and len(workflow.data) > 1 else 0
                forecast = [last_val + mean_diff * (i + 1) for i in range(steps)]
                
                if return_conf_int:
                    std_val = np.std(workflow.data) if hasattr(workflow, 'data') and len(workflow.data) > 0 else 1.0
                    lower = [f - 1.96 * std_val for f in forecast]
                    upper = [f + 1.96 * std_val for f in forecast]
                    return {
                        'forecast': forecast,
                        'lower_bound': lower,
                        'upper_bound': upper,
                        'steps': steps
                    }
                else:
                    return {
                        'forecast': forecast,
                        'lower_bound': None,
                        'upper_bound': None,
                        'steps': steps
                    }
        except Exception as e:
            logger.error(f"DUMMY: Error generating parallel forecast: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"DUMMY: Traceback: {traceback.format_exc()}")
            raise RuntimeError(f"Error al generar forecast paralelo (dummy): {str(e)}")
    
    def get_parallel_arima_metrics(self, workflow: Any) -> Dict[str, Any]:
        """
        DUMMY: Extract metrics from parallel ARIMA workflow (using simple linear calculations)
        
        Args:
            workflow: Fitted ParallelARIMAWorkflow instance (or dummy)
            
        Returns:
            Dictionary with model metrics and results
        """
        try:
            metrics = {}
            
            # DUMMY: Get order from dummy workflow
            if hasattr(workflow, 'order_'):
                order = workflow.order_
                if isinstance(order, tuple):
                    metrics['order'] = f"ARIMA{order}"
                else:
                    metrics['order'] = f"ARIMA({order})"
            else:
                metrics['order'] = "ARIMA(1,1,1)"  # Default dummy order
            
            # DUMMY: Get parameters if available
            if hasattr(workflow, 'parameters_'):
                metrics['parameters'] = workflow.parameters_
            
            # DUMMY: Calculate simple linear metrics
            if hasattr(workflow, 'data') and len(workflow.data) > 0:
                data = workflow.data
                # Simple dummy metrics based on data
                mean_val = np.mean(data)
                std_val = np.std(data)
                metrics['mae'] = std_val * 0.1  # Dummy MAE
                metrics['rmse'] = std_val * 0.15  # Dummy RMSE
                metrics['mape'] = (std_val / abs(mean_val)) * 100 if mean_val != 0 else 5.0  # Dummy MAPE
            else:
                metrics['mae'] = 0.5
                metrics['rmse'] = 0.75
                metrics['mape'] = 5.0
            
            # DUMMY: Original code commented out
            """
            # Get results summary
            if hasattr(workflow, 'get_results'):
                results = workflow.get_results()
                
                # Extract validation metrics
                if 'step_results' in results:
                    validation = results['step_results'].get('step7_8_validation', {})
                    if 'metrics' in validation:
                        metrics['mae'] = validation['metrics'].get('avg_mae')
                        metrics['rmse'] = validation['metrics'].get('avg_rmse')
                        metrics['mape'] = validation['metrics'].get('avg_mape')
                
                # Extract diagnostics
                diagnostics = results['step_results'].get('step9_diagnostics', {})
                if 'pass_rates' in diagnostics:
                    metrics['diagnostics_pass_rate'] = diagnostics['pass_rates'].get('overall')
            
            # Get summary text
            if hasattr(workflow, 'summary'):
                metrics['summary'] = workflow.summary()
            """
            
            return metrics
            
        except Exception as e:
            print(f"DUMMY: Error extracting parallel ARIMA metrics: {e}")
            # Return default dummy metrics on error
            return {
                'order': 'ARIMA(1,1,1)',
                'mae': 0.5,
                'rmse': 0.75,
                'mape': 5.0
            }

