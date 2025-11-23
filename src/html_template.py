def build_html_template(fig) -> str:
    html_template = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <title>Températures années après années</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: linear-gradient(180deg, #f9fafb 0%, #ffffff 40%);
      color: #0f172a;
    }}
    header {{
      padding: 16px 24px;
      border-bottom: 1px solid #e5e7eb;
      background: rgba(255, 255, 255, 0.9);
      position: sticky;
      top: 0;
      backdrop-filter: blur(12px);
      z-index: 10;
    }}
    h1 {{
      margin: 0;
      font-size: 1.4rem;
    }}
    main {{
      max-width: 960px;
      margin: 24px auto 40px;
      padding: 0 16px;
    }}
    .card {{
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
      padding: 16px;
    }}
    @media (min-width: 768px) {{
      .card {{
        padding: 24px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>🌡️ Températures mensuelles</h1>
  </header>
  <main>
    <div class="card">
      {fig.to_html(include_plotlyjs="cdn", full_html=False)}
    </div>
  </main>
</body>
</html>
"""
    return html_template
