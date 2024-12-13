import os
import json
import plotly.express as px
import pandas as pd

electrical_data = r"G:\Electricity-MQTT-Monitor\monitor\electrical-data"

for archivo in os.listdir(electrical_data):
    
    if archivo.endswith("energy.json"):
        file = os.path.join(electrical_data, archivo)
        
        with open(file, "r", encoding="utf-8") as f:
            energy = json.load(f)
        
        energy = energy[-480:]
        date = [energy[i]['date'] for i in range(len(energy))]
        values = [energy[i]['energy_consumed'] for i in range(len(energy))]
        df = pd.DataFrame({'Timestamp': pd.to_datetime(date), 'Value': values})
        
        group_size = 5

        timestamps = []
        results = []
        
        for i in range(0, len(df), group_size):
            group = df[i:i + group_size]
            if len(group) == group_size:
                first = group['Value'].iloc[0]
                last = group['Value'].iloc[-1]
                diff = last - first
                results.append(diff)
                timestamps.append(group['Timestamp'].iloc[0])

        result_df = pd.DataFrame({'Timestamp': timestamps, 'diff': results})

        fig = px.line(
            result_df,
            x='Timestamp',
            y='diff',
            labels={'diff': 'Consumed Energy'},
            line_shape='spline',
            template='plotly_white'
        )

        fig.update_traces(line=dict(width=5), marker=dict(size=12))

        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=32, color='black'),
                title=None  # Remove x-axis title
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=32, color='black'),
                title=dict(
                    text='Consumed Energy (KW-H)',
                    font=dict(size=32, color='black')
                )
            )
        )
        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\energy.png"
        fig.write_image(output_path, format='png', width=2350, height=900)

# ------------------------------------------------------------------------------- 


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
            labels={'Value': 'Active Power'},
            line_shape='spline',
            template='plotly_white'
        )

        fig.update_traces(line=dict(width=5), marker=dict(size=12))

        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=26, color='black'),
                title=None
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=26, color='black'),
                title=dict(
                    text='Active Power',
                    font=dict(size=26, color='black')
                )
            )
        )

        output_path = r"G:\Electricity-MQTT-Monitor\media_outputs\images\power.png"
        fig.write_image(output_path, format='png', width=1500, height=1000)



    if archivo.endswith("current.json"):
        file = os.path.join(electrical_data, archivo)
        
        with open(file, "r", encoding="utf-8") as f:
            current = json.load(f)
        
        current = current[-60:]
        date = [current[i]['date'] for i in range(len(current))]

        current_names = ['Ia', 'Ib', 'Ic']

        combined_data = []
        for name in current_names:
            combined_data.extend([{'Timestamp': pd.to_datetime(date[i]), 'Value': current[i][name], 'Current': name} for i in range(len(current))])
        
        df_combined = pd.DataFrame(combined_data)

        fig_combined = px.line(
            df_combined,
            x='Timestamp',
            y='Value',
            color='Current',
            labels={'Value': 'Current (A)'},
            line_shape='spline',
            template='plotly_white'
        )

        fig_combined.update_traces(line=dict(width=5), marker=dict(size=12))
        fig_combined.update_layout(
            xaxis=dict(
                showgrid=True,
                tickfont=dict(size=26, color='black'),
                title=None
            ),
            yaxis=dict(
                showgrid=True,
                tickfont=dict(size=26, color='black'),
                title=dict(
                    text='Current (A)',
                    font=dict(size=26, color='black')
                )
            ),
            legend=dict(
            font=dict(size=24),
            title=dict(font=dict(size=26)),
            )
        )
        output_path_combined = r"G:\Electricity-MQTT-Monitor\media_outputs\images\current.png"
        fig_combined.write_image(output_path_combined, format='png', width=1500, height=1000)





    if archivo.endswith("voltage.json"):
        file = os.path.join(electrical_data, archivo)
        
        with open(file, "r", encoding="utf-8") as f:
            voltage = json.load(f)
        
        voltage = voltage[-30:]
        date = [voltage[i]['date'] for i in range(len(voltage))]

        grouped_voltage_names = ['Va', 'Vb', 'Vc']
        separate_voltage_names = ['Va_b', 'Vb_c', 'Vc_a']

        combined_data = []
        for name in grouped_voltage_names:
            combined_data.extend([{'Timestamp': pd.to_datetime(date[i]), 'Value': voltage[i][name], 'Phase': name} for i in range(len(voltage))])
        
        df_combined = pd.DataFrame(combined_data)

        fig_combined = px.line(
            df_combined,
            x='Timestamp',
            y='Value',
            color='Phase',
            labels={'Value': 'Voltage (V)', 'Phase': 'Fase'},
            line_shape='spline',
            template='plotly_white'
        )

        fig_combined.update_traces(line=dict(width=5), marker=dict(size=12))
        fig_combined.update_layout(
            xaxis=dict(
                showgrid=True,
                tickfont=dict(size=26, color='black'),
                title=None
            ),
            yaxis=dict(
                showgrid=True,
                tickfont=dict(size=26, color='black'),
                title=dict(
                    text='Voltage (V)',
                    font=dict(size=26, color='black')
                )
            ),
            legend=dict(
            font=dict(size=24),
            title=dict(font=dict(size=26)),
            )
        )
        output_path_combined = r"G:\Electricity-MQTT-Monitor\media_outputs\images\voltage_1.png"
        fig_combined.write_image(output_path_combined, format='png', width=1500, height=1000)

        combined_diff_data = []
        for name in separate_voltage_names:
            combined_diff_data.extend([{'Timestamp': pd.to_datetime(date[i]), 'Value': voltage[i][name], 'Phase': name} for i in range(len(voltage))])
        
        df_combined_diff = pd.DataFrame(combined_diff_data)

        fig_combined_diff = px.line(
            df_combined_diff,
            x='Timestamp',
            y='Value',
            color='Phase',
            labels={'Value': 'Voltage Difference (V)', 'Phase': 'Fase'},
            line_shape='spline',
            template='plotly_white'
        )

        fig_combined_diff.update_traces(line=dict(width=5), marker=dict(size=12))
        fig_combined_diff.update_layout(
            xaxis=dict(
            showgrid=True,
            tickfont=dict(size=26, color='black'),
            title=None
            ),
            yaxis=dict(
            showgrid=True,
            tickfont=dict(size=26, color='black'),
            title=dict(
                text='Voltage Difference (V)',
                font=dict(size=26, color='black')
            )
            ),
            legend=dict(
            font=dict(size=20),
            title=dict(font=dict(size=26)),
            )
        )
        output_path_combined_diff = r"G:\Electricity-MQTT-Monitor\media_outputs\images\voltage_2.png"
        fig_combined_diff.write_image(output_path_combined_diff, format='png', width=1500, height=1000)