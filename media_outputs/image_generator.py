import os
import json
import plotly.express as px
import pandas as pd

electrical_data = "G:/Electricity-MQTT-Monitor/monitor/electrical-data"



for archivo in os.listdir(electrical_data):
    if archivo.endswith("energy.json"):
        file = os.path.join(electrical_data, archivo)
        
        # Leer los datos JSON (opcional)
        with open(file, "r", encoding="utf-8") as f:
            energy = json.load(f)
        
        energy = energy[-60:]
        date = [energy[i]['date'] for i in range(len(energy))]
        values = [energy[i]['energy_consumed'] for i in range(len(energy))]
        df = pd.DataFrame({'Timestamp': pd.to_datetime(date), 'Value': values})
        
        group_size = 5

        timestamps = []
        results = []
        
        for i in range(0, len(df), group_size):
            group = df[i:i + group_size]
            if len(group) == group_size:
                first = group['energy_consumed'].iloc[0]
                last = group['energy_consumed'].iloc[-1]
                diff = last - first
                results.append(diff)
                timestamps.append(group['date'].iloc[0])

        result_df = pd.DataFrame({'Timestamp': timestamps, 'diff': results})

        fig = px.line(
            result_df,
            x='Timestamp',
            y='diff',
            title='Last Hour: Energy',
            labels={'Timestamp': 'Fecha y Hora', 'diff': 'Consumed Energy'},
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
        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\energy.png"
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