"""
TSLib Shiny App - Main Application
Event-driven architecture for time series analysis
"""

from shiny import App, reactive, render, ui
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from pathlib import Path

# Import UI components
from ui.layouts import create_app_ui
from ui.components import loading_spinner, success_message, error_message

# Mock data for demonstration
MOCK_DATA = {
    'airline': pd.DataFrame({
        'date': pd.date_range('1949-01', periods=144, freq='ME'),
        'passengers': [112, 118, 132, 129, 121, 135, 148, 148, 136, 119, 104, 118,
                       115, 126, 141, 135, 125, 149, 170, 170, 158, 133, 114, 140,
                       145, 150, 178, 163, 172, 178, 199, 199, 184, 162, 146, 166,
                       171, 180, 193, 181, 183, 218, 230, 242, 209, 191, 172, 194,
                       196, 196, 236, 235, 229, 243, 264, 272, 237, 211, 180, 201,
                       204, 188, 235, 227, 234, 264, 302, 293, 259, 229, 203, 229,
                       242, 233, 267, 269, 270, 315, 364, 347, 312, 274, 237, 278,
                       284, 277, 317, 313, 318, 374, 413, 405, 355, 306, 271, 306,
                       315, 301, 356, 348, 355, 422, 465, 467, 404, 347, 305, 336,
                       340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337,
                       360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405,
                       417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432]
    }),
    'temperature': pd.DataFrame({
        'date': pd.date_range('2023-01-01', periods=90, freq='D'),
        'temperature': np.random.normal(20, 5, 90) + np.sin(np.arange(90) * 2 * np.pi / 365) * 10
    }),
    'sales': pd.DataFrame({
        'date': pd.date_range('2022-01', periods=36, freq='ME'),
        'sales': np.cumsum(np.random.normal(10000, 5000, 36)) + 100000
    })
}

# Reactive state
current_data = reactive.Value(None)
current_step = reactive.Value(1)
model_fitted = reactive.Value(False)
forecast_data = reactive.Value(None)

# App UI
app_ui = create_app_ui()

