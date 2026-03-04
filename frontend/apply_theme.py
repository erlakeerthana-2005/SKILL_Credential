import os

def rewrite_dashboard_css():
    css = """
:root {
    --primary: #f8fafc;
    --secondary: #f1f5f9;
    --accent: #1e3a8a; /* Navy accent */
    --accent-glow: rgba(30, 58, 138, 0.15);
    --text: #0f172a;
    --text-dim: #64748b;
    --success: #059669;
    --warning: #d97706;
    --danger: #dc2626;
    --info: #2563eb;

    --glass: #ffffff;
    --glass-border: #e2e8f0;
    --glass-heavy: #ffffff;

    --font-main: 'Inter', system-ui, sans-serif;
    --transition: all 0.2s ease;
    --sidebar-width: 250px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: var(--font-main);
    background-color: var(--primary);
    color: var(--text);
    min-height: 100vh;
}

.dashboard { display: flex; }

.sidebar {
    width: var(--sidebar-width);
    background: var(--glass-heavy);
    border-right: 1px solid var(--glass-border);
    padding: 32px 24px;
    position: fixed;
    height: 100vh;
    display: flex;
    flex-direction: column;
    z-index: 100;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 40px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--glass-border);
}

.sidebar-logo {
    width: 32px;
    height: 32px;
    border-radius: 4px;
}

.sidebar-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
}

.user-profile {
    background: var(--secondary);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-avatar {
    width: 36px;
    height: 36px;
    background: var(--accent);
    color: #ffffff;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
}

.user-details h3 {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 2px;
}

.user-details p {
    font-size: 11px;
    color: var(--text-dim);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.nav-menu { list-style: none; flex-grow: 1; }

.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    color: var(--text-dim);
    text-decoration: none;
    border-radius: 6px;
    margin-bottom: 4px;
    font-size: 14px;
    font-weight: 500;
    transition: var(--transition);
}

.nav-link:hover {
    background: var(--secondary);
    color: var(--text);
}

.nav-link.active {
    background: var(--secondary);
    color: var(--accent);
    font-weight: 600;
    border-left: 3px solid var(--accent);
    padding-left: 9px;
    border-radius: 0 6px 6px 0;
}

.logout-btn-sidebar {
    margin-top: auto;
    background: transparent;
    color: var(--text-dim);
    border: 1px solid var(--glass-border);
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: var(--transition);
}

.logout-btn-sidebar:hover {
    background: rgba(220, 38, 38, 0.05);
    color: var(--danger);
    border-color: rgba(220, 38, 38, 0.2);
}

.main-content {
    flex: 1;
    margin-left: var(--sidebar-width);
    padding: 40px;
    max-width: 1200px;
}

.page-header { margin-bottom: 32px; border-bottom: 1px solid var(--glass-border); padding-bottom: 24px;}
.page-header h1 { font-size: 26px; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.page-header p { color: var(--text-dim); font-size: 15px; }

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}

.stat-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
    background: var(--secondary);
}

.stat-card.gold .stat-icon { color: #854d0e; background: #fef9c3; }
.stat-card.success .stat-icon { color: var(--success); background: #d1fae5; }
.stat-card.info .stat-icon { color: var(--info); background: #dbeafe; }
.stat-card.purple .stat-icon { color: #6d28d9; background: #ede9fe; }

.stat-value { font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 2px; }
.stat-label { font-size: 13px; color: var(--text-dim); font-weight: 500; }

.content-section {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 32px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.section-head {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--glass-border);
}

.section-head h2 { font-size: 18px; font-weight: 600; color: var(--text); }

.action-btn {
    background: var(--accent);
    color: #ffffff;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: var(--transition);
}

.action-btn:hover { background: #1e3271; }

.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: separate; border-spacing: 0; }
th {
    text-align: left;
    padding: 12px 16px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    background: var(--secondary);
    border-y: 1px solid var(--glass-border);
}
th:first-child { border-left: 1px solid var(--glass-border); border-top-left-radius: 6px; border-bottom-left-radius: 6px;}
th:last-child { border-right: 1px solid var(--glass-border); border-top-right-radius: 6px; border-bottom-right-radius: 6px;}

td {
    padding: 14px 16px;
    font-size: 13px;
    color: var(--text);
    border-bottom: 1px solid var(--glass-border);
}

tr:nth-child(even) td { background: #fafafa; }
tr:hover td { background: rgba(30, 58, 138, 0.02); }

.badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    border: 1px solid transparent;
}
.badge-success { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.badge-warning { background: #fffbeb; color: #d97706; border-color: #fde68a; }
.badge-info { background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }
.badge-student { background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }
.badge-institution { background: #faf5ff; color: #9333ea; border-color: #e9d5ff; }
.badge-admin { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.badge-external { background: #faf5ff; color: #9333ea; border-color: #e9d5ff; }
.badge-internal { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }

.hash-text { font-family: 'Consolas', monospace; font-size: 12px; color: var(--text-dim); }

.modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.5); z-index: 1000; justify-content: center; align-items: center; }
.modal-content { background: var(--glass-heavy); border: 1px solid var(--glass-border); border-radius: 12px; padding: 32px; width: 90%; max-width: 480px; position: relative; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
.close-btn { position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 20px; color: var(--text-dim); cursor: pointer; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; color: var(--text-dim); margin-bottom: 6px; font-weight: 600; }
.form-group input, .input-group input { width: 100%; background: var(--primary); border: 1px solid var(--glass-border); border-radius: 6px; padding: 10px 12px; color: var(--text); font-family: var(--font-main); }
.form-group input:focus, .input-group input:focus { outline: none; border-color: var(--accent); }

.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: var(--glass-heavy); border: 1px solid var(--glass-border); border-radius: 8px; padding: 20px; transition: var(--transition); }
.card-title { font-size: 16px; font-weight: 600; color: var(--text); margin-bottom: 4px; }
.card-description { font-size: 13px; color: var(--text-dim); }

.input-group label { display: block; font-size: 12px; font-weight: 600; color: var(--text-dim); margin-bottom: 6px; text-transform: uppercase; }
.input-group { margin-bottom: 16px; }
"""
    with open('d:\\SKILL\\frontend\\dashboard.css', 'w', encoding='utf-8') as f:
        f.write(css)

