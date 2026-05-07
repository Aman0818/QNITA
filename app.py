from flask import Flask, render_template, request, Response
from datetime import date

app = Flask(__name__)

SITE_URL = "https://qnita.vercel.app"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/parrticipatingInsti')
def parrticipatingInsti():
    return render_template('parrticipatingInsti.html')

@app.route('/robots.txt')
def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /static/audio.m4a\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    return Response(body, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    today = date.today().isoformat()
    pages = [
        ("/",         "1.0", "weekly"),
        ("/aboutUs",  "0.8", "monthly"),
    ]
    urls = "".join(
        f'  <url>\n'
        f'    <loc>{SITE_URL}{path}</loc>\n'
        f'    <lastmod>{today}</lastmod>\n'
        f'    <changefreq>{cf}</changefreq>\n'
        f'    <priority>{prio}</priority>\n'
        f'  </url>\n'
        for path, prio, cf in pages
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{urls}'
        '</urlset>\n'
    )
    return Response(body, mimetype='application/xml')

@app.after_request
def add_no_cache(response):
    if 'Cache-Control' not in response.headers and request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    else:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response
if __name__ == '__main__':
    app.run(debug=False)
