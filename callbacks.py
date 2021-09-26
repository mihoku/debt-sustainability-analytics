from dash.dependencies import Input, Output
import pathlib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import date

from app import app
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
MAP_PATH = PATH.joinpath("other-datasets").resolve()

input2 = pd.read_csv(DATA_PATH.joinpath('Input 2-Data 2026.csv'),low_memory=False, sep=";", header=0)
input3 = pd.read_csv(DATA_PATH.joinpath('Input 3 - Debt and Banking.csv'),low_memory=False, sep=",", header=0)
input4 = pd.read_csv(DATA_PATH.joinpath('Input 4 - Forecast.csv'),low_memory=False, sep=";", header=0)
existing_debt_repayment_and_interest_projection = pd.read_csv(DATA_PATH.joinpath('existing-debt-repyament-and-interest-projection.csv'),low_memory=False, sep=";", header=0)

#sort data
input2.sort_values('Tahun')
input3.sort_values('Tahun')

#preprocess
input2['GDP deflator (t-1)'] = input2['GDP deflator (level)'].shift(1)
input2['Inflation'] = input2['GDP deflator (level)']/input2['GDP deflator (t-1)']-1
input2['GDP at constant prices (t-1)'] = input2['GDP at constant prices (level)'].shift(1)
input2['GDP at current prices (t-1)'] = input2['GDP at current prices (level)'].shift(1)
input2['Real GDP Growth'] = input2['GDP at constant prices (level)']/input2['GDP at constant prices (t-1)']-1
input2['Nominal GDP Growth'] = input2['GDP at current prices (level)']/input2['GDP at current prices (t-1)']-1
baseline_combined_input_2_3 = pd.merge(input2,input3, on=['Tahun'], how='left')
baseline_combined_input_2_3['Total Public Debt'] = baseline_combined_input_2_3['Denominated in local currency']+baseline_combined_input_2_3['Denominated in foreign currency']
baseline_combined_input_2_3['Total Public Debt (t-1)'] = baseline_combined_input_2_3['Total Public Debt'].shift(1)
baseline_combined_input_2_3_existing = pd.merge(baseline_combined_input_2_3, existing_debt_repayment_and_interest_projection, on=['Tahun'], how='left')
input4['Interest Payment Amount'] = np.where(input4['Interest Payment Type']=='Annual',input4['Rate']/100*input4['Debt Issuance'],input4['Rate']/100*input4['Debt Issuance']/2)

#new debt interest and maturity calculation
interest_and_repayment_schedule = pd.DataFrame()
year_series = []
interest_payment = []
maturity_repayment = []

for i in np.arange(6):
    tahun = date.today().year+i
    year_series.append(tahun)
    
    interest_year = 0.0
    repayment_year = 0.0
    
    for x in np.arange(len(input4)):
        #for interest
        if(input4.loc[x]['Interest Payment Type']=='Semi-annual'):
            
            if(tahun >= input4.loc[x]['Year']) and (tahun <= input4.loc[x]['Year']+input4.loc[x]['Maturity']):
                interest_year = interest_year+input4.loc[x]['Interest Payment Amount']
            
            else:
                interest_year = interest_year
            
        else:
            if(tahun > input4.loc[x]['Year']) and (tahun <= input4.loc[x]['Year']+input4.loc[x]['Maturity']):
                interest_year = interest_year+input4.loc[x]['Interest Payment Amount']
            
            else:
                interest_year = interest_year
                
        #for repayment
        if(tahun==input4.loc[x]['Year']+input4.loc[x]['Maturity']):
            repayment_year = repayment_year+input4.loc[x]['Debt Issuance']
                
        else:
            repayment_year=repayment_year
    
    interest_payment.append(interest_year)
    maturity_repayment.append(repayment_year)
            
interest_and_repayment_schedule['Tahun'] = year_series
interest_and_repayment_schedule['New Debt Interest Payment'] = interest_payment
interest_and_repayment_schedule['New Debt Maturity Repayment'] = maturity_repayment
issuance = input4[['Year','Debt Issuance']].groupby(['Year']).sum()
interest_repayment_issuance_schedule = pd.merge(interest_and_repayment_schedule,issuance,left_on=['Tahun'],right_on=['Year'], how='left')
baseline_combined_input_2_3_existing_new_debt = pd.merge(baseline_combined_input_2_3_existing,interest_repayment_issuance_schedule, on=['Tahun'], how='left')
baseline_combined_input_2_3_existing_new_debt['Debt Issuance (t-1)'] = baseline_combined_input_2_3_existing_new_debt['Debt Issuance'].shift(1)

