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
    "danger_hover": "#F43F5E" 
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
    }
}