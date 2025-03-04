from dash import html, dcc

class UIComponents:
    @staticmethod
    # def create_input_field(label: str, input_id: str) -> html.Div:
    #     """Create a styled input field with label."""
    #     return html.Div([
    #     html.Label(f"{label}:", style={
    #         "font-size": "12px",
    #         "font-weight": "bold",
    #         "color": "#333"
    #     }),
    #     dcc.Input(
    #         id=input_id,
    #         type='text',
    #         placeholder=f'Enter {label}',
    #         style={
    #             "font-size": "12px",
    #             "padding": "4px",
    #             "width": "90%",
    #             "text-align": "center",
    #             "margin-bottom": "10px",
    #             "border-radius": "10px"
    #         }
    #     )
    # ], style={"width": "20%", "display": "inline-block", "margin": "2%"})

    def create_input_field(label: str, input_id: str) -> html.Div:
        """Create a styled input field with label."""
        return html.Div([
            html.Label(f"{label}:", style={
                "font-size": "10px",
                "font-weight": "bold",
                "color": "#555",
                "margin-bottom": "2px",
                "display": "block"
            }),
            dcc.Input(
                id=input_id,
                type='text',
                placeholder=f'Enter {label}',
                style={
                    "font-size": "10px",
                    "padding": "4px",
                    "width": "95%",
                    "text-align": "center",
                    "margin-bottom": "5px",
                    "border-radius": "5px",
                    "border": "1px solid #ccc",
                    "display": "block"
                }
            )
        ], style={
            "width": "calc(50% - 10px)",
            "display": "inline-block",
            "margin": "5px",
            "vertical-align": "top",
            "box-sizing": "border-box",
            "min-width": "150px"
        })

    @staticmethod
    def create_button(text: str, button_id: str) -> html.Button:
        """Create a styled button."""
        return html.Button(
            text,
            id=button_id,
            n_clicks=0,
            style={
                "background-color": "#6A1B9A",
                "color": "white",
                "border": "none",
                "padding": "10px 20px",
                "cursor": "pointer",
                "font-size": "12px",
                "border-radius": "8px",
                "transition": "all 0.3s ease",
                "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"
            },
            className="btn-animated"
        )
        
    def create_nav_button(text: str, button_id: str, href: str) -> html.Div:
        """
        Create a navigation button that redirects to the specified page
        Returns:
        --------
        dash component
            A div containing the button with navigation functionality
        """
        return html.Div([
            # Hidden Location component that will be updated by callback
            dcc.Location(id=f"{button_id}-location", refresh=True),
            
            # Button with the same styling as create_button
            html.Button(
                text,
                id=button_id,
                n_clicks=0,
                style={
                    "background-color": "#6A1B9A",
                    "color": "white",
                    "border": "none",
                    "padding": "10px 20px",
                    "cursor": "pointer",
                    "font-size": "12px",
                    "border-radius": "8px",
                    "transition": "all 0.3s ease",
                    "box-shadow": "0 4px 8px rgba(76, 175, 80, 0.3)"
                },
                className="btn-animated"
            ),
            
            # Store the target href
            dcc.Store(id=f"{button_id}-target", data=href)
        ]),
    @staticmethod
    def create_date_picker(label, id, date=None, min_date=None, max_date=None):
        """
        Creates a standardized date picker with label
        
        Returns:
        --------
        dash component
            A div containing the label and date picker components
        """
        return html.Div([
            html.Label(f"{label}:", style={
                "font-size": "10px",
                "font-weight": "bold",
                "color": "#555",
                "margin-bottom": "2px",
                "display": "block"
            }),
            dcc.DatePickerSingle(
                id=id,
                date=date,
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                display_format='YYYY-MM-DD',
                className="form-control"
            )
        ],  style={
            "width": "calc(50% - 10px)",
            "display": "inline-block",
            "margin": "5px",
            "vertical-align": "top",
            "box-sizing": "border-box",
            "min-width": "150px",
        })