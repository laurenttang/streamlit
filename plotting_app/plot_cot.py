import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import json
from datetime import datetime

# Load your group data from JSON files
def get_data(category):
    with open(f'{category}.json', 'r') as json_file:
        data = json.load(json_file)
    return data

group_value = ['ai', 'fin', 'semi_manu', 'ic_package', 'ic_design', 'ip', 'equipment', 'pcb', 'unit', 'ems', 'ems-unit', 'hi', 'sea_fli', 'bio', 'motor', 'plastic', 'house', 'inner']
group_value2 =['ai - 2382', 'ai - 6669', 'ai - 3231', 'ai - 2357', 'ai - 2353', 'ai - 2301',
                'fin - 2880', 'fin - 2881', 'fin - 2882', 'fin - 2883', 'fin - 2884', 'fin - 2885', 'fin - 2886', 'fin - 2887', 'fin - 2888', 'fin - 2890', 'fin - 2891', 'fin - 2892', 'fin - 5880', 'fin - 2801', 'fin - 2834', 'fin - 5871',
                'semi_manu - 2303', 'semi_manu - 2330', 'semi_manu - 3105', 'semi_manu - 5347', 'semi_manu - 6770', 'semi_manu - 8086', 'semi_manu - 2344', 'semi_manu - 6182', 'semi_manu - 6488',
                'ic_package - 2338', 'ic_package - 2441', 'ic_package - 2449', 'ic_package - 3264', 'ic_package - 3374', 'ic_package - 3711', 'ic_package - 6147', 'ic_package - 6239', 'ic_package - 6257', 'ic_package - 6271', 'ic_package - 6510', 'ic_package - 8150',
                'ic_design - 2379', 'ic_design - 2388', 'ic_design - 2401', 'ic_design - 2454', 'ic_design - 2458', 'ic_design - 3006', 'ic_design - 3034', 'ic_design - 3035', 'ic_design - 3227', 'ic_design - 3443', 'ic_design - 3529', 'ic_design - 4919', 'ic_design - 5269', 'ic_design - 5274', 'ic_design - 6462', 'ic_design - 8299',
                'ip - 3529', 'ip - 3661', 'ip - 3443', 'ip - 6643', 'ip - 3035',
                'equipment - 3131', 'equipment - 3583', 'equipment - 2059', 'equipment - 3693',
                'pcb - 2383', 'pcb - 6213', 'pcb - 6274', 'pcb - 8358', 'pcb - 2313', 'pcb - 2355', 'pcb - 2368', 'pcb - 3037', 'pcb - 3044', 'pcb - 3189', 'pcb - 4958', 'pcb - 6153', 'pcb - 6269', 'pcb - 6278', 'pcb - 8039', 'pcb - 8046',
                'unit - 2327', 'unit - 2492', 'unit - 3042', 'unit - 3152', 'unit - 6173', 'unit - 2328', 'unit - 2392', 'unit - 3533', 'unit - 5457',
                'ems - 2324', 'ems - 2353', 'ems - 2356', 'ems - 2357', 'ems - 2382', 'ems - 3231', 'ems - 2301', 'ems - 2308', 'ems - 2317', 'ems - 2352', 'ems - 3706', 'ems - 4938', 'ems - 6669',
                'ems-unit - 2439', 'ems-unit - 3017', 'ems-unit - 3211', 'ems-unit - 3324', 'ems-unit - 3376', 'ems-unit - 3653', 'ems-unit - 3653', 'ems-unit - 6121', 'ems-unit - 2331', 'ems-unit - 2376', 'ems-unit - 2377',
                'hi - 5274', 'hi - 3008', 'hi - 3661', 'hi - 3529', 'hi - 6669', 'hi - 6409', 'hi - 3443',
                'sea_fli - 2603', 'sea_fli - 2605', 'sea_fli - 2606', 'sea_fli - 2609', 'sea_fli - 2610', 'sea_fli - 2615', 'sea_fli - 2618', 'sea_fli - 2633', 'sea_fli - 2634',
                'bio - 1565', 'bio - 1565', 'bio - 1707', 'bio - 4123', 'bio - 4128', 'bio - 4162', 'bio - 4736', 'bio - 4743', 'bio - 6547', 'bio - 8436',
                'motor - 2201', 'motor - 1319', 'motor - 1536', 'motor - 2231', 'motor - 3552', 'motor - 6279',
                'plastic - 1301', 'plastic - 1303', 'plastic - 1312', 'plastic - 1314', 'plastic - 1326', 'plastic - 1718',
                'house - 2002', 'house - 2006', 'house - 2014', 'house - 2027', 'house - 5009', 'house - 9958', 'house - 2515', 'house - 2520', 'house - 2542', 'house - 2548', 'house - 5534',
                'inner - 2915', 'inner - 5904', 'inner - 8454', 'inner - 1210', 'inner - 1216', 'inner - 1476', 'inner - 1477', 'inner - 2347', 'inner - 2412', 'inner - 3045', 'inner - 4904', 'inner - 2489']