def server(input, output, session):
    """Server logic with event handlers"""
    
    # ============================================================================
    # EVENT HANDLERS - Data Loading
    # ============================================================================
    
    @reactive.event(input.upload_btn)
    def on_upload_file():
        """Handle file upload event"""
        print("📤 Upload button clicked")
        # TODO: Process uploaded file
        # For now, load mock data
        current_data.set(MOCK_DATA['airline'])
        current_step.set(2)
        ui.notification_show("✅ Datos cargados exitosamente", type="success")
    
    @reactive.event(input.load_airline)
    def on_load_airline():
        """Load airline passengers example data"""
        print("✈️ Loading airline data")
        current_data.set(MOCK_DATA['airline'])
        current_step.set(2)
        ui.notification_show("✅ Datos de pasajeros aéreos cargados", type="success")
    
    @reactive.event(input.load_temperature)
    def on_load_temperature():
        """Load temperature example data"""
        print("🌡️ Loading temperature data")
        current_data.set(MOCK_DATA['temperature'])
        current_step.set(2)
        ui.notification_show("✅ Datos de temperatura cargados", type="success")
    
    @reactive.event(input.load_sales)
    def on_load_sales():
        """Load sales example data"""
        print("💰 Loading sales data")
        current_data.set(MOCK_DATA['sales'])
        current_step.set(2)
        ui.notification_show("✅ Datos de ventas cargados", type="success")
    
    # ============================================================================
    # EVENT HANDLERS - Model Configuration
    # ============================================================================
    
    @reactive.event(input.model_mode)
    def on_model_mode_change():
        """Handle model mode change (auto/manual)"""
        print(f"⚙️ Model mode changed to: {input.model_mode()}")
        # TODO: Show/hide manual parameters based on mode
    
    @reactive.event(input.param_p, input.param_d, input.param_q)
    def on_parameter_change():
        """Handle parameter changes"""
        if input.model_mode() == "manual":
            print(f"🔧 Parameters changed: p={input.param_p()}, d={input.param_d()}, q={input.param_q()}")
    
    @reactive.event(input.n_jobs)
    def on_n_jobs_change():
        """Handle n_jobs change"""
        print(f"⚡ n_jobs changed to: {input.n_jobs()}")
    
    # ============================================================================
    # EVENT HANDLERS - Model Fitting
    # ============================================================================
    
    @reactive.event(input.fit_model_btn)
    def on_fit_model():
        """Handle model fitting event"""
        print("🚀 Fitting model...")
        ui.notification_show("🔄 Ajustando modelo ARIMA...", type="message")
        
        # TODO: Actually fit ARIMA model with TSLib
        # For now, simulate fitting
        import time
        time.sleep(2)  # Simulate processing time
        
        model_fitted.set(True)
        current_step.set(4)
        ui.notification_show("✅ Modelo ajustado exitosamente", type="success")
    
    # ============================================================================
    # EVENT HANDLERS - Forecasting
    # ============================================================================
    
    @reactive.event(input.forecast_steps)
    def on_forecast_steps_change():
        """Handle forecast steps change"""
        print(f"🔮 Forecast steps changed to: {input.forecast_steps()}")
        # TODO: Regenerate forecast with new steps
    
    @reactive.event(input.download_forecast)
    def on_download_forecast():
        """Handle forecast download"""
        print("💾 Downloading forecast...")
        ui.notification_show("📥 Descargando predicciones...", type="message")
        # TODO: Generate and download CSV
    
    # ============================================================================
    # EVENT HANDLERS - Navigation
    # ============================================================================
    
    @reactive.event(input.next_step)
    def on_next_step():
        """Navigate to next step"""
        current_step.set(min(current_step() + 1, 6))
        print(f"➡️ Moving to step {current_step()}")
    
    @reactive.event(input.prev_step)
    def on_prev_step():
        """Navigate to previous step"""
        current_step.set(max(current_step() - 1, 1))
        print(f"⬅️ Moving to step {current_step()}")
    
    # ============================================================================
    # OUTPUT RENDERERS - Data Display
    # ============================================================================
    
    @render.data_frame
    def data_preview():
        """Render data preview table"""
        data = current_data()
        if data is not None:
            return data.head(10)
        return pd.DataFrame({"Mensaje": ["No hay datos cargados"]})
    
    @render.plot
    def time_series_plot():
        """Render time series plot"""
        data = current_data()
        if data is not None:
            fig = px.line(
                data, 
                x='date', 
                y=data.columns[1],  # Second column is the value
                title="Serie Temporal",
                labels={'date': 'Fecha', data.columns[1]: 'Valor'}
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12)
            )
            return fig
        
        # Return empty plot if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return fig
    
    @render.data_frame
    def model_params_table():
        """Render model parameters table"""
        if model_fitted():
            # Mock parameters
            params_data = pd.DataFrame({
                'Parámetro': ['AR(1)', 'MA(1)', 'Constante'],
                'Valor': [0.8234, -0.4567, 2.3456],
                'Error Estándar': [0.1234, 0.0987, 0.2345],
                't-valor': [6.67, -4.63, 10.01],
                'p-valor': [0.000, 0.000, 0.000]
            })
            return params_data
        return pd.DataFrame({"Mensaje": ["Modelo no ajustado"]})
    
    # ============================================================================
    # OUTPUT RENDERERS - Diagnostic Plots
    # ============================================================================
    
    @render.plot
    def residuals_plot():
        """Render residuals vs time plot"""
        if model_fitted():
            # Mock residuals
            residuals = np.random.normal(0, 1, 100)
            fig = px.line(
                x=range(len(residuals)),
                y=residuals,
                title="Residuos vs Tiempo"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Tiempo",
                yaxis_title="Residuos"
            )
            return fig
        
        return create_empty_plot("Modelo no ajustado")
    
    @render.plot
    def acf_plot():
        """Render ACF plot"""
        if model_fitted():
            # Mock ACF
            lags = range(1, 21)
            acf_values = [0.8, 0.6, 0.4, 0.2, 0.1] + [0.05] * 15
            fig = px.bar(
                x=lags,
                y=acf_values,
                title="ACF de Residuos"
            )
            fig.add_hline(y=0.2, line_dash="dash", line_color="red")
            fig.add_hline(y=-0.2, line_dash="dash", line_color="red")
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Lag",
                yaxis_title="ACF"
            )
            return fig
        
        return create_empty_plot("Modelo no ajustado")
    
    @render.plot
    def qq_plot():
        """Render Q-Q plot"""
        if model_fitted():
            # Mock Q-Q plot
            residuals = np.random.normal(0, 1, 100)
            fig = px.scatter(
                x=np.sort(residuals),
                y=np.sort(np.random.normal(0, 1, 100)),
                title="Q-Q Plot"
            )
            fig.add_trace(go.Scatter(
                x=[-3, 3],
                y=[-3, 3],
                mode='lines',
                name='Línea de referencia',
                line=dict(dash='dash', color='red')
            ))
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Cuantiles Teóricos",
                yaxis_title="Cuantiles Muestrales"
            )
            return fig
        
        return create_empty_plot("Modelo no ajustado")
    
    @render.plot
    def histogram_plot():
        """Render residuals histogram"""
        if model_fitted():
            # Mock histogram
            residuals = np.random.normal(0, 1, 100)
            fig = px.histogram(
                x=residuals,
                title="Histograma de Residuos",
                nbins=20
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Residuos",
                yaxis_title="Frecuencia"
            )
            return fig
        
        return create_empty_plot("Modelo no ajustado")
    
    # ============================================================================
    # OUTPUT RENDERERS - Forecasting
    # ============================================================================
    
    @render.plot
    def forecast_plot():
        """Render forecast plot"""
        if model_fitted():
            data = current_data()
            if data is not None:
                # Mock forecast
                last_date = data['date'].iloc[-1]
                forecast_dates = pd.date_range(
                    last_date + pd.Timedelta(days=1),
                    periods=input.forecast_steps(),
                    freq='M' if 'M' in str(data['date'].dtype) else 'D'
                )
                
                # Mock forecast values
                last_value = data.iloc[-1, 1]
                forecast_values = [last_value + i * 10 + np.random.normal(0, 5) for i in range(input.forecast_steps())]
                upper_bound = [val + 20 for val in forecast_values]
                lower_bound = [val - 20 for val in forecast_values]
                
                fig = go.Figure()
                
                # Historical data
                fig.add_trace(go.Scatter(
                    x=data['date'],
                    y=data.iloc[:, 1],
                    mode='lines',
                    name='Datos Históricos',
                    line=dict(color='blue')
                ))
                
                # Forecast
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_values,
                    mode='lines',
                    name='Predicción',
                    line=dict(color='red', dash='dash')
                ))
                
                # Confidence interval
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=upper_bound,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=lower_bound,
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.2)',
                    name='Intervalo de Confianza 95%'
                ))
                
                fig.update_layout(
                    title="Predicción con Intervalos de Confianza",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title="Fecha",
                    yaxis_title="Valor"
                )
                
                return fig
        
        return create_empty_plot("Modelo no ajustado")
    
    @render.data_frame
    def forecast_table():
        """Render forecast table"""
        if model_fitted():
            # Mock forecast table
            steps = input.forecast_steps()
            forecast_data = pd.DataFrame({
                'Período': range(1, steps + 1),
                'Predicción': [100 + i * 5 + np.random.normal(0, 2) for i in range(steps)],
                'Límite Inferior': [95 + i * 5 for i in range(steps)],
                'Límite Superior': [105 + i * 5 for i in range(steps)]
            })
            return forecast_data
        return pd.DataFrame({"Mensaje": ["Modelo no ajustado"]})


def create_empty_plot(message="No hay datos"):
    """Create empty plot with message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig


# Create and run the app
app = App(app_ui, server)

if __name__ == "__main__":
    print("🚀 Starting TSLib Shiny App...")
    print("📊 Open your browser to: http://localhost:8000")
    app.run(host="0.0.0.0", port=8000)
