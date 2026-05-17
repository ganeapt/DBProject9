THEME = {
    "bg_dark": "#0A0B1E",      
    "bg_panel": "#161B33",     
    "card_inner": "#1F2544",   
    "btn_main": "#475569",     
    "btn_accent": "#6366F1",   
    "btn_hover": "#818CF8",    
    "text_main": "#F8FAFC",   
    "text_dim": "#94A3B8",     
    "success": "#10B981",      
    "success_hover": "#065F46",
    "danger": "#991B1B",      
    "danger_hover": "#F43F5E",

    "bank_map": {
        "BTRL": {"name": "BT", "color": "#ECF27F", "text": "#FFFFFF"},
        "INGB": {"name": "ING", "color": "#E47631", "text": "#FFFFFF"},
        "BCIT": {"name": "BCR", "color": "#59C7F0", "text": "#FFFFFF"},
        "RZBR": {"name": "RZB", "color": "#EDED00", "text": "#000000"},
        "BRDX": {"name": "BRD", "color": "#CE3035", "text": "#FFFFFF"},
        "GBUI": {"name": "REV", "color": "#C1C1C1", "text": "#F8FAFC"},
        "GENERIC": {"name": "???", "color": "#FFFFFF", "text": "#FFFFFF"}
    }
}

STYLES = {
    "card": {
        "fg_color": THEME["bg_panel"],
        "border_width": 2,
        "border_color": THEME["btn_accent"],
        "hover_color": THEME["btn_accent"],
        "text_color": THEME["text_main"]
    },
    "input": {
        "fg_color": THEME["card_inner"],
        "border_color": THEME["btn_accent"],
        "text_color": THEME["text_main"]
    },
    "btn_action": {
        "fg_color": THEME["btn_accent"],
        "hover_color": THEME["btn_hover"]
    },
    "btn_back": {
        "fg_color": "transparent",
        "border_width": 2,
        "border_color": THEME["btn_accent"],
        "text_color": THEME["text_main"],
        "hover_color": THEME["bg_panel"]
    },
    "combobox": {
        "fg_color": THEME["bg_panel"],
        "border_color": THEME["btn_accent"],
        "border_width": 2,
        "button_color": THEME["btn_accent"],
        "button_hover_color": THEME["btn_hover"],
        "dropdown_fg_color": THEME["bg_panel"],
        "dropdown_hover_color": THEME["btn_hover"],
        "dropdown_text_color": THEME["text_main"],
        "corner_radius": 8
    },
    "transaction_row": {
        "fg_color": THEME["bg_panel"],
        "border_width": 1,
        "border_color": THEME["btn_accent"]
    },
    "lbl_primary": {
        "text_color": THEME["text_main"],
        "font": ("Roboto", 13, "bold")
    },
    "lbl_secondary": {
        "text_color": THEME["text_dim"],
        "font": ("Roboto", 11)
    },
    "lbl_data": {
        "text_color": THEME["text_dim"],
        "font": ("Roboto", 10)
    },
    "btn_danger": {
        "fg_color": THEME["danger"],
        "hover_color": THEME["danger_hover"]
    },
    "scrollbar":{
        "scrollbar_button_color": THEME["btn_accent"],
        "scrollbar_button_hover_color": THEME["btn_hover"]
    },
    "btn_confirm": {
        "fg_color": THEME["success"],
        "hover_color": THEME["success_hover"],
        "text_color": THEME["bg_dark"],
        "font": ("Roboto", 13, "bold")
    },
    "btn_back": {
        "fg_color": "transparent",
        "border_width": 2,
        "border_color": THEME["btn_accent"],
        "text_color": THEME["text_main"],
        "hover_color": THEME["bg_panel"],
        "width": 150, "height": 30
    },
    "btn_options": {
        "width": 200, 
        "height": 100, 
        "font": ("Roboto", 16, "bold"), 
        "fg_color": THEME["bg_panel"],
        "border_width": 2,
        "border_color": THEME["btn_accent"],
        "hover_color": THEME["btn_accent"],
        "text_color": THEME["text_main"]
    }
}