import os
import json
import plotly.express as px
import pandas as pd

electrical_data = "G:/Electricity-MQTT-Monitor/monitor/electrical-data"

for archivo in os.listdir(electrical_data):
    if archivo.endswith("current.json"):
        file = os.path.join(electrical_data, archivo)
        
        # Leer los datos JSON (opcional)
        with open(file, "r", encoding="utf-8") as f:
            current = json.load(f)
        
        current = current[-30:]
        date = [current[i]['date'] for i in range(len(current))]
        values = [current[i]['rms_current'] for i in range(len(current))]
        df = pd.DataFrame({'Timestamp': pd.to_datetime(date), 'Value': values})

        fig = px.line(
            df,
            x='Timestamp',
            y='Value',
            title='Last Hour: Current',
            labels={'Timestamp': 'Fecha y Hora', 'Value': 'rms_current'},
            line_shape='spline',
            template='plotly_white'
        )

        fig.update_traces(line=dict(width=5), marker=dict(size=12))

        fig.update_layout(
            title_font=dict(size=30),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Fecha y Hora',
                    font=dict(size=24, color='black')
                )
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Valor',
                    font=dict(size=24, color='black')
                )
            )
        )
        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\current.png"
        fig.write_image(output_path, format='png', width=1200, height=800)

    if archivo.endswith("potency.json"):
        file = os.path.join(electrical_data, archivo)
        
        with open(file, "r", encoding="utf-8") as f:
            potency = json.load(f)
        
        potency = potency[-30:]
        date = [potency[i]['date'] for i in range(len(potency))]
        values = [potency[i]['total-active-power'] for i in range(len(potency))]
        df = pd.DataFrame({'Timestamp': pd.to_datetime(date), 'Value': values})

        fig = px.line(
            df,
            x='Timestamp',
            y='Value',
            title='Last Hour: Power',
            labels={'Timestamp': 'Fecha y Hora', 'Value': 'Active Power'},
            line_shape='spline',
            template='plotly_white'
        )

        fig.update_traces(line=dict(width=5), marker=dict(size=12))

        fig.update_layout(
            title_font=dict(size=30),
            xaxis=dict(
                showgrid=False,  # Ocultar cuadrícula
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Fecha y Hora',
                    font=dict(size=24, color='black')
                )
            ),
            yaxis=dict(
                showgrid=False,  # Ocultar cuadrícula
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Valor',
                    font=dict(size=24, color='black')
                )
            )
        )

        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\power.png"
        fig.write_image(output_path, format='png', width=1200, height=800)

    if archivo.endswith("voltage.json"):
        file = os.path.join(electrical_data, archivo)
        
        # Leer los datos JSON (opcional)
        with open(file, "r", encoding="utf-8") as f:
            voltage = json.load(f)
        
        voltage = voltage[-30:]
        date = [voltage[i]['date'] for i in range(len(voltage))]
        values = [voltage[i]['instant_energy'] for i in range(len(voltage))]
        # Crear un DataFrame
        df = pd.DataFrame({'Timestamp': pd.to_datetime(date), 'Value': values})

        # Crear nuevamente el gráfico con formato claro
        fig = px.line(
            df,
            x='Timestamp',
            y='Value',
            title='Last Hour: Voltage',
            labels={'Timestamp': 'Fecha y Hora', 'Value': 'Instant Energy'},
            line_shape='spline',
            template='plotly_white'
        )

        fig.update_traces(line=dict(width=5), marker=dict(size=12))

        fig.update_layout(
            title_font=dict(size=30),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Fecha y Hora',
                    font=dict(size=24, color='black')
                )
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=20, color='black'),
                title=dict(
                    text='Valor',
                    font=dict(size=24, color='black')
                )
            )
        )

        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\voltage.png"
        fig.write_image(output_path, format='png', width=1200, height=800)