def rewrite_verify_html():
    with open('d:\\SKILL\\frontend\\verify.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replacing dark gradients and shadow UI with academic clean look
    html = html.replace('background: radial-gradient(circle at top right, #1a1c2c, #0d0e1b);', 'background: #f8fafc;')
    html = html.replace('background: rgba(255, 255, 255, 0.03);', 'background: #ffffff;')
    html = html.replace('border: 1px solid rgba(255, 255, 255, 0.1);', 'border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);')
    html = html.replace('color: var(--text-dim);', 'color: #64748b;')
    html = html.replace('color: #10b981;', 'color: #1e3a8a;') # Verified header from green to navy
    html = html.replace('color: var(--text);', 'color: #0f172a;')
    html = html.replace('color: var(--accent);', 'color: #1e3a8a;')
    html = html.replace('color: #ef4444;', 'color: #dc2626;')
    html = html.replace('border-top: 1px solid rgba(255, 255, 255, 0.1);', 'border-top: 1px solid #e2e8f0;')
    
    with open('d:\\SKILL\\frontend\\verify.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_style_css():
    with open('d:\\SKILL\\frontend\\style.css', 'r', encoding='utf-8') as f:
        css = f.read()
    
    css = css.replace('--primary: #ffffff;', '--primary: #f8fafc;')
    css = css.replace('--bg-mesh: radial-gradient', '/* Removed gradient */\n  --bg-mesh: none;\n  /* radial-gradient')
    css = css.replace('background-image: var(--bg-mesh);', 'background-image: none;')
    css = css.replace('--accent: #ffcc00;', '--accent: #1e3a8a;\n  /* Navy */')
    css = css.replace('background: rgba(255, 204, 0, 0.05)', 'background: transparent')
    css = css.replace('color: #10b981;', 'color: #059669;')
    css = css.replace('color: #ef4444;', 'color: #dc2626;')
    css = css.replace('color: #3b82f6;', 'color: #2563eb;')
    
    with open('d:\\SKILL\\frontend\\style.css', 'w', encoding='utf-8') as f:
        f.write(css)

rewrite_dashboard_css()
rewrite_verify_html()
update_style_css()
print("UI styling update complete!")