baseline_combined_input_2_3_existing_new_debt['Total Gross Public Debt'] = baseline_combined_input_2_3_existing_new_debt['Total Public Debt (t-1)']+baseline_combined_input_2_3_existing_new_debt['Debt Issuance']

baseline_combined_input_2_3_existing_new_debt['Primary Balance'] = baseline_combined_input_2_3_existing_new_debt['Public sector non-interest revenues and grants']-baseline_combined_input_2_3_existing_new_debt['Public sector non-interest expenditures']
baseline_all_columns = baseline_combined_input_2_3_existing_new_debt
baseline_all_columns['Non-interest revenue-to-GDP ratio'] = baseline_all_columns['Public sector non-interest revenues and grants']/baseline_all_columns['GDP at current prices (level)']
baseline_all_columns['Non-interest expenditure-to-GDP ratio'] = baseline_all_columns['Public sector non-interest expenditures']/baseline_all_columns['GDP at current prices (level)']
baseline_all_columns['Primary Balance (Percent of GDP)'] = baseline_all_columns['Primary Balance']/baseline_all_columns['GDP at current prices (level)']

#historical
baseline_historical = baseline_all_columns[baseline_all_columns['Tahun']<date.today().year].reset_index()
Baseline_PB_stddev = baseline_historical['Primary Balance (Percent of GDP)'].std()

#projection_only
baseline_filtered = baseline_all_columns[baseline_all_columns['Tahun']>=date.today().year].reset_index()
baseline_filtered['Gross Financing Needs'] = baseline_filtered['Recognition of implicit contingent liability']+baseline_filtered['Public sector non-interest expenditures']+baseline_filtered['Interest of Current Debt - Local Currency']+baseline_filtered['Interest of Current Debt - Foreign Currency']+baseline_filtered['Principal Payments - Local Currency']+baseline_filtered['Principal Payments - Foreign Currency']+baseline_filtered['New Debt Maturity Repayment']+baseline_filtered['New Debt Interest Payment']-baseline_filtered['Public sector revenues and grants']
baseline_filtered['Financing needs to be financed with new issuance'] = baseline_filtered['Gross Financing Needs']-baseline_filtered['Change in domestic arrears']-baseline_filtered['Change in external arrears']-baseline_filtered['Debt relief']-baseline_filtered['Please specify (1) (e.g.. privatization receipts) (+ reduces financing needs)']+baseline_filtered['Please specify (2) (e.g.. other debt flows) (+ increases financing needs)']

baseline_stress_test = baseline_filtered
total_gross_public_debt = []
total_gross_public_debt_seed = baseline_filtered.loc[0]['Total Gross Public Debt']
for i in np.arange(6):
    if(baseline_stress_test.loc[i]['Tahun']==date.today().year):
        total_gross_public_debt.append(total_gross_public_debt_seed)
    else:
        gross_pd = total_gross_public_debt_seed+baseline_stress_test.loc[i]['Debt Issuance']
        total_gross_public_debt.append(gross_pd)
        total_gross_public_debt_seed = gross_pd

baseline_stress_test['Total Gross Public Debt'] = total_gross_public_debt

projection_benchmark = pd.read_csv(DATA_PATH.joinpath('forecast-error-benchmark.csv'),low_memory=False, sep=";", header=0)
forecast_history = pd.read_csv(DATA_PATH.joinpath('forecast-error-track-record.csv'),low_memory=False, sep=";", header=0)

df1 = pd.read_csv(DATA_PATH.joinpath('Stress-test.csv'),low_memory=False, sep=",", header=0)
#baseline_stress_test = pd.read_csv(DATA_PATH.joinpath('baseline-stress-test.csv'),low_memory=False, sep=";", header=0)
baseline_stress_test['Nominal Debt (in percent of GDP)'] = 100*baseline_stress_test['Total Gross Public Debt']/baseline_stress_test['GDP at current prices (level)']
baseline_stress_test['Gross Financing Need (in percent of GDP)'] = 100*baseline_stress_test['Gross Financing Needs']/baseline_stress_test['GDP at current prices (level)']
baseline_stress_test['Nominal Debt (in percent of Revenue)'] = 100*baseline_stress_test['Total Gross Public Debt']/baseline_stress_test['Public sector revenues and grants']

