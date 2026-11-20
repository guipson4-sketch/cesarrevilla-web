<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/rss/channel">
<html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title><xsl:value-of select="title"/></title>
<style>body{font:16px/1.6 system-ui,sans-serif;max-width:720px;margin:0 auto;padding:24px 16px;color:#14213a}a{color:#1b4b8f}li{margin:0 0 14px}small{color:#5b6577}.n{background:#eef3fb;padding:12px 14px;border-radius:8px}</style></head>
<body><h1><xsl:value-of select="title"/></h1>
<p class="n">Este es el canal RSS del sitio. Cópialo en tu lector de noticias para recibir las novedades, o <a href="/">vuelve al sitio</a>.</p>
<ul><xsl:for-each select="item"><li><a href="{link}"><xsl:value-of select="title"/></a><br/><small><xsl:value-of select="description"/></small></li></xsl:for-each></ul>
</body></html>
</xsl:template></xsl:stylesheet>
