"""
Página inicial do ETO Calculator com mapa mundial interativo.
"""

import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..components.favorites_components import (
    create_clear_favorites_button,
)
from ..components.world_map_leaflet import create_world_map

logger = logging.getLogger(__name__)

# Layout da página inicial
home_layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        # Coluna do Mapa (8 colunas)
                        dbc.Col(
                            [
                                # Accordion com instruções (colapsável)
                                dbc.Accordion(
                                    [
                                        dbc.AccordionItem(
                                            [
                                                dbc.ListGroup(
                                                    [
                                                        dbc.ListGroupItem(
                                                            [
                                                                html.Span(
                                                                    "1.",
                                                                    className="fw-bold me-2",
                                                                ),
                                                                "Click on any point on the map to select coordinates",
                                                            ]
                                                        ),
                                                        dbc.ListGroupItem(
                                                            [
                                                                html.Span(
                                                                    "2.",
                                                                    className=(
                                                                        "fw-bold me-2"
                                                                    ),
                                                                ),
                                                                (
                                                                    "Use the location button ( "
                                                                ),
                                                                html.Img(
                                                                    src=(
                                                                        "/assets/images/"
                                                                        "geo-location.svg"
                                                                    ),
                                                                    alt="Location",
                                                                    style={
                                                                        "height": "16px",
                                                                        "width": "16px",
                                                                        "display": (
                                                                            "inline"
                                                                        ),
                                                                        "verticalAlign": (
                                                                            "middle"
                                                                        ),
                                                                    },
                                                                ),
                                                                (
                                                                    " ) to find your current position"
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.ListGroupItem(
                                                            [
                                                                html.Span(
                                                                    "3.",
                                                                    className="fw-bold me-2",
                                                                ),
                                                                "Use the layer control (🗺️) to view Brazil, MATOPIBA, and Cities",
                                                            ]
                                                        ),
                                                        dbc.ListGroupItem(
                                                            [
                                                                html.Span(
                                                                    "4.",
                                                                    className="fw-bold me-2",
                                                                ),
                                                                "Click the '(⭐ ADD)' button to add to favorites",
                                                            ]
                                                        ),
                                                        dbc.ListGroupItem(
                                                            [
                                                                html.Span(
                                                                    "5.",
                                                                    className=(
                                                                        "fw-bold me-2"
                                                                    ),
                                                                ),
                                                                (
                                                                    "Use the button ("
                                                                ),
                                                                html.Img(
                                                                    src=(
                                                                        "/assets/images/"
                                                                        "calculator_eto.svg"
                                                                    ),
                                                                    alt="Calculator",
                                                                    style={
                                                                        "height": "16px",
                                                                        "width": "16px",
                                                                        "display": (
                                                                            "inline"
                                                                        ),
                                                                        "verticalAlign": (
                                                                            "middle"
                                                                        ),
                                                                    },
                                                                ),
                                                                "CALCULATE ET",
                                                                html.Sub("0"),
                                                                (
                                                                    ") to be redirected to the calculation page",
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    flush=True,
                                                )
                                            ],
                                            title="📋 How to use the map (click to expand)",
                                        ),
                                    ],
                                    start_collapsed=True,  # Inicia fechado
                                    style={
                                        "marginTop": "25px",
                                        "marginBottom": "10px",
                                    },
                                ),
                                # Card do Mapa
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                create_world_map(),
                                                # Exibir coordenadas selecionadas
                                                html.Div(
                                                    id="current-selection-info",
                                                    className="mt-2",
                                                ),
                                            ],
                                            className="p-2",
                                        ),
                                    ],
                                    className="shadow-sm",
                                ),
                            ],
                            md=8,
                            className="mb-2",  # Reduzido de mb-4 para mb-2
                        ),
                        # Coluna dos Favoritos (4 colunas)
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5(
                                                            "⭐ Favorites",
                                                            className="mb-0 d-inline",
                                                        ),
                                                        dbc.Badge(
                                                            "0/5",
                                                            color="info",
                                                            className="ms-2",
                                                            id="favorites-count-badge",
                                                        ),
                                                    ],
                                                    className="d-flex align-items-center",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                # Seção fixa: Botões de ação
                                                html.Div(
                                                    [
                                                        html.H6(
                                                            "Actions",
                                                            className="mb-2",
                                                        ),
                                                        dbc.ButtonGroup(
                                                            [
                                                                dbc.Button(
                                                                    [
                                                                        html.I(
                                                                            className="bi bi-star me-2"
                                                                        ),
                                                                        "Add",
                                                                    ],
                                                                    id="add-favorite-btn",
                                                                    color="warning",
                                                                    size="sm",
                                                                    disabled=True,
                                                                    className="w-100 add-favorite-button",
                                                                    title="Clique para salvar a seleção nos Favoritos",
                                                                ),
                                                            ],
                                                            vertical=True,
                                                            className="w-100 mb-2",
                                                        ),
                                                        dbc.ButtonGroup(
                                                            [
                                                                dbc.Button(
                                                                    [
                                                                        html.I(
                                                                            className="bi bi-calculator me-2"
                                                                        ),
                                                                        "Calculate ETo",
                                                                    ],
                                                                    id="calculate-eto-btn",
                                                                    color="success",
                                                                    size="sm",
                                                                    disabled=True,
                                                                    className="w-100",
                                                                    href="/eto-calculator",
                                                                ),
                                                            ],
                                                            vertical=True,
                                                            className="w-100 mb-3",
                                                        ),
                                                        html.Hr(),
                                                        # Coordenadas selecionadas (fixo)
                                                        html.Div(
                                                            id="selected-coords-display",
                                                            className="mb-2 small text-muted",
                                                        ),
                                                    ],
                                                ),
                                                html.Hr(className="my-2"),
                                                # Título da lista (fixo)
                                                html.H6(
                                                    "List",
                                                    className="mb-2",
                                                ),
                                                # Container scrollável APENAS para a lista
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            id="favorites-list-container",
                                                            style={
                                                                "minHeight": "100px",
                                                                "maxHeight": "280px",
                                                                "overflowY": "auto",
                                                                "overflowX": "hidden",
                                                            },
                                                        ),
                                                        dbc.Alert(
                                                            [
                                                                "List empty. ",
                                                                "Click on the map to select.",
                                                            ],
                                                            color="info",
                                                            id="empty-favorites-alert",
                                                            className="mt-2 mb-0 small",
                                                        ),
                                                    ],
                                                    className="mb-2",
                                                ),
                                                # Espaçador flex para empurrar botão para baixo
                                                html.Div(style={"flex": "1"}),
                                                # Botão Limpar (sempre fixo no final)
                                                html.Div(
                                                    [
                                                        html.Hr(
                                                            className="my-2"
                                                        ),
                                                        html.Div(
                                                            create_clear_favorites_button(),
                                                            className="d-flex justify-content-center",
                                                        ),
                                                    ],
                                                    style={
                                                        "marginTop": "auto"
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "flexDirection": "column",
                                                "height": "100%",
                                            },
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={
                                        "position": "sticky",
                                        "top": "25px",
                                        "height": "680px",
                                        "overflowY": "hidden",
                                        "marginTop": "25px",
                                        "border": "2px solid #e0e0e0",  # Borda cinza média mais visível
                                        "borderRadius": "6px",
                                    },
                                )
                            ],
                            md=4,
                            className="mb-2",  # Reduzido de mb-4 para mb-2
                        ),
                    ]
                ),
            ],
            fluid=False,  # Container com margens laterais
            className="py-3",
        ),
        # Stores específicos da home
        dcc.Store(
            id="favorites-store",
            storage_type="local",
            data=[],
        ),
        dcc.Store(id="home-favorites-count", data=0),
        dcc.Store(id="selected-location-data", data=None),
        dcc.Store(id="map-click-data", data=None),
        # Toast para notificações
        html.Div(
            id="toast-container",
            style={
                "position": "fixed",
                "top": "80px",
                "right": "20px",
                "zIndex": 9999,
                "minWidth": "300px",
            },
        ),
    ],
)


logger.info("✅ Página inicial carregada com sucesso")