@app.callback(
    Output('pb-shock-size-container', 'children'),
    [Input('size-of-pb-shock', 'value')])
def update_output(value):
    return 'Shock size {}%'.format(value*100)

@app.callback(
    Output("Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal", "figure"),
    Output("Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal","figure"),
    Output("Gross_Financing_Need_Macro_Fiscal", "figure"),
    Output("Gross_Nominal_Public_Debt_Percent_GDP_Additional", "figure"),
    Output("Gross_Nominal_Public_Debt_Percent_Revenue_Additional","figure"),
    Output("Gross_Financing_Need_Percent_GDP_Additional", "figure"),
    Output("pb_interest_rate_shock","children"),
    Output("cumulative_pb_shock_impact_adjustment_scenario","children"),
    Output("cumulative_pb_shock_impact_10y_stdev","children"),
    Input("impact-on-revenue-pb","value"),
    Input("size-of-pb-shock","value")
    )

def stress_test(pb_ior,pb_size_shock):
    
    Baseline = baseline_stress_test[['Tahun','Nominal Debt (in percent of GDP)','Gross Financing Need (in percent of GDP)','Nominal Debt (in percent of Revenue)']]
    pb_interest_rate_shock=25
        
    #@preprocess pb shock
    PB_Shock_Processor = baseline_stress_test
    
    #new PB based on 10Y stddev
 
    PB_based_10Y_stdev = []
    for i in np.arange(6):
        if(i==1):
            PB = PB_Shock_Processor.loc[i]['Primary Balance (Percent of GDP)']-0.5*Baseline_PB_stddev
            PB_based_10Y_stdev.append(PB)
        elif(i==2):
            PB = PB_Shock_Processor.loc[i]['Primary Balance (Percent of GDP)']-0.5*Baseline_PB_stddev
            PB_based_10Y_stdev.append(PB)
        else:
            PB = PB_Shock_Processor.loc[i]['Primary Balance (Percent of GDP)']
            PB_based_10Y_stdev.append(PB)
    
    PB_Shock_Processor['Primary Balance based on 10Y historical stdev'] = PB_based_10Y_stdev
    PB_Shock_Processor['PB 10 yrs stddev deterioration'] = PB_Shock_Processor['Primary Balance (Percent of GDP)'] - PB_Shock_Processor['Primary Balance based on 10Y historical stdev']
    
    #new PB based on shock scenario
    PB_Shock_Processor['Primary Balance (Percent of GDP)t-1'] = PB_Shock_Processor['Primary Balance (Percent of GDP)'].shift(1)
    PB_Shock_Processor['Primary Balance Adjustment Scenario'] = np.where(PB_Shock_Processor['Primary Balance (Percent of GDP)']-PB_Shock_Processor['Primary Balance (Percent of GDP)t-1']>0,PB_Shock_Processor['Primary Balance (Percent of GDP)']-pb_size_shock*(PB_Shock_Processor['Primary Balance (Percent of GDP)']-PB_Shock_Processor['Primary Balance (Percent of GDP)t-1']),PB_Shock_Processor['Primary Balance (Percent of GDP)'])
    PB_Shock_Processor['PB adjustment scenario deterioration'] = PB_Shock_Processor['Primary Balance (Percent of GDP)'] - PB_Shock_Processor['Primary Balance Adjustment Scenario']
    
    #primary balance after shock
    cumulative_pb_shock_impact_adjustment_scenario = PB_Shock_Processor['PB adjustment scenario deterioration'].sum()
    cumulative_pb_shock_impact_10y_stdev = PB_Shock_Processor['PB 10 yrs stddev deterioration'].sum()
    PB_Shock_Processor['Primary Balance After Shock'] = np.where(cumulative_pb_shock_impact_adjustment_scenario>cumulative_pb_shock_impact_10y_stdev,PB_Shock_Processor['Primary Balance Adjustment Scenario'],PB_Shock_Processor['Primary Balance based on 10Y historical stdev'])
    cumulative_pb_shock_impact_adjustment_scenario_txt = "Dampak kumulatif shock {}%".format(round(cumulative_pb_shock_impact_adjustment_scenario*100,2))
    cumulative_pb_shock_impact_10y_stdev_txt = "Dampak kumulatif shock {}%".format(round(cumulative_pb_shock_impact_10y_stdev*100,2))
    
    #impact of PB shock to interest rate
    if(cumulative_pb_shock_impact_adjustment_scenario>0.01)or(cumulative_pb_shock_impact_10y_stdev>0.01):
        PB_interest_rate_shock=25
    else:
        PB_interest_rate_shock=0
        
    PB_interest_rate_shock_txt = "Interest rate shock {} bps".format(PB_interest_rate_shock)

    #@interest rate shock
    earliest = PB_Shock_Processor.loc[0]['Tahun']
    PB_Shock_Processor['interest rate shock'] = np.where(PB_Shock_Processor['Tahun']>earliest,PB_interest_rate_shock*(PB_Shock_Processor['Primary Balance (Percent of GDP)']-PB_Shock_Processor['Primary Balance After Shock'])*100,0)    
    PB_interest_rate_shock_data = PB_Shock_Processor[['Tahun','interest rate shock']]
    
    #non interest revenue on PB shock
    if(pb_ior=="Belanja"):
        PB_Shock_Processor['Non-interest revenue-to-GDP ratio PB Shock']=PB_Shock_Processor['Non-interest revenue-to-GDP ratio']
    else:
        PB_Shock_Processor['Non-interest revenue-to-GDP ratio PB Shock']=PB_Shock_Processor['Non-interest revenue-to-GDP ratio']-(PB_Shock_Processor['Primary Balance (Percent of GDP)']-PB_Shock_Processor['Primary Balance After Shock'])
        
    #non interest expenditure on PB shock
    PB_Shock_Processor['Non-interest expenditure-to-GDP ratio PB Shock']=PB_Shock_Processor['Non-interest revenue-to-GDP ratio PB Shock']-PB_Shock_Processor['Primary Balance After Shock']
    
    #additional financing needs
    PB_Shock_Processor['Non-interest expenditure PB Shock']=PB_Shock_Processor['Non-interest expenditure-to-GDP ratio PB Shock']*PB_Shock_Processor['GDP at current prices (level)']
    PB_Shock_Processor['Non-interest revenue PB Shock'] = PB_Shock_Processor['Non-interest revenue-to-GDP ratio PB Shock']*PB_Shock_Processor['GDP at current prices (level)']
    PB_Shock_Processor['Non-interest expenditure PB Shock difference'] = PB_Shock_Processor['Non-interest expenditure PB Shock']-PB_Shock_Processor['Public sector non-interest expenditures']
    PB_Shock_Processor['Non-interest revenue PB Shock difference'] = PB_Shock_Processor['Non-interest revenue PB Shock']-PB_Shock_Processor['Public sector non-interest revenues and grants']
    PB_Shock_Processor['Additional Financing Needs PB Shock'] = round(PB_Shock_Processor['Non-interest expenditure PB Shock difference']-PB_Shock_Processor['Non-interest revenue PB Shock difference'],3)
    additional_financing_needs_PB = PB_Shock_Processor[['Tahun','Additional Financing Needs PB Shock']]
    
    #@primary balance shock impact on financing
    input4_pb = input4
    Financing_Needs_Baseline = baseline_stress_test[['Tahun','Financing needs to be financed with new issuance']]
    input4_pb = pd.merge(input4_pb,Financing_Needs_Baseline,left_on=['Year'],right_on=['Tahun'], how='left')
    input4_pb['Percent_Instrument'] = input4_pb['Debt Issuance']/input4_pb['Financing needs to be financed with new issuance']
    
    #@add PB interest rate shock
    input4_pb = pd.merge(input4_pb,PB_interest_rate_shock_data,on=['Tahun'], how='left')
    input4_pb['Rate'] = input4_pb['Rate']+input4_pb['interest rate shock']/10000
    
    #add PB financing needs
    input4_pb = pd.merge(input4_pb,additional_financing_needs_PB,left_on=['Year'],right_on=['Tahun'], how='left')
    input4_pb['Total Financing Needs Post Shock'] = input4_pb['Financing needs to be financed with new issuance']+input4_pb['Additional Financing Needs PB Shock']
    input4_pb['Debt Issuance post shock'] = input4_pb['Percent_Instrument']*input4_pb['Total Financing Needs Post Shock']
    input4_pb['Interest Payment Amount post shock'] = np.where(input4_pb['Interest Payment Type']=='Annual',input4_pb['Rate']/100*input4_pb['Debt Issuance post shock'],input4_pb['Rate']/100*input4_pb['Debt Issuance post shock']/2)
    
    #@calculation of interest and repayment post PB shock
    PB_interest_and_repayment_schedule = pd.DataFrame()
    PB_year_series = []
    PB_interest_payment = []
    PB_maturity_repayment = []

    for i in np.arange(6):
        tahun = date.today().year+i
        PB_year_series.append(tahun)
        
        interest_year = 0.0
        repayment_year = 0.0
        
        for x in np.arange(len(input4_pb)):
            #for interest
            if(input4_pb.loc[x]['Interest Payment Type']=='Semi-annual'):
                
                if(tahun >= input4_pb.loc[x]['Year']) and (tahun <= input4_pb.loc[x]['Year']+input4_pb.loc[x]['Maturity']):
                    interest_year = interest_year+input4_pb.loc[x]['Interest Payment Amount post shock']
                    
                else:
                    interest_year = interest_year
            
            else:
                if(tahun > input4_pb.loc[x]['Year']) and (tahun <= input4_pb.loc[x]['Year']+input4_pb.loc[x]['Maturity']):
                    interest_year = interest_year+input4_pb.loc[x]['Interest Payment Amount post shock']
            
                else:
                    interest_year = interest_year
                
                #for repayment
            if(tahun==input4_pb.loc[x]['Year']+input4_pb.loc[x]['Maturity']):
                repayment_year = repayment_year+input4_pb.loc[x]['Debt Issuance post shock']
                
            else:
                repayment_year=repayment_year
    
        PB_interest_payment.append(interest_year)
        PB_maturity_repayment.append(repayment_year)
    
    PB_interest_and_repayment_schedule['Tahun'] = PB_year_series
    PB_interest_and_repayment_schedule['New Debt Interest Payment post shock'] = PB_interest_payment
    PB_interest_and_repayment_schedule['New Debt Maturity Repayment post shock'] = PB_maturity_repayment
    PB_issuance = input4_pb[['Year','Debt Issuance post shock']].groupby(['Year']).sum()
    PB_interest_repayment_issuance_schedule = pd.merge(PB_interest_and_repayment_schedule,PB_issuance,left_on=['Tahun'],right_on=['Year'], how='left')
    
    #@join PB shock
    PB_Shock_Processor = pd.merge(PB_Shock_Processor,PB_interest_repayment_issuance_schedule, on=['Tahun'], how='left')
    PB_Shock_Processor['Total Gross Public Debt post shock'] = PB_Shock_Processor['Total Public Debt (t-1)']+PB_Shock_Processor['Debt Issuance post shock']
    PB_Shock_Processor['Gross Financing Needs post shock'] = PB_Shock_Processor['Recognition of implicit contingent liability']+PB_Shock_Processor['Non-interest expenditure PB Shock']+PB_Shock_Processor['Interest of Current Debt - Local Currency']+PB_Shock_Processor['Interest of Current Debt - Foreign Currency']+PB_Shock_Processor['Principal Payments - Local Currency']+PB_Shock_Processor['Principal Payments - Foreign Currency']+PB_Shock_Processor['New Debt Maturity Repayment post shock']+PB_Shock_Processor['New Debt Interest Payment post shock']-PB_Shock_Processor['Non-interest revenue PB Shock']
    
    #@calculate total gross public debt new post shock
    PB_total_gross_public_debt = []
    PB_total_gross_public_debt_seed = PB_Shock_Processor.loc[0]['Total Gross Public Debt post shock']
    for i in np.arange(6):
        if(PB_Shock_Processor.loc[i]['Tahun']==date.today().year):
            PB_total_gross_public_debt.append(PB_total_gross_public_debt_seed)
        else:
            gross_pd = total_gross_public_debt_seed+baseline_stress_test.loc[i]['Debt Issuance']
            PB_total_gross_public_debt.append(gross_pd)
            PB_total_gross_public_debt_seed = gross_pd
    PB_Shock_Processor['Total Gross Public Debt post shock'] = PB_total_gross_public_debt
    
    #copy data to dataframe
    Primary_Balance_Shock = PB_Shock_Processor
    Primary_Balance_Shock['Nominal Debt (in percent of GDP)'] = 100*Primary_Balance_Shock['Total Gross Public Debt post shock']/Primary_Balance_Shock['GDP at current prices (level)']
    Primary_Balance_Shock['Gross Financing Need (in percent of GDP)'] = 100*Primary_Balance_Shock['Gross Financing Needs post shock']/Primary_Balance_Shock['GDP at current prices (level)']
    Primary_Balance_Shock['Nominal Debt (in percent of Revenue)'] = 100*Primary_Balance_Shock['Total Gross Public Debt post shock']/(Primary_Balance_Shock['Public sector revenues and grants']+Primary_Balance_Shock['Non-interest revenue PB Shock difference'])
    
    #Primary_Balance_Shock = df1[df1.Shock=='Primary Balance Shock']
    #GDP_Growth_Shock = df1[df1.Shock=='Real GDP Growth Shock']
    #Interest_Rate = df1[df1.Shock=='Real Interest Rate Shock']
    #Exchange_Rate = df1[df1.Shock=='Real Exchange Rate Shock']
    GDP_Growth_Shock = Baseline
    Interest_Rate = Baseline
    Exchange_Rate = Baseline
    
    #Combined_Shock = df1[df1.Shock=='Combined Shock']
    #Contingent = df1[df1.Shock=='Contingent Liability Shock']
    Combined_Shock = Primary_Balance_Shock
    Contingent = Baseline
    x = Primary_Balance_Shock['Tahun']

    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal = go.Figure()
    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.add_trace(
        go.Scatter(x=x, y=Primary_Balance_Shock['Nominal Debt (in percent of GDP)'],
                   mode='lines',name='Primary Balance', line=dict(color='firebrick', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.add_trace(
        go.Scatter(x=x, y=GDP_Growth_Shock['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='GDP Growth', line=dict(color='yellow', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.add_trace(
        go.Scatter(x=x, y=Interest_Rate['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Interest Rate', line=dict(color='green', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Exchange_Rate['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Exchange Rate', line=dict(color='blue', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Baseline['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))

    Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=50,
            yanchor="top",
            y=1,
            text='Nominal Debt (in percent of GDP)'
            ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
            ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=80,
            ))

    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal = go.Figure()
    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Primary_Balance_Shock['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Primary Balance', line=dict(color='firebrick', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.add_trace(go.Scatter(x=x, y=GDP_Growth_Shock['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='GDP Growth', line=dict(color='yellow', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Interest_Rate['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Interest Rate', line=dict(color='green', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Exchange_Rate['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Exchange Rate', line=dict(color='blue', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Baseline['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))

    Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=30,
            yanchor="top",
            y=1,
            text='Nominal Debt (in percent of Revenue)'
            ),
        showlegend=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=30,
            ))

    Gross_Financing_Need_Macro_Fiscal = go.Figure()
    Gross_Financing_Need_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Primary_Balance_Shock['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Primary Balance', line=dict(color='firebrick', width=4)))
    Gross_Financing_Need_Macro_Fiscal.add_trace(go.Scatter(x=x, y=GDP_Growth_Shock['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='GDP Growth', line=dict(color='yellow', width=4)))
    Gross_Financing_Need_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Interest_Rate['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Interest Rate', line=dict(color='green', width=4)))
    Gross_Financing_Need_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Exchange_Rate['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Exchange Rate', line=dict(color='blue', width=4)))
    Gross_Financing_Need_Macro_Fiscal.add_trace(go.Scatter(x=x, y=Baseline['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))

    Gross_Financing_Need_Macro_Fiscal.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=30,
            yanchor="top",
            y=1,
            text='Financing Needs (in percent of GDP)'
            ),
        showlegend=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=30,
            ))

    Gross_Nominal_Public_Debt_Percent_GDP_Additional = go.Figure()
    Gross_Nominal_Public_Debt_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Baseline['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Combined_Shock['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Combined Shock', line=dict(color='orange', width=4)))
    Gross_Nominal_Public_Debt_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Contingent['Nominal Debt (in percent of GDP)'],
                    mode='lines',
                    name='Contingent Liability Shock', line=dict(color='pink', width=4)))

    Gross_Nominal_Public_Debt_Percent_GDP_Additional.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=50,
            yanchor="top",
            y=1,
            text='Nominal Debt (in percent of GDP)'
            ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
            ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=80,
            ))

    Gross_Nominal_Public_Debt_Percent_Revenue_Additional = go.Figure()
    Gross_Nominal_Public_Debt_Percent_Revenue_Additional.add_trace(
        go.Scatter(x=x, y=Baseline['Nominal Debt (in percent of Revenue)'],
                   mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Additional.add_trace(go.Scatter(x=x, y=Combined_Shock['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Combined Shock', line=dict(color='orange', width=4)))
    Gross_Nominal_Public_Debt_Percent_Revenue_Additional.add_trace(go.Scatter(x=x, y=Contingent['Nominal Debt (in percent of Revenue)'],
                    mode='lines',
                    name='Contingent Liability Shock', line=dict(color='pink', width=4)))

    Gross_Nominal_Public_Debt_Percent_Revenue_Additional.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=30,
            yanchor="top",
            y=1,
            text='Nominal Debt (in percent of Revenue)'
            ),
        showlegend=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=30,
                ))
    
    Gross_Financing_Needs_Percent_GDP_Additional = go.Figure()
    Gross_Financing_Needs_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Baseline['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Baseline', line=dict(color='lightseagreen', width=4)))
    Gross_Financing_Needs_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Combined_Shock['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Combined Shock', line=dict(color='orange', width=4)))
    Gross_Financing_Needs_Percent_GDP_Additional.add_trace(go.Scatter(x=x, y=Contingent['Gross Financing Need (in percent of GDP)'],
                    mode='lines',
                    name='Contingent Liability Shock', line=dict(color='pink', width=4)))

    Gross_Financing_Needs_Percent_GDP_Additional.update_layout(
        height=450,
        title=dict(
            pad_t=0,
            pad_b=30,
            yanchor="top",
                y=1,
                text='Financing Needs (in percent of GDP)'
                    ),
        showlegend=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=30,
                    ))
    
    return Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal, Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal, Gross_Financing_Need_Macro_Fiscal, Gross_Nominal_Public_Debt_Percent_GDP_Additional, Gross_Nominal_Public_Debt_Percent_Revenue_Additional, Gross_Financing_Needs_Percent_GDP_Additional, PB_interest_rate_shock_txt, cumulative_pb_shock_impact_adjustment_scenario_txt, cumulative_pb_shock_impact_10y_stdev_txt
    
@app.callback(
    Output('primary-balance-projection-track-record', 'figure'),
    Output('inflation-projection-track-record', 'figure'),
    Output('gdp-growth-projection-track-record', 'figure'),
    Input('forecast-comparator-group', 'value')
)

def update_graph_projection_track_record(group):
    
    benchmark = projection_benchmark[projection_benchmark['Category']==group]
    benchmark_gdp = benchmark[benchmark['Indicator']=='Growth']
    benchmark_inflation = benchmark[benchmark['Indicator']=='Inflation']
    benchmark_pb = benchmark[benchmark['Indicator']=='Primary Balance']
    
    chart_GDP = go.Figure()
    
    chart_GDP.add_trace(go.Scatter(x=benchmark_gdp['Tahun'], y=benchmark_gdp['25th'],
                                   fill=None,
                                   mode='lines',
                                   name='forecast errors',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   ))
    
    chart_GDP.add_trace(go.Scatter(
        x=benchmark_gdp['Tahun'], y=benchmark_gdp['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))
    
    chart_GDP.add_trace(go.Scatter(
        x=benchmark_gdp['Tahun'], y=benchmark_gdp['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_GDP.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['Growth-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_GDP.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4)
    )
    
    
    chart_Inflation = go.Figure()
    
    chart_Inflation.add_trace(go.Scatter(x=benchmark_inflation['Tahun'], y=benchmark_inflation['25th'],
                                   fill=None,
                                   mode='lines',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   name='forecast errors'
                                   ))
    
    chart_Inflation.add_trace(go.Scatter(
        x=benchmark_inflation['Tahun'], y=benchmark_inflation['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))    
    
    chart_Inflation.add_trace(go.Scatter(
        x=benchmark_inflation['Tahun'], y=benchmark_inflation['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_Inflation.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['Inflation-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_Inflation.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4))
    
    chart_PB = go.Figure()
    
    chart_PB.add_trace(go.Scatter(x=benchmark_pb['Tahun'], y=benchmark_pb['25th'],
                                   fill=None,
                                   mode='lines',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   name='forecast errors'
                                   ))
    
    chart_PB.add_trace(go.Scatter(
        x=benchmark_pb['Tahun'], y=benchmark_pb['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))
    
    chart_PB.add_trace(go.Scatter(
        x=benchmark_pb['Tahun'], y=benchmark_pb['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_PB.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['PB-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_PB.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4))
    
    return chart_PB, chart_Inflation, chart_GDP