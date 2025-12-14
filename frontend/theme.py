"""Global NiceGUI theme styles for the Remote Life Organizer frontend."""

from nicegui import ui

def apply_global_theme():
    """Inject shared CSS/fonts into the NiceGUI page head."""
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

        /* -----------------------
           TIME TRACKER
        ------------------------ */
        .tt-page-title {
            font-size: 30px;
            color: #D9C6A9;
            font-weight: 400;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.4);
        }

        .tt-mail-btn {
            color: #F4EDE1 !important;
        }

        .tt-controls {
            color: #F4EDE1;
        }

        .tt-view-note {
            color: #D9C6A9;
            font-size: 14px;
        }

        .tt-empty-state {
            color: #D9C6A9;
            text-align: center;
            padding: 16px 0;
        }

        .tt-section-card {
            background: #F4EDE1;
            border-radius: 12px;
            border: 1px solid #D9C6A9;
            padding: 10px 10px 12px 10px;
        }

        .tt-section-title {
            color: #2E4A3A;
            font-weight: 700;
            text-align: center;
            margin-bottom: 6px;
        }

        .tt-chart {
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }

        .tt-day-col {
            display: flex;
            flex-direction: column;
            flex: 0 0 56px;
        }

        .tt-day-label {
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding-left: 6px;
            color: #2E4A3A;
            font-size: 12px;
            border: 1px solid rgba(46, 74, 58, 0.35);
            border-bottom: none;
            background: rgba(255, 255, 255, 0.35);
        }

        .tt-day-label-axis {
            height: 24px;
            border-bottom: 1px solid rgba(46, 74, 58, 0.35);
        }

        .tt-grid-scroll {
            overflow-x: auto;
            overflow-y: hidden;
            -webkit-overflow-scrolling: touch;
            border: 1px solid rgba(46, 74, 58, 0.35);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.45);
        }

        .tt-grid {
            --tt-hour-width: 56px;
            width: calc(var(--tt-hours) * var(--tt-hour-width));
            display: flex;
            flex-direction: column;
        }

        .tt-row {
            position: relative;
            height: 28px;
            border-bottom: 1px solid rgba(46, 74, 58, 0.25);
            background-image: repeating-linear-gradient(
                to right,
                rgba(46, 74, 58, 0.22) 0px,
                rgba(46, 74, 58, 0.22) 1px,
                transparent 1px,
                transparent var(--tt-hour-width)
            );
        }

        .tt-bar {
            position: absolute;
            top: 4px;
            height: 20px;
            border-radius: 4px;
            background: rgba(46, 74, 58, 0.70);
        }

        .tt-axis {
            display: grid;
            grid-template-columns: repeat(var(--tt-hours), var(--tt-hour-width));
            height: 24px;
            background: rgba(255, 255, 255, 0.50);
        }

        .tt-axis-label {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #2E4A3A;
            border-left: 1px solid rgba(46, 74, 58, 0.22);
        }
    </style>
    """)
