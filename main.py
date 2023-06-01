import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


df = pd.read_excel('çalışan deneyimi dashboard veri(rev2).xlsx', engine='openpyxl')

extra_columns = [
    "Bu şirkette proje yapmış olmak için yeni proje yapıldığını düşünüyorum. (Bu ifadeye katılım derecenizi belirtiniz.)",
    "Proje yapmayı destekleyen bir kültüre sahip olmadığımızı düşünüyorum. (Bu ifadeye katılım derecenizi belirtiniz.)",
    "Projelerde bireysel yaratıcılığımın açığa çıkabileceği ortamların oluştuğunu ve desteklendiğini düşünüyorum. (Bu ifadeye katılım derecenizi belirtiniz.)",
    "Meslektaşlarınız ve yöneticilerinizle yeni fikir veya önerilerinizi paylaşırken ne kadar rahat hissediyorsunuz?",
    "İş yerindeki bir soruna hiç yenilikçi bir çözüm önerdiniz mi?",
    "Şirketinize yaptığınız katkılara ve sunduğunuz yenilikçi fikirlere iş arkadaşlarınız ve üstleriniz tarafından değer verildiğini düşünüyor musunuz?",
    "Yaratıcılığı ve yeniliği teşvik etmek için tasarlanmış beyin fırtınası oturumlarına veya diğer etkinliklere hiç katıldınız mı?",
    "Şirketinizin, çalışanları; risk almaya ve yeni projeler denemeye teşvik ettiğini düşünüyor musunuz?",
    "Yeni fikirler ve projeler üretmeniz için; gereken finansal özgürlük ve kaynaklar sağlanıyor mu?",
    "Şirketinize yaptığınız katkılara ve sunduğunuz yenilikçi fikirlere iş arkadaşlarınız ve üstleriniz tarafından değer verildiğini düşünüyor musunuz?",
    "Yeni beceriler öğrenmeniz ve yaratıcılığınızı geliştirmeniz için size ne sıklıkla fırsatlar veriliyor?",
    "Şirketiniz başarısızlıkla nasıl başa çıkıyor? Bir öğrenme fırsatı olarak mı yoksa bir ceza kaynağı olarak mı görülüyor?",
    "Şirketinizde yaratıcılığı ve yeniliği engellediğini düşündüğünüz herhangi bir süreç veya politika var mı?",
]

app.layout = dbc.Container([
    html.H1('Dashboard', className='text-center my-4'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='department-dropdown',
                options=[{'label': 'Genel Görünüm', 'value': 'Genel Görünüm'}] +
                        [{'label': i, 'value': i} for i in df["Departmanınızı yazınız"].unique()],
                value='Genel Görünüm',
                clearable=False
            ),
        ], width=12),
    ], align='center'),

    dbc.Row([
        dbc.Col([dcc.Graph(id='gender-graph')], width=6),
        dbc.Col([dcc.Graph(id='department-graph')], width=6),
    ], align='center'),

    dbc.Row([
        dbc.Col([dcc.Graph(id='position-graph')], width=6),
        dbc.Col([dcc.Graph(id='years-graph')], width=6),
    ], align='center'),

    dbc.Row([
        dbc.Col([dcc.Graph(id='physical-graph')], width=6),
        dbc.Col([dcc.Graph(id='branch-graph')], width=6),
    ], align='center'),

    dbc.Row([
        dbc.Col([dcc.Graph(id='project-graph')], width=6),
        dbc.Col([dcc.Graph(id='effect-graph')], width=6),
    ], align='center'),

    *[dbc.Row([dbc.Col([dcc.Graph(id=f'extra-graph-{i}')], width=12)]) for i in range(len(extra_columns))],
], fluid=True)


