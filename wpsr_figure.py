import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
#%%
wpsr = pd.read_csv('wpsr.csv')
p_st = pd.read_excel('psw01.xlsx', sheet_name = 'Data 1')
update = pd.to_datetime(p_st.iloc[:,0], errors = 'coerce').dt.strftime('%Y-%m-%d').iloc[-1]
st.set_page_config(page_title = 'wpsr_figure', page_icon = '📈', layout = "wide")
st.title('📈 Weekly Petroleum Status Report')
st.markdown(f'''
            <div style = "display: flex; justify-content: space-between; align-items: center;">
                <div style = "text-align: left; font-size: 19px;">
                    Last updated: {update}
                </div>
                <div style = "display: flex; align-items: center;">
                    <img src = "https://github.com/Shawnye68/shawnye/blob/main/Bart.jpg?raw=true" 
                    style = "width: 30px; height: 30px; border-radius: 50%; margin-right: 8px;">
                    <span>Shawnye</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
st.write('---')
#%%
ticker = ['WCRSTUS1','WCESTUS1', 'WCSSTUS1', 'WGTSTUS1', 'WKJSTUS1', 'WDISTUS1', 'WTESTUS1',
          'WCRFPUS2', 'W_EPC0_FPF_SAK_MBBLD', 'W_EPC0_FPF_R48_MBBLD', 'WCEIMUS2', 'WCREXUS2', 'WRPUPUS2', 'WGFUPUS2', 'WKJUPUS2', 'WDIUPUS2',
          'WCESTP11', 'WCESTP21', 'W_EPC0_SAX_YCUOK_MBBL', 'WCESTP31', 'WCESTP41', 'WCESTP51',
          'WPULEUS3']
comment = []
for i in ticker:
    A = wpsr.columns[wpsr.columns.get_loc(i) + 1]
    comment.append(A) 
TICKER = {c: t for c, t in zip(comment, ticker)}

ticker4w = ['WCRFPUS2', 'W_EPC0_FPF_SAK_MBBLD', 'W_EPC0_FPF_R48_MBBLD', 'WCEIMUS2', 
            'WCREXUS2', 'WRPUPUS2', 'WGFUPUS2', 'WKJUPUS2', 'WDIUPUS2']

ticker_stock = ['WCESTUS1', 'WCRSTUS1', 'WGTSTUS1', 'WKJSTUS1', 'WDISTUS1', 'WTESTUS1']
comment_stock = []
for i in ticker_stock:
    A = wpsr.columns[wpsr.columns.get_loc(i) + 1]
    comment_stock.append(A)

ticker_supply = ['WGFUPUS2', 'WCRFPUS2', 'W_EPC0_FPF_SAK_MBBLD', 'W_EPC0_FPF_R48_MBBLD', 
                 'WRPUPUS2', 'WKJUPUS2', 'WDIUPUS2']
comment_supply = []
for i in ticker_supply:
    A = wpsr.columns[wpsr.columns.get_loc(i) + 1]
    comment_supply.append(A)

ticker_stock_pad = ['W_EPC0_SAX_YCUOK_MBBL', 'WCESTP11', 'WCESTP21', 'WCESTP31', 
                    'WCESTP41', 'WCESTP51']
comment_stock_pad = []
for i in ticker_stock_pad:
    A = wpsr.columns[wpsr.columns.get_loc(i) + 1]
    comment_stock_pad.append(A)

ticker_other = ['WPULEUS3', 'WCSSTUS1', 'WCEIMUS2', 'WCREXUS2']
comment_other  = []
for i in ticker_other:
    A = wpsr.columns[wpsr.columns.get_loc(i) + 1]
    comment_other.append(A)
#%%
def wpsr_avg4w(keyword):
    
    key = keyword
    df = df4w = wpsr
    arr = df.columns.get_loc(key)
    figtitle = df.columns[arr + 1]
    df = df.iloc[:, arr:arr + 14]
    df.columns = df.iloc[0, :]
    df = df.drop(df.index[0]).reset_index(drop = True)
    current_year = int(pd.to_numeric(df.columns, errors = 'coerce').max())
    current_year_column = df.columns.get_loc(current_year)
    last_week = df.iloc[:, current_year_column].last_valid_index()    
    if keyword in ticker4w:
        key4w = f'4_{keyword}'
        df4w = wpsr
        arr4w = df4w.columns.get_loc(key4w)
        df4w = df4w.iloc[:, arr4w:arr4w + 14]
        df4w.columns = df4w.iloc[0, :]
        df4w = df4w.drop(df4w.index[0]).reset_index(drop = True)
    return df, df4w, figtitle, current_year, current_year_column, last_week
#%%
def wpsr_figures(keyword):
    fig = make_subplots(rows = 1, cols = 2,
                        horizontal_spacing=0.05, column_widths=[0.45, 0.55], 
                        specs = [[{'secondary_y': False}, {'secondary_y': True}]])
    
    fig.add_trace(go.Bar(x = df.index, 
                         y = df.iloc[:, 10],
                         width = 0.65,
                         marker_color = 'rgba(102,139,139,0.65)',
                         name = f'week change', 
                         showlegend = True),
                  row = 1, 
                  col = 2,
                  secondary_y = False)
    fig.add_trace(go.Bar(x = df.index, 
                         y = df.iloc[:, 12],
                         width = 0.65,
                         marker_color = 'rgba(96,123,139,0.4)',
                         name = f'year change', 
                         showlegend = True),
                  row = 1, 
                  col = 2,
                  secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df.iloc[:, 9],
                             mode = 'lines + markers', 
                             line_color = 'rgb(139,131,120)',
                             marker = dict(size = [8 if i == last_week else 0 for i in range(len(df))], 
                                           color = 'rgba(139,131,120, 0.8)'),
                             name = f'5 year avg bias(%)', 
                             showlegend = True),
                  row = 1, 
                  col = 2,
                  secondary_y = True)
    
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df['Max'], 
                             mode = 'lines', 
                             line_color = 'rgb(94,95,93)', 
                             line = dict(width = 0),
                             name = 'Max',
                             showlegend = False),
                  row = 1, 
                  col = 1,
                  secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df['Min'], 
                             mode = 'lines', 
                             line_color = 'rgb(94,95,93)', 
                             line = dict(width = 0), 
                             fill = 'tonexty', 
                             fillcolor = 'rgba(166,166,166, 0.2)', 
                             name = 'Range',
                             showlegend = True),
                  row = 1, 
                  col = 1,
                  secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df['Avg'],
                             mode = 'lines', 
                             line_color = 'rgb(94,95,93)',
                             name = f'Avg ({current_year - 5}-{current_year})', 
                             showlegend = True),
                  row = 1, 
                  col = 1,
                  secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df.iloc[0:, current_year_column - 1], 
                             mode = 'lines', 
                             line_color = 'rgb(96,123,139)', 
                             name = f'{current_year - 1}', 
                             showlegend = True),
                  row = 1, 
                  col = 1,
                  secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, 
                             y = df.iloc[0:, current_year_column], 
                             mode = 'lines + markers', 
                             line_color = 'rgb(255,192,0)', 
                             marker = dict(size = [8 if i == last_week else 0 for i in range(len(df))], 
                                           color = 'rgba(255,192,0, 0.8)'),
                             name = f'{current_year}', 
                             showlegend = True), 
                  row = 1, 
                  col = 1,
                  secondary_y = False)
    
    fig.update_layout(title = dict(text = f'{figtitle}', 
                                   font = dict(size = 20)),
                      xaxis = dict(range = [df.index.min(), df.index.max()]),
                      xaxis2 = dict(range = [df.index.min(), df.index.max()]),
                      yaxis2 = dict(side = 'left', 
                                    showgrid = True, 
                                    zeroline = True),
                      yaxis3 = dict(overlaying = 'y2', 
                                    side = 'right', 
                                    showgrid = False, 
                                    zeroline = False),
                      legend = dict(orientation = 'h',
                                    xanchor = 'center', 
                                    x = 0.5,
                                    y = -0.1),
                      xaxis_spikemode = 'across', 
                      yaxis_spikemode = 'across',
                      xaxis_spikethickness = 0.8, 
                      yaxis_spikethickness = 0.8
                      )    
    return(fig)
#%%
def wpsr_figures_4w(keyword):
    fig1 = make_subplots(rows = 1, 
                         cols = 2, 
                         horizontal_spacing=0.05, 
                         column_widths = [0.45, 0.55], 
                         specs = [[{'secondary_y': False}, {'secondary_y': True}]])
    
    fig1.add_trace(go.Bar(x = df.index, 
                          y = df.iloc[:, 10],
                          width = 0.65,
                          marker_color = 'rgba(102,139,139,0.65)',
                          name = f'week change', 
                          showlegend = True),
                   row = 1, 
                   col = 2,
                   secondary_y = False)
    fig1.add_trace(go.Bar(x = df.index, 
                          y = df.iloc[:, 12],
                          width = 0.65,
                          marker_color = 'rgba(96,123,139,0.4)',
                          name = f'year change', 
                          showlegend = True),
                   row = 1, 
                   col = 2,
                   secondary_y = False)
    fig1.add_trace(go.Scatter(x = df.index, 
                              y = df.iloc[:, 9],
                              mode = 'lines + markers', 
                              line_color = 'rgb(139,131,120)',
                              marker = dict(size = [8 if i == last_week else 0 for i in range(len(df))], 
                                            color = 'rgba(139,131,120, 0.8)'),
                              name = f'5 year avg bias(%)', 
                              showlegend = True),
                   row = 1, 
                   col = 2,
                   secondary_y = True)
    
    fig1.add_trace(go.Scatter(x = df.index, 
                              y = df['Max'],
                              mode = 'lines', 
                              line_color = 'rgb(94,95,93)', 
                              line = dict(width = 0),
                              name = 'Max',
                              showlegend = False),
                   row = 1, 
                   col = 1, 
                   secondary_y = False)
    fig1.add_trace(go.Scatter(x = df.index, 
                              y = df['Min'],
                              mode = 'lines', 
                              line_color = 'rgb(94,95,93)', 
                              line = dict(width = 0),
                              fill = 'tonexty', 
                              fillcolor = 'rgba(166,166,166, 0.2)',
                              name = 'Range', 
                              showlegend = True),
                   row = 1, 
                   col = 1, 
                   secondary_y = False)
    fig1.add_trace(go.Scatter(x = df.index, 
                              y = df['Avg'],
                              mode = 'lines', 
                              line_color = 'rgb(94,95,93)',
                              name = f'Avg ({current_year - 5}-{current_year})', 
                              showlegend = True
        ))
    fig1.add_trace(go.Scatter(x = df.index,
                              y = df.iloc[0:, current_year_column - 1],
                              mode = 'lines', 
                              line_color = 'rgb(86,163,156)',
                              name = f'{current_year - 1}', 
                              showlegend = True),
                   row = 1,
                   col = 1, 
                   secondary_y = False)
    fig1.add_trace(go.Scatter(x = df.index,
                              y = df.iloc[0:, current_year_column],
                              mode = 'lines + markers', 
                              line_color = 'rgb(255,192,0)',
                              marker = dict(size = [8 if i == last_week else 0 for i in range(len(df))], 
                                            color = 'rgba(255,192,0, 0.8)'),
                              name = f'{current_year}', 
                              showlegend = True),
                   row = 1, 
                   col = 1,
                   secondary_y = False)
    button0 = [dict(label = '4 week avg', 
                    method = 'update',
                    args = [{'y': [df.iloc[:, 10],
                                   df.iloc[:, 12],
                                   df.iloc[:, 9],
                                   df['Max'],
                                   df['Min'],
                                   df['Avg'],
                                   df.iloc[:, current_year_column - 1],
                                   df.iloc[:, current_year_column]]}],
                    args2 = [{'y': [df4w.iloc[:, 10],
                                    df4w.iloc[:, 12],
                                    df4w.iloc[:, 9],
                                    df4w['Max'],
                                    df4w['Min'],
                                    df4w['Avg'],
                                    df4w.iloc[:, current_year_column - 1],
                                    df4w.iloc[:, current_year_column]]}]
                    )
               ]
    fig1.update_layout(title = dict(text = f'{figtitle}',
                                    font = dict(size = 20)),
                       xaxis = dict(range = [df.index.min(), df.index.max()]),
                       xaxis2 = dict(range = [df.index.min(), df.index.max()]),
                       yaxis2 = dict(side = 'left', 
                                     showgrid = True, 
                                     zeroline = True),
                       yaxis3 = dict(overlaying = 'y2',
                                     side = 'right', 
                                     showgrid = False, 
                                     zeroline = False),
                       legend = dict(orientation = 'h',
                                     xanchor = 'center',
                                     x = 0.5, 
                                     y = -0.1),
                       xaxis_spikemode = 'across',
                       yaxis_spikemode = 'across',
                       xaxis_spikethickness = 0.8,
                       yaxis_spikethickness = 0.8,
                       updatemenus = [dict(type = 'buttons', 
                                           buttons = button0,
                                           showactive = False, 
                                           direction = 'left',
                                           x = 0.0, xanchor = 'left', 
                                           y = 1.12, yanchor = 'top')],
                       font = dict(size=12)
                       )
    return(fig1)
#%%
def wpsr_dashboard(label, avg4w = False):
    if avg4w:
        label = label + ' (4MA)'
        d = df4w
        value = d.iloc[last_week, current_year_column]
        wchange_index = d.columns.get_loc('Week change')
        ychange_index = d.columns.get_loc('Year change')
        delta1 = float(d.iloc[last_week, wchange_index])
        delta2 = float(d.iloc[last_week, ychange_index])
    else:
        d = df
        value = d.iloc[last_week, current_year_column]
        wchange_index = d.columns.get_loc('Week change')
        ychange_index = d.columns.get_loc('Year change')
        delta1 = float(d.iloc[last_week, wchange_index])
        delta2 = float(d.iloc[last_week, ychange_index])   
    symbol1, color1 = ("▼", "red") if delta1 < 0 else ("▲", "rgb(50,205,50)")
    symbol2, color2 = ("▼", "red") if delta2 < 0 else ("▲", "rgb(50,205,50)")
    markdown_dashbord = f'''
    <div style = "font-size: 16px">
        {label}
    </div>
    <div style = "font-size: 42px"; font-weight: bold">
        {value:,.0f} tb
    </div>
    <div style = "color: {color1}; font-size: 16px">
        {symbol1} &nbsp; {delta1:,.0f} tb <span style="margin-left: 5px;"> week change
    </div>
    <div style = "color: {color2}; font-size: 16px">
        {symbol2} &nbsp; {delta2:,.0f} tb <span style="margin-left: 5px;"> year change
    </div>
    '''
    return markdown_dashbord
#%%
with st.expander('SUMMARY', expanded = True):
    col1, col2, col3 = st.columns(3)
    with col1:
        df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w('WCESTUS1')
        mark1 = wpsr_dashboard('Ending Stocks ex SPR of Crude Oil')
        st.markdown(mark1, unsafe_allow_html=True)
    with col2:
        df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w('WGTSTUS1')
        mark2 = wpsr_dashboard('Ending Stocks of Gasoline')
        st.markdown(mark2, unsafe_allow_html=True)
    with col3:
        df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w('WGFUPUS2')
        mark3 = wpsr_dashboard('Supplied of Gasoline', avg4w = True)
        st.markdown(mark3, unsafe_allow_html=True)
    st.write('')

with st.expander('STOCK', expanded = True):
    sourcekey0 = st.selectbox(' ', comment_stock)
    target_ticker = TICKER[sourcekey0]
    df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w(target_ticker)
    if target_ticker in ticker4w:
        fig = wpsr_figures_4w(target_ticker)
    else:
        fig = wpsr_figures(target_ticker)
    st.plotly_chart(fig, use_container_width = True)

with st.expander('SUPPLIED'):
    sourcekey1 = st.selectbox(' ', comment_supply)
    target_ticker = TICKER[sourcekey1]
    df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w(target_ticker)
    if target_ticker in ticker4w:
        fig = wpsr_figures_4w(target_ticker)
    else:
        fig = wpsr_figures(target_ticker)
    st.plotly_chart(fig, use_container_width = True)

with st.expander('STOCK by PADD'):    
    sourcekey2 = st.selectbox(' ', comment_stock_pad)
    target_ticker = TICKER[sourcekey2]
    df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w(target_ticker)
    if target_ticker in ticker4w:
        fig = wpsr_figures_4w(target_ticker)
    else:
        fig = wpsr_figures(target_ticker)
    st.plotly_chart(fig, use_container_width = True)

with st.expander('OTHER'):
    sourcekey3 = st.selectbox(' ', comment_other)
    target_ticker = TICKER[sourcekey3]
    df, df4w, figtitle, current_year, current_year_column, last_week = wpsr_avg4w(target_ticker)
    if target_ticker in ticker4w:
        fig = wpsr_figures_4w(target_ticker)
    else:
        fig = wpsr_figures(target_ticker)
    st.plotly_chart(fig, use_container_width = True)

st.write('')
st.write('')
st.markdown('''
            <div style='text-align: right'>
                Source:<a href = 'https://www.eia.gov/petroleum/supply/weekly/'> https://www.eia.gov/petroleum/supply/weekly/ </a>
            </div>
            ''', unsafe_allow_html = True)
