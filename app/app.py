#!python3
# Dash driver

# -----------------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------------
import binascii, math, time, uuid

import scapy.all as scapy_all
import scapy.utils as scapy_ut

import dash
import dash_core_components as dcc
import dash_html_components as dhc
import dash.dependencies as ddeps

import cassandra.cluster as ccass

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

#-- connect to Cassandra
cluster = ccass.Cluster(port = 9042)
session = cluster.connect()

#-- get initial list of hosts
h = set()
hosts = []
for _ in session.execute("SELECT hostid FROM test1.t7 LIMIT 10"):
    h.add(_.hostid)
for _ in h:
    hosts.append({"label": str(_), "value": f"{_}"})

#-- define app and its layout
css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    {'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
     'rel': 'stylesheet',
     'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
     'crossorigin': 'anonymous'}
]
dash_app = dash.Dash(__name__, external_stylesheets = css)

dash_app.layout = dhc.Div([
    #-- header
    dhc.Div(dhc.H1("PacketStream"),
        style = {"paddingLeft": "40%",
            "backgroundColor": "#74f3ff"}
    ),

    dhc.Div([
        #-- hosts dropdown
        dhc.Div([dhc.H3("Hosts to monitor"),
                 dcc.Dropdown(id = "hosts", options = hosts, value = [],
                     multi = True)], style = {"display": "inline-block"}
        ),

        #-- packet delay
        dhc.Div([dhc.H4("Time window (sec) "),
                 dcc.Input(id = "delay", value = "1000", type = "text"),
                 dhc.Button(id = "delay-submit", type = "submit",
                     children = "Submit")], style = {"display": "inline-block"}
        ),
        dhc.Div(id = "div-delay"),

        #-- tshark filter rules
        dhc.Div([dhc.H4("Filter rule (similar to Wireshark) "),
                 dcc.Input(id = "filter", value = "tcp", type = "text"),
                 dhc.Button(id = "filter-submit", type = "submit",
                     children = "Submit")], style = {"display": "inline-block"}
        ),
        #dhc.Div(id = "div-filter",
        #    style = {"color": "yellow", 
        #             "background-color": "black"}
        #),
    ], style = {"columnCount": "3"}),

    #-- diagnostic
    dhc.Br(),
    dhc.Br(),
    dhc.Div(id = "div-hosts"),

    #dcc.Interval(id = "i1", interval = 5000, n_intervals = 0),
    #-- collect output ot tshark
    dhc.Iframe(id = "console-out", srcDoc = "",
        style = {"width": "100%",
                 "height": 400,
                 "background": "lightblue",
                 "fontColor": "white",
                 "border": "thin gray solid"}
    )
])

#
# Interactive UI elements
#

#-- host selection
@dash_app.callback(ddeps.Output("div-hosts", "children"),
        [ddeps.Input("hosts", "value")])
def show_selected_hosts(x):
    return f"Showing packet capture from hosts {x}"

#-- tshark filters
"""
@dash_app.callback(ddeps.Output("div-filter", "children"),
        [ddeps.Input("filter-submit", "n_clicks")],
        [ddeps.State("filter", "value")])
def _update(c, inp):
    if (c is not None):
        return str(inp)
"""

#-- get packets from database
@dash_app.callback(ddeps.Output("div-delay", "children"),
        [ddeps.Input("delay-submit", "n_clicks")],
        state = [ddeps.State("delay", "value"),
                 ddeps.State("hosts", "value")])
def _db_output(n_clicks, s_dt, hosts):
    if (n_clicks is None):
        return None

    try:
        dt = int(s_dt)
    except ValueError:
        return f"Invalid time interval \"{s_dt}\""

    r = []
    q = """
        SELECT payload FROM test1.t7
        WHERE hostid = %s AND pktid > maxTimeuuid(%s)
        """
    for i in session.execute(q,
            (uuid.UUID(hosts[0]), math.floor(1000 * (time.time() - dt)))):
        r.append(scapy_all.Ether(binascii.unhexlify(i.payload.encode())))
    scapy_all.wrpcap("/tmp/a.pcap", r, sync = True)

    return None

#-- embed stdout of tshark
@dash_app.callback(ddeps.Output("console-out", "srcDoc"),
        [ddeps.Input("filter-submit", "n_clicks")],
        [ddeps.State("filter", "value")])
def _tshark_dump(n, f):
    data = ""
    for l in subprocess.check_output(
            ["tshark", "-Y", f, "-r", "/tmp/a.pcap"]).decode().split("\n"):
        data = data + l + r"<BR>"

    return data

"""
@dash_app.callback(ddeps.Output("console-out", "srcDoc"),
        [ddeps.Input("i1", "n_intervals")])
def update_cout(n):
    with open("/tmp/a.txt", "rt") as f:
        data = ""
        i = 1
        for l in f:
            data = data + l + r"<BR>"

            i += 1
            if (i >= 20):
                break

    return data
"""

#-- start the app
if (__name__ == "__main__"):
    dash_app.run_server(debug = True, port = 18080, host = "0.0.0.0")
