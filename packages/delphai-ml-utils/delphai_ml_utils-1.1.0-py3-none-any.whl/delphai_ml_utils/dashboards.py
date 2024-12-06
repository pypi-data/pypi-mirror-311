import json


def create_target(service: str, metric: str, multivariate: bool, drift: bool) -> dict:
    expr = ""
    format = ""
    legendFormat = ""
    if metric == "metadata":
        expr = f'metadata_info{{job="{service}/{service}"}}'
        format = "table"
    elif not drift:
        if not multivariate:
            expr = f'({metric}{{job="{service}/{service}"}} and (irate(univariate_event_counter_total{{job="{service}/{service}"}}[1h]))!=0)'
        else:
            expr = f'({metric}{{job="{service}/{service}"}} and (irate(multivariate_event_counter_total{{job="{service}/{service}"}}[1h]))!=0)'
            legendFormat = "{{dimension}}"
    else:
        expr = f'drift_probability{{job="ml-monitoring/ml-monitoring", original_job="{service}/{service}", metric="{metric}"}}'
        legendFormat = "{{window}}"
    target = {
        "datasource": {"type": "prometheus", "uid": "prometheus"},
        "editorMode": "code",
        "expr": expr,
        "format": format,
        "instant": False,
        "legendFormat": legendFormat,
        "range": True,
        "refId": "A",
    }
    return target


def create_options(metric: str, multivariate: bool, drift: bool) -> dict:
    if metric == "metadata":
        options = {
            "cellHeight": "sm",
            "footer": {
                "countRows": False,
                "fields": "",
                "reducer": ["sum"],
                "show": False,
            },
            "showHeader": True,
            "sortBy": [{"desc": True, "displayName": "Time"}],
        }
    else:
        if not multivariate and not drift:
            showLegend = False
        else:
            showLegend = True
        options = {
            "legend": {
                "calcs": [],
                "displayMode": "list",
                "placement": "bottom",
                "showLegend": showLegend,
            },
            "tooltip": {"mode": "single", "sort": "none"},
        }
    return options


def create_panel(
    service: str,
    metric: str,
    multivariate: bool = False,
    position: tuple = (0, 0),
    drift: bool = False,
) -> dict:
    panel = dict()
    panel["datasource"] = {"type": "prometheus", "uid": "prometheus"}
    panel["fieldConfig"] = {
        "defaults": {
            "color": {
                "mode": "thresholds" if metric == "metadata" else "palette-classic"
            },
            "custom": {
                "align": "auto",
                "axisCenteredZero": False,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "cellOptions": {"type": "auto"},
                "drawStyle": "points",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                    "legend": False,
                    "tooltip": False,
                    "viz": False,
                },
                "inspect": False,
                "insertNulls": False,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {"type": "linear"},
                "showPoints": "auto",
                "spanNulls": False,
                "stacking": {"group": "A", "mode": "none"},
                "thresholdsStyle": {"mode": "off"},
            },
            "mappings": [],
            "thresholds": {
                "mode": "absolute",
                "steps": [{"color": "green", "value": None}],
            },
        },
        "overrides": [],
    }
    panel["gridPos"] = (
        {"h": 8, "w": 24, "x": 0, "y": 0}
        if metric == "metadata"
        else {"h": 8, "w": 12, "x": position[0] * 12, "y": position[1] * 8}
    )
    panel["id"] = position[0] + position[1] + 1
    panel["interval"] = "15s" if not drift else "1m"
    panel["options"] = create_options(metric, multivariate, drift)
    panel["pluginVersion"] = "10.1.5"
    panel["targets"] = [create_target(service, metric, multivariate, drift)]
    panel["title"] = metric if not drift else f"{metric}_drift"
    if metric == "metadata":
        panel["transformations"] = [
            {
                "id": "organize",
                "options": {
                    "excludeByName": {
                        "Value": True,
                        "__name__": True,
                        "container": True,
                        "endpoint": True,
                        "instance": True,
                        "job": True,
                        "namespace": True,
                        "pod": True,
                    },
                    "renameByName": {},
                },
            }
        ]
        panel["type"] = "table"
    else:
        panel["type"] = "timeseries"
    return panel


def generate_dashboard(name: str, metrics: dict) -> str:
    dashboard = dict()
    dashboard["annotations"] = {
        "list": [
            {
                "builtIn": 1,
                "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                "enable": True,
                "hide": True,
                "iconColor": "rgba(0, 211, 255, 1)",
                "name": "Annotations & Alerts",
                "type": "dashboard",
            }
        ]
    }
    dashboard["description"] = f"ML Monitoring for the {name} service"
    dashboard["editable"] = True
    dashboard["fiscalYearStartMonth"] = 0
    dashboard["graphTooltip"] = 0
    dashboard["links"] = []
    dashboard["liveNow"] = False
    dashboard["panels"] = [create_panel(service=name, metric="metadata")]
    metric_counter = 1
    for metric_area, metric_list in metrics.items():
        multivariate = "multivariate" in metric_area
        for metric in metric_list:
            dashboard["panels"].append(
                create_panel(
                    service=name,
                    metric=metric,
                    multivariate=multivariate,
                    position=(0, metric_counter),
                )
            )
            dashboard["panels"].append(
                create_panel(
                    service=name,
                    metric=metric,
                    multivariate=True,
                    position=(1, metric_counter),
                    drift=True,
                )
            )
            metric_counter += 1
    dashboard["refresh"] = "15s"
    dashboard["schemaVersion"] = 38
    dashboard["style"] = "dark"
    dashboard["tags"] = []
    dashboard["templating"] = {"list": []}
    dashboard["time"] = {"from": "now-1h", "to": "now"}
    dashboard["timepicker"] = {"refresh_intervals": ["15s", "1m", "15m", "1h", "1d"]}
    dashboard["timezone"] = ""
    dashboard["title"] = name
    dashboard["version"] = 0
    dashboard["weekStart"] = ""

    return json.dumps(dashboard)