# Main Streamlit app
def main():
    st.title("Data Visualization")
    
    mode_selector = st.radio("Select Mode", ['Group', 'Individual'])
    year_selection = st.radio("Select Year", ['High Point', 'Low Point'])
    if mode_selector == 'Group':
        category_selection = st.selectbox("Select Category", group_value)
        data = get_data(category_selection)
    else:
        category_selection = st.selectbox("Select Category", group_value2)
        code = category_selection.split('-')[0].strip() if '-' in category_selection else None
        data = get_data(code)
    
    
    # data = get_data(category_selection)
    fig_data =  go.Figure()
    # print(data)

    if mode_selector == 'Group':
        # Process data for group mode
        if year_selection == 'High Point':
                    
            for code in data["Gh"]:
                close_data = data["Gh"][code]["Close"][::-1]
                cot_data = (data["G2h"]["Fdollar"], data["G2h"]["Idollar"])
                x_axis = data["G2h"]["Date"]
                x_axis = [str(date) for date in x_axis]
                x_axis_datetime = [datetime.strptime(date, "%Y%m%d") for date in x_axis]

                line_trace = go.Scatter(x=x_axis_datetime, y=close_data, mode='lines', name=f'Close Data - {code}', yaxis='y1')
                fig_data.add_trace(line_trace)

            # Create bar traces after iterating through the loop to ensure all line traces are added first
            bar_trace1 = go.Bar(x=x_axis_datetime, y=cot_data[0], name='Fdollar', yaxis='y2')
            bar_trace2 = go.Bar(x=x_axis_datetime, y=cot_data[1], name='Idollar', yaxis='y2')
            bar_data = [bar_trace1, bar_trace2]
            fig_data.add_traces(bar_data)

            # Define layout with dual y-axes
            fig_data.update_layout(
                yaxis=dict(title='Close Data', showgrid=False),
                yaxis2=dict(title='COT Data', showgrid=False, overlaying='y', side='right'),
                legend=dict(
                    orientation="h",  # horizontal orientation for the legend
                    y=-0.2,  # adjust the position of the legend outside the figure
                    x=0.5,   # adjust the position of the legend horizontally
                    xanchor='center'  # anchor the legend to the center horizontally
                    )
                    )   

            # Display the plot using Streamlit
            st.plotly_chart(fig_data)

        elif year_selection == 'Low Point':
        
                # Process data for low point
            for code in data["Gl"]:
                close_data = data["Gl"][code]["Close"][::-1]
                cot_data = data["G2l"]["Fdollar"], data["G2l"]["Idollar"]
                x_axis = data["G2l"]["Date"]
                x_axis = [str(date) for date in x_axis]
                x_axis_datetime = [datetime.strptime(date, "%Y%m%d") for date in x_axis]

                line_trace = go.Scatter(x=x_axis_datetime, y=close_data, mode='lines', name=f'Close Data - {code}', yaxis='y1')
                fig_data.add_trace(line_trace)

            # Create bar traces after iterating through the loop to ensure all line traces are added first
            bar_trace1 = go.Bar(x=x_axis_datetime, y=cot_data[0], name='Fdollar', yaxis='y2')
            bar_trace2 = go.Bar(x=x_axis_datetime, y=cot_data[1], name='Idollar', yaxis='y2')
            bar_data = [bar_trace1, bar_trace2]
            fig_data.add_traces(bar_data)

            # Define layout with dual y-axes
            fig_data.update_layout(
                yaxis=dict(title='Close Data', showgrid=False),
                yaxis2=dict(title='COT Data', showgrid=False, overlaying='y', side='right'),
                legend=dict(
                    orientation="h",  # horizontal orientation for the legend
                    y=-0.2,  # adjust the position of the legend outside the figure
                    x=0.5,   # adjust the position of the legend horizontally
                    xanchor='center'  # anchor the legend to the center horizontally
                    )
                    )   

            # Display the plot using Streamlit
            st.plotly_chart(fig_data)

    elif mode_selector == 'Individual':
        # Process data for individual mode
        code = category_selection.split('-')[1].strip() if '-' in category_selection else None
        print(code)
        if code:
            if year_selection == 'High Point':
                close_data = data["Gh"][code]["Close"]
                print(close_data)
                cot_data = data["G2h_2"][code]["Fdollar"][::-1], data["G2h_2"][code]["Idollar"][::-1]
                x_axis = data["Gh"][code]["Date"]
                x_axis = [str(date) for date in x_axis]
                x_axis_datetime = [datetime.strptime(date, "%Y%m%d") for date in x_axis]
                line_trace = go.Scatter(x=x_axis_datetime, y=close_data, mode='lines', name=f'Close Data - {code}', yaxis='y1')
                fig_data.add_trace(line_trace)

                bar_trace1 = go.Bar(x=x_axis_datetime, y=cot_data[0], name='Fdollar', yaxis='y2')
                bar_trace2 = go.Bar(x=x_axis_datetime, y=cot_data[1], name='Idollar', yaxis='y2')
                bar_data = [bar_trace1, bar_trace2]
                fig_data.add_traces(bar_data)
                fig_data.update_layout(
                    yaxis=dict(title='Close Data', showgrid=True),
                    yaxis2=dict(title='COT Data', showgrid=False, overlaying='y', side='right'),
                    legend=dict(
                        orientation="h",  # horizontal orientation for the legend
                        y=-0.2,  # adjust the position of the legend outside the figure
                        x=0.5,   # adjust the position of the legend horizontally
                        xanchor='center'  # anchor the legend to the center horizontally
                        )
                        )
                # Display the plot using Streamlit
                st.plotly_chart(fig_data)

            elif year_selection == 'Low Point':
                close_data = data["Gl"][code]["Close"]
                cot_data = data["G2l_2"][code]["Fdollar"][::-1], data["G2l_2"][code]["Idollar"][::-1]
                x_axis = data["Gl"][code]["Date"]
                x_axis = [str(date) for date in x_axis]
                x_axis_datetime = [datetime.strptime(date, "%Y%m%d") for date in x_axis]
                line_trace = go.Scatter(x=x_axis_datetime, y=close_data, mode='lines', name=f'Close Data - {code}', yaxis='y1')
                fig_data.add_trace(line_trace)

                bar_trace1 = go.Bar(x=x_axis_datetime, y=cot_data[0], name='Fdollar', yaxis='y2')
                bar_trace2 = go.Bar(x=x_axis_datetime, y=cot_data[1], name='Idollar', yaxis='y2')
                bar_data = [bar_trace1, bar_trace2]
                fig_data.add_traces(bar_data)
                fig_data.update_layout(
                    yaxis=dict(title='Close Data', showgrid=True),
                    yaxis2=dict(title='COT Data', showgrid=False, overlaying='y', side='right'),
                    legend=dict(
                        orientation="h",  # horizontal orientation for the legend
                        y=-0.2,  # adjust the position of the legend outside the figure
                        x=0.5,   # adjust the position of the legend horizontally
                        xanchor='center'  # anchor the legend to the center horizontally
                        )
                        )
                # Display the plot using Streamlit
                st.plotly_chart(fig_data)

if __name__ == "__main__":
    main()
