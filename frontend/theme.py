from nicegui import ui

def apply_global_theme():
    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

    <style>
        body {
            background: #1B301B !important; /* deep forest green */
            font-family: "Poiret One", sans-serif !important;
        }

        /* ----------------------- */
        /* HEADER THEME            */
        /* ----------------------- */
        .header-bar {
            background: linear-gradient(90deg, #2E4A3A, #1F3528) !important;
            border-bottom: 2px solid #D9C6A9 !important;
        }
        .header-bar button {
            color: #F4EDE1 !important; /* beige icon and text */
        }

        /* ----------------------- */
        /* SIDEBAR / DRAWER        */
        /* ----------------------- */
        .drawer-bg {
            background: #F4EDE1 !important; /* soft beige */
            padding: 10px;
        }

        /* menu button text */
        .drawer-btn {
            color: #2E4A3A !important; /* dark green text */
            font-weight: 600 !important;
            width: 100% !important;
            text-align: left !important;
            padding: 10px !important;
            border-radius: 6px;
        }

        .drawer-btn:hover {
            background: #E6D9C7 !important; /* lighter beige */
        }

        .signout-btn {
            color: #8A2E2E !important;
            font-weight: bold !important;
        }

        /* Fixing blank sidebar issue */
        .q-drawer-container {
            background: #F4EDE1 !important;
        }

        /* ----------------------- */
        /* CARDS                   */
        /* ----------------------- */
        .earth-card, .home-card, .events-card {
            background: #F9F5EE !important;
            border: 1.5px solid #D9C6A9 !important;
            border-radius: 18px !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }

        /* ----------------------- */
        /* TITLES                  */
        /* ----------------------- */
        .earth-title, .home-title, .events-title {
            color: #D9C6A9 !important;
            font-size: 30px !important;
            font-weight: 400 !important;
            text-align: center !important;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.4);
        }

        .earth-text, .item-text, .event-label {
            color: #2E4A3A !important;
        }

        /* ----------------------- */
        /* BUTTONS                 */
        /* ----------------------- */
        .event-btn {
            background: #2E4A3A !important;  /* dark green */
            color: #F4EDE1 !important;       /* beige text */
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 8px !important;
        }

        .event-btn:hover {
            background: #1F3528 !important;
        }

        /* Inputs */
        .event-input {
            border: 2px solid #D9C6A9 !important;
            border-radius: 8px !important;
            padding: 6px !important;
            color: #2E4A3A !important;
        }
    </style>
    """)

