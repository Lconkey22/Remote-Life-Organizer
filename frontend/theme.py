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
        }

        /* HEADER */
        .header-bar {
            background: linear-gradient(90deg, #2E4A3A, #1F3528);
            border-bottom: 2px solid #D9C6A9;
        }

        /* DRAWER */
        .drawer-bg {
            background: #F4EDE1 !important;
        }

        .drawer-btn {
            color: #2E4A3A !important;
            font-weight: 600;
        }

        .drawer-btn:hover {
            background: #E6D9C7 !important;
        }

        .signout-btn {
            color: #7a1f1f !important;
            font-weight: bold;
        }

        /* CARDS */
        .earth-card {
            background: #F9F5EE;
            border-radius: 18px;
            border: 1.5px solid #D9C6A9;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }

        /* TITLES */
        .earth-title {
            color: #D9C6A9;
            font-size: 30px;
            font-weight: 400;
            text-align: center;
            margin-top: 20px;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.4);
        }

        .earth-text {
            color: #2E4A3A;
        }
    </style>
    """)