@app.callback(
    [Output('gender-graph', 'figure'),
     Output('department-graph', 'figure'),
     Output('position-graph', 'figure'),
     Output('years-graph', 'figure'),
     Output('physical-graph', 'figure'),
     Output('branch-graph', 'figure'),
     Output('project-graph', 'figure'),
     Output('effect-graph', 'figure'),

     *[Output(f'extra-graph-{i}', 'figure') for i in range(len(extra_columns))]],
    [Input('department-dropdown', 'value')]
)
def update_graphs(department):
    if department == 'Genel Görünüm':
        dff = df
    else:
        dff = df[df["Departmanınızı yazınız"] == department]

    gen_df = dff["Cinsiyetinizi seçiniz"].value_counts()
    dep_df = dff["Departmanınızı yazınız"].value_counts()
    pos_df = dff["Unvanınızı yazınız"].value_counts()
    years_df = dff["Kaç yıldır bu şirkette çalışıyorsunuz?"].value_counts().sort_index()
    physical_df = dff["Daha önce çalıştığınız fiziki birim varsa yazınız."].value_counts()
    branch_df = dff["Çalıştığınız şubeyi yazınız"].value_counts()
    pro_df = dff["Şirketinizde / biriminizde son bir sene içerisinde bireysel yaratıcılığınızı katabileceğiniz bir proje içerisinde yer aldınız mı?"].value_counts()
    eff_df = dff["Bu durum sizi nasıl etkiledi?"].value_counts().sort_index()
    eff_mean = dff["Bu durum sizi nasıl etkiledi?"].mean()

    gender_fig = go.Figure(data=[go.Pie(labels=gen_df.index, values=gen_df.values, hovertemplate="%{label}: %{value} kişi")])
    gender_fig.update_layout(title_text='Cinsiyet Dağılımı')

    department_fig = go.Figure(data=[go.Pie(labels=dep_df.index, values=dep_df.values, hovertemplate="%{label}: %{value} kişi")])
    department_fig.update_layout(title_text='Departman Dağılımı')

    position_fig = go.Figure(data=[go.Pie(labels=pos_df.index, values=pos_df.values, hovertemplate="%{label}: %{value} kişi")])
    position_fig.update_layout(title_text='Unvan Dağılımı')

    years_fig = go.Figure(data=[go.Bar(x=years_df.index, y=years_df.values, hovertemplate="%{x}: %{y} kişi")])
    years_fig.update_layout(title_text='Kıdem')

    physical_fig = go.Figure(data=[go.Pie(labels=physical_df.index, values=physical_df.values, hovertemplate="%{label}: %{value} kişi")])
    physical_fig.update_layout(title_text='Daha Önce Çalışılan Fiziki Birim')

    branch_fig = go.Figure(data=[go.Pie(labels=branch_df.index, values=branch_df.values, hovertemplate="%{label}: %{value} kişi")])
    branch_fig.update_layout(title_text='Şube Dağılımı')

    project_fig = go.Figure(data=[go.Pie(labels=pro_df.index, values=pro_df.values, hovertemplate="%{label}: %{value} kişi")])
    project_fig.update_layout(title_text='Bireysel yaratıcılığınızı katabileceğiniz bir proje içerisinde yer aldınız mı?')

    effect_fig = go.Figure()

    effect_fig.add_trace(go.Bar(
        x=eff_df.index,
        y=eff_df.values,
        hovertemplate="%{x}: %{y} kişi",
        name='Puanların Frekansı'
    ))

    effect_fig.add_trace(go.Scatter(
        x=eff_df.index,
        y=[eff_mean] * len(eff_df.index),
        mode='lines',
        name='Ortalama Puan',
        line=dict(color='red'),
    ))

    effect_fig.update_layout(
        title_text='Bu durum sizi nasıl etkiledi?',
        xaxis_title='Puan',
        yaxis_title='Frekans',
        autosize=False,
        width=700,
        height=500,
    )

    extra_figs = []
    for column in extra_columns:
        extra_df = dff[column].value_counts()
        extra_fig = go.Figure(data=[go.Pie(labels=extra_df.index, values=extra_df.values, hovertemplate="%{label}: %{value} kişi")])
        extra_fig.update_layout(title_text=column)
        extra_figs.append(extra_fig)

    return [gender_fig, department_fig, position_fig, years_fig, physical_fig, branch_fig, project_fig, effect_fig] + extra_figs


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

