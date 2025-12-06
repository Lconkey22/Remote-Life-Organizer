from nicegui import ui

def apply_global_theme():
    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

    <style>
        /* GLOBAL */
        body {
            background: #1B301B;
            font-family: "Poiret One", sans-serif;
            color: #F4EDE1;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }

        /* Smooth transitions on everything */
        * {
            transition: all 0.25s ease;
        }

        /* PAGE TRANSITIONS */
        .page-enter {
            opacity: 0;
            transform: translateY(15px);
        }
        .page-enter-active {
            opacity: 1;
            transform: translateY(0);
        }

        /* HEADER */
        .header-bar {
            background: linear-gradient(90deg, #2E4A3A, #1F3528);
            border-bottom: 2px solid #D9C6A9;
            padding: 10px 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }

        /* ===== MODERN SIDEBAR ANIMATION (MERGED) ===== */

        /* Your original drawer background, now animated */
        .drawer-bg {
            background: #F4EDE1 !important;
            transform: translateX(-280px);
            opacity: 0;
            width: 260px !important;
            box-shadow: 4px 0px 12px rgba(0,0,0,0.25);
            padding: 10px;
        }

        /* Quasar adds this when sidebar is visible */
        .q-drawer--visible.drawer-bg {
            transform: translateX(0);
            opacity: 1;
        }

        .drawer-btn {
            color: #2E4A3A !important;
            font-weight: 600;
            border-radius: 8px;
            padding: 8px 15px;
            display: block;
        }

        .drawer-btn:hover {
            background: #E6D9C7 !important;
            transform: translateX(6px);
        }

        .signout-btn {
            color: #7a1f1f !important;
            font-weight: bold;
        }

        /* ===== CARDS ===== */
        .earth-card {
            background: #F9F5EE;
            border-radius: 18px;
            border: 1.5px solid #D9C6A9;
            padding: 20px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }

        .earth-card:hover {
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
            transform: translateY(-4px);
        }

        /* ===== TITLES & TEXT ===== */
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

        /* ===== INPUTS ===== */
        input, textarea, select {
            background: #F9F5EE;
            border: 1.5px solid #D9C6A9;
            border-radius: 10px;
            padding: 10px;
            color: #2E4A3A;
            width: 100%;
        }

        input:focus, textarea:focus, select:focus {
            border-color: #2E4A3A;
            box-shadow: 0 0 6px rgba(46, 74, 58, 0.4);
            outline: none;
        }

        /* ===== BUTTON THEMES ===== */
        .btn-primary {
            background: #2E4A3A !important;
            color: #F4EDE1 !important;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 600;
        }

        .btn-primary:hover {
            background: #3C6B4C !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        }

        .btn-secondary {
            background: #D9C6A9 !important;
            color: #1F3528 !important;
            padding: 10px 20px;
            border-radius: 10px;
        }

        .btn-secondary:hover {
            background: #E6D9C7 !important;
            transform: scale(1.03);
        }

        .btn-danger {
            background: #7A1F1F !important;
            color: white !important;
        }

        .btn-danger:hover {
            background: #9F2A2A !important;
            transform: translateY(-2px);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .earth-title { font-size: 26px; }
            .earth-card { padding: 16px; }
        }
    </style>
    """)

