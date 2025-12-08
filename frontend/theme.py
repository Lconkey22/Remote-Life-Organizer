from nicegui import ui

def apply_global_theme():
    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

    <style>
        body {
            background: #1B301B;
            font-family: "Poiret One", sans-serif;
            margin: 0;
        }

        /* -----------------------
           HEADER STYLING
        ------------------------ */
        .header-bar {
            background: linear-gradient(90deg, #2E4A3A, #1F3528);
            border-bottom: 2px solid #D9C6A9;
        }


        /* -----------------------
           DRAWER / SIDEBAR
        ------------------------ */
        .drawer-bg {
            background: #2E4A3A !important; /* forest green */
            color: #F4EDE1 !important;      /* beige text */
        }

        .drawer-btn {
            color: #F4EDE1 !important;
            font-weight: 500;
            text-align: left;
        }

        .drawer-btn:hover {
            background: #3C5A45 !important; /* lighter green hover */
        }

        .signout-btn {
            color: #D96A6A !important;
            font-weight: bold;
        }


        /* -----------------------
           CARDS / TEXT
        ------------------------ */
        .earth-card {
            background: #F9F5EE;
            border-radius: 16px;
            border: 1.5px solid #D9C6A9;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .home-card {
            background: #F4EDE1;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid #D9C6A9;
        }

        .home-title {
            font-size: 30px;
            color: #D9C6A9;
            font-weight: 400;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.4);
        }

        .item-text {
            color: #2E4A3A;
        }

        /* -----------------------
           BUTTONS
        ------------------------ */
        .event-btn {
            background-color: #3D5A40 !important;
            color: #F4EDE1 !important;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
        }

        .event-btn:hover {
            background-color: #2E4A3A !important;
        }

        .event-input {
            background: #ffffff;
            border: 1px solid #D9C6A9;
            border-radius: 6px;
            padding: 8px;
            color: #2E4A3A;
        }
    </style>
    """)

